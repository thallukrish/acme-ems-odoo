from odoo import api, fields, models
from odoo.exceptions import ValidationError


class AcmeApprovedSupply(models.Model):
    _name = 'acme.approved.supply'
    _description = 'Approved Supplier Offer'
    _order = 'manufacturer_part_id, is_preferred desc, unit_price'

    manufacturer_part_id = fields.Many2one('acme.manufacturer.part', required=True, ondelete='cascade', index=True)
    supplier_id = fields.Many2one('res.partner', required=True, domain=[('supplier_rank', '>', 0)], index=True)
    supplier_part_number = fields.Char(required=True)
    approval_state = fields.Selection([
        ('approved', 'Approved'), ('conditional', 'Conditional'), ('blocked', 'Blocked')
    ], required=True, default='approved')
    is_preferred = fields.Boolean(default=False)
    moq = fields.Float(string='Minimum Order Quantity', default=1.0)
    lead_time_days = fields.Integer(default=30)
    unit_price = fields.Monetary(required=True)
    currency_id = fields.Many2one('res.currency', required=True, default=lambda self: self.env.company.currency_id)
    freight_cost_per_unit = fields.Monetary(currency_field='currency_id', default=0.0)
    expedite_premium_per_unit = fields.Monetary(currency_field='currency_id', default=0.0)
    on_time_delivery_pct = fields.Float(default=95.0)
    quality_acceptance_pct = fields.Float(default=99.0)
    valid_from = fields.Date()
    valid_to = fields.Date()

    @api.constrains('is_preferred', 'approval_state')
    def _check_preferred_is_approved(self):
        for rec in self:
            if rec.is_preferred and rec.approval_state != 'approved':
                raise ValidationError('A preferred source must be approved.')
