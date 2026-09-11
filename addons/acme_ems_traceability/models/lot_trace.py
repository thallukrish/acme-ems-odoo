from odoo import fields, models


class AcmeLotTrace(models.Model):
    _name = 'acme.lot.trace'
    _description = 'EMS Component to Finished Lot Trace'
    _order = 'production_id, component_product_id'

    production_id = fields.Many2one('mrp.production', required=True, ondelete='cascade', index=True)
    component_product_id = fields.Many2one('product.product', required=True, index=True)
    component_lot_id = fields.Many2one('stock.lot', required=True, index=True)
    component_supplier_id = fields.Many2one('res.partner', index=True)
    consumed_qty = fields.Float(required=True)
    finished_product_id = fields.Many2one('product.product', required=True, index=True)
    finished_lot_id = fields.Many2one('stock.lot', required=True, index=True)
    customer_order_ref = fields.Char(index=True)
    shipment_ref = fields.Char(index=True)
