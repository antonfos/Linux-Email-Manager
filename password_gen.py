#!/usr/bin/env python2.7

from appsrc.mailpwd import pwdutil
import getpass

print ""
print "=============================================================="
print "Enter your password"
p = getpass.getpass()

pr = p
#print "Repeat the Password"
#pr = getpass.getpass()

if  p == pr:
    pwdset = pwdutil()
    pwd = pwdset.genSHA512(p)
    print ""
    print "=============================================================="
    print "                   Password Generated      "
    print "=============================================================="
    print "Copy this password into your config.py file ADMIN_PASSWORD to"
    print "                set the admin password"
    print "--------------------------------------------------------------"
    print ""
    print "ADMIN_PASSWORD = %s" % pwd
    print ""
    print "=============================================================="
else:
    print "Error Passwords did not match"

