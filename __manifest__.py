{
    "name": "Test Shopify Connector",
    "summary": """Connects to Shopify, pulls products every hour, creates/updates
     product information""",
    "author": "Vnikolayev",
    "website": "https://github.com/vnikolayev1/",
    "category": "Other",
    "version": "16.0.0.0.1",
    "license": "Other proprietary",
    "depends": [
        "base",
        "sale_management",
        "stock",
    ],
    "data": [
        "security/ir.model.access.csv",
        "data/ir_cron.xml",
        "views/res_config_settings.xml",
    ],
    "assets": {},
    "demo": [],
    "external_dependencies": {
        'python': [
            'shopify',
        ],
    },
    'application': True,
}
