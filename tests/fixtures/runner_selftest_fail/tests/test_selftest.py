from odoo.tests import TransactionCase, tagged


@tagged("post_install", "-at_install")
class TestSelftestFail(TransactionCase):
    """Deliberately fails so odoo-runner's non-zero exit path can be verified."""

    def test_always_fails(self):
        self.fail("odoo-runner selftest: intentional failure")
