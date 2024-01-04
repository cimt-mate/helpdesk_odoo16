{
    'name': 'CIMT Helpdesk',
    'version': '1.0',
    'summary': 'Custom Helpdesk Module',
    'sequence': 10,
    'description': """Custom Helpdesk Module For CIMT""",
    'category': 'Productivity',
    'depends': ['base'],
    'data': [
        'security/ir.model.access.csv',
        'views/helpdesk_view.xml',
    ],
    'demo': [],
    'installable': True,
    'application': True,
    'auto_install': False,
}
