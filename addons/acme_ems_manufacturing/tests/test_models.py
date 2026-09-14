from odoo.tests.common import TransactionCase


class TestAcmeEmsManufacturing(TransactionCase):
    def test_mrp_production_keeps_only_real_acme_extension_fields(self):
        fields = self.env['mrp.production']._fields
        self.assertIn('ems_revision_id', fields)
        for name in (
            'ems_blocking_component_id',
            'ems_shortage_qty',
            'ems_delay_reason',
            'ems_customer_order_ref',
            'ems_planned_ship_date',
            'ems_estimated_delay_days',
        ):
            self.assertNotIn(name, fields)
