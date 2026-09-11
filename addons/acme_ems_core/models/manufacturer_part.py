from odoo import fields, models


class AcmeManufacturerPart(models.Model):
    _name = 'acme.manufacturer.part'
    _description = 'Approved Manufacturer Part'
    _order = 'manufacturer_name, mpn'

    name = fields.Char(required=True)
    manufacturer_name = fields.Char(required=True, index=True)
    mpn = fields.Char(string='Manufacturer Part Number', required=True, index=True)
    package = fields.Char()
    lifecycle_state = fields.Selection([
        ('active', 'Active'),
        ('nrnd', 'Not Recommended for New Designs'),
        ('obsolete', 'Obsolete'),
    ], default='active', required=True)
    product_tmpl_id = fields.Many2one('product.template', string='Internal Part', ondelete='cascade', index=True)
    is_preferred = fields.Boolean(default=False)
    notes = fields.Text()

    _sql_constraints = [
        ('manufacturer_mpn_unique', 'unique(manufacturer_name, mpn)', 'Manufacturer + MPN must be unique.'),
    ]
