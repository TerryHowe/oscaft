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

import httpretty

from openstackclient.network.v2_0.fw import firewall
from openstackclient.tests.oscaft import common


class TestFirewallIntegration(common.TestIntegrationBase):
    HOSTESS = common.TestIntegrationBase.HOST + common.TestIntegrationBase.VER
    POLICY_URL = HOSTESS + "/fw/firewall_policies.json"
    POLICY = '{ "firewall_policies": [{ "id": "9300303" }] }'
    CREATE_URL = HOSTESS + "/fw/firewalls.json"
    CREATE = """
{
   "firewall":
   {
       "status": "ACTIVE",
       "name": "gator",
       "tenant_id": "33a40233",
       "id": "a9254bdb"
   }
}"""
    DELETE_URL = HOSTESS + "/fw/firewalls/a9254bdb.json"
    DELETE = "{}"
    LIST_URL = HOSTESS + "/fw/firewalls.json"
    LIST_ONE = '{ "firewalls": [{ "id": "a9254bdb" }] }'
    LIST = """
{
   "firewalls": [
       {
          "status": "ACTIVE",
          "name": "gator",
          "tenant_id": "33a40233",
          "id": "a9254bdb"
       },
       {
          "status": "ACTIVE",
          "name": "croc",
          "tenant_id": "33a40233",
          "id": "b8408dgd"
       }
   ]
}"""
    SET_URL = HOSTESS + "/fw/firewalls/a9254bdb.json"
    SET = "{}"
    SHOW_URL = HOSTESS + "/fw/firewalls/a9254bdb.json"
    SHOW = CREATE

    @httpretty.activate
    def test_create(self):
        pargs = common.FakeParsedArgs()
        pargs.name = 'gator'
        pargs.firewall_policy_id = 'policy'
        pargs.description = None
        pargs.shared = False
        pargs.admin_state = True
        pargs.tenant_id = '33a40233'
        httpretty.register_uri(httpretty.GET, self.POLICY_URL,
                               body=self.POLICY)
        httpretty.register_uri(httpretty.POST, self.CREATE_URL,
                               body=self.CREATE)
        self.when_run(firewall.CreateFirewall, pargs)
        self.assertEqual('', self.stderr())
        self.assertEqual(u"""\
Created a new firewall:
id="a9254bdb"
name="gator"
status="ACTIVE"
tenant_id="33a40233"
""", self.stdout())

    @httpretty.activate
    def test_delete(self):
        pargs = common.FakeParsedArgs()
        pargs.identifier = 'gator'
        httpretty.register_uri(httpretty.GET, self.LIST_URL,
                               body=self.LIST_ONE)
        httpretty.register_uri(httpretty.DELETE, self.DELETE_URL,
                               body=self.DELETE)
        self.when_run(firewall.DeleteFirewall, pargs)
        self.assertEqual('', self.stderr())
        self.assertEqual(u'Deleted firewall: gator\n',
                         self.stdout())

    @httpretty.activate
    def test_list(self):
        pargs = common.FakeParsedArgs()
        pargs.formatter = 'csv'
        httpretty.register_uri(httpretty.GET, self.LIST_URL,
                               body=self.LIST)
        self.when_run(firewall.ListFirewall, pargs)
        self.assertEqual('', self.stderr())
        self.assertEqual("""\
id,name
a9254bdb,gator
b8408dgd,croc
""", self.stdout())

    @httpretty.activate
    def test_set(self):
        pargs = common.FakeParsedArgs()
        pargs.identifier = 'gator'
        httpretty.register_uri(httpretty.GET, self.LIST_URL,
                               body=self.LIST_ONE)
        httpretty.register_uri(httpretty.PUT, self.SET_URL,
                               body=self.SET)
        self.when_run(firewall.SetFirewall, pargs)
        self.assertEqual('', self.stderr())
        self.assertEqual('Updated firewall: gator\n', self.stdout())

    @httpretty.activate
    def test_show(self):
        pargs = common.FakeParsedArgs()
        pargs.identifier = 'gator'
        httpretty.register_uri(httpretty.GET, self.LIST_URL,
                               body=self.LIST_ONE)
        httpretty.register_uri(httpretty.GET, self.SHOW_URL,
                               body=self.SHOW)
        self.when_run(firewall.ShowFirewall, pargs)
        self.assertEqual('', self.stderr())
        self.assertEqual(u"""\
id="a9254bdb"
name="gator"
status="ACTIVE"
tenant_id="33a40233"
""", self.stdout())
