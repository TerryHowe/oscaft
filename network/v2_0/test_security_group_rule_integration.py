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

from openstackclient.network.v2_0 import security_group_rule
from openstackclient.tests.oscaft import common


class TestSecurityGroupRuleIntegration(common.TestIntegrationBase):
    HOSTESS = common.TestIntegrationBase.HOST + common.TestIntegrationBase.VER
    SECURITY_GROUP_URL = HOSTESS + "/security-groups.json"
    SECURITY_GROUP = '{ "security_groups": [{ "id": "9393939" }] }'
    CREATE_URL = HOSTESS + "/security-group-rules.json"
    CREATE = """
{
   "security_group_rule":
   {
       "status": "ACTIVE",
       "direction": "ingress",
       "tenant_id": "33a40233",
       "id": "a9254bdb"
   }
}"""
    DELETE_URL = HOSTESS + "/security-group-rules/a9254bdb.json"
    DELETE = "{}"
    LIST_URL = HOSTESS + "/security-group-rules.json"
    LIST_ONE = '{ "security_group_rules": [{ "id": "a9254bdb" }] }'
    LIST = """
{
   "security_group_rules": [
       {
          "id": "a9254bdb",
          "security_group_id": "44444444",
          "direction": "egress",
          "protocol": "TCP",
          "remote_ip_prefix": "127.0.0.0/24",
          "remote_group_id": "2222222",
          "tenant_id": "33a40233"
       },
       {
          "id": "a9254bdb",
          "security_group_id": "55555555",
          "direction": "ingress",
          "protocol": "UDP",
          "remote_ip_prefix": "10.0.0.0/24",
          "remote_group_id": "",
          "tenant_id": "33a40233"
       }
   ]
}"""
    SHOW_URL = HOSTESS + "/security-group-rules/a9254bdb.json"
    SHOW = CREATE

    @httpretty.activate
    def test_create(self):
        pargs = common.FakeParsedArgs()
        pargs.security_group_id = 'sg1'
        pargs.direction = 'ingress'
        pargs.ethertype = 'IPv4'
        pargs.protocol = 'TCP'
        pargs.port_range_min = '0'
        pargs.port_range_max = '1000'
        pargs.remote_ip_prefix = '20.1.2.1/24'
        pargs.remote_group_id = None
        pargs.tenant_id = '33a40233'
        httpretty.register_uri(httpretty.GET, self.SECURITY_GROUP_URL,
                               body=self.SECURITY_GROUP)
        httpretty.register_uri(httpretty.POST, self.CREATE_URL,
                               body=self.CREATE)
        self.when_run(security_group_rule.CreateSecurityGroupRule, pargs)
        self.assertEqual('', self.stderr())
        self.assertEqual(u"""\
Created a new security_group_rule:
direction="ingress"
id="a9254bdb"
status="ACTIVE"
tenant_id="33a40233"
""", self.stdout())

    @httpretty.activate
    def test_delete(self):
        pargs = common.FakeParsedArgs()
        pargs.identifier = 'a9254bdb'
        httpretty.register_uri(httpretty.GET, self.LIST_URL,
                               body=self.LIST_ONE)
        httpretty.register_uri(httpretty.DELETE, self.DELETE_URL,
                               body=self.DELETE)
        self.when_run(security_group_rule.DeleteSecurityGroupRule, pargs)
        self.assertEqual('', self.stderr())
        self.assertEqual(u'Deleted security_group_rule: a9254bdb\n',
                         self.stdout())

    @httpretty.activate
    def test_list(self):
        pargs = common.FakeParsedArgs()
        pargs.formatter = 'csv'
        pargs.no_nameconv = True
        httpretty.register_uri(httpretty.GET, self.LIST_URL,
                               body=self.LIST)
        self.when_run(security_group_rule.ListSecurityGroupRule, pargs)
        self.assertEqual('', self.stderr())
        self.assertEqual("""\
id,security_group_id,direction,protocol,remote_ip_prefix,remote_group_id
a9254bdb,44444444,egress,TCP,127.0.0.0/24,2222222
a9254bdb,55555555,ingress,UDP,10.0.0.0/24,
""", self.stdout())

    @httpretty.activate
    def test_show(self):
        pargs = common.FakeParsedArgs()
        pargs.identifier = 'a9254bdb'
        httpretty.register_uri(httpretty.GET, self.SHOW_URL,
                               body=self.SHOW)
        self.when_run(security_group_rule.ShowSecurityGroupRule, pargs)
        self.assertEqual('', self.stderr())
        self.assertEqual(u"""\
direction="ingress"
id="a9254bdb"
status="ACTIVE"
tenant_id="33a40233"
""", self.stdout())
