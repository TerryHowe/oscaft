import pexpect
import sys
import traceback

def main():
    rc = 1
    prompt = '\(openstack\) '
    child = pexpect.spawn('openstack')
    try:
        child.expect(prompt)
        child.sendline("network delete lucky")
        child.expect(prompt)
        child.sendline('network create lucky -f shell -c id')
        child.expect('id="(.*)"')
        id = child.match.group(1)
        child.expect(prompt)
        child.sendline("network show " + id + " -f shell -c name")
        child.expect('name="lucky"')
        child.expect(prompt)
        child.sendline("network list -f csv -c id -c name")
        child.expect("\"" + id + "\",\"lucky\"")
        child.expect(prompt)
        child.sendline("network set " + id + " -f shell -c name")
        child.expect('Must specify new values to update network')
        child.expect(prompt)
        child.sendline("network delete lucky")
        child.expect('Deleted network: lucky')
        child.expect(prompt)
        rc = 0
    except Exception:
        traceback.print_exc(file=sys.stdout)
        child.sendline("network delete lucky")
        child.expect(prompt)
    sys.exit(rc)

if __name__ == "__main__":
    main()
