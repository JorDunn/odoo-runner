{
    "name": "Odoo Runner Selftest Fail",
    "summary": "Minimal module used by odoo-runner to validate its failing-test path.",
    # See runner_selftest_ok/__manifest__.py: no hardcoded series prefix so
    # this stays installable across any --odoo version.
    "version": "1.0.0",
    "category": "Hidden",
    "author": "3C LLC",
    "license": "AGPL-3",
    "depends": ["base"],
    "data": [],
    "installable": True,
    "application": False,
}
