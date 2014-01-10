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

from openstackclient.network.v2_0.vpn import service
from openstackclient.tests.network.v2_0 import common


class TestServiceIntegration(common.TestIntegrationBase):
    HOSTESS = common.TestIntegrationBase.HOST + common.TestIntegrationBase.VER
    SUBNETS_URL = HOSTESS + "/subnets.json"
    SUBNETS_ONE = '{ "subnets": [{ "id": "12312311" }]}'
    ROUTERS_URL = HOSTESS + "/routers.json"
    ROUTERS_ONE = '{ "routers": [{ "id": "33333333" }]}'
    CREATE_URL = HOSTESS + "/vpn/vpnservices.json"
    CREATE = """
{
   "vpnservice":
   {
       "status": "ACTIVE",
       "name": "gator",
       "tenant_id": "33a40233",
       "id": "a9254bdb"
   }
}"""
    DELETE_URL = HOSTESS + "/vpn/vpnservices/a9254bdb.json"
    DELETE = "{}"
    LIST_URL = HOSTESS + "/vpn/vpnservices.json"
    LIST_ONE = """
{
   "vpnservices": [{
       "id": "a9254bdb"
   }]
}"""
    LIST = """
{
   "vpnservices": [
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
    SHOW_URL = HOSTESS + "/vpn/vpnservices/a9254bdb.json"
    SHOW = CREATE

    @httpretty.activate
    def test_create(self):
        pargs = common.FakeParsedArgs()
        pargs.name = 'gator'
        pargs.subnet = 'subby'
        pargs.router = 'rooty'
        pargs.admin_state = True
        pargs.tenant_id = '33a40233'
        httpretty.register_uri(httpretty.GET, self.SUBNETS_URL,
                               body=self.SUBNETS_ONE)
        httpretty.register_uri(httpretty.GET, self.ROUTERS_URL,
                               body=self.ROUTERS_ONE)
        httpretty.register_uri(httpretty.POST, self.CREATE_URL,
                               body=self.CREATE)
        self.when_run(service.CreateService, pargs)
        self.assertEqual('', self.stderr())
        self.assertEqual(u"""\
Created a new vpnservice:
id="a9254bdb"
name="gator"
status="ACTIVE"
tenant_id="33a40233"
""", self.stdout())

    @httpretty.activate
    def test_delete(self):
        pargs = common.FakeParsedArgs()
        pargs.id = 'gator'
        httpretty.register_uri(httpretty.GET, self.LIST_URL,
                               body=self.LIST_ONE)
        httpretty.register_uri(httpretty.DELETE, self.DELETE_URL,
                               body=self.DELETE)
        self.when_run(service.DeleteService, pargs)
        self.assertEqual('', self.stderr())
        self.assertEqual(u'Deleted vpnservice: gator\n',
                         self.stdout())

    @httpretty.activate
    def test_list(self):
        pargs = common.FakeParsedArgs()
        pargs.formatter = 'csv'
        httpretty.register_uri(httpretty.GET, self.LIST_URL,
                               body=self.LIST)
        self.when_run(service.ListService, pargs)
        self.assertEqual('', self.stderr())
        self.assertEqual("""\
id,name,status
a9254bdb,gator,ACTIVE
b8408dgd,croc,ACTIVE
""", self.stdout())

    @httpretty.activate
    def test_set(self):
        pargs = common.FakeParsedArgs()
        pargs.name = 'gator'
        httpretty.register_uri(httpretty.GET, self.LIST_URL,
                               body=self.LIST_ONE)
        self.when_run(service.SetService, pargs)
        self.assertEqual('', self.stderr())
        self.assertEqual('', self.stdout())

    @httpretty.activate
    def test_show(self):
        pargs = common.FakeParsedArgs()
        pargs.id = 'gator'
        httpretty.register_uri(httpretty.GET, self.LIST_URL,
                               body=self.LIST_ONE)
        httpretty.register_uri(httpretty.GET, self.SHOW_URL,
                               body=self.SHOW)
        self.when_run(service.ShowService, pargs)
        self.assertEqual('', self.stderr())
        self.assertEqual(u"""\
id="a9254bdb"
name="gator"
status="ACTIVE"
tenant_id="33a40233"
""", self.stdout())
