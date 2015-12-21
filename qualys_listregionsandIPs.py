#!/usr/bin/python
__author__ = 'Adrian Puente Z. <apuente@medallia.com>'
__company__ = 'Medallia Inc.'

import subprocess
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
    qgc = qualysapi.connect()
 
    arrHostGroups = getQualysHostGroups( qgc )
    printSuccess ("Found %i AWS groups: \n%s" % ( len(arrHostGroups) , "\n[+] ".join(arrHostGroups) ))
    for HostGroup in arrHostGroups:
        printSuccess ( ", ".join( getQualysIPs( qgc , HostGroup )))

if __name__ == "__main__": main()
