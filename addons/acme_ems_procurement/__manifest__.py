{
    'name': 'ACME EMS Procurement',
    'version': '19.0.1.0.0',
    'summary': 'Approved supply sources and sourcing economics for EMS parts',
    'category': 'Purchases',
    'license': 'LGPL-3',
    'depends': ['purchase', 'acme_ems_core'],
    'data': ['security/ir.model.access.csv', 'views/approved_supply_views.xml'],
    'installable': True,
}
