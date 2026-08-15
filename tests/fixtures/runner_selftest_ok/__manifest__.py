{
    "name": "Odoo Runner Selftest OK",
    "summary": "Minimal module used by odoo-runner to validate its passing-test path.",
    # No hardcoded series prefix. Odoo's own adapt_version() (odoo/modules/
    # module.py) auto-prefixes an "x.y.z"-shaped version with whatever
    # series is actually running, so this stays installable across
    # odoo-runner's --odoo 18, 19, 20, ... without editing the fixture.
    "version": "1.0.0",
    "category": "Hidden",
    "author": "3C LLC",
    "license": "AGPL-3",
    "depends": ["base"],
    "data": [],
    "installable": True,
    "application": False,
}
