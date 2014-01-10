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

from openstackclient.network.v2_0.vpn import ikepolicy
from openstackclient.tests.network.v2_0 import common


class TestIkepolicyIntegration(common.TestIntegrationBase):
    HOSTESS = common.TestIntegrationBase.HOST + common.TestIntegrationBase.VER
    CREATE_URL = HOSTESS + "/vpn/ikepolicies.json"
    CREATE = """
{
   "ikepolicy":
   {
       "status": "ACTIVE",
       "name": "gator",
       "tenant_id": "33a40233",
       "id": "a9254bdb"
   }
}"""
    DELETE_URL = HOSTESS + "/vpn/ikepolicies/a9254bdb.json"
    DELETE = "{}"
    LIST_URL = HOSTESS + "/vpn/ikepolicies.json"
    LIST_ONE = """
{
   "ikepolicies": [{
       "id": "a9254bdb"
   }]
}"""
    LIST = """
{
   "ikepolicies": [
       {
          "name": "gator",
          "tenant_id": "33a40233",
          "auth_algorithm": "sha1",
          "encryption_algorithm": "aes-128",
          "ike_version": "v1",
          "pfs": "group5",
          "tenant_id": "33a40233",
          "id": "a9254bdb"
       },
       {
          "name": "croc",
          "auth_algorithm": "sha1",
          "encryption_algorithm": "aes-128",
          "ike_version": "v2",
          "pfs": "group5",
          "tenant_id": "33a40233",
          "id": "b8408dgd"
       }
   ]
}"""
    SHOW_URL = HOSTESS + "/vpn/ikepolicies/a9254bdb.json"
    SHOW = CREATE

    @httpretty.activate
    def test_create(self):
        pargs = common.FakeParsedArgs()
        pargs.name = 'gator'
        pargs.description = 'gatorific'
        pargs.auth_algorithm = 'sha1'
        pargs.encryption_algorithm = 'aes-128'
        pargs.phase1_negotiation_mode = 'main'
        pargs.ike_version = 'v2'
        pargs.pfs = 'group5'
        pargs.lifetime = {'units': 'seconds', 'value': '200'}
        pargs.tenant_id = '999999'
        httpretty.register_uri(httpretty.POST, self.CREATE_URL,
                               body=self.CREATE)
        self.when_run(ikepolicy.CreateIkepolicy, pargs)
        self.assertEqual('', self.stderr())
        self.assertEqual(u"""\
Created a new ikepolicy:
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
        self.when_run(ikepolicy.DeleteIkepolicy, pargs)
        self.assertEqual('', self.stderr())
        self.assertEqual(u'Deleted ikepolicy: gator\n',
                         self.stdout())

    @httpretty.activate
    def test_list(self):
        pargs = common.FakeParsedArgs()
        pargs.formatter = 'csv'
        httpretty.register_uri(httpretty.GET, self.LIST_URL,
                               body=self.LIST)
        self.when_run(ikepolicy.ListIkepolicy, pargs)
        self.assertEqual('', self.stderr())
        self.assertEqual("""\
id,name,auth_algorithm,encryption_algorithm,ike_version,pfs
a9254bdb,gator,sha1,aes-128,v1,group5
b8408dgd,croc,sha1,aes-128,v2,group5
""", self.stdout())

    @httpretty.activate
    def test_set(self):
        pargs = common.FakeParsedArgs()
        pargs.name = 'gator'
        httpretty.register_uri(httpretty.GET, self.LIST_URL,
                               body=self.LIST_ONE)
        self.when_run(ikepolicy.SetIkepolicy, pargs)
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
        self.when_run(ikepolicy.ShowIkepolicy, pargs)
        self.assertEqual('', self.stderr())
        self.assertEqual(u"""\
id="a9254bdb"
name="gator"
status="ACTIVE"
tenant_id="33a40233"
""", self.stdout())
