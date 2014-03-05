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
    CREATE_VOLUME_URL = HOSTESS + "/volumes"
    CREATE_IMAGE = """

{
   "os-volume_upload_image":
   {
       "status": "uploading",
       "name": "nameo",
       "tenant_id": "33a40233",
       "id": "a9254bdb",
       "image_id": "b2348002"
   }
}"""
    LIST_VOLUME_URL = HOSTESS + "/volumes"
    SHOW_VOLUME_URL = HOSTESS + "/volumes/detail"
    LIST_VOLUME = """{"volumes": [{"id": "a9254bdb", "name": "volly"}]}"""
    ACTION_VOLUME_URL = HOSTESS + "/volumes/a9254bdb/action"

    @httpretty.activate
    def test_create(self):
        pargs = common.FakeParsedArgs()
        pargs.name = 'nameo'
        pargs.volume = 'volly'
        pargs.force = False
        pargs.container_format = 'bare'
        pargs.disk_format = 'raw'
        httpretty.register_uri(httpretty.GET, self.SHOW_VOLUME_URL,
                               body=self.LIST_VOLUME)
        httpretty.register_uri(httpretty.POST, self.ACTION_VOLUME_URL,
                               body=self.CREATE_IMAGE)
        self.when_run(image.CreateImage, pargs)
        self.assertEqual('', self.stderr())
        self.assertEqual(u"""\
id="a9254bdb"
image_id="b2348002"
name="nameo"
status="uploading"
tenant_id="33a40233"
""", self.stdout())
