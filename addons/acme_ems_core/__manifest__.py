{
    'name': 'ACME EMS Core',
    'version': '19.0.1.0.0',
    'summary': 'EMS part master and customer-specific product semantics',
    'category': 'Manufacturing',
    'license': 'LGPL-3',
    'depends': ['product', 'stock'],
    'data': [
        'security/ir.model.access.csv',
        'views/manufacturer_part_views.xml',
    ],
    'installable': True,
}
