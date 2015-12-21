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
__author__ = 'Adrian Puente Z. <apuente@medallia.com>'
__company__ = 'Medallia Inc.'

import subprocess
import boto3
import qualysapi
import sys
import json
from array import array
from lxml import objectify
from lxml.builder import E

def printMessage ( strMsg ):
    print ( "[*] %s" % strMsg )

def printSuccess ( strMsg ):
    print ( "[+] %s" % strMsg )

def printError ( strMsg ):
    print ( "[!] %s" % strMsg )

def errorQuit ( strMsg ):
    printError( strMsg+"Quitting gracefully." )
    return False

def errorSuccess ( strMsg ):
    printMessage( strMsg+"Quitting gracefully" )

def getAWSInstances ( strProfile , strRegion ):
#
# ---Get Amazon Instances---
#
# Logs into an Amazon profile using aws cli and request all the instances in that account
#
    printMessage( "Querying Amazon profile: "+strProfile+" region: "+strRegion+"." )
    command = "aws ec2 --profile "+strProfile+" --region "+strRegion+" describe-instances"
    proc = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE)
    output = proc.communicate()[0]
    jsonAWSQuery = json.loads( output.decode('utf-8') )
    printSuccess("Got "+str(len(jsonAWSQuery))+" AWS instances.")
    return jsonAWSQuery

def getAWSPublicIps ( strProfile , strRegion ):
#
# ---Get Amazon Instances---
#
# Logs into an Amazon profile using aws cli and request all the instances in that account
#
    lstIpAddress = list()
    session = boto3.session.Session( profile_name=strProfile, region_name=strRegion )
    ec2 = session.client('ec2')
    printMessage( "Querying Amazon profile: "+strProfile+" region: "+strRegion+"." )
    addresses_dict = ec2.describe_addresses()
    for eip_dict in addresses_dict['Addresses']:
        lstIpAddress.append( eip_dict['PublicIp'] )
    return lstIpAddress


def getQualysHostGroups ( qConnector ):
#
# ---Get Qualys Host Groups---
#
# Logs into an Qualys and brings the he inventory of Host Groups
#
    arrHostGroups = list()
    xml_output = qConnector.request( 'asset_group_list.php?', '' )
    root = objectify.fromstring(xml_output)
    printMessage("Requesting hosts groups to Qualys.")
    for AssetGroup in root.ASSET_GROUP:
        if 'Amazon AWS' in AssetGroup.TITLE.text:
            if 'Amazon AWS - All Hosts' not in AssetGroup.TITLE.text:
                arrHostGroups.append(AssetGroup.TITLE.text)
    printSuccess("Got "+str(len(arrHostGroups))+" AWS group hosts")
    return arrHostGroups

def getQualysIPs ( qConnector , strHostGroup ):
#
# ---Get Qualys IPs---
#
# Logs into an Qualys and brings the AWS IP inventory for comparison
#
    arrIPs = list()
    parameters = 'title='+strHostGroup
    printMessage("Requesting hosts groups to Qualys from host group: %s." %strHostGroup )
    xml_output = qConnector.request('asset_group_list.php?', parameters)
    root = objectify.fromstring(xml_output)
    for IPAddr in root.ASSET_GROUP.SCANIPS.IP:
        arrIPs.append(IPAddr.text)
    printSuccess("Got "+str(len(arrIPs))+" IPs in host group "+strHostGroup)
    return arrIPs


def main():
    ec2 = boto3.resource('ec2')
    arrProfile = [ "corp-it" ,
                 "admin" ,
                 "demoadmin" ,
                 "demostgadmin" ,
                 "engineering" ]

    dicRegions = { "us-east-1" : "US East (N. Virginia)" ,
                   "us-west-2" : "US West (Oregon)" ,
                   "us-west-1" : "US West (N. California)" ,
                   "eu-west-1" : "EU (Ireland)" ,
                   "eu-central-1" : "EU (Frankfurt)" ,
                   "ap-southeast-1" : "Asia Pacific (Singapore)" ,
                   "ap-southeast-2" : "Asia Pacific (Sydney)",
                   "ap-northeast-1" : "Asia Pacific (Tokyo)" ,
                   "sa-east-1" :  "South America (Sao Paulo)" }

    #qgc = qualysapi.connect()



    #ec2 = boto3.resource('ec2')


    for strProfile in arrProfile:
        for strRegion in dicRegions.keys():
            lstAmazon = getAWSPublicIps ( strProfile , strRegion )
            if len(lstAmazon) is 0:
                printError("No instances with public IPs found")
            else:
                printMessage ( "Found %i public Ips found: %s" % ( len(lstAmazon) , ', '.join(lstAmazon) ))

    #for HostGroup in getQualysHostGroups( qgc ):
     #   print (getQualysIPs( qgc , HostGroup ))

    #getQualysIPs( qgc )



if __name__ == "__main__": main()