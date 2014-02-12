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

from openstackclient.network.v2_0 import network
from openstackclient.tests.oscaft import common


class TestNetworkIntegration(common.TestIntegrationBase):
    HOSTESS = common.TestIntegrationBase.HOST + common.TestIntegrationBase.VER
    SUBNETS_URL = HOSTESS + "/subnets.json"
    SUBNETS_ONE = '{ "subnets": [{ "id": "12312311" }]}'
    GATEWAY_URL = HOSTESS + "/network-gateways.json"
    GATEWAY_ONE = '{ "network_gateways": [{ "id": "88888888" }]}'
    DHCP_URL = HOSTESS + "/agents/orange/dhcp-networks.json"
    CREATE_URL = HOSTESS + "/networks.json"
    CREATE = """
{
   "network":
   {
       "status": "ACTIVE",
       "name": "gator",
       "tenant_id": "33a40233",
       "id": "a9254bdb"
   }
}"""
    DELETE_URL = HOSTESS + "/networks/a9254bdb.json"
    DELETE = "{}"
    LIST_URL = HOSTESS + "/networks.json"
    LIST_ONE = """
{
   "networks": [{
       "id": "a9254bdb"
   }]
}"""
    LIST = """
{
   "networks": [
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
    SET_URL = HOSTESS + "/networks/a9254bdb.json"
    SET = "{}"
    SHOW_URL = HOSTESS + "/networks/a9254bdb.json"
    SHOW = CREATE
    CONNECT_URL = HOSTESS + "/network-gateways/88888888/connect_network.json"
    CONNECT = "{}"
    DISCONNECT_URL = HOSTESS + \
        "/network-gateways/88888888/disconnect_network.json"
    DISCONNECT = "{}"

    @httpretty.activate
    def test_create(self):
        pargs = common.FakeParsedArgs()
        pargs.name = 'gator'
        pargs.admin_state = True
        pargs.shared = True
        pargs.tenant_id = '33a40233'
        httpretty.register_uri(httpretty.POST, self.CREATE_URL,
                               body=self.CREATE)
        self.when_run(network.CreateNetwork, pargs)
        self.assertEqual('', self.stderr())
        self.assertEqual(u"""\
Created a new network:
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
        self.when_run(network.DeleteNetwork, pargs)
        self.assertEqual('', self.stderr())
        self.assertEqual(u'Deleted network: gator\n',
                         self.stdout())

    @httpretty.activate
    def test_list(self):
        pargs = common.FakeParsedArgs()
        pargs.formatter = 'csv'
        pargs.external = False
        pargs.dhcp_agent = None
        httpretty.register_uri(httpretty.GET, self.SUBNETS_URL,
                               body=self.SUBNETS_ONE)
        httpretty.register_uri(httpretty.GET, self.LIST_URL,
                               body=self.LIST)
        self.when_run(network.ListNetwork, pargs)
        self.assertEqual('', self.stderr())
        self.assertEqual("""\
id,name
a9254bdb,gator
b8408dgd,croc
""", self.stdout())

    @httpretty.activate
    def test_list_external(self):
        pargs = common.FakeParsedArgs()
        pargs.formatter = 'csv'
        pargs.external = True
        pargs.dhcp_agent = None
        httpretty.register_uri(httpretty.GET, self.SUBNETS_URL,
                               body=self.SUBNETS_ONE)
        httpretty.register_uri(httpretty.GET, self.LIST_URL,
                               body=self.LIST)
        self.when_run(network.ListNetwork, pargs)
        self.assertEqual('', self.stderr())
        self.assertEqual("""\
id,name
a9254bdb,gator
b8408dgd,croc
""", self.stdout())

    #@httpretty.activate
    #def test_list_dhcp_agent(self):
    #    pargs = common.FakeParsedArgs()
    #    pargs.formatter = 'csv'
    #    pargs.external = False
    #    pargs.dhcp_agent = 'orange'
    #    httpretty.register_uri(httpretty.GET, self.DHCP_URL,
    #                           body=self.LIST)
    #    httpretty.register_uri(httpretty.GET, self.SUBNETS_URL,
    #                           body=self.SUBNETS_ONE)
    #    self.when_run(network.ListNetwork, pargs)
    #    self.assertEqual('', self.stderr())
    #    self.assertEqual("""\
#id,name
#a9254bdb,gator
#b8408dgd,croc
#""", self.stdout())

    @httpretty.activate
    def test_set(self):
        pargs = common.FakeParsedArgs()
        pargs.identifier = 'gator'
        httpretty.register_uri(httpretty.GET, self.LIST_URL,
                               body=self.LIST_ONE)
        httpretty.register_uri(httpretty.PUT, self.SET_URL,
                               body=self.SET)
        self.when_run(network.SetNetwork, pargs)
        self.assertEqual('', self.stderr())
        self.assertEqual('Updated network: gator\n', self.stdout())

    @httpretty.activate
    def test_show(self):
        pargs = common.FakeParsedArgs()
        pargs.identifier = 'gator'
        httpretty.register_uri(httpretty.GET, self.LIST_URL,
                               body=self.LIST_ONE)
        httpretty.register_uri(httpretty.GET, self.SHOW_URL,
                               body=self.SHOW)
        self.when_run(network.ShowNetwork, pargs)
        self.assertEqual('', self.stderr())
        self.assertEqual(u"""\
id="a9254bdb"
name="gator"
status="ACTIVE"
tenant_id="33a40233"
""", self.stdout())

    @httpretty.activate
    def test_add_gateway(self):
        pargs = common.FakeParsedArgs()
        pargs.network = 'gator'
        pargs.gateway = 'way'
        pargs.segmentation_type = None
        pargs.segmentation_id = None
        httpretty.register_uri(httpretty.GET, self.GATEWAY_URL,
                               body=self.GATEWAY_ONE)
        httpretty.register_uri(httpretty.GET, self.LIST_URL,
                               body=self.LIST_ONE)
        httpretty.register_uri(httpretty.PUT, self.CONNECT_URL,
                               body=self.CONNECT)
        self.when_run(network.AddGatewayNetwork, pargs)
        self.assertEqual('', self.stderr())
        self.assertEqual(u'Connected network to gateway 88888888\n',
                         self.stdout())

    @httpretty.activate
    def test_remove_gateway(self):
        pargs = common.FakeParsedArgs()
        pargs.network = 'gator'
        pargs.gateway = 'way'
        pargs.segmentation_type = None
        pargs.segmentation_id = None
        httpretty.register_uri(httpretty.GET, self.GATEWAY_URL,
                               body=self.GATEWAY_ONE)
        httpretty.register_uri(httpretty.GET, self.LIST_URL,
                               body=self.LIST_ONE)
        httpretty.register_uri(httpretty.PUT, self.DISCONNECT_URL,
                               body=self.DISCONNECT)
        self.when_run(network.RemoveGatewayNetwork, pargs)
        self.assertEqual('', self.stderr())
        self.assertEqual(u'Disconnected network from gateway 88888888\n',
                         self.stdout())
