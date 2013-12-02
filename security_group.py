import pexpect
import sys
import traceback

def main():
    rc = 1
    prompt = '\(openstack\) '
    child = pexpect.spawn('openstack')
    try:
        child.expect(prompt)
        child.sendline("security group delete lucky")
        child.expect(prompt)
        child.sendline('security group create lucky --description oscaft -f shell -c id')
        child.expect('id="(.*)"')
        id = child.match.group(1)
        child.expect(prompt)
        child.sendline("security group show " + id + " -f shell -c name")
        child.expect('name="lucky"')
        child.expect(prompt)
        child.sendline("security group list -f csv -c id -c name")
        child.expect("\"" + id + "\",\"lucky\"")
        child.expect(prompt)
        child.sendline("security group set --description OSCAFT --name lucky " + id)
        child.expect('Updated security_group: ' + id)
        child.expect(prompt)
        child.sendline("security group delete lucky")
        child.expect('Deleted security_group: lucky')
        child.expect(prompt)
        print "SUCCESS"
        rc = 0
    except Exception:
        traceback.print_exc(file=sys.stdout)
        child.sendline("security group delete lucky")
        child.expect(prompt)
    sys.exit(rc)

if __name__ == "__main__":
    main()
