from odoo.tests.common import TransactionCase


class TestAcmeEmsProcurement(TransactionCase):
    def test_approved_supply_extends_standard_supplierinfo_instead_of_copying_it(self):
        fields = self.env['acme.approved.supply']._fields
        self.assertIn('manufacturer_part_id', fields)
        self.assertIn('supplierinfo_id', fields)
        self.assertIn('approval_state', fields)
        self.assertIn('is_preferred', fields)
        self.assertIn('freight_cost_per_unit', fields)
        self.assertIn('expedite_premium_per_unit', fields)
        self.assertIn('quality_acceptance_pct', fields)
        for name in (
            'supplier_id',
            'supplier_part_number',
            'moq',
            'lead_time_days',
            'unit_price',
            'currency_id',
            'on_time_delivery_pct',
            'valid_from',
            'valid_to',
        ):
            self.assertNotIn(name, fields)

    def test_preferred_supply_requires_approved_state(self):
        self.assertTrue(self.env.registry)
