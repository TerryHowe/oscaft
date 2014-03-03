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

from openstackclient.image.v1 import image
from openstackclient.tests.oscaft import common


class TestImageIntegration(common.TestIntegrationBase):
    HOSTESS = common.TestIntegrationBase.HOST + '/v1'
    CREATE_URL = HOSTESS + "/image"
    CREATE = """
{
   "image":
   {
       "status": "ACTIVE",
       "name": "nameo",
       "tenant_id": "33a40233",
       "id": "a9254bdb"
   }
}"""
    SHOW_URL = HOSTESS + "/images/detail"
    LIST_URL = HOSTESS + "/images"
    LIST_ONE = """ { "images": [{ "id": "a9254bdb" }] }"""
    LIST_TWO = """ { "images": [] }"""
    LIST = """
{
   "images": [
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

    @httpretty.activate
    def test_create(self):
        pargs = common.FakeParsedArgs()
        pargs.name = 'nameo'
        pargs.admin_state = True
        pargs.shared = True
        pargs.tenant_id = '33a40233'
        #httpretty.register_uri(httpretty.GET, self.LIST_URL,
        #                       body="asdfasdfasdf", content_type="application/json")
        httpretty.register_uri(httpretty.GET, unicode(self.SHOW_URL),
                               responses=[
                                    httpretty.Response("first response", status=201),
                                    httpretty.Response(self.LIST, status=202),
                                    httpretty.Response(self.LIST_TWO)], Streaming=True)
        httpretty.register_uri(httpretty.POST, self.CREATE_URL,
                               body=self.CREATE, content_type="text/json")
        print '~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~'
        print self.LIST_URL
        print self.SHOW_URL
        print self.CREATE_URL
        print '~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~'
        self.when_run(image.CreateImage, pargs)
        self.assertEqual('', self.stderr())
        self.assertEqual(u"""\
Created a new image:
id="a9254bdb"
name="nameo"
status="ACTIVE"
tenant_id="33a40233"
""", self.stdout())
