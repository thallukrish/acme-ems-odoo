from odoo import fields, models


class AcmeTestResult(models.Model):
    _name = 'acme.test.result'
    _description = 'EMS Functional Test Result'
    _order = 'tested_at desc, id desc'

    name = fields.Char(required=True)
    production_id = fields.Many2one('mrp.production', required=True, ondelete='cascade', index=True)
    finished_lot_id = fields.Many2one('stock.lot', string='Finished Lot / Serial', index=True)
    workcenter_id = fields.Many2one('mrp.workcenter', index=True)
    tested_at = fields.Datetime(default=fields.Datetime.now, required=True)
    result = fields.Selection([('pass', 'Pass'), ('fail', 'Fail')], required=True, index=True)
    failure_code = fields.Char(index=True)
    cycle_minutes = fields.Float()
    retest = fields.Boolean(default=False)
