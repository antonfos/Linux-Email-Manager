#!/usr/bin/python

import os
#s.environ['PYTHON_EGG_CACHE'] = '/idev/apache/www/.python-eggs'

import sys
import logging

logging.basicConfig(stream=sys.stderr)
sys.path.insert(0,"/opt/mail/Linux-Email-Manager/")

from appsrc import app as application
