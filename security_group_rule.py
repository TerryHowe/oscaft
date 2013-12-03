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

import pexpect
import sys
import traceback


def main():
    rc = 1
    prompt = '\(openstack\) '
    child = pexpect.spawn('openstack')
    try:
        child.expect(prompt)
        child.sendline("security group delete oscaft")
        child.expect(prompt)
        child.sendline("security group create oscaft -f shell -c id")
        child.expect('id="(.*)"')
        sgid = child.match.group(1)
        child.expect(prompt)
        child.sendline('security group rule create oscaft -f shell -c id')
        child.expect('id="(.*)"')
        id = child.match.group(1)
        child.expect(prompt)
        child.sendline("security group rule show " + id + " -f shell -c"
                       " security_group_id")
        child.expect('security_group_id="' + sgid + '"')
        child.expect(prompt)
        child.sendline("security group rule list -f csv -c id -c"
                       " security_group")
        child.expect("\"" + id + "\",\"oscaft\"")
        child.expect(prompt)
        child.sendline("security group rule delete " + id)
        child.expect('Deleted security_group_rule: ' + id)
        child.expect(prompt)
        print("SUCCESS")
        rc = 0
    except Exception:
        traceback.print_exc(file=sys.stdout)
    sys.exit(rc)

if __name__ == "__main__":
    main()
