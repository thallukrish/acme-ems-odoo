{
    'name': 'ACME EMS Traceability',
    'version': '19.0.1.0.0',
    'summary': 'Explicit component-lot to finished-lot manufacturing traceability',
    'category': 'Inventory',
    'license': 'LGPL-3',
    'depends': ['stock', 'mrp', 'acme_ems_quality'],
    'data': ['security/ir.model.access.csv', 'views/traceability_views.xml'],
    'installable': True,
}
