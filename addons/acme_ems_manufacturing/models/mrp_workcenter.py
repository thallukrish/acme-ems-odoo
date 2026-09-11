from odoo import fields, models


class MrpWorkcenter(models.Model):
    _inherit = 'mrp.workcenter'

    ems_process_type = fields.Selection([
        ('smt', 'SMT'), ('assembly', 'Assembly / THT'), ('aoi', 'AOI / Inspection'),
        ('functional_test', 'Functional Test'), ('rework', 'Rework')
    ], string='EMS Process Type', index=True)
    ems_planned_units_per_day = fields.Float(string='Planned Units / Day')
    ems_actual_units_per_day = fields.Float(string='Actual Units / Day')
    ems_downtime_hours_month = fields.Float(string='Downtime Hours / Month')
    ems_queue_units = fields.Float(string='Current Queue Units')
    ems_overtime_hours_month = fields.Float(string='Overtime Hours / Month')
