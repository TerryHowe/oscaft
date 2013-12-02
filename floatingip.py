import pexpect
import sys
import traceback

def main():
    rc = 1
    prompt = '\(openstack\) '
    child = pexpect.spawn('openstack')
    try:
        child.expect(prompt)
        child.sendline('network show Ext-Net -f shell -c id')
        child.expect('id="(.*)"')
        netid = child.match.group(1)
        child.expect(prompt)
        child.sendline('ip floating create ' + netid + ' -f shell -c id')
        child.expect('id="(.*)"')
        id = child.match.group(1)
        child.expect(prompt)
        child.sendline("ip floating show " + id + " -f shell -c id")
        child.expect('id="' + id + '"')
        child.expect(prompt)
        child.sendline("ip floating list -f csv -c id")
        child.expect("\"" + id + "\"")
        child.expect(prompt)
        child.sendline("ip floating delete " + id)
        child.expect('Deleted floatingip: ' + id)
        child.expect(prompt)
        print "SUCCESS"
        rc = 0
    except Exception:
        traceback.print_exc(file=sys.stdout)
        child.sendline("ip floating delete lucky")
        child.expect(prompt)
    sys.exit(rc)

if __name__ == "__main__":
    main()
