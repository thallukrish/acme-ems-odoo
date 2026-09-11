from odoo.tests.common import TransactionCase


class Testacmeemsmanufacturing(TransactionCase):
    def test_module_models_registered(self):
        self.assertTrue(self.env.registry)
