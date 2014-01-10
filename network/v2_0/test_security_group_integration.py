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

from openstackclient.network.v2_0 import security_group
from openstackclient.tests.network.v2_0 import common


class TestSecurityGroupIntegration(common.TestIntegrationBase):
    HOSTESS = common.TestIntegrationBase.HOST + common.TestIntegrationBase.VER
    CREATE_URL = HOSTESS + "/security-groups.json"
    CREATE = """
{
   "security_group":
   {
       "status": "ACTIVE",
       "name": "gator",
       "tenant_id": "33a40233",
       "id": "a9254bdb"
   }
}"""
    DELETE_URL = HOSTESS + "/security-groups/a9254bdb.json"
    DELETE = "{}"
    LIST_URL = HOSTESS + "/security-groups.json"
    LIST_ONE = '{ "security_groups": [{ "id": "a9254bdb" }] }'
    LIST = """
{
   "security_groups": [
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
    SHOW_URL = HOSTESS + "/security-groups/a9254bdb.json"
    SHOW = CREATE

    @httpretty.activate
    def test_create(self):
        pargs = common.FakeParsedArgs()
        pargs.name = 'gator'
        pargs.description = 'groupo'
        pargs.tenant_id = '33a40233'
        httpretty.register_uri(httpretty.GET, self.LIST_URL,
                               body=self.LIST_ONE)
        httpretty.register_uri(httpretty.POST, self.CREATE_URL,
                               body=self.CREATE)
        self.when_run(security_group.CreateSecurityGroup, pargs)
        self.assertEqual('', self.stderr())
        self.assertEqual(u"""\
Created a new security_group:
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
        self.when_run(security_group.DeleteSecurityGroup, pargs)
        self.assertEqual('', self.stderr())
        self.assertEqual(u'Deleted security_group: gator\n',
                         self.stdout())

    @httpretty.activate
    def test_list(self):
        pargs = common.FakeParsedArgs()
        pargs.formatter = 'csv'
        httpretty.register_uri(httpretty.GET, self.LIST_URL,
                               body=self.LIST)
        self.when_run(security_group.ListSecurityGroup, pargs)
        self.assertEqual('', self.stderr())
        self.assertEqual("""\
id,name
a9254bdb,gator
b8408dgd,croc
""", self.stdout())

    @httpretty.activate
    def test_set(self):
        pargs = common.FakeParsedArgs()
        pargs.name = 'gator'
        httpretty.register_uri(httpretty.GET, self.LIST_URL,
                               body=self.LIST_ONE)
        self.when_run(security_group.SetSecurityGroup, pargs)
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
        self.when_run(security_group.ShowSecurityGroup, pargs)
        self.assertEqual('', self.stderr())
        self.assertEqual(u"""\
id="a9254bdb"
name="gator"
status="ACTIVE"
tenant_id="33a40233"
""", self.stdout())
