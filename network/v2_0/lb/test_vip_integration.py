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

from openstackclient.network.v2_0.lb import vip
from openstackclient.tests.network.v2_0 import common


class TestVipIntegration(common.TestIntegrationBase):
    HOSTESS = common.TestIntegrationBase.HOST + common.TestIntegrationBase.VER
    POOLS_URL = HOSTESS + "/lb/pools.json"
    POOLS = '{ "pools": [{ "id": "1111111" }] }'
    SUBNETS_URL = HOSTESS + "/subnets.json"
    SUBNETS = '{ "subnets": [{ "id": "222222" }] }'
    CREATE_URL = HOSTESS + "/lb/vips.json"
    CREATE = """
{
   "vip":
   {
       "status": "ACTIVE",
       "name": "nameo",
       "tenant_id": "33a40233",
       "id": "a9254bdb"
   }
}"""
    DELETE_URL = HOSTESS + "/lb/vips/a9254bdb.json"
    DELETE = "{}"
    LIST_URL = HOSTESS + "/lb/vips.json"
    LIST_ONE = '{ "vips": [{ "id": "a9254bdb" }] }'
    LIST = """
{
   "vips": [
       {
          "status": "ACTIVE",
          "name": "nameo",
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
    SHOW_URL = HOSTESS + "/lb/vips/a9254bdb.json"
    SHOW = CREATE
    ADD_REMOVE_URL = HOSTESS + "/floatingips/127.0.0.1.json"
    ADD_REMOVE = "{}"

    @httpretty.activate
    def test_create(self):
        pargs = common.FakeParsedArgs()
        pargs.name = 'nameo'
        pargs.pool_id = 'swimming'
        pargs.address = '127.0.0.1'
        pargs.admin_state = True
        pargs.connection_limit = '10'
        pargs.description = None
        pargs.protocol_port = '22'
        pargs.protocol = 'TCP'
        pargs.subnet_id = 'subby'
        pargs.tenant_id = '33a40233'
        httpretty.register_uri(httpretty.GET, self.POOLS_URL,
                               body=self.POOLS)
        httpretty.register_uri(httpretty.GET, self.SUBNETS_URL,
                               body=self.SUBNETS)
        httpretty.register_uri(httpretty.POST, self.CREATE_URL,
                               body=self.CREATE)
        self.when_run(vip.CreateVip, pargs)
        self.assertEqual('', self.stderr())
        self.assertEqual(u"""\
Created a new vip:
id="a9254bdb"
name="nameo"
status="ACTIVE"
tenant_id="33a40233"
""", self.stdout())

    @httpretty.activate
    def test_delete(self):
        pargs = common.FakeParsedArgs()
        pargs.id = 'nameo'
        httpretty.register_uri(httpretty.GET, self.LIST_URL,
                               body=self.LIST_ONE)
        httpretty.register_uri(httpretty.DELETE, self.DELETE_URL,
                               body=self.DELETE)
        self.when_run(vip.DeleteVip, pargs)
        self.assertEqual('', self.stderr())
        self.assertEqual(u'Deleted vip: nameo\n',
                         self.stdout())

    @httpretty.activate
    def test_list(self):
        pargs = common.FakeParsedArgs()
        pargs.page_size = None
        pargs.sort_key = []
        pargs.sort_dir = []
        pargs.formatter = 'csv'
        httpretty.register_uri(httpretty.GET, self.LIST_URL,
                               body=self.LIST)
        self.when_run(vip.ListVip, pargs)
        self.assertEqual('', self.stderr())
        self.assertEqual("""\
id,name,status
a9254bdb,nameo,ACTIVE
b8408dgd,croc,ACTIVE
""", self.stdout())

    @httpretty.activate
    def test_set(self):
        pargs = common.FakeParsedArgs()
        pargs.name = 'nameo'
        httpretty.register_uri(httpretty.GET, self.LIST_URL,
                               body=self.LIST_ONE)
        self.when_run(vip.SetVip, pargs)
        self.assertEqual('', self.stderr())
        self.assertEqual('', self.stdout())

    @httpretty.activate
    def test_show(self):
        pargs = common.FakeParsedArgs()
        pargs.id = 'nameo'
        httpretty.register_uri(httpretty.GET, self.LIST_URL,
                               body=self.LIST_ONE)
        httpretty.register_uri(httpretty.GET, self.SHOW_URL,
                               body=self.SHOW)
        self.when_run(vip.ShowVip, pargs)
        self.assertEqual('', self.stderr())
        self.assertEqual(u"""\
id="a9254bdb"
name="nameo"
status="ACTIVE"
tenant_id="33a40233"
""", self.stdout())
