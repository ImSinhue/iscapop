# -*- coding: utf-8 -*-
{
    'name': "Iscapop_APP",

    'summary': "App to donate material to other schools",

    'description': """
App to donate material to other schools
    """,

    'author': "Miguel Alanzabes Narbona",
    'website': "https://www.miguel.com",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/15.0/odoo/addons/base/data/ir_module_category_data.xml
    # for the full list
    'category': 'Uncategorized',
    'version': '0.1',

    # any module necessary for this one to work correctly
    'depends': ['base'],

    # always loaded
    'data': [
        'security/ir.model.access.csv',
        'views/itemView.xml',
        'views/categoryView.xml',
        'views/locationView.xml',
        'views/bulkanaddview.xml',
        'views/wizardmoveview.xml',
        'views/donationswizardview.xml',
        'views/returndonationsview.xml',
        'views/donationsview.xml',
        'views/pdfRecordView.xml',
        'views/wizardretire.xml',
        'views/wizardlocation.xml',
        'views/pdfRetiredView.xml',

    ],
    # only loaded in demonstration mode
    'demo': [
        'demo/demo.xml',
    ],

    'application': True,
    'installable': True,
}

