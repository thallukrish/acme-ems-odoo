from odoo import fields, models


class AcmeIncomingInspection(models.Model):
    _name = 'acme.incoming.inspection'
    _description = 'Incoming Component Inspection'
    _order = 'inspection_date desc, id desc'

    name = fields.Char(required=True)
    inspection_date = fields.Date(required=True, default=fields.Date.context_today)
    supplier_id = fields.Many2one('res.partner', required=True, index=True)
    product_id = fields.Many2one('product.product', required=True, index=True)
    lot_id = fields.Many2one('stock.lot', required=True, index=True)
    receipt_id = fields.Many2one('stock.picking', string='Receipt', index=True)
    inspected_qty = fields.Float(required=True)
    rejected_qty = fields.Float(default=0.0)
    disposition = fields.Selection([
        ('accepted', 'Accepted'), ('rejected', 'Rejected'), ('conditional', 'Conditional Release')
    ], required=True, default='accepted', index=True)
    defect_code = fields.Char(index=True)
    notes = fields.Text()
