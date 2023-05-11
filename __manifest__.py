# -*- coding: utf-8 -*-
{
    "name": "Onesta - centro de costo",
    "version": "1.0",
    "author": "Mobilize (Jorge Quico)",
    'category': 'Mobilize/Apps',
    "application": True,
    "license": 'OPL-1',
    "depends": [ "purchase", "web", "sh_cost_center", "account", "account_reports", "stock_account", "stock_landed_costs" ],
    "data": [
        "views/search_template_view.xml",
        "views/sh_cost_center.xml",
    ],
    "summary": "Onesta - centro de costo",
    "description": """
        Onesta - centro de costo
        Agrega funcionalidad al módulo sh_cost_center
    """,
    'assets': {
        'web.assets_backend': [
            'mblz_onesta_cost_center/static/src/js/account_reports.js',
        ],
    }
}