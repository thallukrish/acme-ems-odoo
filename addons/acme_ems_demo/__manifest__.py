{
    'name': 'ACME EMS Demo Company',
    'version': '19.0.1.0.0',
    'summary': 'Deterministic EMS business scenario for semantic-map and data-query demonstrations',
    'category': 'Manufacturing',
    'license': 'LGPL-3',
    'depends': [
        'sale_mrp', 'purchase', 'account',
        'acme_ems_core', 'acme_ems_procurement', 'acme_ems_manufacturing',
        'acme_ems_quality', 'acme_ems_traceability'
    ],
    'post_init_hook': 'post_init_hook',
    'installable': True,
}
