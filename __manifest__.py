# -*- coding: utf-8 -*-
{
    'name': "Auto Servicios",

    'summary': """
        """,

    'description': """
        Auto servicios con facturación y reportes basicos.
    """,

    'author': "Luis Auyadermont",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/13.0/odoo/addons/base/data/ir_module_category_data.xml
    # for the full list
    'category': 'account',
    'version': '0.31',

    # any module necessary for this one to work correctly
    'depends': ['base','account','product'],

    # always loaded
    'data': [
        'security/ir.model.access.csv',
        'views/auto_services.xml',
        'views/product_view.xml',
        'report/report_services_analitc.xml',
        'report/report_services_vehicle.xml',
        'data/products.xml',
    ],
    # only loaded in demonstration mode
    'demo': [
        'demo/demo.xml',
    ],
}
