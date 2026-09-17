from datetime import date, timedelta
from odoo import Command

from .scenario_extension import extend_demo_scenario


def _partner(env, name, supplier=False, customer=False):
    vals = {'name': name, 'company_type': 'company'}
    if supplier:
        vals['supplier_rank'] = 1
    if customer:
        vals['customer_rank'] = 1
    return env['res.partner'].create(vals)


def _product(env, name, code, price=0.0, source='purchased', critical=False, customer_part=None):
    tmpl = env['product.template'].create({
        'name': name,
        'default_code': code,
        'type': 'consu',
        'is_storable': True,
        'standard_price': price,
        'list_price': max(price * 1.35, price),
        'ems_material_source': source,
        'ems_critical_part': critical,
        'ems_customer_part_number': customer_part,
        'tracking': 'lot',
    })
    return tmpl.product_variant_id


def _mfr(env, product, manufacturer, mpn, package='', preferred=False):
    return env['acme.manufacturer.part'].create({
        'name': f'{manufacturer} {mpn}',
        'manufacturer_name': manufacturer,
        'mpn': mpn,
        'package': package,
        'product_tmpl_id': product.product_tmpl_id.id,
        'is_preferred': preferred,
    })


def _offer(env, mfr, supplier, spn, price, lead, reliability, quality, preferred=False, freight=0, expedite=0, moq=1):
    return env['acme.approved.supply'].create({
        'manufacturer_part_id': mfr.id,
        'supplier_id': supplier.id,
        'supplier_part_number': spn,
        'unit_price': price,
        'lead_time_days': lead,
        'on_time_delivery_pct': reliability,
        'quality_acceptance_pct': quality,
        'is_preferred': preferred,
        'freight_cost_per_unit': freight,
        'expedite_premium_per_unit': expedite,
        'moq': moq,
    })


def post_init_hook(env):
    company = env.company
    company.name = 'ACME EMS Pvt Ltd'
    inr = env.ref('base.INR', raise_if_not_found=False)
    if inr:
        company.currency_id = inr

    # Customers deliberately have different order profiles.
    apex = _partner(env, 'Apex Industrial Controls Pvt Ltd', customer=True)
    zenith = _partner(env, 'Zenith Energy Systems Ltd', customer=True)

    # Suppliers deliberately trade off price vs delivery/quality.
    fastchip = _partner(env, 'FastChip Components India', supplier=True)
    economy = _partner(env, 'EconomySemi Distribution', supplier=True)
    passives = _partner(env, 'Bharat Passive Components', supplier=True)
    pcb_vendor = _partner(env, 'Precision PCB Technologies', supplier=True)

    controller = _product(env, 'Industrial Controller PCB Assembly', 'FG-CTRL-100', 6200, customer_part='APX-CTRL-9001')
    gateway = _product(env, 'Industrial IoT Gateway Assembly', 'FG-GW-200', 8200, customer_part='ZEN-GW-441')
    mcu = _product(env, 'High Performance MCU', 'IC-MCU-H7', 1680, critical=True)
    ethernet = _product(env, 'Industrial Ethernet PHY', 'IC-ETH-01', 420, critical=True)
    resistor = _product(env, '10k 1% 0603 Resistor', 'R-10K-0603', 0.22)
    capacitor = _product(env, '100nF X7R 0603 Capacitor', 'C-100N-0603', 0.18)
    pcb = _product(env, 'Controller Bare PCB Rev C', 'PCB-CTRL-C', 510, source='mixed')
    connector = _product(env, '12-way Industrial Connector', 'CON-12W', 210)

    # The finished controller is replenished specifically for each sales order
    # and fulfilled by manufacturing. This makes SO -> procurement -> MO a real
    # Odoo workflow rather than a synthetic demo relationship.
    mto_route = env.ref('stock.route_warehouse0_mto')
    manufacture_route = env.ref('mrp.route_warehouse0_manufacture')
    mto_route.active = True
    manufacture_route.product_selectable = True
    controller.product_tmpl_id.route_ids = [Command.set((mto_route | manufacture_route).ids)]

    mcu_st = _mfr(env, mcu, 'STMicroelectronics', 'STM32H743VIT6', 'LQFP100', True)
    eth_ti = _mfr(env, ethernet, 'Texas Instruments', 'DP83867IRPAP', 'HTQFP64', True)
    eth_micro = _mfr(env, ethernet, 'Microchip', 'KSZ9031RNX', 'QFN48')
    r_yageo = _mfr(env, resistor, 'Yageo', 'RC0603FR-0710KL', '0603', True)
    r_vishay = _mfr(env, resistor, 'Vishay', 'CRCW060310K0FKEA', '0603')

    # Single-source MCU is the material scaling constraint.
    _offer(env, mcu_st, fastchip, 'FC-STM32H743', 1750, 45, 91, 99.4, True, freight=18, expedite=140, moq=90)
    # Ethernet has an expensive fast source and a cheaper slower source.
    _offer(env, eth_ti, fastchip, 'FC-DP83867', 455, 12, 97, 99.6, True, freight=9, expedite=22, moq=50)
    _offer(env, eth_micro, economy, 'EC-KSZ9031', 382, 35, 78, 98.7, False, freight=6, expedite=65, moq=200)
    _offer(env, r_yageo, passives, 'BP-R10K-Y', 0.24, 8, 98, 99.9, True, moq=5000)
    _offer(env, r_vishay, passives, 'BP-R10K-V', 0.27, 8, 98, 99.9, False, moq=5000)

    # BOM + active revision.
    rev = env['acme.bom.revision'].create({
        'name': 'Controller PCB Revision C', 'revision_code': 'C',
        'product_tmpl_id': controller.product_tmpl_id.id,
        'effective_from': date.today() - timedelta(days=120), 'state': 'active',
        'engineering_change_reason': 'Improved Ethernet surge protection and connector retention.',
    })
    bom = env['mrp.bom'].create({
        'product_tmpl_id': controller.product_tmpl_id.id,
        'product_qty': 1.0,
        'ems_revision_id': rev.id,
        'ems_customer_approved': True,
        'bom_line_ids': [
            Command.create({'product_id': mcu.id, 'product_qty': 1}),
            Command.create({'product_id': ethernet.id, 'product_qty': 1}),
            Command.create({'product_id': resistor.id, 'product_qty': 18}),
            Command.create({'product_id': capacitor.id, 'product_qty': 14}),
            Command.create({'product_id': pcb.id, 'product_qty': 1}),
            Command.create({'product_id': connector.id, 'product_qty': 2}),
        ],
    })

    # Capacity: test is intentionally the primary bottleneck.
    smt = env['mrp.workcenter'].create({'name': 'SMT Line 1', 'ems_process_type': 'smt', 'ems_planned_units_per_day': 650, 'ems_actual_units_per_day': 590, 'ems_queue_units': 280, 'ems_downtime_hours_month': 9})
    assembly = env['mrp.workcenter'].create({'name': 'Assembly / THT', 'ems_process_type': 'assembly', 'ems_planned_units_per_day': 560, 'ems_actual_units_per_day': 525, 'ems_queue_units': 240, 'ems_downtime_hours_month': 5})
    aoi = env['mrp.workcenter'].create({'name': 'AOI Inspection', 'ems_process_type': 'aoi', 'ems_planned_units_per_day': 540, 'ems_actual_units_per_day': 500, 'ems_queue_units': 310, 'ems_downtime_hours_month': 7})
    test_wc = env['mrp.workcenter'].create({'name': 'Functional Test Station', 'ems_process_type': 'functional_test', 'ems_planned_units_per_day': 390, 'ems_actual_units_per_day': 342, 'ems_queue_units': 1180, 'ems_downtime_hours_month': 21, 'ems_overtime_hours_month': 46})
    rework_wc = env['mrp.workcenter'].create({'name': 'Rework Cell', 'ems_process_type': 'rework', 'ems_planned_units_per_day': 80, 'ems_actual_units_per_day': 67, 'ems_queue_units': 190})

    # Routings/operations on the BOM make the process visible in Odoo source/data.
    for name, wc, minutes in [
        ('SMT placement', smt, 5.5), ('Assembly / THT', assembly, 4.2), ('AOI inspection', aoi, 3.0), ('Functional test', test_wc, 7.8)
    ]:
        env['mrp.routing.workcenter'].create({'name': name, 'workcenter_id': wc.id, 'bom_id': bom.id, 'time_cycle': minutes})

    # Customer orders create demand. Because the finished product uses MTO +
    # Manufacture, confirming each SO creates its corresponding MO through
    # standard Odoo procurement rules.
    so1 = env['sale.order'].create({'partner_id': apex.id, 'client_order_ref': 'APX-PO-26091', 'order_line': [Command.create({'product_id': controller.id, 'product_uom_qty': 5000, 'price_unit': 9050})]})
    so1.action_confirm()
    so2 = env['sale.order'].create({'partner_id': zenith.id, 'client_order_ref': 'ZEN-PO-7712', 'order_line': [Command.create({'product_id': controller.id, 'product_uom_qty': 3000, 'price_unit': 9350})]})
    so2.action_confirm()

    # Enrich the MOs created by the real sale -> procurement -> manufacture
    # workflow with deterministic EMS constraints used by the demo queries.
    mo_shortage = env['mrp.production'].search([
        ('sale_line_id', 'in', so1.order_line.ids),
        ('product_id', '=', controller.id),
    ], order='id desc', limit=1)
    mo_capacity = env['mrp.production'].search([
        ('sale_line_id', 'in', so2.order_line.ids),
        ('product_id', '=', controller.id),
    ], order='id desc', limit=1)
    if not mo_shortage or not mo_capacity:
        raise RuntimeError('ACME demo expected sales-order confirmation to create manufacturing orders')

    mo_shortage.write({
        'ems_revision_id': rev.id, 'ems_blocking_component_id': mcu.id, 'ems_shortage_qty': 710,
        'ems_delay_reason': 'component_shortage', 'ems_customer_order_ref': so1.name,
        'ems_estimated_delay_days': 18, 'ems_planned_ship_date': date.today() + timedelta(days=28),
    })
    mo_capacity.write({
        'ems_revision_id': rev.id, 'ems_delay_reason': 'capacity', 'ems_customer_order_ref': so2.name,
        'ems_estimated_delay_days': 11, 'ems_planned_ship_date': date.today() + timedelta(days=21),
    })

    # Lots and quality data. One incoming Ethernet lot fails inspection.
    lot_mcu = env['stock.lot'].create({'name': 'MCU-LOT-2608-A', 'product_id': mcu.id, 'company_id': company.id})
    lot_eth_bad = env['stock.lot'].create({'name': 'ETH-LOT-2608-Q7', 'product_id': ethernet.id, 'company_id': company.id})
    lot_finished = env['stock.lot'].create({'name': 'CTRL-C-2609-001', 'product_id': controller.id, 'company_id': company.id})
    env['acme.incoming.inspection'].create({
        'name': 'IQC-2609-0041', 'supplier_id': economy.id, 'product_id': ethernet.id, 'lot_id': lot_eth_bad.id,
        'inspected_qty': 500, 'rejected_qty': 74, 'disposition': 'rejected', 'defect_code': 'SOLDERABILITY',
        'notes': 'Oxidation observed on exposed leads; lot quarantined.'
    })

    # Product B exists as a high-cost/rework contrast for business queries.
    env['acme.rework.event'].create({
        'name': 'RW-CTRL-001', 'production_id': mo_capacity.id, 'event_type': 'rework', 'reason_code': 'AOI-BRIDGE',
        'quantity': 96, 'labor_hours': 23.5, 'labor_cost': 28200, 'material_cost': 11600, 'external_cost': 0,
        'notes': 'Recurring solder bridge on fine-pitch MCU pins.'
    })
    env['acme.rework.event'].create({
        'name': 'SC-CTRL-001', 'production_id': mo_capacity.id, 'event_type': 'scrap', 'reason_code': 'PCB-PAD-LIFT',
        'quantity': 18, 'labor_hours': 3.0, 'labor_cost': 3600, 'material_cost': 62800,
    })
    env['acme.test.result'].create({
        'name': 'FT-CTRL-001', 'production_id': mo_capacity.id, 'finished_lot_id': lot_finished.id,
        'workcenter_id': test_wc.id, 'result': 'fail', 'failure_code': 'ETH-LINK', 'cycle_minutes': 9.4,
    })

    # Explicit trace path for reverse impact analysis.
    env['acme.lot.trace'].create({
        'production_id': mo_capacity.id, 'component_product_id': mcu.id, 'component_lot_id': lot_mcu.id,
        'component_supplier_id': fastchip.id, 'consumed_qty': 1080,
        'finished_product_id': controller.id, 'finished_lot_id': lot_finished.id,
        'customer_order_ref': so2.name, 'shipment_ref': 'OUT/2609/0142'
    })

    # Make the second product visible without adding a full second BOM in V1.
    gateway.product_tmpl_id.ems_material_source = 'mixed'

    # Add generic cross-functional facts used by the supplier-switch and cost
    # analysis demonstrations. The extension stores source data only; no query
    # answer or recommendation is precomputed.
    extend_demo_scenario(env)
