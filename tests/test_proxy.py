
import unittest

from mazure.services import app
from mazure.proxy import Mazure
from mazure.services.utils import register, services


class TestMazureProxy(unittest.TestCase):
    def setUp(self):
        app.config['TESTING'] = True
        self.proxy = Mazure(['compute', 'storage'])
        register(app, services(app, self.proxy.targets))

    def test_setup(self):
        self.assertEqual(len(self.proxy.http.registered()), 0)
        self.proxy.setup()
        self.assertGreater(len(self.proxy.http.registered()), 0)

    def test_cleanup(self):
        self.proxy.setup()
        self.assertGreater(len(self.proxy.http.registered()), 0)

        self.proxy.cleanup()
        self.assertEqual(len(self.proxy.http.registered()), 0)

    def test_routable(self):
        valid = [
            ('/common/discovery/instance', 'GET'),
            ('/f2b5fff9-6c2e-45c0-8e9e-0d738ea0a87e/oauth2/v2.0/token', 'POST'),
            ('/5a59ee82-e041-4aab-bbef-03ff058c7ba1/v2.0/.well-known/openid-configuration', 'GET'),
        ]
        for path, method in valid:
            self.assertTrue(self.proxy.routable(path, method))

        invalid = [
            ('/common/discovery/instance?api-version=1.1&authorization_endpoint=https://login.microsoftonline.com/common/oauth2/authorize', 'GET')
        ]
        for path, method in invalid:
            self.assertFalse(self.proxy.routable(path, method))


if __name__ == '__main__':
    unittest.main()
