#   Copyright 2013 OpenStack, LLC.
#
#   Licensed under the Apache License, Version 2.0 (the "License"); you may
#   not use this file except in compliance with the License. You may obtain
#   a copy of the License at
#
#        http://www.apache.org/licenses/LICENSE-2.0
#
#   Unless required by applicable law or agreed to in writing, software
#   distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
#   WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
#   License for the specific language governing permissions and limitations
#   under the License.
#

import argparse
import httpretty
import sys
import traceback

from openstackclient import shell
from openstackclient.tests import fakes
from openstackclient.tests import utils
from neutronclient.v2_0 import client


class FakeOptions(argparse.Namespace):
    def __init__(self):
        super(FakeOptions, self).__init__()
        self.debug = False
        self.deferred_help = False
        self.insecure = True
        self.os_default_domain = 'testing'
        self.os_cacert = False
        self.os_identity_api_version = 'idversion'
        self.os_password = 'password'
        self.os_project_id = 'project_id'
        self.os_project_name = 'project_name'
        self.os_region_name = 'region_name'
        self.os_network_api_version = '2.0'
        self.os_token = 'token'
        self.os_url = 'http://127.0.0.1'
        self.os_auth_url = 'http://127.0.0.1/identity'
        self.os_username = 'username'


class FakeParsedArgs(argparse.Namespace):
    def __init__(self):
        super(FakeParsedArgs, self).__init__()
        self.show_details = True
        self.request_format = 'json'
        self.prefix = ''
        self.fields = []
        self.columns = []
        self.variables = []
        self.formatter = 'shell'
        self.quote_mode = 'none'


class FakeShell(shell.OpenStackShell):
    def __init__(self):
        super(FakeShell, self).__init__()
        self.options = { 'debug': False,
                         'insecure': True,
                         'endpoint_url': 'http://127.0.0.1',
                         'region_name': 'region_x',
                         'token': 'token',
                         'auth_url': 'http://127.0.0.1/identity',
                         'password': 'wasspord',
                         'tenant_id': 'iddy',
                         'tenant_name': 'nameo',
                         'username': 'username'}
        try:
            self.initialize_app(["run.py", "help"])
        except Exception:
            print('\n'.join(traceback.format_tb(sys.exc_info()[2])))
        try:
            self.authenticate_user()
        except Exception:
            print('\n'.join(traceback.format_tb(sys.exc_info()[2])))
        self.stdout = fakes.FakeStdout()
        self.stderr = fakes.FakeStdout()
        self.client_manager = fakes.FakeClientManager()
        self.client_manager.network = client.Client(**self.options)


class TestIntegrationBase(utils.TestCase):
    HOST = "http://127.0.0.1"
    VER = "/v2.0"

    def setUp(self):
        super(TestIntegrationBase, self).setUp()
        self.app = FakeShell()

    def when_run(self, clazz, pargs, expected_body=None):
        try:
            result = clazz(self.app, pargs).run(pargs)
        except Exception as e:
            print('\n'.join(traceback.format_tb(sys.exc_info()[2])))
            print(str(e))
            lasty = httpretty.last_request()
            print('====================================================')
            print("body = " + str(lasty.body))
            print("querystring = " + str(getattr(lasty, 'querystring', '')))
            print("command = " + str(getattr(lasty, 'command', '')))
            print("method = " + str(getattr(lasty, 'method', '')))
            print("path = " + str(getattr(lasty, 'path', '')))
            print('====================================================')
            raise e
        self.assertEqual(0, result)
        if expected_body:
            lasty = httpretty.last_request()
            self.assertEqual(expected_body, lasty.body)

    def stdout(self):
        return self.app.stdout.lines()

    def stderr(self):
        return self.app.stderr.lines()