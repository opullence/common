import unittest

from opulence.common.plugins import BasePlugin, PluginStatus, PluginManager


class TestPluginManager(unittest.TestCase):
    def test_plugin_manager_empty(self):
        class basePlugin(BasePlugin):
            _name_ = "name"
            _description_ = "desc"
            _author_ = "author"
            _version_ = 1

        pm = PluginManager()
        pm._plugins_ = {}
        self.assertFalse(pm.get_plugins())
        basePlugin()
        self.assertTrue(pm.get_plugins())
        self.assertTrue(pm.get_plugins(package="tests."))
