from odoo import api, fields, models
from odoo.exceptions import ValidationError


class AcmeBomRevision(models.Model):
    _name = 'acme.bom.revision'
    _description = 'EMS BOM Revision'
    _order = 'product_tmpl_id, revision_code desc'

    name = fields.Char(required=True)
    revision_code = fields.Char(required=True, index=True)
    product_tmpl_id = fields.Many2one('product.template', required=True, ondelete='cascade', index=True)
    effective_from = fields.Date(required=True)
    effective_to = fields.Date()
    state = fields.Selection([
        ('draft', 'Draft'), ('active', 'Active'), ('superseded', 'Superseded')
    ], default='draft', required=True, index=True)
    engineering_change_reason = fields.Text()
    bom_ids = fields.One2many('mrp.bom', 'ems_revision_id', string='Bills of Materials')

    @api.constrains('effective_from', 'effective_to')
    def _check_dates(self):
        for rec in self:
            if rec.effective_to and rec.effective_to < rec.effective_from:
                raise ValidationError('Effective To cannot be earlier than Effective From.')

    @api.constrains('state', 'product_tmpl_id')
    def _check_single_active_revision(self):
        for rec in self.filtered(lambda r: r.state == 'active'):
            count = self.search_count([
                ('id', '!=', rec.id), ('product_tmpl_id', '=', rec.product_tmpl_id.id), ('state', '=', 'active')
            ])
            if count:
                raise ValidationError('Only one active EMS BOM revision is allowed per product.')
