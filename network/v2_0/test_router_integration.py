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

from openstackclient.network.v2_0 import router
from openstackclient.tests.network.v2_0 import common


class TestShowRouterIntegration(common.TestIntegrationBase):
    HOSTESS = common.TestIntegrationBase.HOST + common.TestIntegrationBase.VER
    SUBNET_URL = HOSTESS + "/subnets.json"
    SUBNET_ONE = '{ "subnets": [{ "id": "45456777" }] }'
    PORT_URL = HOSTESS + "/ports.json"
    PORT_ONE = '{ "ports": [{ "id": "23422222" }] }'
    CREATE_URL = HOSTESS + "/routers.json"
    CREATE = """
{
   "router":
   {
       "status": "ACTIVE",
       "name": "rooty",
       "tenant_id": "33a40233",
       "id": "a9254bdb"
   }
}"""
    DELETE_URL = HOSTESS + "/routers/a9254bdb.json"
    DELETE = "{}"
    LIST_URL = HOSTESS + "/routers.json"
    LIST_ONE = '{ "routers": [{ "id": "a9254bdb" }] }'
    LIST = """
{
   "routers": [
       {
          "status": "ACTIVE",
          "name": "rooty",
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
    LIST_L3_URL = HOSTESS + "/agents/elthree/l3-routers.json"
    LIST_L3 = """
{
   "routers": [
       {
            "status": "ACTIVE",
            "external_gateway_info": {},
            "name": "rooty",
            "admin_state_up": true,
            "tenant_id": "3671f46ec35e4bbca6ef92ab7975e463",
            "routes": [],
            "id": "8eef2388"
       }
   ]
}"""
    SHOW_URL = HOSTESS + "/routers/a9254bdb.json"
    SHOW = CREATE
    ADD_URL = HOSTESS + "/routers/a9254bdb/add_router_interface.json"
    ADD = """
{
    "subnet_id": "45456777",
    "port_id": "93939392"
}"""
    REMOVE_URL = HOSTESS + "/routers/a9254bdb/remove_router_interface.json"
    REMOVE = "{}"

    @httpretty.activate
    def test_create(self):
        pargs = common.FakeParsedArgs()
        pargs.name = 'rooty'
        pargs.admin_state = 'ACTIVE'
        pargs.tenant_id = '33a40233'
        httpretty.register_uri(httpretty.POST, self.CREATE_URL,
                               body=self.CREATE)
        self.when_run(router.CreateRouter, pargs)
        self.assertEqual('', self.stderr())
        self.assertEqual(u"""\
Created a new router:
id="a9254bdb"
name="rooty"
status="ACTIVE"
tenant_id="33a40233"
""", self.stdout())

    @httpretty.activate
    def test_delete(self):
        pargs = common.FakeParsedArgs()
        pargs.id = 'rooty'
        httpretty.register_uri(httpretty.GET, self.LIST_URL,
                               body=self.LIST_ONE)
        httpretty.register_uri(httpretty.DELETE, self.DELETE_URL,
                               body=self.DELETE)
        self.when_run(router.DeleteRouter, pargs)
        self.assertEqual('', self.stderr())
        self.assertEqual(u'Deleted router: rooty\n',
                         self.stdout())

    @httpretty.activate
    def test_list(self):
        pargs = common.FakeParsedArgs()
        pargs.formatter = 'csv'
        pargs.l3_agent = None
        httpretty.register_uri(httpretty.GET, self.LIST_URL,
                               body=self.LIST)
        self.when_run(router.ListRouter, pargs)
        self.assertEqual('', self.stderr())
        self.assertEqual("""\
id,name
a9254bdb,rooty
b8408dgd,croc
""", self.stdout())

    @httpretty.activate
    def test_list_l3(self):
        pargs = common.FakeParsedArgs()
        pargs.formatter = 'csv'
        pargs.l3_agent = 'elthree'
        httpretty.register_uri(httpretty.GET, self.LIST_L3_URL,
                               body=self.LIST_L3)
        self.when_run(router.ListRouter, pargs)
        self.assertEqual('', self.stderr())
        self.assertEqual("""\
id,name,external_gateway_info
8eef2388,rooty,{}
""", self.stdout())

    @httpretty.activate
    def test_set(self):
        pargs = common.FakeParsedArgs()
        pargs.name = 'rooty'
        pargs.router_id = '88888823'
        pargs.no_gateway = True
        httpretty.register_uri(httpretty.GET, self.LIST_URL,
                               body=self.LIST_ONE)
        httpretty.register_uri(httpretty.PUT, self.SHOW_URL,
                               body=self.SHOW)
        self.when_run(router.SetRouter, pargs)
        self.assertEqual('', self.stderr())
        self.assertEqual(u'Removed gateway from router 88888823\n',
                         self.stdout())

    @httpretty.activate
    def test_show(self):
        pargs = common.FakeParsedArgs()
        pargs.id = 'rooty'
        httpretty.register_uri(httpretty.GET, self.LIST_URL,
                               body=self.LIST_ONE)
        httpretty.register_uri(httpretty.GET, self.SHOW_URL,
                               body=self.SHOW)
        self.when_run(router.ShowRouter, pargs)
        self.assertEqual('', self.stderr())
        self.assertEqual(u"""\
id="a9254bdb"
name="rooty"
status="ACTIVE"
tenant_id="33a40233"
""", self.stdout())

    @httpretty.activate
    def test_add_subnet(self):
        pargs = common.FakeParsedArgs()
        pargs.router_id = 'rooty'
        pargs.interface = 'subby'
        httpretty.register_uri(httpretty.GET, self.LIST_URL,
                               body=self.LIST_ONE)
        httpretty.register_uri(httpretty.GET, self.SUBNET_URL,
                               body=self.SUBNET_ONE)
        httpretty.register_uri(httpretty.PUT, self.ADD_URL,
                               body=self.ADD)
        expected_body = '{"subnet_id": "45456777"}'
        self.when_run(router.AddSubnetRouter, pargs, expected_body)
        self.assertEqual('', self.stderr())
        self.assertEqual(u'Added interface 93939392 to router rooty.\n',
                         self.stdout())

    @httpretty.activate
    def test_remove_subnet(self):
        pargs = common.FakeParsedArgs()
        pargs.router_id = 'rooty'
        pargs.interface = 'subby'
        httpretty.register_uri(httpretty.GET, self.LIST_URL,
                               body=self.LIST_ONE)
        httpretty.register_uri(httpretty.GET, self.SUBNET_URL,
                               body=self.SUBNET_ONE)
        httpretty.register_uri(httpretty.PUT, self.REMOVE_URL,
                               body=self.REMOVE)
        expected_body = '{"subnet_id": "45456777"}'
        self.when_run(router.RemoveSubnetRouter, pargs, expected_body)
        self.assertEqual('', self.stderr())
        self.assertEqual(u'Removed interface from router rooty.\n',
                         self.stdout())

    @httpretty.activate
    def test_add_port(self):
        pargs = common.FakeParsedArgs()
        pargs.router_id = 'rooty'
        pargs.port = 'puerto'
        httpretty.register_uri(httpretty.GET, self.LIST_URL,
                               body=self.LIST_ONE)
        httpretty.register_uri(httpretty.GET, self.PORT_URL,
                               body=self.PORT_ONE)
        httpretty.register_uri(httpretty.PUT, self.ADD_URL,
                               body=self.ADD)
        expected_body = '{"port_id": "23422222"}'
        self.when_run(router.AddPortRouter, pargs, expected_body)
        self.assertEqual('', self.stderr())
        self.assertEqual(u'Added interface 93939392 to router rooty.\n',
                         self.stdout())

    @httpretty.activate
    def test_remove_port(self):
        pargs = common.FakeParsedArgs()
        pargs.router_id = 'rooty'
        pargs.port = 'puerto'
        httpretty.register_uri(httpretty.GET, self.LIST_URL,
                               body=self.LIST_ONE)
        httpretty.register_uri(httpretty.GET, self.PORT_URL,
                               body=self.PORT_ONE)
        httpretty.register_uri(httpretty.PUT, self.REMOVE_URL,
                               body=self.REMOVE)
        expected_body = '{"port_id": "23422222"}'
        self.when_run(router.RemovePortRouter, pargs, expected_body)
        self.assertEqual('', self.stderr())
        self.assertEqual(u'Removed interface from router rooty.\n',
                         self.stdout())
