{
    'name': 'CIMT Helpdesk',
    'version': '1.0',
    'summary': 'Custom Helpdesk Module',
    'sequence': 10,
    'description': """Custom Helpdesk Module For CIMT""",
    'category': 'Productivity',
    'depends': ['base', 'cimt_odoo16'],
    'data': [
        'security/ir.model.access.csv',
        'views/helpdesk_view.xml',
        'views/monthly_report_view.xml',
        'views/report_monthly_tickets.xml',
        'views/report_helpdesk_tickets.xml'
    ],
    'demo': [],
    'installable': True,
    'application': True,
    'auto_install': False,
}
