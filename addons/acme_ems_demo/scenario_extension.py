from datetime import date, timedelta


def extend_demo_scenario(env):
    """Add cross-functional analysis facts after the base ACME demo seed.

    These are ordinary EMS master/history records. They intentionally carry
    trade-offs rather than precomputed query answers so LeMap has to connect
    the underlying business facts.
    """
    controller = env['product.product'].search([('default_code', '=', 'FG-CTRL-100')], limit=1)
    mcu = env['product.product'].search([('default_code', '=', 'IC-MCU-H7')], limit=1)
    if not controller or not mcu:
        raise RuntimeError('ACME demo extension expected controller and MCU products from base seed')

    alternate_supplier = env['res.partner'].create({
        'name': 'AltSilicon Distribution India',
        'company_type': 'company',
        'supplier_rank': 1,
    })
    alternate_mcu = env['acme.manufacturer.part'].create({
        'name': 'NXP Semiconductors MIMXRT1176DVMAA',
        'manufacturer_name': 'NXP Semiconductors',
        'mpn': 'MIMXRT1176DVMAA',
        'package': 'MAPBGA289',
        'product_tmpl_id': mcu.product_tmpl_id.id,
        'is_preferred': False,
        'notes': 'Approved functional alternate for the controller MCU requirement.',
    })
    env['acme.approved.supply'].create({
        'manufacturer_part_id': alternate_mcu.id,
        'supplier_id': alternate_supplier.id,
        'supplier_part_number': 'AS-NXP-RT1176',
        'approval_state': 'approved',
        'is_preferred': False,
        'moq': 500,
        'lead_time_days': 28,
        'unit_price': 1625,
        'freight_cost_per_unit': 12,
        'expedite_premium_per_unit': 95,
        'on_time_delivery_pct': 82,
        'quality_acceptance_pct': 98.5,
    })

    # Historical cost facts for the same finished product. Total cost is
    # computed by the model from these numeric components, so no explanatory
    # answer is stored in the data.
    env['acme.product.cost.snapshot'].create({
        'product_id': controller.id,
        'period_date': date.today() - timedelta(days=180),
        'material_unit_cost': 6550,
        'conversion_unit_cost': 820,
        'rework_scrap_unit_cost': 65,
        'freight_expedite_unit_cost': 40,
    })
    env['acme.product.cost.snapshot'].create({
        'product_id': controller.id,
        'period_date': date.today() - timedelta(days=30),
        'material_unit_cost': 6860,
        'conversion_unit_cost': 940,
        'rework_scrap_unit_cost': 210,
        'freight_expedite_unit_cost': 155,
    })
