from odoo import fields, models


class ProductTemplate(models.Model):
    _inherit = 'product.template'

    ems_customer_part_number = fields.Char(string='Customer Part Number', index=True)
    ems_material_source = fields.Selection([
        ('purchased', 'Purchased'),
        ('consigned', 'Customer Consigned'),
        ('mixed', 'Mixed Source'),
    ], string='EMS Material Source', default='purchased')
    ems_manufacturer_part_ids = fields.One2many(
        'acme.manufacturer.part', 'product_tmpl_id', string='Approved Manufacturer Parts'
    )
    ems_critical_part = fields.Boolean(string='Production Critical')
