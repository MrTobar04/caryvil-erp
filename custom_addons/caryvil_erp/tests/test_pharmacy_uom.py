# -*- coding: utf-8 -*-

from odoo.tests.common import TransactionCase


class TestPharmacyUom(TransactionCase):

    def setUp(self):
        super().setUp()

        self.unit = self.env.ref('caryvil_erp.uom_unit_pill')
        self.blister4 = self.env.ref('caryvil_erp.uom_blister_4')
        self.blister10 = self.env.ref('caryvil_erp.uom_blister_10')
        self.box20 = self.env.ref('caryvil_erp.uom_box_20')
        self.box50 = self.env.ref('caryvil_erp.uom_box_50')
        self.box100 = self.env.ref('caryvil_erp.uom_box_100')

    def test_blister_4_to_unit(self):
        """Un blíster x4 debe convertirse en 4 unidades."""
        result = self.blister4._compute_quantity(
            1,
            self.unit
        )

        self.assertEqual(
            result,
            4,
            "Un Blíster x4 debe equivaler a 4 unidades."
        )

    def test_blister_10_to_unit(self):
        """Un blíster x10 debe convertirse en 10 unidades."""
        result = self.blister10._compute_quantity(
            1,
            self.unit
        )

        self.assertEqual(
            result,
            10,
            "Un Blíster x10 debe equivaler a 10 unidades."
        )

    def test_box_20_to_unit(self):
        """Una caja x20 debe convertirse en 20 unidades."""
        result = self.box20._compute_quantity(
            1,
            self.unit
        )

        self.assertEqual(
            result,
            20,
            "Una Caja x20 debe equivaler a 20 unidades."
        )

    def test_box_50_to_unit(self):
        """Una caja x50 debe convertirse en 50 unidades."""
        result = self.box50._compute_quantity(
            1,
            self.unit
        )

        self.assertEqual(
            result,
            50,
            "Una Caja x50 debe equivaler a 50 unidades."
        )

    def test_box_100_to_unit(self):
        """Una caja x100 debe convertirse en 100 unidades."""
        result = self.box100._compute_quantity(
            1,
            self.unit
        )

        self.assertEqual(
            result,
            100,
            "Una Caja x100 debe equivaler a 100 unidades."
        )