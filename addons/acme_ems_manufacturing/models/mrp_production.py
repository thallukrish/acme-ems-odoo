from odoo import fields, models


class MrpProduction(models.Model):
    _inherit = 'mrp.production'

    ems_revision_id = fields.Many2one('acme.bom.revision', string='EMS BOM Revision', index=True)
