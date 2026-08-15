# Deliberately no `from . import tests` here: Odoo's own test loader
# (odoo/tests/loader.py get_test_modules) imports the tests subpackage
# directly. Importing it from the top-level __init__ would pull the test
# framework into every normal module load, not just test runs.
