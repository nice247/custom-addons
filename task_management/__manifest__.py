{
    'name': 'Task Management',
    'author': 'Baha',
    'category': '',
    'version': '1.0',
    'depends': ['base', 'mail'],
    'data': [
        'security/ir.model.access.csv',
        'views/task_view.xml',
        'views/base_menu.xml',
        'reports/task_report_view.xml',
        'reports/time_sheet_report_view.xml',
    ],
    'application': True
}
