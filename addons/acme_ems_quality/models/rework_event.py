from odoo import fields, models


class AcmeReworkEvent(models.Model):
    _name = 'acme.rework.event'
    _description = 'EMS Rework Event'
    _order = 'event_date desc, id desc'

    name = fields.Char(required=True)
    production_id = fields.Many2one('mrp.production', required=True, ondelete='cascade', index=True)
    event_date = fields.Date(default=fields.Date.context_today, required=True)
    reason_code = fields.Char(required=True, index=True)
    quantity = fields.Float(required=True, default=1.0)
    labor_hours = fields.Float(default=0.0)
    labor_cost = fields.Monetary(default=0.0)
    material_cost = fields.Monetary(default=0.0)
    external_cost = fields.Monetary(default=0.0)
    currency_id = fields.Many2one('res.currency', required=True, default=lambda self: self.env.company.currency_id)
    notes = fields.Text()
