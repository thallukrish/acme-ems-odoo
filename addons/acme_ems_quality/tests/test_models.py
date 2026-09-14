from odoo.tests.common import TransactionCase


class TestAcmeEmsQuality(TransactionCase):
    def test_incoming_inspection_remains_explicit_supplier_quality_evidence(self):
        fields = self.env['acme.incoming.inspection']._fields
        for name in ('supplier_id', 'product_id', 'lot_id', 'receipt_id', 'inspected_qty', 'rejected_qty', 'disposition'):
            self.assertIn(name, fields)

    def test_rework_event_does_not_duplicate_standard_scrap_classification(self):
        fields = self.env['acme.rework.event']._fields
        self.assertNotIn('event_type', fields)
        for name in ('production_id', 'reason_code', 'quantity', 'labor_hours', 'labor_cost', 'material_cost', 'external_cost'):
            self.assertIn(name, fields)
