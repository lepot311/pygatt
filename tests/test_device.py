from nose.tools import ok_, eq_
from mock import Mock, patch
import unittest

from bluetooth_adapter import BleDevice


class BleDeviceTest(unittest.TestCase):

    mock_backend = Mock()

    def make_patch(self, *args, **kwargs):
        p = patch(*args, **kwargs)
        p.start()
        self.patchers.append(p)

    def setUp(self):
        self.patchers = []

    def tearDown(self):
        for p in self.patchers:
            p.stop()

    def test_init(self):
        ok_(BleDevice(self.mock_backend, '01:23:45:67:89:AB',
            name='Hello, World!', scan_response_rssi=-80))

    def test_get_name(self):
        expected_name = 'Hello, World!'
        dev = BleDevice(self.mock_backend, '01:23:45:67:89:AB',
                        name=expected_name, scan_response_rssi=-80)
        name = dev.get_name()
        eq_(name, expected_name)

    def test_get_mac_address(self):
        expected_mac = '01:23:45:67:89:AB'
        dev = BleDevice(self.mock_backend, expected_mac, name='Foobar',
                        scan_response_rssi=-80)
        mac = dev.get_mac_address()
        eq_(mac, expected_mac)

    def test_get_rssi_from_scan_response(self):
        expected_rssi = -74
        dev = BleDevice(self.mock_backend, '01:23:45:67:89:AB', name='Foobar',
                        scan_response_rssi=expected_rssi)
        rssi = dev.get_rssi(from_connection=False)
        eq_(rssi, expected_rssi)

    def test_get_rssi_from_connection(self):
        expected_rssi = -74
        dev = BleDevice(self.mock_backend, '01:23:45:67:89:AB', name='Foobar',
                        scan_response_rssi=-72)
        dev.connect()
        self.mock_backend.get_rssi.return_value = expected_rssi
        rssi = dev.get_rssi(from_connection=True)
        eq_(rssi, expected_rssi)
