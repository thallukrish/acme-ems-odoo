#!/usr/bin/env python3
"""Export a small operational-data snapshot from a running Odoo demo.

This is intentionally generic operational data, not a LeMap semantic file.
LeMap can use these CSVs in V1 before a direct PostgreSQL/Odoo connector exists.
"""
import csv
import os
import pathlib
import xmlrpc.client

URL = os.getenv('ODOO_URL', 'http://localhost:8069')
DB = os.getenv('ODOO_DB', 'acme_ems')
USER = os.getenv('ODOO_USER', 'admin')
PASSWORD = os.getenv('ODOO_PASSWORD', 'admin')
OUT = pathlib.Path(os.getenv('EXPORT_DIR', 'exports'))
OUT.mkdir(parents=True, exist_ok=True)

common = xmlrpc.client.ServerProxy(f'{URL}/xmlrpc/2/common')
uid = common.authenticate(DB, USER, PASSWORD, {})
if not uid:
    raise SystemExit('Odoo authentication failed')
models = xmlrpc.client.ServerProxy(f'{URL}/xmlrpc/2/object')

EXPORTS = {
    'production_orders.csv': ('mrp.production', ['name', 'product_id', 'product_qty', 'state', 'ems_delay_reason', 'ems_blocking_component_id', 'ems_shortage_qty', 'ems_customer_order_ref', 'ems_estimated_delay_days']),
    'workcenters.csv': ('mrp.workcenter', ['name', 'ems_process_type', 'ems_planned_units_per_day', 'ems_actual_units_per_day', 'ems_downtime_hours_month', 'ems_queue_units', 'ems_overtime_hours_month']),
    'approved_supply.csv': ('acme.approved.supply', ['manufacturer_part_id', 'supplier_id', 'supplier_part_number', 'approval_state', 'is_preferred', 'moq', 'lead_time_days', 'unit_price', 'freight_cost_per_unit', 'expedite_premium_per_unit', 'on_time_delivery_pct', 'quality_acceptance_pct']),
    'incoming_inspections.csv': ('acme.incoming.inspection', ['name', 'inspection_date', 'supplier_id', 'product_id', 'lot_id', 'inspected_qty', 'rejected_qty', 'disposition', 'defect_code']),
    'rework_scrap.csv': ('acme.rework.event', ['name', 'production_id', 'event_date', 'event_type', 'reason_code', 'quantity', 'labor_hours', 'labor_cost', 'material_cost', 'external_cost']),
    'lot_trace.csv': ('acme.lot.trace', ['production_id', 'component_product_id', 'component_lot_id', 'component_supplier_id', 'consumed_qty', 'finished_product_id', 'finished_lot_id', 'customer_order_ref', 'shipment_ref']),
}

for filename, (model, fields) in EXPORTS.items():
    rows = models.execute_kw(DB, uid, PASSWORD, model, 'search_read', [[]], {'fields': fields, 'order': 'id'})
    with (OUT / filename).open('w', newline='', encoding='utf-8') as fh:
        writer = csv.DictWriter(fh, fieldnames=['id', *fields])
        writer.writeheader()
        for row in rows:
            writer.writerow({k: row.get(k) for k in ['id', *fields]})
    print(f'exported {len(rows):4d} rows -> {OUT / filename}')
