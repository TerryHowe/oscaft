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

from openstackclient.network.v2_0 import dhcp
from openstackclient.tests.oscaft import common


class TestGatewayIntegration(common.TestIntegrationBase):
    HOSTESS = common.TestIntegrationBase.HOST + common.TestIntegrationBase.VER
    NETWORK_URL = HOSTESS + "/networks.json"
    NETWORK_ONE = '{ "networks": [{ "id": "12312311" }]}'
    ADD_URL = HOSTESS + "/agents/cash/dhcp-networks.json"
    ADD = """
{
   "agent":
   {
       "status": "ACTIVE",
       "name": "gator",
       "tenant_id": "33a40233",
       "id": "a9254bdb"
   }
}"""
    REMOVE_URL = HOSTESS + "/agents/nelson/dhcp-networks/12312311.json"
    REMOVE = "{}"
    LIST_URL = HOSTESS + "/networks/12312311/dhcp-agents.json"
    LIST = """
{
   "agents": [
       {
          "status": "ACTIVE",
          "host": "gator",
          "tenant_id": "33a40233",
          "admin_state_up": "true",
          "alive": false,
          "id": "a9254bdb"
       },
       {
          "host": "croc",
          "tenant_id": "33a40233",
          "admin_state_up": "true",
          "alive": true,
          "id": "b8408dgd"
       }
   ]
}"""

    @httpretty.activate
    def test_add(self):
        pargs = common.FakeParsedArgs()
        pargs.network = 'johnny'
        pargs.dhcp_agent = 'cash'
        pargs.tenant_id = '33a40233'
        httpretty.register_uri(httpretty.GET, self.NETWORK_URL,
                               body=self.NETWORK_ONE)
        httpretty.register_uri(httpretty.POST, self.ADD_URL,
                               body=self.ADD)
        self.when_run(dhcp.AddNetworkDhcpAgent, pargs)
        self.assertEqual('', self.stderr())
        self.assertEqual(u'Added network johnny to DHCP agent\n',
                         self.stdout())

    @httpretty.activate
    def test_remove(self):
        pargs = common.FakeParsedArgs()
        pargs.network = 'willie'
        pargs.dhcp_agent = 'nelson'
        httpretty.register_uri(httpretty.GET, self.NETWORK_URL,
                               body=self.NETWORK_ONE)
        httpretty.register_uri(httpretty.DELETE, self.REMOVE_URL,
                               body=self.REMOVE)
        self.when_run(dhcp.RemoveNetworkDhcpAgent, pargs)
        self.assertEqual('', self.stderr())
        self.assertEqual(u'Removed network willie to DHCP agent\n',
                         self.stdout())

    @httpretty.activate
    def test_list(self):
        pargs = common.FakeParsedArgs()
        pargs.network = 'range'
        pargs.formatter = 'csv'
        httpretty.register_uri(httpretty.GET, self.NETWORK_URL,
                               body=self.NETWORK_ONE)
        httpretty.register_uri(httpretty.GET, self.LIST_URL,
                               body=self.LIST)
        self.when_run(dhcp.ListDhcpAgent, pargs)
        self.assertEqual('', self.stderr())
        self.assertEqual("""\
id,host,admin_state_up,alive
a9254bdb,gator,true,xxx
b8408dgd,croc,true,:-)
""", self.stdout())
