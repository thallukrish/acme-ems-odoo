from odoo import api, fields, models


class AcmeProductCostSnapshot(models.Model):
    _name = 'acme.product.cost.snapshot'
    _description = 'Product Cost Snapshot'
    _order = 'product_id, period_date desc'

    product_id = fields.Many2one('product.product', required=True, ondelete='cascade', index=True)
    period_date = fields.Date(required=True, index=True)
    currency_id = fields.Many2one(
        'res.currency',
        required=True,
        default=lambda self: self.env.company.currency_id,
    )
    material_unit_cost = fields.Monetary(currency_field='currency_id', default=0.0)
    conversion_unit_cost = fields.Monetary(currency_field='currency_id', default=0.0)
    rework_scrap_unit_cost = fields.Monetary(currency_field='currency_id', default=0.0)
    freight_expedite_unit_cost = fields.Monetary(currency_field='currency_id', default=0.0)
    total_unit_cost = fields.Monetary(
        currency_field='currency_id',
        compute='_compute_total_unit_cost',
        store=True,
    )

    @api.depends(
        'material_unit_cost',
        'conversion_unit_cost',
        'rework_scrap_unit_cost',
        'freight_expedite_unit_cost',
    )
    def _compute_total_unit_cost(self):
        for rec in self:
            rec.total_unit_cost = (
                rec.material_unit_cost
                + rec.conversion_unit_cost
                + rec.rework_scrap_unit_cost
                + rec.freight_expedite_unit_cost
            )

    _sql_constraints = [
        (
            'product_period_unique',
            'unique(product_id, period_date)',
            'Only one cost snapshot is allowed per product and period date.',
        ),
    ]
