#!/usr/bin/python
# Script by Adrian Puente Z..
# Powered by Hackarandas www.hackarandas.com
# Licensed by GNU GPLv3
# http://www.gnu.org/licenses/gpl-3.0.txt 
#
# Description:
# This script will quary Amazon to retrieve all the Amazon servers
# in our accounts
#
# Keywords: 
# Amazon, aws, awscli
#
# [ `id -u` -ne 0 ] && echo "Only root can do that! sudoing..." 
# if [ "$EUID" != 0 ]; then sudo `which $0` $@; exit; fi
#
#
import pycurl
from StringIO import StringIO

buffer = StringIO()
c = pycurl.Curl()
c.setopt(c.URL, 'http://pycurl.sourceforge.net/')
c.setopt(c.WRITEDATA, buffer)
c.perform()
c.close()

body = buffer.getvalue()
# Body is a string in some encoding.
# # In Python 2, we can print it without knowing what the encoding is.
# print(body)
