# -*- encoding: utf-8 -*-
'''
    :codeauthor: :email: `Ondrej Holecek <oholecek@suse.com>`

    tests.integration.states.firewalld
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
'''
# Python libs
from __future__ import absolute_import, unicode_literals, print_function

# Import salt testing libs
from tests.support.case import ModuleCase
from tests.support.helpers import destructiveTest
from tests.support.mixins import SaltReturnAssertsMixin


@destructiveTest
class FirewalldTest(ModuleCase, SaltReturnAssertsMixin):
    '''
    Validate firwalld state module

    This is a destructive test, it creates new firewalld zones 'test-zone' and 'test-zone2'.
    '''
    def setUp(self):
        os_family = self.run_function('grains.get', ['os_family'])
        if os_family not in ('RedHat', 'Suse'):
            self.skipTest('Network state only supported on RedHat and SUSE based systems')

    def test_present(self):
        '''
        firewalld.present
        '''
        ret = self.run_state('firewalld.present', name='test-zone', interface='dummy0')
        self.assertSaltTrueReturn(ret)
        self.assertSaltStateChangesEqual(ret, 'dummy0', keys=['interfaces'])
        ret = self.run_function('firewalld.get_interfaces', name='test-zone')
        self.assertEqual(ret, 'dummy0')
        ret = self.run_state('firewall.present', name='test-zone2', interface='dummy0')
        self.assertSaltTrueReturn(ret)
        self.assertSaltStateChangesEqual(ret, 'dummy0', keys=['interfaces'])
        ret = self.run_function('firewalld.get_interfaces', name='test-zone')
        self.assertEqual(ret, '')
        ret = self.run_function('firewalld.get_interfaces', name='test-zone2')
        self.assertEqual(ret, 'dummy0')
