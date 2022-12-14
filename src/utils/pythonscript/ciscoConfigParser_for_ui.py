# -*- coding: utf-8 -*-
"""
Created on June 22 2021
@author: venaddep
"""
import csv, re, os
from ciscoconfparse import *
from random import sample
from sqlalchemy import create_engine, types
import pandas as pd
import lib
import pdb
import urllib.parse
import sys
import os.path

# m_user='root'
# m_password=''
# m_host='127.0.0.1'

# engine = create_engine('mysql://{0}:{1}@{2}/custconfigDB'.format(m_user,m_password,m_host))
# print(engine)

m_user= sys.argv[1]
m_password= urllib.parse.quote_plus(sys.argv[2])
m_host= sys.argv[3]
m_db_name = sys.argv[4]
tempfile = "./src/utils/temp/temp.csv"
print("password", m_password)
engine = create_engine('mysql://{0}:{1}@{2}/{3}'.format(m_user,m_password,m_host,m_db_name))
print('mysql://{0}:{1}@{2}/{3}'.format(m_user,m_password,m_host,m_db_name))

def myShuffle(x, *s):
    x[slice(*s)] = sample(x[slice(*s)], len(x[slice(*s)]))

dirname  = './src/utils/cfgFiles/'

###
def copyRunning(src):
    #print("copyRunning",dst)
    dst=src+".runn"
    dst_dup=dst+".dup"
    startPattern1 = ".*show running-config"
    startPattern = ".*Building configuration"
    startPattern2= ".*Last configuration change.*"
    endPattern = "^end"
    endPattern1 = "^: end"
    endPattern2 = ".*#end"
    endPattern3 = ".*].*end"
    endPattern4 = ".*:.*:.*end"
    count = 0
    print("copyRunning",dst)
    print("copyRunning",dst_dup)
    with open(src) as infile, open(dst,'w+') as outfile, open(dst_dup, 'w+') as dupFile:
        copy = False
        #line = line.strip()
        for line in infile:
            #print(line)
            if re.match(startPattern, line) or re.match(startPattern1, line) or re.match(startPattern2,line):
                print("start pattern")
                copy = True
            if copy:
                #print(count)
                #print(line)
                count = count + 1
                outfile.write(line)
                dupFile.write(line)
            if re.match(endPattern, line) or re.match(endPattern1, line) or re.match(endPattern2, line) or re.match(endPattern3, line) or re.match(endPattern4, line):
                print("end pattern")
                copy = False
    print("end copyRunning")
    return(count)

def removeLine(file,pattern):
    file = file + ".runn"
    file = file + ".dup"
    replacement = ""
    count = 0
    pattern1 = ".*"+pattern+".*"
    patternCert= ".*[0-9]+.* .*[0-9]+.* .*[0-9]+.*"

    with open(file,"r") as input:
        for line in input:
            # print(line)
            #line = line.strip()
            if (re.match(pattern, line) or re.match(pattern1, line) or re.match(patternCert, line)):
                #print(pattern)
                #print(line)
                if(re.match("^interface", line) or re.match("^router", line) or re.match("^vrf", line) or \
                        re.match("^archive", line) or re.match("^radius", line) or re.match("^monitor",line) or \
                        re.match("^!radius", line) or re.match("^!!radius", line)):
                    changes = "!"+line
                    #print(line)
                    #print(changes)
                    #pdb.set_trace()
                else:
                    changes = ""
                    #print("else 1")

                replacement = replacement + changes
                count = count + 1
                #print(replacement)
            else:
                replacement = replacement + line
                #print("else 2")
    #print(replacement)
    fout = open(file, "w")
    fout.write(replacement)
    fout.close()
    #print("removeLine: matching lines",count)


def percentMiss(file,orig):
    file = file + ".runn" + ".dup"
    uniqFile= file + ".uniq"
    # os.system('sort -u "%s" > "%s"' %(file,uniqFile))
    os.system('cat "%s" > "%s"' %(file,uniqFile))
    with open(uniqFile,"r") as input:
        count = 0
        for line in input:
            if re.match(".*!.*[a-zA-Z0-9]+",line):
                pass
                #count = count + 1
            else:
                count = count + 1
    if count == 0:
        return 0
    print("not matching lines",count)
    per= float(count) / float(orig) * 100
    print("percentage not matching:",per)
    os.system('sed -i \'/^\!$/d\' "%s"' %(uniqFile))
    os.system('sed -i \'/^crypto pki certificate.*/d\' "%s"' %(uniqFile))
    os.system('sed -i \'/^ certificate .*/d\' "%s"' %(uniqFile))
    os.system('sed -i \'/^.*quit.*/d\' "%s"' %(uniqFile))
    os.system('sed -i \'/.*\([0-9A-F]\{8\}\).*/d\' "%s"' %(uniqFile))
    #os.system('sed -i \'/^[0-9A-F]*.*/d\' "%s"' %(uniqFile))
    return(per)

def max(retailwt,govtwt,healthwt,ngewt,educationwt,financewt,pewt,ngevpnwt,sdawt):
    maxwt = retailwt
    profileType = 1
    if govtwt >= maxwt:
        maxwt = govtwt
        profileType = 2
    if healthwt >= maxwt:
        maxwt = healthwt
        profileType = 3
    if ngewt >= maxwt:
        maxwt = govtwt
        profileType = 4
    if educationwt >= maxwt:
        maxwt = educationwt
        profileType = 5
    if financewt >= maxwt:
        maxwt = financewt
        profileType = 6
    if pewt >= maxwt:
        maxwt = pewt
        profileType = 7
    if ngevpnwt >= maxwt:
        maxwt = ngevpnwt
        profileType = 8
    if sdawt >= maxwt:
        maxwt = sdawt
        profileType = 9
    return(profileType)

def updateWt(df,wt,i):
    print("in updateWT")
    retail=['sda_ipv4Overlay','evpn_evpnEnable','sec_SXP','prog_mdns','l3v4_bgp','mcast_mcast','mcast_mcastv6','mcast_pim','mpls_6pe','policy_WRED']
    govt=['policy_WRED','mpls_mvpn','mpls_6pe','service_span','service_rspan','service_erspan','service_http','service_https','l3_hsrp']
    health=['mcast_pim','mcast_mld','l3v4_tunnel','l3v4_l3dot1q','l3v4_svi','l3v4_ospfv4','service_rspan','service_erspan']
    nge=['l3v6_ospfv6','l3v6_ipv6acl','l3v6_eigrpv6','l3v6_bfdv6','l3v4_tunnel','mcast_mcastv6','mcast_pimv6','policy_Inv6Acl']
    education=['sec_dot1x','sec_mab','sec_radiusv4','sec_webauth','sec_ctsSAP','policy_qos','policy_autoQos','policy_WRED','mpls_mvpn','mpls_6pe']
    finance=['sec_ctsSAP','sec_dot1x','sec_mab','mcast_igmp','prog_netconf']
    pe=['mpls_ldp','mpls_mplsTE','mpls_vpnv4','mpls_vpnv6','mpls_l2vpn','mpls_6pe','mpls_bgpLU','mpls_mvpn','mpls_ngMvpn']
    ngevpn=['evpn_evpnEnable','evpn_bgp','evpn_l2vni','evpn_l3vni','evpn_l3trmV4','evpn_l3trmV6']
    sda=['sda_ipv4Overlay','sda_ipv6Overlay','sda_l2Overlay','sda_multicast','sda_controlPlane']
    retailwt=0
    govtwt=0
    healthwt=0
    ngewt=0
    educationwt=0
    financewt=0
    pewt=0
    ngevpnwt=0
    sdawt=0
    # computing number of rows
    rows = len(df.axes[0])

    # computing number of columns
    cols = len(df.axes[1])
    baseWt=0
    #for i in range(rows):

    for j in range(cols):
        #print(i)
        #print(j)
        #print(type(df.iloc[i,j]))
        #print("xxxxxx")
        if "str" in str(type(df.iloc[i,j])):
            print(i)
            print(j)
            continue
        if df.iloc[i,j] <= 1:
            baseWt = baseWt + df.iloc[i,j]
        #print(df.iloc[i,j])
    print("\n***base wt is****\n",baseWt)

    retailwt = baseWt
    govtwt = baseWt
    healthwt = baseWt
    ngewt = baseWt
    educationwt = baseWt
    financewt = baseWt
    pewt = baseWt
    ngevpnwt = baseWt
    sdawt = baseWt
    #if wt == 1:
    for x in retail:
            if df.loc[i,x] != 0:
                #print('updating',df.loc[i,x])
                df.loc[i,x] = 5
                retailwt = retailwt + 5
            else:
                df.loc[i,x] = 0
    #if wt == 2:
    for x in govt:
            if df.loc[i,x] != 0:
                df.loc[i,x] = 5
                #print('updating',df.loc[i,x])
                govtwt = govtwt + 5
            else:
                df.loc[i,x] = 0
    #if wt == 3:
    for x in health:
            if df.loc[i,x] != 0:
                #print('updating',df.loc[i,x])
                df.loc[i,x] = 5
                healthwt = healthwt + 5
            else:
                df.loc[i,x] = 0
    #if wt == 4:
    for x in nge:
            if df.loc[i,x] != 0:
                #print('updating',df.loc[i,x])
                df.loc[i,x] = 5
                ngewt = ngewt + 5
            else:
                df.loc[i,x] = 0
    #if wt == 5:
    for x in education:
            if df.loc[i,x] != 0:
                #print('updating',df.loc[i,x])
                df.loc[i,x] = 5
                educationwt = educationwt + 5
            else:
                df.loc[i,x] = 0
    #if wt == 6:
    for x in finance:
            if df.loc[i,x] != 0:
                #print('updating',df.loc[i,x])
                df.loc[i,x] = 5
                financewt = financewt + 5
            else:
                df.loc[i,x] = 0
    #if wt == 7:
    for x in pe:
            if df.loc[i,x] != 0:
                #print('updating',df.loc[i,x])
                df.loc[i,x] = 5
                pewt = pewt + 5
            else:
                df.loc[i,x] = 0
    #if wt == 8:
    for x in ngevpn:
            if df.loc[i,x] != 0:
                #print('updating',df.loc[i,x])
                df.loc[i,x] = 5
                ngevpnwt = ngevpnwt + 5
            else:
                df.loc[i,x] = 0
    #if wt == 9:
    for x in sda:
            if df.loc[i,x] != 0:
                #print('updating',df.loc[i,x])
                df.loc[i,x] = 5
                sdawt = sdawt + 5
            else:
                df.loc[i,x] = 0
    df.loc[i,'retailwt']=retailwt
    df.loc[i,'govtwt']=govtwt
    df.loc[i,'healthwt']=healthwt
    df.loc[i,'ngewt']=ngewt
    df.loc[i,'educationwt']=educationwt
    df.loc[i,'financewt']=financewt
    df.loc[i,'pewt']=pewt
    df.loc[i,'ngevpnwt']=ngevpnwt
    df.loc[i,'sdawt']=sdawt
    print(retailwt,govtwt,healthwt,ngewt,educationwt,financewt,pewt,ngevpnwt,sdawt)
    maxwt = max(retailwt,govtwt,healthwt,ngewt,educationwt,financewt,pewt,ngevpnwt,sdawt)
    df.loc[i,'cust_segment']=maxwt
    ####
    if maxwt == 1:
        df.loc[i,'retailwt']= retailwt + 12
    if maxwt == 2:
        df.loc[i,'govtwt']=govtwt + 12
    if maxwt == 3:
        df.loc[i,'healthwt']=healthwt + 12
    if maxwt == 4:
        df.loc[i,'ngewt']=ngewt+12
    if maxwt == 5:
        df.loc[i,'educationwt']=educationwt + 12
    if maxwt == 6:
        df.loc[i,'financewt']=financewt + 12
    if maxwt == 7:
        df.loc[i,'pewt']=pewt+12
    if maxwt == 8:
        df.loc[i,'ngevpnwt']=ngevpn+12
    if maxwt == 9:
        df.loc[i,'sdawt']=sdawt+12

    ####
    return(df)

###

#dirname  = '/home/bjatti/configCompareTool/project/custConfs/cfgFiles/Sit_Configs/'
# dirname  = '/home/bjatti/configCompareTool/project/custConfs/cfgFiles/test/'
#dirname  = '/home/bjatti/configCompareTool/project/custConfs/cfgFiles/'
#dirname  = '/ws/venaddep-sjc/pyatsLatest/SIT_Project/configParser/'
#fileList = [dirname+'86937_2_25.cfg',dirname+'81640_2_2.cfg',dirname+'4605_2_1.cfg']
fileList = sys.argv[5].split(',')
print("fileList", str(fileList))
# fileList          = []
TRUE              = 1
FALSE             = 0
cust_segment      = ''
cust_mgmtstn      = ''
cust_secstation   = ''
cust_dnac         = ''
# access = 1 dist =2 core =3
cust_devicepin    = '1'
cust_topologytype = '3 tier'

# if os.path.exists(os.path.join(dirname)):
#     for (root,dirs,files) in os.walk(dirname):
#         for f in files:
#             if f.endswith('.cfg'):
#                 fileList.append(dirname+f)

# csv writer
csvfile = open(tempfile, 'w', newline='')
# csvfile = open('/home/bjatti/configCompareTool/project/custConfs/cfgFiles/test/temp.csv', 'w', newline='') # This is for Internal SIT Configs Path
# csvfile = open('ciscoconf_6800.csv', 'w', newline='') # This is for 6800 Path
# csvfile = open('ciscoconf_6500.csv', 'w', newline='') # This is for 6500 Path

ciscowriter = csv.writer(csvfile,delimiter=',')

# Define list variable for Headers
csvheader = ['cust_id','cust_segment','cust_topologytype','cust_devicepin','cust_mgmtstn','cust_secstation','cust_dnac',
             'techsupport_sw_type','techsupport_uptime','techsupport_cpu','techsupport_memory','techsupport_hastate',
             'techsupport_version','techsupport_sl','techsupport_systemmtu',
             'l2_vtp','l2_cdp','l2_lldp','l2_udld','l2_udldAgg','l2_pagp','l2_lacp','l2_on','l2_l2ec','l2_pvst','l2_rstp',
             'l2_mst','l2_stormBcast','l2_stormMcast','l2_uufb','l2_access','l2_trunk','l2_vlan','l2_errdisableRec','l2_macacl',
             'l3v4_l3ec','l3v4_l3if','l3v4_tunnel','l3v4_l3dot1q','l3v4_svi','l3v4_ospfv4','l3v4_eigrpv4','l3v4_ripv4','l3v4_isis',
             'l3v4_bgp','l3v4_static','l3v4_ipacl','l3v4_bfdv4','l3v6_ipv6acl','l3v6_ospfv6','l3v6_eigrpv6','l3v6_bfdv6',
             'sec_portsec','sec_dot1x','sec_mab','sec_webauth','sec_vvlan','sec_ctsSAP','sec_radiusv4','sec_radiusv6','sec_tacac','sec_dhcpSnoop',
             'mcast_mcast','mcast_mcastv6','mcast_igmp','mcast_pim','mcast_pimv6','mcast_mld','mcast_msdp',
             'policy_qos','policy_police','policy_mark','policy_shape','policy_fnf',
             'platform_autoconf','platform_template','platform_asp','platform_svl','platform_stack','platform_len_stk',
             'service_dhcpServer','service_dns','service_span','service_rspan','service_erspan','service_http','service_https','service_callhome',
             'mgmt_tftp','mgmt_ftp','mgmt_mgmt','mgmt_archiveLogging','mgmt_snmpv1','mgmt_snmpv2','mgmt_snmpv3','mgmt_snmp','mgmt_snmpTrap',
             'mgmt_syslog','mgmt_ssh','mgmt_telnet',
             'prog_mdns','mpls_mpls',
             'up_count','access_ports_count','trunk_ports_count','l3_ports_count','up_tunnel_count','loopback_count','ipv6_ports_count',
             'pim_ports_count','pimv6_ports_count','dot1q_ports_count','policy_map_count','class_map_count','span_count','acl_count','v6acl_count',
             'macacl_count','static_route_count','bfd_count','l2_po_count','l3_po_count','ipv6_count','qos_count','psec_count','dot1x_count',
             'mab_count','webauth_count','svi_count','vrf_count','ospf_count','eigrp_count','bgp_count','rip_count','ospf_peer_count','eigrp_peer_count',
             'rip_peer_count','bgp_peer_count','isis_peer_count','flow_mon_count','flow_rec_count','flow_exp_count','mac',
             'policy_autoQos','policy_Copp','policy_ecIngressQos','policy_ecEgressQos','policy_ingressPolicing','policy_egressPolicing','policy_egressShping',
             'policy_WRED','policy_QoSSharing','policy_Inv4Acl','policy_Egressv4Acl','policy_Inv6Acl','policy_Egressv6Acl',
             'policy_v4OGACL','policy_v6OGACL',
             'mpls_ldp','mpls_mplsTE','mpls_vpnv4','mpls_vpnv6','mpls_l2vpn','mpls_6pe','mpls_bgpLU','mpls_mvpn','mpls_ngMvpn',
             'sec_qnq','sec_macsec','l3_bfd','l3_udld','l2_dhcpSnooping','l3_hsrp','mcast_igmpStaticJoin','l3_bfd_template',
             'policy_fnfSGT','policy_fnfV6','sec_ctsSGTMAP','sec_httpLocalAuth','sec_SXP','sec_CoA','sec_accounting',
             'sec_v6RAGuard','prog_netconf','misc_snmp_trap',
             'evpn_evpnEnable','evpn_bgp','evpn_l2vni','evpn_l3vni','evpn_l3trmV4','evpn_l3trmV6',
             'sda_ipv4Overlay','sda_ipv6Overlay','sda_l2Overlay','sda_multicast','sda_controlPlane']

# Write Header Row into '.csv' file
ciscowriter.writerow(csvheader)

try:
    for line in fileList:
        line = dirname + line
        # Parsing file by file to validate
        parse = CiscoConfParse(line)

        try:
            orig=copyRunning(line)
            print("----")
        except:
            print("copyRunning exception")
            continue

        print("lines in running config:",orig)
        srcFile=line
        runningConfig=line+".runn"
        dupConfig=runningConfig+".dup"

        # Grep the number to identify CustomerID from filename
        mat = re.match(dirname+r'([a-zA-Z0-9]+)\_*',line)
        cust_id = mat.group(1)

        # Switch Type
        r0 = ''
        tech_sw_type = parse.find_objects(' DESCR:')
        for obj in tech_sw_type:
            r0 = obj.re_match(r' DESCR: "(.*)"')
            if(r0):
                break
        techsupport_sw_type = r0
        #print("--------")
        # Uptime
        r1=r2=r3=r4=r5=r6=''
        tech_uptime = parse.find_objects('Available system uptime')
        for obj in tech_uptime:
            r1 = obj.re_match(r' Available system uptime =(.*)')

        if(r1==""):
            tech_uptime = parse.find_objects('uptime is ')
            for obj in tech_uptime:
                r1 = obj.re_match(r'uptime is (.*)')

        # cpu
        tech_cpu = parse.find_objects('^CPU utilization for five seconds:')
        for obj in tech_cpu:
            r2 = obj.re_match(r'one minute: (.*)%;')
            if r2:
                break

        # Memory get % of memory free / used
        tech_mem = parse.find_objects('^System memory  :')
        for obj in tech_mem:
            r31  = obj.re_match(r':(.*)K total')
            r32  = obj.re_match(r', (.*)K used')
            r311 = int(r31)
            r322 = int(r32)
            r3   = int(r322/r311*100)

        # Another memory output
        tech_mem = parse.find_objects('^Processor Pool Total:')
        for obj in tech_mem:
            r31  = obj.re_match(r'Processor Pool Total: (.*) Used')
            r32  = obj.re_match(r'Used: (.*) Free')
            r311 = int(r31)
            r322 = int(r32)
            r3   = int(r322/r311*100)

        # HA State
        r4 = 'Simplex'
        tech_hastate = parse.find_objects('Hardware Mode =')
        for obj in tech_hastate:
            r4 = obj.re_match(r'Hardware Mode = (.*)')

        # Version
        r5 = 0
        tech_version = parse.find_objects('Image Version =')
        for obj in tech_version:
            r5 = obj.re_match(r'Image Version =.* Version (.*) RELEASE')

        if r5 == 0 :
            tech_version = parse.find_objects('Cisco IOS Software ')
            for obj in tech_version:
                r5 = obj.re_match(r' Version (.*),')
                if r5 == "":
                    r5 = obj.re_match(r' Version (.*) \[')
                    if r5 == "" :
                        break

        # System MTU
        techsupport_systemmtu = parse.find_objects('system mtu')
        for obj in techsupport_systemmtu:
            r6 = obj.re_match(r'system mtu(.*)')
        if r6 == 0:
            r6 = '1500'


        # MAC Address
        mac = 0
        mac_scale = ""
        mac_scale = parse.find_objects(r'  ([0-9a-f]{4})[.]([0-9a-f]{4})[.]([0-9a-f]{4})  ')
        for obj in mac_scale:
            mac = mac+1

        techsupport_uptime    = r1
        techsupport_cpu       = r2
        techsupport_memory    = r3
        techsupport_hastate   = r4
        techsupport_version   = r5
        techsupport_sl        = ''
        techsupport_systemmtu = r6

        # Layer2
        # ======
        # VTP Version
        if parse.find_objects('vtp version 2'):
            vtp = 1
        elif parse.find_objects('vtp version 3'):
            vtp = 1
        else:
            vtp = 1
        removeLine(srcFile,"vtp version")

        # CDP
        if parse.find_objects('no cdp run'):
            cdp = FALSE
        else:
            cdp = TRUE
        removeLine(srcFile,"cdp run")

        # LLDP
        if parse.find_objects('no lldp run'):
            lldp = FALSE
        else:
            lldp = TRUE
        removeLine(srcFile,"lldp run")

        # UDLD
        if parse.find_objects('no udld enable'):
            udld = FALSE
        else:
            udld = TRUE
        removeLine(srcFile,"udld enable")

        # Fast UDLD
        if parse.find_objects('udld aggressive'):
            udldAgg = TRUE
        else:
            udldAgg = FALSE
        removeLine(srcFile,"udld aggressive")

        # EtherChannel pAgp
        if parse.find_objects('mode desirable') or parse.find_objects('mode auto'):
            pagp = TRUE
        else:
            pagp = FALSE
        removeLine(srcFile,"mode desirable")
        removeLine(srcFile,"mode auto")

        # EtherChannel LACP
        if parse.find_objects('mode active') or parse.find_objects('mode passive'):
            lacp = TRUE
        else:
            lacp = FALSE
        removeLine(srcFile,"mode active")
        removeLine(srcFile,"mode passive")

        # EtherChannel ON
        if parse.find_objects('mode on'):
            on = TRUE
        else:
            on = FALSE
        removeLine(srcFile,"mode on")

        # Layer2 EtherChannel
        if parse.find_parents_w_child('^interf','switchport mode','channel-group '):
            l2ec = TRUE
        else:
            l2ec = FALSE
        removeLine(srcFile,"switchport mode")
        removeLine(srcFile,"channel-group")

        # PVST
        if parse.find_objects('spanning-tree mode pvst'):
            pvst = TRUE
        else:
            pvst = FALSE
        removeLine(srcFile,"spanning-tree mode pvst")

        # RSTP
        if parse.find_objects('spanning-tree mode rapid'):
            rstp = TRUE
        else:
            rstp = FALSE
        removeLine(srcFile,"spanning-tree mode rapid")

        # MST
        if parse.find_objects('spanning-tree mode mst'):
            mst = TRUE
        else:
            mst = FALSE
        removeLine(srcFile,"spanning-tree mode mst")

        # StormControl BCAST
        if parse.find_parents_w_child('^interf','storm-control broadcast') or parse.find_parents_w_child('^template','storm-control broadcast'):
            stormBcast = TRUE
        else:
            stormBcast = FALSE
        removeLine(srcFile,"template")
        removeLine(srcFile,"storm-control broadcast")

        # StormControl MCAST
        if parse.find_parents_w_child('^interf','storm-control multicast') or parse.find_parents_w_child('^template','storm-control multicast'):
            stormMcast = TRUE
        else:
            stormMcast = FALSE
        removeLine(srcFile,"template")
        removeLine(srcFile,"storm-control multicast")

        # UUFB
        if parse.find_objects('switchport block unicast'):
            uufb = TRUE
        else:
            uufb = FALSE
        removeLine(srcFile,"switchport block unicast")

        # Access Ports
        if parse.find_parents_w_child('^interf','switchport mode access'):
            access = TRUE
        else:
            access = FALSE
        removeLine(srcFile,"switchport mode access")

        # Trunk Ports
        if parse.find_parents_wo_child('^interf','switchport mode trunk'):
            trunk = TRUE
        else:
            trunk = FALSE
        removeLine(srcFile,"switchport mode trunk")

        # Vlans
        if parse.find_objects('^vlan'):
            vlan = TRUE
        else:
            vlan = FALSE
        removeLine(srcFile,"^vlan")

        # Err-Disable Recovery Cause
        if parse.find_objects('errdisable recovery cause'):
            errdisableRec = TRUE
        else:
            errdisableRec = FALSE
        removeLine(srcFile,"errdisable recovery cause")

        # Mac Acl
        if parse.find_objects('mac access'):
            macacl = TRUE
        else:
            macacl = FALSE
        removeLine(srcFile,"mac access")

        # Layer3
        # ======
        # Layer3 EtherChannel
        if parse.find_parents_w_child('^interf','no switchport','channel-group '):
            l3ec = TRUE
        else:
            l3ec = FALSE
        removeLine(srcFile,"no switchport")
        removeLine(srcFile,"channel-group ")

        # Layer3 Interfaces
        if parse.find_parents_w_child('^interf','no switchport'):
            l3if = TRUE
        else:
            l3if = FALSE

        # Tunnel Interfaces
        if parse.find_parents_wo_child('^interface Tunnel','shutdown'):
            tunnel = TRUE
        else:
            tunnel = FALSE
        removeLine(srcFile,"^interface Tunnel")

        # Layer3 Dot1q Sub Interface
        if parse.find_parents_wo_child(r'^interface.*\.\d+','shutdown'):
            l3dot1q = TRUE
        else:
            l3dot1q = FALSE
        removeLine(srcFile,"^interface.*\d+")

        # SVI
        if parse.find_parents_wo_child('^interface Vlan','shutdown'):
            svi = TRUE
        else:
            svi = FALSE
        removeLine(srcFile,"^interface Vlan")

        # Ospf
        if parse.find_parents_w_child('^router ospf','network'):
            ospfv4 = TRUE
        else:
            ospfv4 = FALSE
        removeLine(srcFile,"^router ospf")
        removeLine(srcFile,"network")

        # Eigrp
        if parse.find_parents_w_child('^router eigrp','network'):
            eigrpv4 = TRUE
        else:
            eigrpv4 = FALSE
        removeLine(srcFile,"^router eigrp")
        removeLine(srcFile,"network")

        # Rip
        if parse.find_parents_w_child('^router rip','network'):
            ripv4 = TRUE
        else:
            ripv4 = FALSE
        removeLine(srcFile,"^router rip")
        removeLine(srcFile,"network")

        # Isis
        if parse.find_parents_wo_child('^router isis','shut'):
            isis = TRUE
        else:
            isis = FALSE
        removeLine(srcFile,"^router isis")
        removeLine(srcFile,"network")

        # Bgp
        if parse.find_parents_wo_child('^router bgp','shut'):
            bgp = TRUE
        else:
            bgp = FALSE
        removeLine(srcFile,"^router bgp")

        if bgp == TRUE:
            # cust_devicepin = 'Core'
            cust_devicepin = '3'
        # Static Routes
        if parse.find_objects('ip route '):
            static = TRUE
        else:
            static = FALSE
        removeLine(srcFile,"ip route ")

        # Ip Access-list
        if parse.find_objects('ip access'):
            ipacl = TRUE
        else:
            ipacl = FALSE
        removeLine(srcFile,"ip access")
        removeLine(srcFile,"match ip address.*\.")
        removeLine(srcFile,"permit")
        removeLine(srcFile,"match")
        removeLine(srcFile,"deny")
        removeLine(srcFile,"ip vrf forwarding")
        removeLine(srcFile,"ip address")
        removeLine(srcFile,"switchport")
        removeLine(srcFile,"description")
        removeLine(srcFile,"neighbor")
        removeLine(srcFile,"show")

        # BFDv4
        if parse.find_parents_w_child('^router ','bfd all-interface'):
            bfdv4 = TRUE
        else:
            bfdv4 = FALSE
        removeLine(srcFile,"bfd all-interface")

        # Ipv6 Access-list
        if parse.find_objects('ipv6 access'):
            ipv6acl = TRUE
        else:
            ipv6acl = FALSE
        removeLine(srcFile,"ipv6 access")

        # Ospfv3
        if parse.find_parents_wo_child('^ipv6 router','shut'):
            ospfv6 = TRUE
        else:
            ospfv6 = FALSE
        removeLine(srcFile,"^ipv6 router")

        # EigrpV6
        if parse.find_parents_w_child('^router eigrp','address-family ipv6'):
            eigrpv6 = TRUE
        else:
            eigrpv6 = FALSE
        removeLine(srcFile,"address-family ipv6")

        # BFDv6
        if parse.find_parents_w_child('^ipv6 router ','bfd all-interface'):
            bfdv6 = TRUE
        else:
            bfdv6 = FALSE

        # Security
        # ========
        # PortSec
        if parse.find_parents_w_child('^interf','switchport port-sec') or parse.find_parents_w_child('^template','switchport port-sec'):
            portsec = TRUE
        else:
            portsec = FALSE
        removeLine(srcFile,"switchport port-sec")

        # Dot1x
        if parse.find_objects('dot1x system-auth-control') and parse.find_objects('dot1x pae auth'):
            dot1x = TRUE
        else:
            dot1x = FALSE
        removeLine(srcFile,"dot1x pae auth")
        removeLine(srcFile,"dot1x system-auth-control")

        # Mab
        if parse.find_objects('dot1x system-auth-control') and parse.find_objects('mab'):
            mab = TRUE
        else:
            mab = FALSE
        removeLine(srcFile,"mab")

        # WebAuth
        if parse.find_objects('dot1x system-auth-control') and parse.find_objects('webauth'):
            webauth = TRUE
        else:
            webauth = FALSE
        removeLine(srcFile,"webauth")

        # Voice Vlan
        if parse.find_objects('voice vlan'):
            vvlan = TRUE
        else:
            vvlan = FALSE
        removeLine(srcFile,"voice vlan")

        if mab == TRUE or dot1x == TRUE or vvlan == TRUE or webauth == TRUE:
            # cust_devicepin = 'Access'
            cust_devicepin = '1'

        # CTS SAP
        if parse.find_objects('cts man'):
            ctsSAP = TRUE
        else:
            ctsSAP = FALSE
        removeLine(srcFile,"cts man")

        # Radius V4
        if parse.find_parents_w_child('^radius server','address ipv4'):
            radiusv4 = TRUE
        else:
            radiusv4 = FALSE
        removeLine(srcFile,"^radius server")
        removeLine(srcFile,"address ipv4")

        # Radius V6
        if parse.find_parents_w_child('^radius server','address ipv6'):
            radiusv6 = TRUE
        else:
            radiusv6 = FALSE
        removeLine(srcFile,"^radius server")
        removeLine(srcFile,"address ipv6")

        # AAA Tacacs+
        if parse.find_objects('tacac'):
            tacac = TRUE
        else:
            tacac = FALSE
        removeLine(srcFile,"tacac")

        # Dhcp Snooping
        if parse.find_objects('ip dhcp snooping'):
            dhcpSnoop = TRUE
        else:
            dhcpSnoop = FALSE
        removeLine(srcFile,"ip dhcp snooping")

        # Multicast
        # =========
        # Mcastv4
        if parse.find_objects('ip multicast-routing'):
            mcast = TRUE
        else:
            mcast = FALSE
        removeLine(srcFile,"ip multicast-routing")

        # Mcastv6
        if parse.find_objects('ipv6 multicast-routing'):
            mcastv6 = TRUE
        else:
            mcastv6 = FALSE
        removeLine(srcFile,"ipv6 multicast-routing")

        # Igmp
        # Igmp Snooping
        if parse.find_objects('ip igmp'):
            igmp = TRUE
        else:
            igmp = FALSE
        removeLine(srcFile,"ip igmp")

        # Pim
        if parse.find_parents_w_child('^interface ','ip pim'):
            pim = TRUE
        else:
            pim = FALSE
        removeLine(srcFile,"ip pim")

        # PimV6
        if parse.find_parents_w_child('^interface ','ip pim','ipv6 address'):
            pimv6 = TRUE
        else:
            pimv6 = FALSE
        removeLine(srcFile,"ipv6 address")

        # Mld Snooping
        if parse.find_objects('ipv6 mld snooping'):
            mld = TRUE
        else:
            mld = FALSE
        removeLine(srcFile,"ipv6 mld snooping")

        # MSDP
        if parse.find_objects('msdp'):
            msdp = TRUE
        else:
            msdp = FALSE
        removeLine(srcFile,"msdp")

        # Policy
        # ======
        # QOS
        if parse.find_parents_w_child('^interface ','service-policy'):
            qos = TRUE
        else:
            qos = FALSE
        removeLine(srcFile,"service-policy")

        # Policing
        if parse.find_parents_w_child('^policy-map ','police'):
            police = TRUE
        else:
            police = FALSE
        #removeLine(srcFile,"^policy-map")
        removeLine(srcFile,"police")

        # Marking
        if parse.find_parents_w_child('^policy-map ','set'):
            mark = TRUE
        else:
            mark = FALSE
        removeLine(srcFile,"set")

        # Shaping
        if parse.find_parents_w_child('^policy-map ','shape'):
            shape = TRUE
        else:
            shape = FALSE
        removeLine(srcFile,"shape")

        # Netflow
        if parse.find_objects('flow export') and parse.find_objects('flow moni') and parse.find_objects('flow rec'):
            fnf = TRUE
        else:
            fnf = FALSE
        removeLine(srcFile,"flow export")
        removeLine(srcFile,"flow moni")
        removeLine(srcFile,"flow rec")

        # Platform
        # ========
        # Autoconf
        if parse.find_objects('autoconf enable'):
            autoconf = TRUE
        else:
            autoconf = FALSE
        removeLine(srcFile,"autoconf enable")

        # Interface Template
        if parse.find_objects('source template'):
            template = TRUE
        else:
            template = FALSE
        removeLine(srcFile,"source template")


        # ASP
        if parse.find_parents_w_child('^interface ','macro auto'):
            asp = TRUE
        else:
            asp = FALSE
        removeLine(srcFile,"macro auto")

        # SVL
        if parse.find_objects('stackwise-virtual'):
            svl = TRUE
        else:
            svl = FALSE
        removeLine(srcFile,"stackwise-virtual")

        # Stacking
        stk = parse.find_objects(r'switch.*provi')
        len_stk = len(stk)
        if len(stk) > 1:
            stack = TRUE
        else:
            stack = FALSE
        removeLine(srcFile,"switch.*provi")

        # Services
        # ========
        # Dhcp Server
        if parse.find_objects('ip dhcp pool'):
            dhcpServer = TRUE
        else:
            dhcpServer = FALSE
        removeLine(srcFile,"ip dhcp pool")

        # DNS
        if parse.find_objects('^ip domain'):
            dns = TRUE
        else:
            dns = FALSE
        removeLine(srcFile,"^ip domain")

        # Span
        if parse.find_objects(r'monitor session.*destination interface'):
            span = TRUE
        else:
            span = FALSE
        removeLine(srcFile,"monitor session.*destination interface")

        # RSpan
        if parse.find_objects(r'monitor session.*remote vlan'):
            rspan = TRUE
        else:
            rspan = FALSE
        removeLine(srcFile,"monitor session.*remote vlan")

        # ERSpan
        if parse.find_objects(r'erspan'):
            erspan = TRUE
        else:
            erspan = FALSE
        removeLine(srcFile,"erspan")

        # Http Server
        if parse.find_objects('^ip http server'):
            http = TRUE
        else:
            http = FALSE
        removeLine(srcFile,"^ip http server")

        # Https Server
        if parse.find_objects('^ip http secure-server'):
            https = TRUE
        else:
            https = FALSE
        removeLine(srcFile,"^ip http secure-server")

        # Call Home
        if parse.find_objects('^call-home'):
            callhome = TRUE
        else:
            callhome = FALSE
        removeLine(srcFile,"^call-home")

        # Management
        # ==========
        # Tftp
        if parse.find_objects('^tftp-server'):
            tftp = TRUE
        else:
            tftp = FALSE
        removeLine(srcFile,"^tftp-server")


        # Ftp
        if parse.find_objects('^ip ftp'):
            ftp = TRUE
        else:
            ftp = FALSE
        removeLine(srcFile,"^ip ftp")

        # Mgmt Port
        if parse.find_parents_w_child('^interface ','vrf forwarding Mgmt'):
            mgmt = TRUE
        else:
            mgmt = FALSE
        removeLine(srcFile,"vrf forwarding Mgmt")

        # Logging Archive
        if parse.find_objects('^archive'):
            archiveLogging = TRUE
        else:
            archiveLogging = FALSE
        removeLine(srcFile,"^archive")

        # SnmpV1
        if parse.find_objects(r'snmp-server.*v1'):
            snmpv1 = TRUE
        else:
            snmpv1 = FALSE
        removeLine(srcFile,"snmp-server.*v1")

        # Snmp2c
        if parse.find_objects('snmp-server.*2c'):
            snmpv2 = TRUE
        else:
            snmpv2 = FALSE
        removeLine(srcFile,"snmp-server.*2c")

        # SnmpV3
        if parse.find_objects('snmp-server.*v3'):
            snmpv3 = TRUE
        else:
            snmpv3 = FALSE
        removeLine(srcFile,"snmp-server.*v3")

        # Snmp
        if parse.find_objects('snmp-server'):
            snmp = TRUE
        else:
            snmp = FALSE
        removeLine(srcFile,"snmp-server")

        # Snmp Trap
        if parse.find_objects('snmp trap'):
            snmpTrap = TRUE
        else:
            snmpTrap = FALSE
        removeLine(srcFile,"snmp trap")

        # Syslog Server
        if parse.find_objects('logging host'):
            syslog = TRUE
        else:
            syslog = FALSE
        removeLine(srcFile,"logging host")

        # SSH
        if parse.find_objects('^ip ssh'):
            ssh = TRUE
        else:
            ssh = FALSE
        removeLine(srcFile,"ip ssh version")

        # Telnet
        if parse.find_objects('transport input all') or parse.find_objects('transport input telnet'):
            telnet = TRUE
        else:
            telnet = FALSE
        removeLine(srcFile,"transport input all")
        removeLine(srcFile,"transport input telnet")

        # Program
        # =======
        # MDNS
        if parse.find_objects('mdns'):
            mdns = TRUE
        else:
            mdns = FALSE
        removeLine(srcFile,"mdns")

        # MPLS
        # ====
        # Mpls
        if parse.find_objects('mpls ip'):
            mpls = TRUE
        else:
            mpls = FALSE
        removeLine(srcFile,"mpls ip")
        # Extra features
        #
        #policy_autoQos
        if parse.find_parents_w_child('^interface ','auto qos'):
            policy_autoQos = TRUE
        else:
            policy_autoQos = FALSE
        removeLine(srcFile,"auto qos")
        #policy_Copp,
        if parse.find_objects('service-policy input system-cpp-policy'):
            policy_Copp = TRUE
        else:
            policy_Copp = FALSE
        removeLine(srcFile,"service-policy input system-cpp-policy")
        #policy_ecIngressQos,
        if parse.find_parents_w_child('^interface Port-channel ','service-policy input'):
            policy_ecIngressQos = TRUE
        else:
            policy_ecIngressQos = FALSE
        removeLine(srcFile,"service-policy input")
        #policy_ecEgressQos,
        if parse.find_parents_w_child('^interface Port-channel ','service-policy output'):
            policy_ecEgressQos = TRUE
        else:
            policy_ecEgressQos = FALSE
        removeLine(srcFile,"service-policy output")
        #policy_ingressPolicing,
        if parse.find_parents_w_child('policy-map ','police rate '):
            policy_ingressPolicing = TRUE
        else:
            policy_ingressPolicing = FALSE
        removeLine(srcFile,"police rate ")
        #policy_egressPolicing,
        if parse.find_parents_w_child('policy-map ','police rate '):
            policy_egressPolicing = TRUE
        else:
            policy_egressPolicing = FALSE
        #policy_egressShping,
        if parse.find_parents_w_child('policy-map ','shape '):
            policy_egressShping = TRUE
        else:
            policy_egressShping = FALSE
        removeLine(srcFile,"shape")
        #policy_WRED,
        if parse.find_parents_w_child('policy-map ','random-detect '):
            policy_WRED = TRUE
        else:
            policy_WRED = FALSE
        removeLine(srcFile,"random-detect")

        #policy_QoSSharing,
        if parse.find_parents_w_child('policy-map ','bandwidth '):
            policy_QoSSharing = TRUE
        else:
            policy_QoSSharing = FALSE
        removeLine(srcFile,"bandwidth")

        #policy_Inv4Acl,
        if parse.find_parents_w_child('^interface ','ip access-group.*in'):
            policy_Inv4Acl = TRUE
        else:
            policy_Inv4Acl = FALSE
        removeLine(srcFile,"ip access-group.*in")
        #policy_Egressv4Acl,
        if parse.find_parents_w_child('^interface ','ip access-group.*out'):
            policy_Egressv4Acl = TRUE
        else:
            policy_Egressv4Acl = FALSE
        removeLine(srcFile,"ip access-group.*out")
        #policy_Inv6Acl,
        if parse.find_parents_w_child('^interface ','ipv6 traffic-filter.*in'):
            policy_Inv6Acl = TRUE
        else:
            policy_Inv6Acl = FALSE
        removeLine(srcFile,"ipv6 traffic-filter.*in")
        #policy_Egressv6Acl,
        if parse.find_parents_w_child('^interface ','ipv6 traffic-filter.*out'):
            policy_Egressv6Acl = TRUE
        else:
            policy_Egressv6Acl = FALSE
        removeLine(srcFile,"ipv6 traffic-filter.*out")
        #policy_v4OGACL,
        if parse.find_parents_w_child('ip access-list ','object-group'):
            policy_v4OGACL = TRUE
        else:
            policy_v4OGACL = FALSE
        removeLine(srcFile,"object-group")
        #policy_v6OGACL,
        if parse.find_parents_w_child('ipv6 access-list ','object-group'):
            policy_v6OGACL = TRUE
        else:
            policy_v6OGACL = FALSE
        removeLine(srcFile,"ipv6 access-list")
        #mpls_ldp,
        if parse.find_parents_w_child('^interface ','mpls ip'):
            mpls_ldp = TRUE
        else:
            mpls_ldp = FALSE
        removeLine(srcFile,"mpls ip")
        #mpls_mplsTE,
        if parse.find_parents_w_child('^interface Tunnel ','tunnel mode mpls traffic-eng'):
            mpls_mplsTE = TRUE
        else:
            mpls_mplsTE = FALSE
        removeLine(srcFile,"tunnel mode mpls traffic-eng")
        #mpls_vpnv4,
        if parse.find_parents_w_child('^router bgp ','address-family vpnv4'):
            mpls_vpnv4 = TRUE
        else:
            mpls_vpnv4 = FALSE
        removeLine(srcFile,"router bgp")
        removeLine(srcFile,"address-family vpnv4")
        #mpls_vpnv6,
        if parse.find_parents_w_child('^router bgp ','address-family vpnv6'):
            mpls_vpnv6 = TRUE
        else:
            mpls_vpnv6 = FALSE
        removeLine(srcFile,"address-family vpnv6")
        #mpls_l2vpn,
        if parse.find_parents_w_child('^router bgp ','address-family l2vpn vpls'):
            mpls_l2vpn = TRUE
        else:
            mpls_l2vpn = FALSE
        removeLine(srcFile,"address-family l2vpn vpls")
        #mpls_6pe,
        if parse.find_parents_w_child('^router bgp ','template peer-policy'):
            mpls_6pe = TRUE
        else:
            mpls_6pe = FALSE
        removeLine(srcFile,"template peer-policy")
        #mpls_bgpLU,
        if parse.find_parents_w_child('^router bgp ','template peer-policy'):
            mpls_bgpLU = TRUE
        else:
            mpls_bgpLU = FALSE
        #mpls_mvpn,
        if parse.find_parents_w_child('^router bgp ','address-family ipv4 mdt'):
            mpls_mvpn = TRUE
        else:
            mpls_mvpn = FALSE
        removeLine(srcFile,"address-family ipv4 mdt")
        #mpls_ngMvpn,
        if parse.find_parents_w_child('^router bgp ','address-family ipv4 mvpn'):
            mpls_ngMvpn = TRUE
        else:
            mpls_ngMvpn = FALSE
        removeLine(srcFile,"address-family ipv4 mvpn")
        #sec_qnq,
        if parse.find_parents_w_child('^interface ','switchport vlan mapping'):
            sec_qnq = TRUE
        else:
            sec_qnq = FALSE
        removeLine(srcFile,"switchport vlan mapping")
        #sec_macsec,
        if parse.find_parents_w_child('^interface ','mka policy '):
            sec_macsec = TRUE
        else:
            sec_macsec = FALSE
        removeLine(srcFile,"mka policy ")
        #l3_bfd,
        if parse.find_parents_w_child('^interface ','bfd interval'):
            l3_bfd = TRUE
        else:
            l3_bfd = FALSE
        removeLine(srcFile,"bfd interval")
        #l3_udld,
        if parse.find_parents_w_child('^interface ','udld '):
            l3_udld = TRUE
        else:
            l3_udld = FALSE
        removeLine(srcFile,"udld ")
        #l2_dhcpSnooping,
        if parse.find_parents_w_child('^interface ','ip dhcp snooping '):
            l2_dhcpSnooping = TRUE
        else:
            l2_dhcpSnooping = FALSE
        removeLine(srcFile,"ip dhcp snooping")
        #l3_hsrp,
        if parse.find_parents_w_child('^interface ','standby'):
            l3_hsrp = TRUE
        else:
            l3_hsrp = FALSE
        removeLine(srcFile,"standby")
        #mcast_igmpStaticJoin,
        if parse.find_parents_w_child('^interface ','ip igmp join-group '):
            mcast_igmpStaticJoin = TRUE
        else:
            mcast_igmpStaticJoin = FALSE
        removeLine(srcFile,"ip igmp join-group ")
        #l3_bfd_template,
        if parse.find_parents_w_child('^bfd-template ','interval min-tx'):
            l3_bfd_template = TRUE
        else:
            l3_bfd_template = FALSE
        removeLine(srcFile,"^bfd-template")
        removeLine(srcFile,"interval min-tx")
        #policy_fnfSGT,
        if parse.find_parents_w_child('^flow record ','match flow cts '):
            policy_fnfSGT = TRUE
        else:
            policy_fnfSGT = FALSE
        removeLine(srcFile,"match flow cts ")
        removeLine(srcFile,"^flow record")
        #policy_fnfV6,
        if parse.find_objects('ipv6 flow monitor'):
            policy_fnfV6 = TRUE
        else:
            policy_fnfV6 = FALSE
        removeLine(srcFile,"ipv6 flow monitor")
        #sec_ctsSGTMAP,
        if parse.find_objects('cts role-based sgt-map'):
            sec_ctsSGTMAP = TRUE
        else:
            sec_ctsSGTMAP = FALSE
        removeLine(srcFile,"cts role-based sgt-map")
        #sec_httpLocalAuth,
        if parse.find_objects('ip http authentication local'):
            sec_httpLocalAuth = TRUE
        else:
            sec_httpLocalAuth = FALSE
        removeLine(srcFile,"ip http authentication local")
        #sec_SXP,
        if parse.find_objects('cts sxp enable'):
            sec_SXP = TRUE
        else:
            sec_SXP = FALSE
        removeLine(srcFile,"cts sxp enable")
        #sec_CoA,
        if parse.find_objects('aaa server radius dynamic-author'):
            sec_CoA = TRUE
        else:
            sec_CoA = FALSE
        removeLine(srcFile,"aaa server radius dynamic-author")
        #sec_accounting,
        if parse.find_objects('aaa accounting'):
            sec_accounting = TRUE
        else:
            sec_accounting = FALSE
        removeLine(srcFile,"aaa accounting")
        #sec_v6RAGuard,
        if parse.find_parents_w_child('^interface ','ipv6 nd raguard '):
            sec_v6RAGuard = TRUE
        else:
            sec_v6RAGuard = FALSE
        removeLine(srcFile,"ipv6 nd raguard ")
        #prog_netconf,
        if parse.find_objects('netconf-yang'):
            prog_netconf = TRUE
        else:
            prog_netconf = FALSE
        removeLine(srcFile,"netconf-yang")
        #misc_snmp_trap,
        if parse.find_objects('snmp-server enable traps'):
            misc_snmp_trap = TRUE
        else:
            misc_snmp_trap = FALSE
        removeLine(srcFile,"snmp-server enable traps")
        #evpn_evpnEnable,
        if parse.find_objects('l2vpn evpn'):
            evpn_evpnEnable = TRUE
        else:
            evpn_evpnEnable = FALSE
        removeLine(srcFile,"l2vpn evpn")
        #evpn_bgp,
        if parse.find_parents_w_child('^router bgp ','address-family l2vpn evpn'):
            evpn_bgp = TRUE
        else:
            evpn_bgp = FALSE
        removeLine(srcFile,"address-family l2vpn evpn")
        #evpn_l2vni,
        if parse.find_parents_w_child('^l2vpn evpn instance ','encapsulation vxlan'):
            evpn_l2vni = TRUE
        else:
             evpn_l2vni= FALSE
        removeLine(srcFile,"^l2vpn evpn instance ")
        removeLine(srcFile,"encapsulation vxlan")
        #evpn_l3vni,
        if parse.find_parents_w_child('vlan configuration ','member vni'):
            evpn_l3vni = TRUE
        else:
            evpn_l3vni = FALSE
        removeLine(srcFile,"vlan configuration")
        removeLine(srcFile,"member vni")
        #evpn_l3trmV4,
        if parse.find_parents_w_child('^vrf definition ','mdt auto-discovery vxlan'):
            evpn_l3trmV4 = TRUE
        else:
            evpn_l3trmV4 = FALSE
        removeLine(srcFile,"mdt auto-discovery vxlan")
        removeLine(srcFile,"vrf definition")
        #evpn_l3trmV6,
        if parse.find_parents_w_child('^router bgp ','address-family ipv6 mvpn'):
            evpn_l3trmV6 = TRUE
        else:
            evpn_l3trmV6 = FALSE
        if parse.find_parents_w_child('^vrf definition ','mdt auto-discovery vxlan') and evpn_l3trmV6 == TRUE:
            evpn_l3trmV6 = TRUE
        else:
            evpn_l3trmV6 = FALSE
        removeLine(srcFile,"mdt auto-discovery vxlan")
        #sda_ipv4Overlay,
        if parse.find_parents_w_child('^router lisp','service ipv4'):
            sda_ipv4Overlay = TRUE
        else:
            sda_ipv4Overlay = FALSE
        removeLine(srcFile,"router lisp")
        removeLine(srcFile,"service ipv4")
        #sda_ipv6Overlay,
        if parse.find_parents_w_child('^router lisp','service ipv6'):
            sda_ipv6Overlay = TRUE
        else:
            sda_ipv6Overlay = FALSE
        removeLine(srcFile,"service ipv6")
        #sda_l2Overlay,
        if parse.find_parents_w_child('^router lisp','service ethernet'):
            sda_l2Overlay = TRUE
        else:
            sda_l2Overlay = FALSE
        removeLine(srcFile,"service ethernet")
        #sda_multicast,
        if parse.find_parents_w_child('^interface LISP0 ','ip pim '):
            sda_multicast = TRUE
        else:
            sda_multicast = FALSE
        removeLine(srcFile,"^interface LISP0 ")
        removeLine(srcFile,"ip pim")
        #sda_controlPlane
        if parse.find_parents_w_child('^router lisp','eid-record instance-id'):
            sda_controlPlane = TRUE
        else:
            sda_controlPlane = FALSE
        removeLine(srcFile,"eid-record instance-id")
              # biswa added on 15 Feb 2022
        removeLine(srcFile,"ipv6 enable")
        removeLine(srcFile,"aaa")
        removeLine(srcFile," server")
        removeLine(srcFile,"hostname")
        removeLine(srcFile," enable")
        removeLine(srcFile," no enable")
        removeLine(srcFile," no ip address")
        removeLine(srcFile,"no ")
        removeLine(srcFile," exit")
        removeLine(srcFile,"enable password")
        removeLine(srcFile,"clock")
        removeLine(srcFile,"boot")
        removeLine(srcFile,"ipv6")
        removeLine(srcFile,"service call-home")
        #removeLine(srcFile,"")
        removeLine(srcFile,"password")
        removeLine(srcFile,"length")
        removeLine(srcFile,"transport")
        removeLine(srcFile," stop")
        removeLine(srcFile," exec")
        removeLine(srcFile,"line")
        removeLine(srcFile,"username")
        removeLine(srcFile,"ntp")
        removeLine(srcFile,"ip nat")
        notParsedPercentage = percentMiss(srcFile,orig)


        # Scaling Part
        # ============
        # Number of UP Ports
        up = parse.find_parents_wo_child('^interface ','shut')
        up_count = len(up)

        # Number of Layer2 Ports
        access_ports = parse.find_parents_w_child('^interface ','switchport mode access')
        access_ports_count = len(access_ports)

        # Number of Trunk Ports
        trunk_ports = parse.find_parents_w_child('^interface ','switchport mode trunk')
        trunk_ports_count = len(trunk_ports)

        # Number of Layer3 Ports
        l3_ports = parse.find_parents_w_child('^interface ','no switchport')
        l3_ports_count = len(l3_ports)

        # Number of Tunnel Interfaces
        up_tunnel = parse.find_parents_wo_child('^interface Tunn','shut')
        up_tunnel_count = len(up_tunnel)

        # Number of Loopback Interfaces
        loopback = parse.find_objects('interface Loop')
        loopback_count = len(loopback)

        # Number of Ipv6 Interfaces
        ipv6_ports = parse.find_parents_w_child('^interface ','ipv6 enable')
        ipv6_ports_count = len(ipv6_ports)
        removeLine(srcFile,"ipv6 enable")

        # Number of Pim Interfaces
        pim_ports = parse.find_parents_w_child('^interface ','ip pim')
        pim_ports_count = len(pim_ports)

        # Number of Ipv6 Pim Interfaces
        pimv6_ports = parse.find_parents_w_child('^interface ','ipv6 pim')
        pimv6_ports_count = len(pimv6_ports)

        # Number of Dot1q SubInterfaces
        dot1q_ports = parse.find_parents_w_child('^interface ','encapsulation dot1q')
        dot1q_ports_count = len(dot1q_ports)

        # Number of Policy Maps
        policy_map = parse.find_objects('policy-map')
        policy_map_count = len(policy_map)

        # Number of Class Maps
        class_map = parse.find_objects('class-map')
        class_map_count = len(class_map)

        # Number of Span Sessions
        span_s = parse.find_objects('monitor session')
        span_count = len(span_s)

        # Number of Acls
        acl = parse.find_objects('ip access-list ')
        acl_count = len(acl)

        # Number of Ipv6 Acls
        v6acl = parse.find_objects('ipv6 access-list ')
        v6acl_count = len(v6acl)

        # Number of Mac Acls
        macacl_l = parse.find_objects('mac access-list ')
        macacl_count = len(macacl_l)

        # Number of Static Routes
        static_route = parse.find_objects('ip route ')
        static_route_count = len(static_route)

        # Number of Bfd Interfaces
        bfd_tim = parse.find_objects('bfd interval ')
        bfd_count = len(bfd_tim)

        # Number of Layer2 EtehrChannel
        l2_po_c = parse.find_parents_w_child('^interface Po','switchport mode')
        l2_po_count = len(l2_po_c)

        # Number of Layer3 EtherChannel
        l3_po_c = parse.find_parents_w_child('^interface Po','no switchport')
        l3_po_count = len(l3_po_c)

        # Number of Ipv6 Interfaces
        ipv6_c = parse.find_parents_w_child('^interface ','ipv6 enable')
        ipv6_count = len(ipv6_c)

        # Number of Qos Ports
        qos_c = parse.find_parents_w_child('^interface ','service-policy')
        qos_count = len(qos_c)

        # Number of Portsec Ports
        psec_c = parse.find_parents_w_child('^interface ','switchport port-sec')
        psec_count = len(psec_c)

        # Number of Dot1x Ports
        dot1x_c = parse.find_parents_w_child('^interface ','source template')
        dot1x_count = len(dot1x_c)

        # Number of Mab Ports
        mab_count = dot1x_count

        # Number of WebAuth Ports
        webauth_count = dot1x_count

        # Number of SVIs
        svi_c = parse.find_parents_wo_child('^interface Vlan','shut')
        svi_count = len(svi_c)

        # Number of VRFs
        vrf_c = parse.find_objects('^vrf definition')
        vrf_count = len(vrf_c)

        # Number of Ospf Processes
        ospf_c = parse.find_objects('^router ospf')
        ospf_count = len(ospf_c)

        # Number of Eigrp Processes
        eigrp_c = parse.find_objects('^router eigrp')
        eigrp_count = len(eigrp_c)

        # Number of Bgp Processes
        bgp_c = parse.find_objects('^router bgp')
        bgp_count = len(bgp_c)

        # Number of Rip Processes
        rip_c = parse.find_objects('^router rip')
        rip_count = len(rip_c)

        # Number of Ospf Peers
        ospf_peer_c = parse.find_parents_w_child('^router ospf','network')
        ospf_peer_count = len(ospf_peer_c)

        # Number of Eigrp Peers
        eigrp_peer_c = parse.find_parents_w_child('^router eigrp','network')
        eigrp_peer_count = len(eigrp_peer_c)

        # Number of Rip Peers
        rip_peer_c = parse.find_parents_w_child('^router rip','network')
        rip_peer_count = len(rip_peer_c)

        # Number of Bgp Peers
        bgp_peer_c = parse.find_parents_w_child('^router bgp','neighbor')
        bgp_peer_count = len(bgp_peer_c)

        # Number of Isis Peers
        isis_peer_c = parse.find_parents_w_child('^router isis','net')
        isis_peer_count = len(isis_peer_c)

        # Number of Flow Monitors
        flow_mon_c = parse.find_objects('^flow moni')
        flow_mon_count = len(flow_mon_c)

        # Number of Flow Recorders
        flow_rec_c = parse.find_objects('^flow rec')
        flow_rec_count = len(flow_rec_c)

        # Number of Flow Exporters
        flow_exp_c = parse.find_objects('^flow exp')
        flow_exp_count = len(flow_exp_c)

        # Extra 12 Jan 22


        csvrow = [cust_id,cust_segment,cust_topologytype,cust_devicepin,cust_mgmtstn,cust_secstation,cust_dnac,
                  techsupport_sw_type,techsupport_uptime,techsupport_cpu,techsupport_memory,techsupport_hastate,
                  techsupport_version,techsupport_sl,techsupport_systemmtu,
                  vtp,cdp,lldp,udld,udldAgg,pagp,lacp,on,l2ec,pvst,rstp,mst,stormBcast,stormMcast,uufb,access,trunk,vlan,errdisableRec,macacl,
                  l3ec,l3if,tunnel,l3dot1q,svi,ospfv4,eigrpv4,ripv4,isis,bgp,static,ipacl,bfdv4,ipv6acl,ospfv6,eigrpv6,bfdv6,
                  portsec,dot1x,mab,webauth,vvlan,ctsSAP,radiusv4,radiusv6,tacac,dhcpSnoop,
                  mcast,mcastv6,igmp,pim,pimv6,mld,msdp,
                  qos,police,mark,shape,fnf,
                  autoconf,template,asp,svl,stack,len_stk,
                  dhcpServer,dns,span,rspan,erspan,http,https,callhome,
                  tftp,ftp,mgmt,archiveLogging,snmpv1,snmpv2,snmpv3,snmp,snmpTrap,syslog,ssh,telnet,
                  mdns,mpls,
                  up_count,access_ports_count,trunk_ports_count,l3_ports_count,up_tunnel_count,loopback_count,
                  ipv6_ports_count,pim_ports_count,pimv6_ports_count,dot1q_ports_count,policy_map_count,class_map_count,span_count,acl_count,v6acl_count,
                  macacl_count,static_route_count,bfd_count,l2_po_count,l3_po_count,ipv6_count,qos_count,psec_count,dot1x_count,mab_count,webauth_count,
                  svi_count,vrf_count,ospf_count,eigrp_count,bgp_count,rip_count,ospf_peer_count,eigrp_peer_count,rip_peer_count,bgp_peer_count,
                  isis_peer_count,flow_mon_count,flow_rec_count,flow_exp_count,mac,
                  policy_autoQos,policy_Copp,policy_ecIngressQos,policy_ecEgressQos,policy_ingressPolicing,policy_egressPolicing,policy_egressShping,policy_WRED,policy_QoSSharing,policy_Inv4Acl,policy_Egressv4Acl,policy_Inv6Acl,policy_Egressv6Acl, policy_v4OGACL, policy_v6OGACL, mpls_ldp, mpls_mplsTE, mpls_vpnv4, mpls_vpnv6, mpls_l2vpn, mpls_6pe, mpls_bgpLU, mpls_mvpn, mpls_ngMvpn, sec_qnq, sec_macsec, l3_bfd, l3_udld, l2_dhcpSnooping, l3_hsrp, mcast_igmpStaticJoin, l3_bfd_template, policy_fnfSGT, policy_fnfV6, sec_ctsSGTMAP, sec_httpLocalAuth, sec_SXP, sec_CoA, sec_accounting, sec_v6RAGuard, prog_netconf, misc_snmp_trap, evpn_evpnEnable, evpn_bgp, evpn_l2vni, evpn_l3vni, evpn_l3trmV4, evpn_l3trmV6, sda_ipv4Overlay, sda_ipv6Overlay, sda_l2Overlay, sda_multicast, sda_controlPlane
                 ]

        # Write Config File entries as rows into '.csv' file
        ciscowriter.writerow(csvrow)
        print("END")
        myShuffle(csvrow,60)
except:
    print("An exception occurred")

csvfile.close()
print('Total No. of Cfg Files Available in Path : {}'.format(len(fileList)))

####

####
###Train ML model and get custType fill it in csv and populate db
from sklearn.ensemble import RandomForestClassifier
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestRegressor
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.feature_selection import SelectKBest
from sklearn.feature_selection import chi2
from sklearn.feature_selection import SelectKBest
from sklearn.feature_selection import chi2
from sklearn.feature_selection import f_classif

#import sklearn.external.joblib as extjoblib
import joblib
#from sklearn.externals import joblib
# tempfile = "/home/bjatti/configCompareTool/project/custConfs/cfgFiles/test/temp.csv"
print("tempfile 1700",tempfile)
df_query = pd.read_csv(tempfile)
print(" 1702",df_query)
try:
    query = df_query.drop(['cust_id','cust_segment','cust_topologytype','cust_mgmtstn','cust_secstation','cust_dnac','techsupport_sw_type','techsupport_uptime','techsupport_cpu','techsupport_memory','techsupport_hastate','techsupport_version','techsupport_sl','techsupport_systemmtu'],axis=1)
except Exception as e:
    print(e)
print(" 1704", query)
classifier = joblib.load('./src/utils/pythonscript/rfc.pkl')
print(" 1706", classifier)
try:
    predict = classifier.predict(query)
except Exception as e:
    print(e)
print('++++++++1705')
print("1709",query)
print("1710",predict)
##write to csv
f = open(tempfile,'r')
reader = csv.reader(f)
mylist = list(reader)
f.close()
mylist[1][1]=predict[0]
my_new_list = open(tempfile,'w')
csv_writer = csv.writer(my_new_list)
csv_writer.writerows(mylist)
my_new_list.close()

#####
# tempfile = "/home/bjatti/configCompareTool/project/custConfs/cfgFiles/test/temp.csv"
import pandas as pd
df = pd.read_csv(tempfile)
f = open(tempfile,'r')
reader = csv.reader(f)
#reader = csv.DictReader(f)
mylist = list(reader)
f.close()
csvRowsCount = len(mylist)
print("1729",csvRowsCount)
try:
    for i in range(csvRowsCount-1):
        #df.loc[i,'ML Learnt'] = 0
        #1-retail 2-govt 3-healthcare 4-nge 5-education 6-finance
        if df.loc[i,'cust_segment'] == 1:
            print('cust_segment is retail')
            df=updateWt(df,1,i)
        if df.loc[i,'cust_segment'] == 2:
            df=updateWt(df,2,i)
            print('cust_segment is govt')
        if df.loc[i,'cust_segment'] == 3:
            df=updateWt(df,3,i)
            print('cust_segment is health')
        if df.loc[i,'cust_segment'] == 4:
            df=updateWt(df,4,i)
            print('cust_segment is nge')
        if df.loc[i,'cust_segment'] == 5:
            df=updateWt(df,5,i)
            print('cust_segment is education')
        if df.loc[i,'cust_segment'] == 6:
            df=updateWt(df,6,i)
            print('cust_segment is finance')
        if df.loc[i,'cust_segment'] == 7:
            df=updateWt(df,7,i)
            print('cust_segment is pe')
        if df.loc[i,'cust_segment'] == 8:
            df=updateWt(df,8,i)
            print('cust_segment is ngevpn')
        if df.loc[i,'cust_segment'] == 9:
            df=updateWt(df,9,i)
            print('cust_segment is sda')
        print('in MAIN')
        print(df.loc[i,'retailwt'],df.loc[i,'govtwt'],df.loc[i,'healthwt'],df.loc[i,'ngewt'],df.loc[i,'educationwt'],df.loc[i,'financewt'],df.loc[i,'pewt'],df.loc[i,'ngevpnwt'],df.loc[i,'sdawt'])
except Exception as e:
    print(e)

print("1763")
try:
    df.to_csv(tempfile, index=False)
except Exception as e:
    print(e)
print('1765 df',df)
#####
df = pd.read_csv(tempfile, sep=',', encoding='utf8')
print(tempfile)
print('df',df)
# df = pd.read_csv('/home/bjatti/configCompareTool/project/custConfs/cfgFiles/test/temp.csv', sep=',', encoding='utf8')
df.to_sql('customerData', con=engine, index=False, if_exists='append')
result = lib.customersData()
