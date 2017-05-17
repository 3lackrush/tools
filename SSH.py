#!/usr/bin/env python
# -*- coding: utf-8 -*-

import pexpect
import argparse
import sys

def ssh_cmd(args):
    ret = -1
    ssh = pexpect.spawn('ssh root@%s "%s"' % (args.ip, args.cmd))
    try:
        i = ssh.expect(['password:', 'continue connecting (yes/no)?'], timeout=5)
        if i == 0 :
            ssh.sendline(args.passwd)
        elif i == 1:
            ssh.sendline('yes\n')
            ssh.expect('password: ')
            ssh.sendline(args.passwd)
        ssh.sendline(args.cmd)
        r = ssh.read()
        print r
        ret = 0
    except pexpect.EOF:
        print "EOF"
        ssh.close()
        ret = -1
    except pexpect.TIMEOUT:
        print "TIMEOUT"
        ssh.close()
        ret = -2
    return ret


#ssh_cmd("172.16.86.137","1", "whoami")

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('-i','--ip', dest='ip', default=None)
    parser.add_argument('-p','--passwd', dest='passwd', default=None)
    parser.add_argument('-c','--cmd', dest='cmd', default='whoami')
    args = parser.parse_args()
    
    if len(sys.argv) == 1:
        parser.print_help()
        sys.exit(-1)
    ssh_cmd(args)
