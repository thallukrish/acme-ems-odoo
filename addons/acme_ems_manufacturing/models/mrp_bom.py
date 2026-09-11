from odoo import fields, models


class MrpBom(models.Model):
    _inherit = 'mrp.bom'

    ems_revision_id = fields.Many2one('acme.bom.revision', string='EMS BOM Revision', index=True)
    ems_customer_approved = fields.Boolean(string='Customer Approved BOM', default=False)
