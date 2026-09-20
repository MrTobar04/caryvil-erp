from odoo.exceptions import ValidationError
from odoo.tests.common import TransactionCase, tagged


@tagged("post_install", "-at_install")
class TestResPartnerVendor(TransactionCase):

    def setUp(self):
        super().setUp()
        # Empresa (Laboratorio) válida, reutilizada como base en varias pruebas.
        self.laboratorio = self.env["res.partner"].create(
            {
                "name": "Laboratorios Vijosa",
                "is_company": True,
                "is_pharmacy_vendor": True,
                "vendor_type": "laboratorio",
                "nit": "0614-123456-001-2",
                "nrc": "12345-6",
            }
        )

    # Al crear un vendedor marcado como proveedor, debe asignarse un código automático (P0001...).
    def test_vendor_code_autogenerado(self):
        vendedor = self.env["res.partner"].create(
            {
                "name": "Carlos Méndez",
                "is_pharmacy_vendor": True,
                "parent_id": self.laboratorio.id,
            }
        )
        self.assertTrue(vendedor.vendor_code)
        self.assertTrue(vendedor.vendor_code.startswith("P"))

    # Un vendedor sin marca de proveedor no debe recibir código automático.
    def test_sin_codigo_si_no_es_proveedor(self):
        contacto_normal = self.env["res.partner"].create(
            {
                "name": "Cliente Cualquiera",
            }
        )
        self.assertFalse(contacto_normal.vendor_code)

    # Un mismo laboratorio puede tener más de un vendedor asociado.
    def test_multiples_vendedores_por_laboratorio(self):
        vendedor_1 = self.env["res.partner"].create(
            {
                "name": "Carlos Méndez",
                "is_pharmacy_vendor": True,
                "parent_id": self.laboratorio.id,
            }
        )
        vendedor_2 = self.env["res.partner"].create(
            {
                "name": "Ana López",
                "is_pharmacy_vendor": True,
                "parent_id": self.laboratorio.id,
            }
        )
        self.assertEqual(vendedor_1.parent_id, vendedor_2.parent_id)
        self.assertIn(vendedor_1, self.laboratorio.child_ids)
        self.assertIn(vendedor_2, self.laboratorio.child_ids)

    # Un NIT con formato inválido debe rechazar el guardado.
    def test_nit_formato_invalido(self):
        with self.assertRaises(ValidationError):
            self.laboratorio.write({"nit": "12345"})

    # Un NIT con formato correcto se guarda sin problema.
    def test_nit_formato_valido(self):
        self.laboratorio.write({"nit": "0614-654321-002-3"})
        self.assertEqual(self.laboratorio.nit, "0614-654321-002-3")

    # Una Empresa proveedora sin NRC debe rechazar el guardado.
    def test_nrc_obligatorio(self):
        with self.assertRaises(ValidationError):
            self.env["res.partner"].create(
                {
                    "name": "Distribuidora Sin NRC",
                    "is_company": True,
                    "is_pharmacy_vendor": True,
                }
            )

    # Un teléfono con formato inválido debe rechazar el guardado.
    def test_telefono_formato_invalido(self):
        with self.assertRaises(ValidationError):
            self.env["res.partner"].create(
                {
                    "name": "Carlos Méndez",
                    "is_pharmacy_vendor": True,
                    "parent_id": self.laboratorio.id,
                    "phone": "12345",
                }
            )

    # Un teléfono con formato correcto se guarda sin problema.
    def test_telefono_formato_valido(self):
        vendedor = self.env["res.partner"].create(
            {
                "name": "Carlos Méndez",
                "is_pharmacy_vendor": True,
                "parent_id": self.laboratorio.id,
                "phone": "7788-9900",
            }
        )
        self.assertEqual(vendedor.phone, "7788-9900")

    # Las validaciones de NIT/NRC/Teléfono no deben afectar contactos normales (clientes).
    def test_validaciones_no_afectan_contactos_normales(self):
        cliente = self.env["res.partner"].create(
            {
                "name": "Cliente Sin Formato",
                "phone": "12345",
            }
        )
        self.assertEqual(cliente.phone, "12345")
