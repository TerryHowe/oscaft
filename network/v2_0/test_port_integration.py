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

from openstackclient.network.v2_0 import port
from openstackclient.tests.oscaft import common


class TestPortIntegration(common.TestIntegrationBase):
    HOSTESS = common.TestIntegrationBase.HOST + common.TestIntegrationBase.VER
    NETWORK_URL = HOSTESS + "/networks.json"
    NETWORK = '{ "networks": [{ "id": "1111111" }] }'
    ROUTER_URL = HOSTESS + "/routers.json"
    ROUTER = '{ "routers": [{ "id": "22222222" }] }'
    CREATE_URL = HOSTESS + "/ports.json"
    CREATE = """
{
   "port":
   {
       "status": "ACTIVE",
       "name": "puerto",
       "tenant_id": "33a40233",
       "id": "a9254bdb"
   }
}"""
    DELETE_URL = HOSTESS + "/ports/a9254bdb.json"
    DELETE = "{}"
    LIST_URL = HOSTESS + "/ports.json"
    LIST_ONE = '{ "ports": [{ "id": "a9254bdb" }] }'
    LIST = """
{
   "ports": [
       {
          "status": "ACTIVE",
          "name": "puerto",
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
    SET_URL = HOSTESS + "/ports/a9254bdb.json"
    SET = "{}"
    SHOW_URL = HOSTESS + "/ports/a9254bdb.json"
    SHOW = CREATE
    ADD_REMOVE_URL = HOSTESS + "/floatingips/127.0.0.1.json"
    ADD_REMOVE = "{}"

    @httpretty.activate
    def test_create(self):
        pargs = common.FakeParsedArgs()
        pargs.name = 'puerto'
        pargs.network_id = '44444448'
        pargs.admin_state = 'UP'
        pargs.mac_address = '1231233212'
        pargs.device_id = '1231231237'
        pargs.fixed_ip = None
        pargs.security_groups = None
        pargs.no_security_groups = False
        pargs.extra_dhcp_opts = None
        pargs.tenant_id = '33a40233'
        httpretty.register_uri(httpretty.GET, self.NETWORK_URL,
                               body=self.NETWORK)
        httpretty.register_uri(httpretty.POST, self.CREATE_URL,
                               body=self.CREATE)
        self.when_run(port.CreatePort, pargs)
        self.assertEqual('', self.stderr())
        self.assertEqual(u"""\
Created a new port:
id="a9254bdb"
name="puerto"
status="ACTIVE"
tenant_id="33a40233"
""", self.stdout())

    @httpretty.activate
    def test_delete(self):
        pargs = common.FakeParsedArgs()
        pargs.identifier = 'puerto'
        httpretty.register_uri(httpretty.GET, self.LIST_URL,
                               body=self.LIST_ONE)
        httpretty.register_uri(httpretty.DELETE, self.DELETE_URL,
                               body=self.DELETE)
        self.when_run(port.DeletePort, pargs)
        self.assertEqual('', self.stderr())
        self.assertEqual(u'Deleted port: puerto\n',
                         self.stdout())

    @httpretty.activate
    def test_list(self):
        pargs = common.FakeParsedArgs()
        pargs.router = 'roo'
        pargs.page_size = None
        pargs.sort_key = []
        pargs.sort_dir = []
        pargs.formatter = 'csv'
        httpretty.register_uri(httpretty.GET, self.ROUTER_URL,
                               body=self.ROUTER)
        httpretty.register_uri(httpretty.GET, self.LIST_URL,
                               body=self.LIST)
        self.when_run(port.ListPort, pargs)
        self.assertEqual('', self.stderr())
        self.assertEqual("""\
id,name
a9254bdb,puerto
b8408dgd,croc
""", self.stdout())

    @httpretty.activate
    def test_set(self):
        pargs = common.FakeParsedArgs()
        pargs.identifier = 'puerto'
        httpretty.register_uri(httpretty.GET, self.LIST_URL,
                               body=self.LIST_ONE)
        httpretty.register_uri(httpretty.PUT, self.SET_URL,
                               body=self.SET)
        self.when_run(port.SetPort, pargs)
        self.assertEqual('', self.stderr())
        self.assertEqual('', self.stdout())

    @httpretty.activate
    def test_show(self):
        pargs = common.FakeParsedArgs()
        pargs.identifier = 'puerto'
        httpretty.register_uri(httpretty.GET, self.LIST_URL,
                               body=self.LIST_ONE)
        httpretty.register_uri(httpretty.GET, self.SHOW_URL,
                               body=self.SHOW)
        self.when_run(port.ShowPort, pargs)
        self.assertEqual('', self.stderr())
        self.assertEqual(u"""\
id="a9254bdb"
name="puerto"
status="ACTIVE"
tenant_id="33a40233"
""", self.stdout())

    @httpretty.activate
    def test_add(self):
        pargs = common.FakeParsedArgs()
        pargs.port_id = 'puerto'
        pargs.floatingip_id = '127.0.0.1'
        pargs.fixed_ip_address = None
        httpretty.register_uri(httpretty.PUT, self.ADD_REMOVE_URL,
                               body=self.ADD_REMOVE)
        self.when_run(port.AddPort, pargs)
        self.assertEqual('', self.stderr())
        self.assertEqual(u'Associated floatingip 127.0.0.1\n', self.stdout())

    @httpretty.activate
    def test_remove(self):
        pargs = common.FakeParsedArgs()
        pargs.port_id = 'puerto'
        pargs.floatingip_id = '127.0.0.1'
        httpretty.register_uri(httpretty.PUT, self.ADD_REMOVE_URL,
                               body=self.ADD_REMOVE)
        self.when_run(port.RemovePort, pargs)
        self.assertEqual('', self.stderr())
        self.assertEqual(u'Disassociated floatingip 127.0.0.1\n',
                         self.stdout())
