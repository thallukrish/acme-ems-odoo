#!/usr/bin/env python3
import ast
import pathlib
import sys
import xml.etree.ElementTree as ET

ROOT = pathlib.Path(__file__).resolve().parents[1]
ADDONS = ROOT / 'addons'
EXPECTED = {
    'acme_ems_core', 'acme_ems_procurement', 'acme_ems_manufacturing',
    'acme_ems_quality', 'acme_ems_traceability', 'acme_ems_demo'
}
found = {p.name for p in ADDONS.iterdir() if p.is_dir()}
missing = EXPECTED - found
assert not missing, f'missing addons: {sorted(missing)}'

for addon in sorted(EXPECTED):
    manifest = ADDONS / addon / '__manifest__.py'
    assert manifest.exists(), f'{addon}: missing manifest'
    data = ast.literal_eval(manifest.read_text())
    assert data.get('version', '').startswith('19.0.'), f'{addon}: not Odoo 19'
    assert data.get('installable') is True, f'{addon}: not installable'

for py in ROOT.rglob('*.py'):
    compile(py.read_text(), str(py), 'exec')

for xml in ROOT.rglob('*.xml'):
    ET.parse(xml)

required_tokens = {
    'addons/acme_ems_core/models/manufacturer_part.py': ['_name = \'acme.manufacturer.part\'', 'Many2one'],
    'addons/acme_ems_procurement/models/approved_supply.py': ['lead_time_days', 'expedite_premium_per_unit', 'on_time_delivery_pct'],
    'addons/acme_ems_manufacturing/models/mrp_production.py': ['ems_blocking_component_id', 'ems_shortage_qty', 'ems_delay_reason'],
    'addons/acme_ems_quality/models/rework_event.py': ['labor_cost', 'material_cost', 'event_type'],
    'addons/acme_ems_traceability/models/lot_trace.py': ['component_lot_id', 'finished_lot_id', 'shipment_ref'],
}
for rel, tokens in required_tokens.items():
    text = (ROOT / rel).read_text()
    for token in tokens:
        assert token in text, f'{rel}: missing {token}'

print('source validation passed')
