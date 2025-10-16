# activ/__manifest__.py
{
    'name': 'ACTIV - Volunteer Management System',
    'version': '1.0',
    'summary': 'Attendance & Committee Tracking for Involved Volunteers',
    'description': """
        Comprehensive volunteer management system with attendance tracking, 
        committee management, GPS-based check-in, and multi-language support.

        Key Features:
        • Volunteer and committee management
        • Advanced attendance tracking with GPS
        • Online and physical event management
        • Multi-language support (Arabic & English)
        • Automated certificate generation
        • Real-time notifications and reminders
        • Advanced reporting and analytics
        • Role-based access control
        • Mobile-responsive design

        Supports all volunteer management needs from registration to recognition.
    """,
    'category': 'Human Resources',
    'author': 'Volunteer Hub Organization',
    'depends': [
        'base',
       ],
    'data': [],

    'installable': True,
    'application': True,
}
