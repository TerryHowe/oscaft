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

from openstackclient.network.v2_0 import floatingip
from openstackclient.tests.oscaft import common


class TestFloatingIpIntegration(common.TestIntegrationBase):
    HOSTESS = common.TestIntegrationBase.HOST + common.TestIntegrationBase.VER
    NETWORK_URL = HOSTESS + "/networks.json"
    NETWORK_ONE = '{ "networks": [{ "id": "2222223" }] }'
    CREATE_URL = HOSTESS + "/floatingips.json"
    CREATE = """
{
   "floatingip":
   {
       "status": "ACTIVE",
       "name": "nameo",
       "tenant_id": "33a40233",
       "id": "a9254bdb"
   }
}"""
    DELETE_URL = HOSTESS + "/floatingips/nameo.json"
    DELETE = "{}"
    LIST_URL = HOSTESS + "/floatingips.json"
    LIST_ONE = '{ "floatingips": [{ "id": "a9254bdb" }] }'
    LIST = """
{
   "floatingips": [
       {
          "id": "a9254bdb",
          "fixed_ip_address": "10.1.1.1",
          "floating_ip_address": "15.1.1.2",
          "port_id": "9090909",
          "tenant_id": "33a40233"
       },
       {
          "id": "b8408dgd",
          "fixed_ip_address": "10.1.1.2",
          "floating_ip_address": "15.1.1.3",
          "port_id": "8080808",
          "tenant_id": "33a40233"
       }
   ]
}"""
    SHOW_URL = HOSTESS + "/floatingips/nameo.json"
    SHOW = CREATE

    @httpretty.activate
    def test_create(self):
        pargs = common.FakeParsedArgs()
        pargs.name = 'nameo'
        pargs.floating_network_id = '123123'
        pargs.port_id = '7777899'
        pargs.fixed_ip_address = None
        pargs.tenant_id = '33a40233'
        httpretty.register_uri(httpretty.GET, self.NETWORK_URL,
                               body=self.NETWORK_ONE)
        httpretty.register_uri(httpretty.POST, self.CREATE_URL,
                               body=self.CREATE)
        self.when_run(floatingip.CreateFloatingIp, pargs)
        self.assertEqual('', self.stderr())
        self.assertEqual(u"""\
Created a new floatingip:
id="a9254bdb"
name="nameo"
status="ACTIVE"
tenant_id="33a40233"
""", self.stdout())

    @httpretty.activate
    def test_delete(self):
        pargs = common.FakeParsedArgs()
        pargs.identifier = 'nameo'
        httpretty.register_uri(httpretty.DELETE, self.DELETE_URL,
                               body=self.DELETE)
        self.when_run(floatingip.DeleteFloatingIp, pargs)
        self.assertEqual('', self.stderr())
        self.assertEqual(u'Deleted floatingip: nameo\n',
                         self.stdout())

    @httpretty.activate
    def test_list(self):
        pargs = common.FakeParsedArgs()
        pargs.formatter = 'csv'
        httpretty.register_uri(httpretty.GET, self.LIST_URL,
                               body=self.LIST)
        self.when_run(floatingip.ListFloatingIp, pargs)
        self.assertEqual('', self.stderr())
        self.assertEqual("""\
id,fixed_ip_address,floating_ip_address,port_id
a9254bdb,10.1.1.1,15.1.1.2,9090909
b8408dgd,10.1.1.2,15.1.1.3,8080808
""", self.stdout())

    @httpretty.activate
    def test_show(self):
        pargs = common.FakeParsedArgs()
        pargs.identifier = 'nameo'
        httpretty.register_uri(httpretty.GET, self.SHOW_URL,
                               body=self.SHOW)
        self.when_run(floatingip.ShowFloatingIp, pargs)
        self.assertEqual('', self.stderr())
        self.assertEqual(u"""\
id="a9254bdb"
name="nameo"
status="ACTIVE"
tenant_id="33a40233"
""", self.stdout())
