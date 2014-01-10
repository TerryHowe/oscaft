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

from openstackclient.network.v2_0.lb import healthmonitor
from openstackclient.tests.network.v2_0 import common


class TestHealthMonitorIntegration(common.TestIntegrationBase):
    HOSTESS = common.TestIntegrationBase.HOST + common.TestIntegrationBase.VER
    POOLS_URL = HOSTESS + "/lb/pools.json"
    POOLS = '{ "pools": [{ "id": "1111111" }] }'
    ADD_URL = HOSTESS + "/lb/pools/1111111/health_monitors.json"
    ADD = '{}'
    REMOVE_URL = HOSTESS + "/lb/pools/1111111/health_monitors/healthy.json"
    REMOVE = '{}'
    CREATE_URL = HOSTESS + "/lb/health_monitors.json"
    CREATE = """
{
   "health_monitor":
   {
       "status": "ACTIVE",
       "name": "nameo",
       "tenant_id": "33a40233",
       "id": "a9254bdb"
   }
}"""
    DELETE_URL = HOSTESS + "/lb/health_monitors/a9254bdb.json"
    DELETE = "{}"
    LIST_URL = HOSTESS + "/lb/health_monitors.json"
    LIST_ONE = '{ "health_monitors": [{ "id": "a9254bdb" }] }'
    LIST = """
{
   "health_monitors": [
       {
          "admin_state_up": "True",
          "type": "PING",
          "tenant_id": "33a40233",
          "id": "a9254bdb"
       },
       {
          "admin_state_up": "False",
          "type": "HTTP",
          "tenant_id": "33a40233",
          "id": "b8408dgd"
       }
   ]
}"""
    SHOW_URL = HOSTESS + "/lb/health_monitors/a9254bdb.json"
    SHOW = CREATE

    @httpretty.activate
    def test_create(self):
        pargs = common.FakeParsedArgs()
        pargs.admin_state = True
        pargs.expected_codes = None
        pargs.http_method = None
        pargs.url_path = None
        pargs.delay = '30'
        pargs.max_retries = '10'
        pargs.timeout = '80'
        pargs.type = 'PING'
        pargs.tenant_id = '33a40233'
        httpretty.register_uri(httpretty.POST, self.CREATE_URL,
                               body=self.CREATE)
        self.when_run(healthmonitor.CreateHealthMonitor, pargs)
        self.assertEqual('', self.stderr())
        self.assertEqual(u"""\
Created a new health_monitor:
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
        self.when_run(healthmonitor.DeleteHealthMonitor, pargs)
        self.assertEqual('', self.stderr())
        self.assertEqual(u'Deleted health_monitor: nameo\n',
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
        self.when_run(healthmonitor.ListHealthMonitor, pargs)
        self.assertEqual('', self.stderr())
        self.assertEqual("""\
id,type,admin_state_up
a9254bdb,PING,True
b8408dgd,HTTP,False
""", self.stdout())

    @httpretty.activate
    def test_set(self):
        pargs = common.FakeParsedArgs()
        pargs.id = 'nameo'
        httpretty.register_uri(httpretty.GET, self.LIST_URL,
                               body=self.LIST_ONE)
        self.when_run(healthmonitor.SetHealthMonitor, pargs)
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
        self.when_run(healthmonitor.ShowHealthMonitor, pargs)
        self.assertEqual('', self.stderr())
        self.assertEqual(u"""\
id="a9254bdb"
name="nameo"
status="ACTIVE"
tenant_id="33a40233"
""", self.stdout())

    @httpretty.activate
    def test_add_pool(self):
        pargs = common.FakeParsedArgs()
        pargs.pool_id = 'pooly'
        pargs.health_monitor_id = 'healthy'
        httpretty.register_uri(httpretty.GET, self.POOLS_URL,
                               body=self.POOLS)
        httpretty.register_uri(httpretty.POST, self.ADD_URL,
                               body=self.ADD)
        self.when_run(healthmonitor.AddPool, pargs)
        self.assertEqual('', self.stderr())
        self.assertEqual(u"Associated health monitor healthy\n",
                         self.stdout())

    @httpretty.activate
    def test_remove_pool(self):
        pargs = common.FakeParsedArgs()
        pargs.pool_id = 'pooly'
        pargs.health_monitor_id = 'healthy'
        httpretty.register_uri(httpretty.GET, self.POOLS_URL,
                               body=self.POOLS)
        httpretty.register_uri(httpretty.DELETE, self.REMOVE_URL,
                               body=self.REMOVE)
        self.when_run(healthmonitor.RemovePool, pargs)
        self.assertEqual('', self.stderr())
        self.assertEqual(u"Disassociated health monitor healthy\n",
                         self.stdout())
