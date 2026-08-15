from odoo.tests import HttpCase, TransactionCase, tagged


@tagged("post_install", "-at_install")
class TestSelftestOk(TransactionCase):
    """Sanity check that the module installs and the ORM is queryable."""

    def test_partner_search(self):
        partners = self.env["res.partner"].search([], limit=1)
        self.assertIsInstance(partners.ids, list)


@tagged("post_install", "-at_install")
class TestSelftestOkHttp(HttpCase):
    """Exercises the browser-driven HttpCase path.

    A plain url_open (no headless Chrome involved) always runs. The
    browser_js call below drives a real headless Chrome tab and needs both
    the Chrome binary and the websocket-client Python package; without
    them Odoo raises unittest.SkipTest automatically, which is exactly the
    path odoo-runner's --browser flag exists to enable.
    """

    def test_login_page_loads(self):
        self.url_open("/web/login")

    def test_login_page_tour(self):
        self.browser_js("/odoo/login", "console.log('test successful')", login=None)
