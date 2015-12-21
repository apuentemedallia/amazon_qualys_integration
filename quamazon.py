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

# [ $# -eq 0 ] && echo  "Syntax: `basename $0` <arg>" && exit 0
import subprocess
import sys
import json

#arrAccts = [ "corp-it" , "admin" , "demoadmin" , "demostgadmin" ,"engineering" ]
arrAccts = [ "corp-it" ,
             "admin" , 
             "demoadmin" , 
             "demostgadmin" ,
             "engineering" ]

arrRegions = [ "us-east-1" , 
               "us-west-2" , 
               "us-west-1" , 
               "eu-west-1" , 
               "eu-central-1" , 
               "ap-southeast-1" , 
               "ap-southeast-2" , 
               "ap-northeast-1" , 
               "sa-east-1" ]

def getInstances ( strAccount , strRegion ):
  command = "aws ec2 --profile "+strAccount+" --region "+strRegion+" describe-instances"
  child = subprocess.Popen(command, shell=True, stderr=subprocess.PIPE)
  while True:
      out = child.stderr.read(1)
      if out == '' and child.poll() != None:
        break
      if out != '':
        return json
        sys.stdout.write(out)
        sys.stdout.flush()
  return json.loa

for strRegion in arrRegions:
  print ( "Region: %s" % strRegion )
  getInstances ( "corp-it" , strRegion )

