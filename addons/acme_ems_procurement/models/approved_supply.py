from odoo import api, fields, models
from odoo.exceptions import ValidationError


class AcmeApprovedSupply(models.Model):
    _name = 'acme.approved.supply'
    _description = 'Approved Supplier Offer'
    _order = 'manufacturer_part_id, is_preferred desc, id'

    manufacturer_part_id = fields.Many2one('acme.manufacturer.part', required=True, ondelete='cascade', index=True)
    supplierinfo_id = fields.Many2one('product.supplierinfo', string='Odoo Vendor Offer', required=True, ondelete='cascade', index=True)
    approval_state = fields.Selection([
        ('approved', 'Approved'), ('conditional', 'Conditional'), ('blocked', 'Blocked')
    ], required=True, default='approved')
    is_preferred = fields.Boolean(default=False)
    supplier_currency_id = fields.Many2one('res.currency', related='supplierinfo_id.currency_id', readonly=True)
    freight_cost_per_unit = fields.Monetary(currency_field='supplier_currency_id', default=0.0)
    expedite_premium_per_unit = fields.Monetary(currency_field='supplier_currency_id', default=0.0)
    quality_acceptance_pct = fields.Float(default=99.0)

    @api.constrains('is_preferred', 'approval_state')
    def _check_preferred_is_approved(self):
        for rec in self:
            if rec.is_preferred and rec.approval_state != 'approved':
                raise ValidationError('A preferred source must be approved.')

    @api.constrains('manufacturer_part_id', 'supplierinfo_id')
    def _check_offer_matches_internal_part(self):
        for rec in self:
            offer_template = rec.supplierinfo_id.product_tmpl_id
            internal_template = rec.manufacturer_part_id.product_tmpl_id
            if offer_template and internal_template and offer_template != internal_template:
                raise ValidationError('The Odoo vendor offer must belong to the approved manufacturer part internal product.')
