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

from openstackclient.network.v2_0.lb import pool
from openstackclient.tests.oscaft import common


class TestPoolIntegration(common.TestIntegrationBase):
    HOSTESS = common.TestIntegrationBase.HOST + common.TestIntegrationBase.VER
    AGENTS_URL = HOSTESS + "/agents/foo/loadbalancer-pools.json"
    POOLS_URL = HOSTESS + "/lb/pools.json"
    POOLS = '{ "pools": [{ "id": "1111111" }] }'
    SUBNETS_URL = HOSTESS + "/subnets.json"
    SUBNETS = '{ "subnets": [{ "id": "222222" }] }'
    CREATE_URL = HOSTESS + "/lb/pools.json"
    CREATE = """
{
   "pool":
   {
       "status": "ACTIVE",
       "name": "nameo",
       "tenant_id": "33a40233",
       "id": "a9254bdb"
   }
}"""
    DELETE_URL = HOSTESS + "/lb/pools/a9254bdb.json"
    DELETE = "{}"
    LIST_URL = HOSTESS + "/lb/pools.json"
    LIST_ONE = '{ "pools": [{ "id": "a9254bdb" }] }'
    LIST = """
{
   "pools": [
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
    SET_URL = HOSTESS + "/lb/pools/a9254bdb.json"
    SET = "{}"
    SHOW_URL = HOSTESS + "/lb/pools/a9254bdb.json"
    SHOW_AGENT_URL = HOSTESS + "/lb/pools/a9254bdb/loadbalancer-agent.json"
    SHOW_AGENT = """
{
    "agent": {
        "admin_state_up": true,
        "agent_type": "Loadbalancer agent",
        "alive": true,
        "binary": "neutron-loadbalancer-agent",
        "configurations": {
            "device_driver": "neutron.services.HaproxyNSDriver",
            "devices": 0,
            "interface_driver": "neutron.agent.OVSInterfaceDriver"
        },
        "created_at": "2013-10-01 12:50:13",
        "description": null,
        "heartbeat_timestamp": "2013-10-01 12:56:29",
        "host": "ostack02",
        "id": "6ee1df7f-bae4-4ee9-910a-d33b000773b0",
        "started_at": "2013-10-01 12:50:13",
        "topic": "lbaas_process_on_host_agent"
    }
}"""
    SHOW = CREATE
    STATS_URL = HOSTESS + "/lb/pools/nameo/stats.json"
    STATS = """
{
    "stats" : {
                         "bytes_in" : 36839202,
                         "bytes_out" : 673193022,
                         "active_connections" : 39,
                         "total_connections" : 682
              }
}"""
    ADD_REMOVE_URL = HOSTESS + "/floatingips/127.0.0.1.json"
    ADD_REMOVE = "{}"

    @httpretty.activate
    def test_create(self):
        pargs = common.FakeParsedArgs()
        pargs.name = 'nameo'
        pargs.admin_state = True
        pargs.description = None
        pargs.lb_method = 'LEAST_CONNECTIONS'
        pargs.protocol = 'TCP'
        pargs.subnet_id = 'subby'
        pargs.provider = 'ryder'
        pargs.tenant_id = '33a40233'
        #httpretty.register_uri(httpretty.GET, self.POOLS_URL,
        #                       body=self.POOLS)
        httpretty.register_uri(httpretty.GET, self.SUBNETS_URL,
                               body=self.SUBNETS)
        httpretty.register_uri(httpretty.POST, self.CREATE_URL,
                               body=self.CREATE)
        self.when_run(pool.CreatePool, pargs)
        self.assertEqual('', self.stderr())
        self.assertEqual(u"""\
Created a new pool:
id="a9254bdb"
name="nameo"
status="ACTIVE"
tenant_id="33a40233"
""", self.stdout())

    @httpretty.activate
    def test_delete(self):
        pargs = common.FakeParsedArgs()
        pargs.identifier = 'nameo'
        httpretty.register_uri(httpretty.GET, self.LIST_URL,
                               body=self.LIST_ONE)
        httpretty.register_uri(httpretty.DELETE, self.DELETE_URL,
                               body=self.DELETE)
        self.when_run(pool.DeletePool, pargs)
        self.assertEqual('', self.stderr())
        self.assertEqual(u'Deleted pool: nameo\n',
                         self.stdout())

    @httpretty.activate
    def test_list(self):
        pargs = common.FakeParsedArgs()
        pargs.lbaas_agent = None
        pargs.page_size = None
        pargs.sort_key = []
        pargs.sort_dir = []
        pargs.formatter = 'csv'
        httpretty.register_uri(httpretty.GET, self.LIST_URL,
                               body=self.LIST)
        self.when_run(pool.ListPool, pargs)
        self.assertEqual('', self.stderr())
        self.assertEqual("""\
id,name,status
a9254bdb,nameo,ACTIVE
b8408dgd,croc,ACTIVE
""", self.stdout())

    @httpretty.activate
    def test_list_lbaas_agent(self):
        pargs = common.FakeParsedArgs()
        pargs.lbaas_agent = 'foo'
        pargs.page_size = None
        pargs.sort_key = []
        pargs.sort_dir = []
        pargs.formatter = 'csv'
        httpretty.register_uri(httpretty.GET, self.AGENTS_URL,
                               body=self.LIST)
        self.when_run(pool.ListPool, pargs)
        self.assertEqual('', self.stderr())
        self.assertEqual("""\
id,name,status
a9254bdb,nameo,ACTIVE
b8408dgd,croc,ACTIVE
""", self.stdout())

    @httpretty.activate
    def test_set(self):
        pargs = common.FakeParsedArgs()
        pargs.identifier = 'nameo'
        httpretty.register_uri(httpretty.GET, self.LIST_URL,
                               body=self.LIST_ONE)
        httpretty.register_uri(httpretty.PUT, self.SET_URL,
                               body=self.SET)
        self.when_run(pool.SetPool, pargs)
        self.assertEqual('', self.stderr())
        self.assertEqual('', self.stdout())

    @httpretty.activate
    def test_show(self):
        pargs = common.FakeParsedArgs()
        pargs.pool = 'nameo'
        pargs.agent = False
        pargs.stats = False
        httpretty.register_uri(httpretty.GET, self.LIST_URL,
                               body=self.LIST_ONE)
        httpretty.register_uri(httpretty.GET, self.SHOW_URL,
                               body=self.SHOW)
        self.when_run(pool.ShowPool, pargs)
        self.assertEqual('', self.stderr())
        self.assertEqual(u"""\
id="a9254bdb"
name="nameo"
status="ACTIVE"
tenant_id="33a40233"
""", self.stdout())

    @httpretty.activate
    def test_show_agent(self):
        pargs = common.FakeParsedArgs()
        pargs.pool = 'nameo'
        pargs.agent = True
        pargs.stats = False
        httpretty.register_uri(httpretty.GET, self.LIST_URL,
                               body=self.LIST_ONE)
        httpretty.register_uri(httpretty.GET, self.SHOW_AGENT_URL,
                               body=self.SHOW_AGENT)
        self.when_run(pool.ShowPool, pargs)
        self.assertEqual('', self.stderr())
        self.assertEqual(u"""\
id="(u'6ee1df7f-bae4-4ee9-910a-d33b000773b0', u'ostack02', True, ':-)')"
""", self.stdout())

    @httpretty.activate
    def test_show_stats(self):
        pargs = common.FakeParsedArgs()
        pargs.pool = 'nameo'
        pargs.agent = False
        pargs.stats = True
        httpretty.register_uri(httpretty.GET, self.STATS_URL,
                               body=self.STATS)
        self.when_run(pool.ShowPool, pargs)
        self.assertEqual('', self.stderr())
        self.assertEqual(u"""\
active_connections="39"
bytes_in="36839202"
bytes_out="673193022"
total_connections="682"
""", self.stdout())
