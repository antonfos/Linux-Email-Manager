#!/usr/bin/env python2.7

from appsrc.mailpwd import pwdutil
import getpass
import re

minlength = 6
strength = 3

def Generate():
    print ""
    print "=============================================================="
    print "Enter your password"
    p = getpass.getpass()

    pr = p
    #print "Repeat the Password"
    #pr = getpass.getpass()
    if not CheckPasswordLength(p) :
        print ""
        print "!!! Error Password too short min length %d" % minlength
        print ""

    score = CheckPasswordStrength(p)
    if score < strength:
        print ""
        print "!!! Error Password too weak, Password score = %d you need a minimum of %d" % (score, strength)
        print ""

    if  p == pr:
        
        print ""
        print "=============================================================="
        print "                   Password Generator      "
        print "=============================================================="
        print "Copy this password into your config.py file ADMIN_PASSWORD to"
        print "                set the admin password"
        print "          Statistics Length = %d score = %d " % ( len(p), score )
        print "--------------------------------------------------------------"
        print ""
        if score >= strength and CheckPasswordLength(p):
            pwdset = pwdutil()
            pwd = pwdset.genSHA512(p)
            print "ADMIN_PASSWORD = %s" % pwd
        else:
            print "Unable to generate password due to length or score errors"
        print ""
        print "=============================================================="
    else:
        print "Error Passwords did not match"

def CheckPasswordLength(pw):
    if len(pw) >= minlength:
        return  True
    else:
        return False

def CheckPasswordStrength(pw):
    score = 0
    plen = len(pw)
    if plen >= minlength and plen <= minlength + 2:
        score = 1
    elif plen > minlength +2 and plen <= minlength + 4:
        score = 2
    elif plen > minlength + 4:
        score = 3

    rpat = re.compile('[)(@]')

    if rpat.search(pw) is not None:
         score += 1

    if re.search('[0-9]', pw) is not None:
         score += 1

    if re.search('[A-Z]', pw) is not None:
         score += 1

    if re.search('[a-z]', pw) is not None:
         score += 1

    return score



Generate()    

