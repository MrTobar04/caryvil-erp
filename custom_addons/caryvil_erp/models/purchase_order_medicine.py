# -*- coding: utf-8 -*-
from odoo import models, fields, api, _
from odoo.exceptions import ValidationError


class PurchaseOrderMedicine(models.Model):
    _inherit = 'purchase.order'

    laboratory_id = fields.Many2one(
        'res.partner',
        string='Proveedor',
        related='partner_id.commercial_partner_id',
        store=True,
        readonly=True,
        help='Empresa (laboratorio/droguería) a la que pertenece el vendedor (Nombre Vendedor) seleccionado.',
    )
    commercial_terms_id = fields.Selection([
        ('contado', 'Contado'),
        ('credito_15', 'Crédito 15 días'),
        ('credito_30', 'Crédito 30 días'),
        ('credito_45', 'Crédito 45 días'),
        ('credito_60', 'Crédito 60 días'),
    ], string='Condiciones de Pago', default='contado')
    expected_delivery_date = fields.Date(string='Fecha Límite de Entrega')
    notes_reception = fields.Text(
        string='Requerimientos de Recepción',
        default='Requerir lotes con fecha de caducidad mayor a 18 meses.',
    )
    state_label = fields.Selection([
        ('pendiente', 'Pendiente'),
        ('recibido', 'Recibido'),
        ('cancelado', 'Cancelado'),
    ], string='Estado', compute='_compute_state_label', store=True)
    amount_discount_total = fields.Monetary(
        string='Descuento',
        compute='_compute_amount_discount_summary',
        store=True,
        currency_field='currency_id',
    )
    iva_percibido_check = fields.Boolean(
        string='Aplicar IVA Percibido (1%)',
        help='El IVA Percibido (1%) aplica a facturas de $100.00 o más, cuando el proveedor es Gran Contribuyente. '
             'Se sugiere automáticamente al superar $100, pero puede desactivarse manualmente.',
    )
    amount_iva_percibido = fields.Monetary(
        string='IVA Percibido (1%)',
        compute='_compute_amount_iva_percibido',
        store=True,
        currency_field='currency_id',
    )
    amount_total_final = fields.Monetary(
        string='Total Final (con IVA Percibido)',
        compute='_compute_amount_iva_percibido',
        store=True,
        currency_field='currency_id',
    )
    amount_residual_total = fields.Monetary(
        string='Saldo Pendiente en Factura',
        compute='_compute_payment_status_caryvil',
        store=True,
        currency_field='currency_id',
        help='Suma del saldo pendiente de las facturas de proveedor (Bills) ligadas a esta orden. '
             'Se reduce con cada abono registrado en la factura.',
    )
    payment_status_label = fields.Selection([
        ('sin_facturar', 'Sin Facturar'),
        ('pendiente', 'Pendiente de Pago'),
        ('parcial', 'Abono Parcial'),
        ('pagado', 'Pagado'),
    ], string='Estado de Factura', compute='_compute_payment_status_caryvil', store=True,
        help='Estado contable formal (Factura de Proveedor + Pago). Se activa al generar la '
             'factura final, una vez completados los Abonos.')
    payment_count = fields.Integer(string='Pagos en Factura', compute='_compute_payment_ids_caryvil')

    # Abonos informales: lo que se usa día a día para registrar pagos parciales al proveedor,
    # sin tener que pasar por Contabilidad en cada uno.
    abono_ids = fields.One2many('purchase.order.abono', 'order_id', string='Abonos')
    monto_abonado = fields.Monetary(
        string='Total Abonado', compute='_compute_abonos_caryvil', store=True, currency_field='currency_id',
    )
    saldo_abonos_pendiente = fields.Monetary(
        string='Saldo Pendiente', compute='_compute_abonos_caryvil', store=True, currency_field='currency_id',
    )
    abono_status_label = fields.Selection([
        ('pendiente', 'Pendiente'),
        ('parcial', 'Abono Parcial'),
        ('pagado', 'Completo'),
    ], string='Estado de Abonos', compute='_compute_abonos_caryvil', store=True)

    # Historial de Pagos: lista los abonos (account.payment) reconciliados contra las facturas
    # de proveedor de esta orden, para verlos sin salir del módulo de Compras. Se obtienen vía
    # la conciliación contable (matched_credit_ids/matched_debit_ids) en vez del campo
    # reconciled_bill_ids (no es buscable por dominio, solo sirve para leer).
    def _get_caryvil_payments(self):
        self.ensure_one()
        lines = self.invoice_ids.line_ids
        return (lines.matched_credit_ids.credit_move_id.payment_id
                | lines.matched_debit_ids.debit_move_id.payment_id)

    def _compute_payment_ids_caryvil(self):
        for order in self:
            order.payment_count = len(order._get_caryvil_payments())

    def action_view_caryvil_payments(self):
        self.ensure_one()
        payments = self._get_caryvil_payments()
        return {
            'name': _('Historial de Pagos'),
            'type': 'ir.actions.act_window',
            'res_model': 'account.payment',
            'view_mode': 'tree,form',
            'domain': [('id', 'in', payments.ids)],
        }

    # SPEC-8.1.2 (rediseño): los abonos se anotan directo en la orden (fecha, monto, nota),
    # sin pasar por Contabilidad para cada uno. Solo al terminar de pagar (saldo en $0) se
    # genera la Factura de Proveedor formal, de un solo clic, con el pago ya reconciliado.
    @api.depends('abono_ids.monto', 'amount_total_final')
    def _compute_abonos_caryvil(self):
        for order in self:
            abonado = sum(order.abono_ids.mapped('monto'))
            saldo = order.amount_total_final - abonado
            order.monto_abonado = abonado
            order.saldo_abonos_pendiente = max(saldo, 0.0)
            if abonado <= 0:
                order.abono_status_label = 'pendiente'
            elif saldo > 0.005:
                order.abono_status_label = 'parcial'
            else:
                order.abono_status_label = 'pagado'

    # Un clic: genera la Factura de Proveedor, y si ya tiene fecha la confirma y registra el
    # pago completo automáticamente (reconciliado). Solo se habilita cuando ya se abonó el
    # 100% mediante la lista de Abonos. Si la factura está en borrador sin fecha, te lleva a
    # esa pantalla para que la completes tú (no se pone fecha automática).
    def action_generar_factura_final_caryvil(self):
        self.ensure_one()
        if self.abono_status_label != 'pagado':
            raise ValidationError(_('Aún falta abonar $%.2f para poder generar la factura final.') % self.saldo_abonos_pendiente)

        if not self.invoice_ids:
            self.action_create_invoice()

        borradores = self.invoice_ids.filtered(lambda m: m.state == 'draft')
        sin_fecha = borradores.filtered(lambda m: not m.invoice_date)
        if sin_fecha:
            return {
                'name': _('Completa la fecha y confirma la Factura de Proveedor'),
                'type': 'ir.actions.act_window',
                'res_model': 'account.move',
                'res_id': sin_fecha[0].id,
                'view_mode': 'form',
                'target': 'current',
            }
        borradores.action_post()

        bills_por_pagar = self.invoice_ids.filtered(
            lambda m: m.state == 'posted' and m.payment_state not in ('paid', 'in_payment')
        )
        if bills_por_pagar:
            wizard = self.env['account.payment.register'].with_context(
                active_model='account.move', active_ids=bills_por_pagar.ids,
            ).create({})
            wizard._create_payments()
        return True

    # Sugiere activar el IVA Percibido cuando el total (nativo, con IVA 13% ya incluido) supera $100.
    # Se usa 'amount_total' (campo nativo de Odoo, siempre reactivo en pantalla) en vez de un
    # cálculo propio, para que el resumen se actualice al instante como el resto de la orden.
    @api.onchange('amount_total')
    def _onchange_amount_total_iva_percibido(self):
        for order in self:
            order.iva_percibido_check = order.amount_total > 100

    # El 1% de IVA Percibido solo se cobra si el total supera $100 y el check está activo.
    @api.depends('amount_total', 'iva_percibido_check')
    def _compute_amount_iva_percibido(self):
        for order in self:
            if order.iva_percibido_check and order.amount_total > 100:
                order.amount_iva_percibido = order.amount_total * 0.01
            else:
                order.amount_iva_percibido = 0.0
            order.amount_total_final = order.amount_total + order.amount_iva_percibido

    # Abonos: usa las Facturas de Proveedor (Bills) y sus pagos nativos de Odoo (Accounting) para
    # reflejar el saldo pendiente y el estado de pago (Pendiente / Abono Parcial / Pagado) de la
    # orden directamente en Compras, sin tener que entrar a Contabilidad a revisarlo.
    @api.depends('invoice_ids.amount_residual', 'invoice_ids.payment_state', 'invoice_ids.state')
    def _compute_payment_status_caryvil(self):
        for order in self:
            bills = order.invoice_ids.filtered(lambda move: move.state == 'posted')
            if not bills:
                order.amount_residual_total = 0.0
                order.payment_status_label = 'sin_facturar'
                continue
            order.amount_residual_total = sum(bills.mapped('amount_residual'))
            states = set(bills.mapped('payment_state'))
            if states <= {'paid', 'in_payment'}:
                order.payment_status_label = 'pagado'
            elif states & {'partial'}:
                order.payment_status_label = 'parcial'
            else:
                order.payment_status_label = 'pendiente'

    # Simplifica los 6 estados nativos de Odoo a los 3 que maneja el negocio: Pendiente, Recibido, Cancelado.
    @api.depends('state')
    def _compute_state_label(self):
        for order in self:
            if order.state == 'cancel':
                order.state_label = 'cancelado'
            elif order.state == 'done':
                order.state_label = 'recibido'
            else:
                order.state_label = 'pendiente'

    # Monto total descontado (cantidad x precio unitario, sin descuento, menos el subtotal neto
    # nativo 'amount_untaxed'). Se apoya en 'amount_untaxed' porque ese campo nativo sí se
    # actualiza al instante en pantalla; un cálculo 100% propio se quedaba en $0.00 hasta el
    # siguiente clic (bug de reactividad del cliente web con o2m recién creados).
    @api.depends('order_line.product_qty', 'order_line.price_unit', 'amount_untaxed')
    def _compute_amount_discount_summary(self):
        for order in self:
            gross = sum(line.product_qty * line.price_unit for line in order.order_line)
            order.amount_discount_total = gross - order.amount_untaxed

    # Asigna el código autogenerado (PE0001, PE0002...) a las nuevas órdenes de compra.
    @api.model_create_multi
    def create(self, vals_list):
        for vals in vals_list:
            if vals.get('name', 'New') == 'New':
                vals['name'] = self.env['ir.sequence'].next_by_code('caryvil.purchase.order') or 'New'
        return super().create(vals_list)

    # El proveedor (vendedor o su empresa/laboratorio) debe estar catalogado como proveedor farmacéutico.
    @api.constrains('partner_id')
    def _check_pharmacy_vendor(self):
        for order in self:
            partner = order.partner_id
            if partner and not (partner.is_pharmacy_vendor or partner.commercial_partner_id.is_pharmacy_vendor):
                raise ValidationError(_(
                    'El proveedor "%s" no está catalogado como proveedor farmacéutico.'
                ) % partner.name)

    def button_confirm(self):
        for order in self:
            if not order.order_line:
                raise ValidationError(_('No puede confirmar una orden de compra sin líneas de medicamentos.'))
            for line in order.order_line:
                if line.product_qty <= 0:
                    raise ValidationError(_('La cantidad del medicamento %s debe ser mayor a 0.') % line.product_id.name)
        return super().button_confirm()


class PurchaseOrderLineMedicine(models.Model):
    _inherit = 'purchase.order.line'
    # NOTA: "Fecha Prevista" (date_planned) se deja 100% nativa, sin tocar.

    # IVA 13% automático por línea: se asigna solo el impuesto propio de Caryvil (nunca el que
    # traiga configurado el producto), y sin mostrárselo al usuario. Esto permite usar el motor
    # de impuestos NATIVO de Odoo (amount_untaxed/amount_tax/amount_total), que sí se actualiza
    # al instante en pantalla — en vez de un cálculo propio que solo se refrescaba hasta el
    # siguiente clic.
    @api.onchange('product_id')
    def _onchange_product_id_iva_caryvil(self):
        for line in self:
            if line.product_id and not line.display_type:
                iva = self.env.ref('caryvil_erp.tax_caryvil_iva_compras_13', raise_if_not_found=False)
                if iva:
                    line.taxes_id = [(6, 0, iva.ids)]

    @api.model_create_multi
    def create(self, vals_list):
        iva = self.env.ref('caryvil_erp.tax_caryvil_iva_compras_13', raise_if_not_found=False)
        for vals in vals_list:
            if iva and vals.get('product_id') and not vals.get('display_type') and not vals.get('taxes_id'):
                vals['taxes_id'] = [(6, 0, iva.ids)]
        return super().create(vals_list)
