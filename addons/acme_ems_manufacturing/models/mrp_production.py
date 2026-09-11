from odoo import fields, models


class MrpProduction(models.Model):
    _inherit = 'mrp.production'

    ems_revision_id = fields.Many2one('acme.bom.revision', string='EMS BOM Revision', index=True)
    ems_blocking_component_id = fields.Many2one('product.product', string='Blocking Component', index=True)
    ems_shortage_qty = fields.Float(string='Shortage Quantity')
    ems_delay_reason = fields.Selection([
        ('component_shortage', 'Component Shortage'),
        ('capacity', 'Capacity Constraint'),
        ('quality', 'Quality Hold'),
        ('engineering', 'Engineering Change'),
        ('other', 'Other'),
    ], string='Delay Reason', index=True)
    ems_customer_order_ref = fields.Char(string='Customer Order Reference', index=True)
    ems_planned_ship_date = fields.Date(string='Planned Ship Date')
    ems_estimated_delay_days = fields.Integer(string='Estimated Delay Days')
