import mysql.connector
from mysql.connector import Error


class customersData():

    def __init__(self):
        self.uniqCusIdList    = []
        self.l2FeatureList    = {}
        self.l3FeatureList    = {}
        self.secFeatureList   = {}        
        self.mcastFeatureList = {}   
        self.polFeatureList   = {} 
        self.platFeatureList  = {}     
        self.servFeatureList  = {}             
        self.mgmtFeatureList  = {}    
        self.pgmFeatureList   = {} 
        self.mplsFeatureList  = {}  
        self.allFeaturesList  = {}        
        
        self.sitIntProfList                 = ['finance','education','retail','healthcare','government','NGE']
        
        self.l2_cust_fin_comp_list          = {}
        self.l3_cust_fin_comp_list          = {}
        self.sec_cust_fin_comp_list         = {}
        self.mcast_cust_fin_comp_list       = {}
        self.pol_cust_fin_comp_list         = {}
        self.plat_cust_fin_comp_list        = {}
        self.serv_cust_fin_comp_list        = {}
        self.mgmt_cust_fin_comp_list        = {}
        self.pgm_cust_fin_comp_list         = {}
        self.mpls_cust_fin_comp_list        = {}
        self.tot_cust_fin_comp_list         = {} 
        self.cust_fin_feat_per_cov_list     = {}
        self.cust_fin_feat_per_not_cov_list = {}

        self.l2_cust_edu_comp_list          = {}
        self.l3_cust_edu_comp_list          = {}
        self.sec_cust_edu_comp_list         = {}
        self.mcast_cust_edu_comp_list       = {}
        self.pol_cust_edu_comp_list         = {}
        self.plat_cust_edu_comp_list        = {}
        self.serv_cust_edu_comp_list        = {}
        self.mgmt_cust_edu_comp_list        = {}
        self.pgm_cust_edu_comp_list         = {}
        self.mpls_cust_edu_comp_list        = {}
        self.tot_cust_edu_comp_list         = {} 
        self.cust_edu_feat_per_cov_list     = {}
        self.cust_edu_feat_per_not_cov_list = {}
		
        self.l2_cust_ret_comp_list          = {}
        self.l3_cust_ret_comp_list          = {}
        self.sec_cust_ret_comp_list         = {}
        self.mcast_cust_ret_comp_list       = {}
        self.pol_cust_ret_comp_list         = {}
        self.plat_cust_ret_comp_list        = {}
        self.serv_cust_ret_comp_list        = {}
        self.mgmt_cust_ret_comp_list        = {}
        self.pgm_cust_ret_comp_list         = {}
        self.mpls_cust_ret_comp_list        = {}
        self.tot_cust_ret_comp_list         = {} 
        self.cust_ret_feat_per_cov_list     = {}
        self.cust_ret_feat_per_not_cov_list = {}

        self.l2_cust_hc_comp_list           = {}
        self.l3_cust_hc_comp_list           = {}
        self.sec_cust_hc_comp_list          = {}
        self.mcast_cust_hc_comp_list        = {}
        self.pol_cust_hc_comp_list          = {}
        self.plat_cust_hc_comp_list         = {}
        self.serv_cust_hc_comp_list         = {}
        self.mgmt_cust_hc_comp_list         = {}
        self.pgm_cust_hc_comp_list          = {}
        self.mpls_cust_hc_comp_list         = {}
        self.tot_cust_hc_comp_list          = {} 
        self.cust_hc_feat_per_cov_list      = {}
        self.cust_hc_feat_per_not_cov_list  = {}

        self.l2_cust_gov_comp_list          = {}
        self.l3_cust_gov_comp_list          = {}
        self.sec_cust_gov_comp_list         = {}
        self.mcast_cust_gov_comp_list       = {}
        self.pol_cust_gov_comp_list         = {}
        self.plat_cust_gov_comp_list        = {}
        self.serv_cust_gov_comp_list        = {}
        self.mgmt_cust_gov_comp_list        = {}
        self.pgm_cust_gov_comp_list         = {}
        self.mpls_cust_gov_comp_list        = {}
        self.tot_cust_gov_comp_list         = {} 
        self.cust_gov_feat_per_cov_list     = {}
        self.cust_gov_feat_per_not_cov_list = {}

        self.l2_cust_nge_comp_list          = {}
        self.l3_cust_nge_comp_list          = {}
        self.sec_cust_nge_comp_list         = {}
        self.mcast_cust_nge_comp_list       = {}
        self.pol_cust_nge_comp_list         = {}
        self.plat_cust_nge_comp_list        = {}
        self.serv_cust_nge_comp_list        = {}
        self.mgmt_cust_nge_comp_list        = {}
        self.pgm_cust_nge_comp_list         = {}
        self.mpls_cust_nge_comp_list        = {}
        self.tot_cust_nge_comp_list         = {}         
        self.cust_nge_feat_per_cov_list     = {}
        self.cust_nge_feat_per_not_cov_list = {}
     
    def uniqCustList(self):
        try:
            connection = mysql.connector.connect(host     = 'localhost',
                                                 database = 'custConfigDB',
                                                 user     = 'bjatti',
                                                 password = 'Maglev123!')
        
            cursor = connection.cursor()
            cursor.execute('select cust_id from customerData')  
            cusIdList = cursor.fetchall()
            
            for custId in cusIdList:
                if custId not in self.uniqCusIdList:
                    self.uniqCusIdList.append(custId)            
        except Error as e:
            print("Error while connecting to MySQL", e)
        finally:
            return self.uniqCusIdList
            if connection.is_connected():
                cursor.close()
                connection.close()
    
    def layer2List(self):            
        try:
            self.uniqCustList()
            
            connection = mysql.connector.connect(host     = 'localhost',
                                                 database = 'custConfigDB',
                                                 user     = 'bjatti',
                                                 password = 'Maglev123!')
            
            cursor = connection.cursor()
            
            # Display table     
            for custid in self.uniqCusIdList:                              
                query = """
                        select cust_id,l2_vtp,l2_cdp,l2_lldp,l2_udld,l2_udldAgg,l2_pagp,l2_lacp,\
                        l2_on,l2_l2ec,l2_pvst,l2_rstp,l2_mst,l2_stormBcast,l2_stormMcast,l2_uufb,l2_access,\
                        l2_trunk,l2_vlan,l2_errdisableRec,l2_macacl from customerData where cust_id = %s
                        """
                cursor.execute(query,custid)        
                data = cursor.fetchall()  
                
                for line in data:
                    for val in range(0,len(line)):
                        if str(line[0]) not in self.l2FeatureList:
                            self.l2FeatureList[str(line[0])] = []
                        if line[1] == '1':
                            if 'vtp' not in self.l2FeatureList[str(line[0])]:                    
                                self.l2FeatureList[str(line[0])].append('vtp')
                        if line[2] == '1':
                            if 'cdp' not in self.l2FeatureList[str(line[0])]:
                                self.l2FeatureList[str(line[0])].append('cdp')
                        if line[3] == '1':
                            if 'lldp' not in self.l2FeatureList[str(line[0])]:
                                self.l2FeatureList[str(line[0])].append('lldp')
                        if line[4] == '1':
                            if 'udld' not in self.l2FeatureList[str(line[0])]:
                                self.l2FeatureList[str(line[0])].append('udld')
                        if line[5] == '1':
                            if 'udldAgg' not in self.l2FeatureList[str(line[0])]:
                                self.l2FeatureList[str(line[0])].append('udldAgg')
                        if line[6] == '1':
                            if 'pagp' not in self.l2FeatureList[str(line[0])]:
                                self.l2FeatureList[str(line[0])].append('pagp')
                        if line[7] == '1':
                            if 'lacp' not in self.l2FeatureList[str(line[0])]:
                                self.l2FeatureList[str(line[0])].append('lacp')
                        if line[8] == '1':
                            if 'on' not in self.l2FeatureList[str(line[0])]:
                                self.l2FeatureList[str(line[0])].append('on')
                        if line[9] == '1':
                            if 'l2ec' not in self.l2FeatureList[str(line[0])]:
                                self.l2FeatureList[str(line[0])].append('l2ec')
                        if line[10] == '1':
                            if 'pvst' not in self.l2FeatureList[str(line[0])]:
                                self.l2FeatureList[str(line[0])].append('pvst')
                        if line[11] == '1':
                            if 'rstp' not in self.l2FeatureList[str(line[0])]:
                                self.l2FeatureList[str(line[0])].append('rstp')
                        if line[12] == '1':
                            if 'mst' not in self.l2FeatureList[str(line[0])]:
                                self.l2FeatureList[str(line[0])].append('mst')
                        if line[13] == '1':
                            if 'stormBcast' not in self.l2FeatureList[str(line[0])]:
                                self.l2FeatureList[str(line[0])].append('stormBcast')
                        if line[14] == '1':
                            if 'stormMcast' not in self.l2FeatureList[str(line[0])]:
                                self.l2FeatureList[str(line[0])].append('stormMcast')
                        if line[15] == '1':
                            if 'uufb' not in self.l2FeatureList[str(line[0])]:
                                self.l2FeatureList[str(line[0])].append('uufb')
                        if line[16] == '1':
                            if 'access' not in self.l2FeatureList[str(line[0])]:
                                self.l2FeatureList[str(line[0])].append('access')                                
                        if line[17] == '1':
                            if 'trunk' not in self.l2FeatureList[str(line[0])]:
                                self.l2FeatureList[str(line[0])].append('trunk')                        
                        if line[18] == '1':
                            if 'vlan' not in self.l2FeatureList[str(line[0])]:
                                self.l2FeatureList[str(line[0])].append('vlan')
                        if line[19] == '1':
                            if 'errdisableRec' not in self.l2FeatureList[str(line[0])]:
                                self.l2FeatureList[str(line[0])].append('errdisableRec')
                        if line[20] == '1':
                            if 'macacl' not in self.l2FeatureList[str(line[0])]:
                                self.l2FeatureList[str(line[0])].append('macacl')                            
        except Error as e:
            print("Error while connecting to MySQL", e)
        finally:
            return self.l2FeatureList
            if connection.is_connected():
                cursor.close()
                connection.close()

    def layer3List(self):                
        try:
            self.uniqCustList()
            
            connection = mysql.connector.connect(host     = 'localhost',
                                                 database = 'custConfigDB',
                                                 user     = 'bjatti',
                                                 password = 'Maglev123!')
        
            cursor = connection.cursor()

            for custid in self.uniqCusIdList:                              
                query = """
                        select cust_id,l3v4_l3ec,l3v4_l3if,l3v4_tunnel,l3v4_l3dot1q,l3v4_svi,l3v4_ospfv4,\
                        l3v4_eigrpv4,l3v4_ripv4,l3v4_isis,l3v4_bgp,l3v4_static,l3v4_ipacl,l3v4_bfdv4,l3v6_ipv6acl,\
                        l3v6_ospfv6,l3v6_eigrpv6,l3v6_bfdv6 from customerData where cust_id = %s
                        """
                cursor.execute(query,custid)        
                data = cursor.fetchall()
                  
                for line in data:
                    for val in range(0,len(line)):
                        if str(line[0]) not in self.l3FeatureList:
                            self.l3FeatureList[str(line[0])] = []
                        if line[1] == '1':
                            if 'l3ec' not in self.l3FeatureList[str(line[0])]:                    
                                self.l3FeatureList[str(line[0])].append('l3ec')
                        if line[2] == '1':
                            if 'l3if' not in self.l3FeatureList[str(line[0])]:
                                self.l3FeatureList[str(line[0])].append('l3if')
                        if line[3] == '1':
                            if 'tunnel' not in self.l3FeatureList[str(line[0])]:
                                self.l3FeatureList[str(line[0])].append('tunnel')
                        if line[4] == '1':
                            if 'l3dot1q' not in self.l3FeatureList[str(line[0])]:
                                self.l3FeatureList[str(line[0])].append('l3dot1q')
                        if line[5] == '1':
                            if 'svi' not in self.l3FeatureList[str(line[0])]:
                                self.l3FeatureList[str(line[0])].append('svi')
                        if line[6] == '1':
                            if 'ospfv4' not in self.l3FeatureList[str(line[0])]:
                                self.l3FeatureList[str(line[0])].append('ospfv4')
                        if line[7] == '1':
                            if 'eigrpv4' not in self.l3FeatureList[str(line[0])]:
                                self.l3FeatureList[str(line[0])].append('eigrpv4')
                        if line[8] == '1':
                            if 'ripv4' not in self.l3FeatureList[str(line[0])]:
                                self.l3FeatureList[str(line[0])].append('ripv4')
                        if line[9] == '1':
                            if 'isis' not in self.l3FeatureList[str(line[0])]:
                                self.l3FeatureList[str(line[0])].append('isis')
                        if line[10] == '1':
                            if 'bgp' not in self.l3FeatureList[str(line[0])]:
                                self.l3FeatureList[str(line[0])].append('bgp')
                        if line[11] == '1':
                            if 'static' not in self.l3FeatureList[str(line[0])]:
                                self.l3FeatureList[str(line[0])].append('static')
                        if line[12] == '1':
                            if 'ipacl' not in self.l3FeatureList[str(line[0])]:
                                self.l3FeatureList[str(line[0])].append('ipacl')
                        if line[13] == '1':
                            if 'bfdv4' not in self.l3FeatureList[str(line[0])]:
                                self.l3FeatureList[str(line[0])].append('bfdv4')
                        if line[14] == '1':
                            if 'ipv6acl' not in self.l3FeatureList[str(line[0])]:
                                self.l3FeatureList[str(line[0])].append('ipv6acl')
                        if line[15] == '1':
                            if 'ospfv6' not in self.l3FeatureList[str(line[0])]:
                                self.l3FeatureList[str(line[0])].append('ospfv6')
                        if line[16] == '1':
                            if 'eigrpv6' not in self.l3FeatureList[str(line[0])]:
                                self.l3FeatureList[str(line[0])].append('eigrpv6')                                
                        if line[17] == '1':
                            if 'bfdv6' not in self.l3FeatureList[str(line[0])]:
                                self.l3FeatureList[str(line[0])].append('bfdv6')            
        except Error as e:
            print("Error while connecting to MySQL", e)            
        finally:
            return self.l3FeatureList
            if connection.is_connected():
                cursor.close()
                connection.close()

    def securityList(self):                
        try:
            self.uniqCustList()
            
            connection = mysql.connector.connect(host     = 'localhost',
                                                 database = 'custConfigDB',
                                                 user     = 'bjatti',
                                                 password = 'Maglev123!')
        
            cursor = connection.cursor()

            for custid in self.uniqCusIdList:                              
                query = """
                        select cust_id,sec_portsec,sec_dot1x,sec_mab,sec_webauth,sec_vvlan,sec_ctsSAP,\
                        sec_radiusv4,sec_radiusv6,sec_tacac,sec_dhcpSnoop from customerData where cust_id = %s
                        """
                cursor.execute(query,custid)        
                data = cursor.fetchall()
                  
                for line in data:
                    for val in range(0,len(line)):
                        if str(line[0]) not in self.secFeatureList:
                            self.secFeatureList[str(line[0])] = []
                        if line[1] == '1':
                            if 'portsec' not in self.secFeatureList[str(line[0])]:                    
                                self.secFeatureList[str(line[0])].append('portsec')
                        if line[2] == '1':
                            if 'dot1x' not in self.secFeatureList[str(line[0])]:
                                self.secFeatureList[str(line[0])].append('dot1x')
                        if line[3] == '1':
                            if 'mab' not in self.secFeatureList[str(line[0])]:
                                self.secFeatureList[str(line[0])].append('mab')
                        if line[4] == '1':
                            if 'webauth' not in self.secFeatureList[str(line[0])]:
                                self.secFeatureList[str(line[0])].append('webauth')
                        if line[5] == '1':
                            if 'vvlan' not in self.secFeatureList[str(line[0])]:
                                self.secFeatureList[str(line[0])].append('vvlan')
                        if line[6] == '1':
                            if 'ctsSAP' not in self.secFeatureList[str(line[0])]:
                                self.secFeatureList[str(line[0])].append('ctsSAP')
                        if line[7] == '1':
                            if 'radiusv4' not in self.secFeatureList[str(line[0])]:
                                self.secFeatureList[str(line[0])].append('radiusv4')
                        if line[8] == '1':
                            if 'radiusv6' not in self.secFeatureList[str(line[0])]:
                                self.secFeatureList[str(line[0])].append('radiusv6')
                        if line[9] == '1':
                            if 'tacac' not in self.secFeatureList[str(line[0])]:
                                self.secFeatureList[str(line[0])].append('tacac')
                        if line[10] == '1':
                            if 'dhcpSnoop' not in self.secFeatureList[str(line[0])]:
                                self.secFeatureList[str(line[0])].append('dhcpSnoop')            
        except Error as e:
            print("Error while connecting to MySQL", e)            
        finally:
            return self.secFeatureList
            if connection.is_connected():
                cursor.close()
                connection.close()

    def multicastList(self):                
        try:
            self.uniqCustList()
            
            connection = mysql.connector.connect(host     = 'localhost',
                                                 database = 'custConfigDB',
                                                 user     = 'bjatti',
                                                 password = 'Maglev123!')
        
            cursor = connection.cursor()

            for custid in self.uniqCusIdList:                              
                query = """
                        select cust_id,mcast_mcast,mcast_mcastv6,mcast_igmp,mcast_pim,\
                        mcast_pimv6,mcast_mld,mcast_msdp from customerData where cust_id = %s
                        """
                cursor.execute(query,custid)        
                data = cursor.fetchall()
                  
                for line in data:
                    for val in range(0,len(line)):
                        if str(line[0]) not in self.mcastFeatureList:
                            self.mcastFeatureList[str(line[0])] = []
                        if line[1] == '1':
                            if 'mcast' not in self.mcastFeatureList[str(line[0])]:                    
                                self.mcastFeatureList[str(line[0])].append('mcast')
                        if line[2] == '1':
                            if 'mcastv6' not in self.mcastFeatureList[str(line[0])]:
                                self.mcastFeatureList[str(line[0])].append('mcastv6')
                        if line[3] == '1':
                            if 'igmp' not in self.mcastFeatureList[str(line[0])]:
                                self.mcastFeatureList[str(line[0])].append('igmp')
                        if line[4] == '1':
                            if 'pim' not in self.mcastFeatureList[str(line[0])]:
                                self.mcastFeatureList[str(line[0])].append('pim')
                        if line[5] == '1':
                            if 'pimv6' not in self.mcastFeatureList[str(line[0])]:
                                self.mcastFeatureList[str(line[0])].append('pimv6')
                        if line[6] == '1':
                            if 'mld' not in self.mcastFeatureList[str(line[0])]:
                                self.mcastFeatureList[str(line[0])].append('mld')
                        if line[7] == '1':
                            if 'msdp' not in self.mcastFeatureList[str(line[0])]:
                                self.mcastFeatureList[str(line[0])].append('msdp')
        except Error as e:
            print("Error while connecting to MySQL", e)            
        finally:
            return self.mcastFeatureList
            if connection.is_connected():
                cursor.close()
                connection.close()                

    def policyList(self):                
        try:
            self.uniqCustList()
            
            connection = mysql.connector.connect(host     = 'localhost',
                                                 database = 'custConfigDB',
                                                 user     = 'bjatti',
                                                 password = 'Maglev123!')
        
            cursor = connection.cursor()

            for custid in self.uniqCusIdList:                              
                query = """
                        select cust_id,policy_qos,policy_police,policy_mark,policy_shape,\
                        policy_fnf from customerData where cust_id = %s
                        """
                cursor.execute(query,custid)        
                data = cursor.fetchall()
                  
                for line in data:
                    for val in range(0,len(line)):
                        if str(line[0]) not in self.polFeatureList:
                            self.polFeatureList[str(line[0])] = []
                        if line[1] == '1':
                            if 'qos' not in self.polFeatureList[str(line[0])]:                    
                                self.polFeatureList[str(line[0])].append('qos')
                        if line[2] == '1':
                            if 'police' not in self.polFeatureList[str(line[0])]:
                                self.polFeatureList[str(line[0])].append('police')
                        if line[3] == '1':
                            if 'mark' not in self.polFeatureList[str(line[0])]:
                                self.polFeatureList[str(line[0])].append('mark')
                        if line[4] == '1':
                            if 'shape' not in self.polFeatureList[str(line[0])]:
                                self.polFeatureList[str(line[0])].append('shape')
                        if line[5] == '1':
                            if 'fnf' not in self.polFeatureList[str(line[0])]:
                                self.polFeatureList[str(line[0])].append('fnf')
        except Error as e:
            print("Error while connecting to MySQL", e)            
        finally:
            return self.polFeatureList
            if connection.is_connected():
                cursor.close()
                connection.close()                                

    def platformList(self):                
        try:
            self.uniqCustList()
            
            connection = mysql.connector.connect(host     = 'localhost',
                                                 database = 'custConfigDB',
                                                 user     = 'bjatti',
                                                 password = 'Maglev123!')
        
            cursor = connection.cursor()

            for custid in self.uniqCusIdList:                              
                query = """
                        select cust_id,platform_autoconf,platform_template,platform_asp,\
                        platform_svl,platform_stack,platform_len_stk from customerData where cust_id = %s
                        """
                cursor.execute(query,custid)        
                data = cursor.fetchall()
                  
                for line in data:
                    for val in range(0,len(line)):
                        if str(line[0]) not in self.platFeatureList:
                            self.platFeatureList[str(line[0])] = []
                        if line[1] == '1':
                            if 'autoconf' not in self.platFeatureList[str(line[0])]:                    
                                self.platFeatureList[str(line[0])].append('autoconf')
                        if line[2] == '1':
                            if 'template' not in self.platFeatureList[str(line[0])]:
                                self.platFeatureList[str(line[0])].append('template')
                        if line[3] == '1':
                            if 'asp' not in self.platFeatureList[str(line[0])]:
                                self.platFeatureList[str(line[0])].append('asp')
                        if line[4] == '1':
                            if 'svl' not in self.platFeatureList[str(line[0])]:
                                self.platFeatureList[str(line[0])].append('svl')
                        if line[5] == '1':
                            if 'stack' not in self.platFeatureList[str(line[0])]:
                                self.platFeatureList[str(line[0])].append('stack')
                        if line[6] > '0':
                            if 'stackLen' not in self.platFeatureList[str(line[0])]:
                                self.platFeatureList[str(line[0])].append('stackLen')
        except Error as e:
            print("Error while connecting to MySQL", e)            
        finally:
            return self.platFeatureList
            if connection.is_connected():
                cursor.close()
                connection.close()                

    def serviceList(self):                
        try:
            self.uniqCustList()
            
            connection = mysql.connector.connect(host     = 'localhost',
                                                 database = 'custConfigDB',
                                                 user     = 'bjatti',
                                                 password = 'Maglev123!')
        
            cursor = connection.cursor()

            for custid in self.uniqCusIdList:                              
                query = """
                        select cust_id,service_dhcpServer,service_dns,service_span,service_rspan,\
                        service_erspan,service_http,service_https,service_callhome from customerData where cust_id = %s
                        """
                cursor.execute(query,custid)        
                data = cursor.fetchall()
                  
                for line in data:
                    for val in range(0,len(line)):
                        if str(line[0]) not in self.servFeatureList:
                            self.servFeatureList[str(line[0])] = []
                        if line[1] == '1':
                            if 'dhcpServer' not in self.servFeatureList[str(line[0])]:                    
                                self.servFeatureList[str(line[0])].append('dhcpServer')
                        if line[2] == '1':
                            if 'dns' not in self.servFeatureList[str(line[0])]:
                                self.servFeatureList[str(line[0])].append('dns')
                        if line[3] == '1':
                            if 'span' not in self.servFeatureList[str(line[0])]:
                                self.servFeatureList[str(line[0])].append('span')
                        if line[4] == '1':
                            if 'rspan' not in self.servFeatureList[str(line[0])]:
                                self.servFeatureList[str(line[0])].append('rspan')
                        if line[5] == '1':
                            if 'erspan' not in self.servFeatureList[str(line[0])]:
                                self.servFeatureList[str(line[0])].append('erspan')
                        if line[6] == '1':
                            if 'http' not in self.servFeatureList[str(line[0])]:
                                self.servFeatureList[str(line[0])].append('http')
                        if line[7] == '1':
                            if 'https' not in self.servFeatureList[str(line[0])]:
                                self.servFeatureList[str(line[0])].append('https')
                        if line[8] == '1':
                            if 'callhome' not in self.servFeatureList[str(line[0])]:
                                self.servFeatureList[str(line[0])].append('callhome')                                
        except Error as e:
            print("Error while connecting to MySQL", e)            
        finally:
            return self.servFeatureList
            if connection.is_connected():
                cursor.close()
                connection.close()                 

    def managementList(self):                
        try:
            self.uniqCustList()
            
            connection = mysql.connector.connect(host     = 'localhost',
                                                 database = 'custConfigDB',
                                                 user     = 'bjatti',
                                                 password = 'Maglev123!')
        
            cursor = connection.cursor()

            for custid in self.uniqCusIdList:                              
                query = """
                        select cust_id,mgmt_tftp,mgmt_ftp,mgmt_mgmt,mgmt_archiveLogging,mgmt_snmpv1,\
                        mgmt_snmpv2,mgmt_snmpv3,mgmt_snmp,mgmt_snmpTrap,mgmt_syslog,mgmt_ssh,\
                        mgmt_telnet from customerData where cust_id = %s
                        """
                cursor.execute(query,custid)        
                data = cursor.fetchall()
                  
                for line in data:
                    for val in range(0,len(line)):
                        if str(line[0]) not in self.mgmtFeatureList:
                            self.mgmtFeatureList[str(line[0])] = []
                        if line[1] == '1':
                            if 'tftp' not in self.mgmtFeatureList[str(line[0])]:                    
                                self.mgmtFeatureList[str(line[0])].append('tftp')
                        if line[2] == '1':
                            if 'ftp' not in self.mgmtFeatureList[str(line[0])]:
                                self.mgmtFeatureList[str(line[0])].append('ftp')
                        if line[3] == '1':
                            if 'mgmt' not in self.mgmtFeatureList[str(line[0])]:
                                self.mgmtFeatureList[str(line[0])].append('mgmt')
                        if line[4] == '1':
                            if 'archiveLogging' not in self.mgmtFeatureList[str(line[0])]:
                                self.mgmtFeatureList[str(line[0])].append('archiveLogging')
                        if line[5] == '1':
                            if 'snmpv1' not in self.mgmtFeatureList[str(line[0])]:
                                self.mgmtFeatureList[str(line[0])].append('snmpv1')
                        if line[6] == '1':
                            if 'snmpv2' not in self.mgmtFeatureList[str(line[0])]:
                                self.mgmtFeatureList[str(line[0])].append('snmpv2')
                        if line[7] == '1':
                            if 'snmpv3' not in self.mgmtFeatureList[str(line[0])]:
                                self.mgmtFeatureList[str(line[0])].append('snmpv3')
                        if line[8] == '1':
                            if 'snmp' not in self.mgmtFeatureList[str(line[0])]:
                                self.mgmtFeatureList[str(line[0])].append('snmp')
                        if line[9] == '1':
                            if 'snmpTrap' not in self.mgmtFeatureList[str(line[0])]:
                                self.mgmtFeatureList[str(line[0])].append('snmpTrap')
                        if line[10] == '1':
                            if 'syslog' not in self.mgmtFeatureList[str(line[0])]:
                                self.mgmtFeatureList[str(line[0])].append('syslog')
                        if line[11] == '1':
                            if 'ssh' not in self.mgmtFeatureList[str(line[0])]:
                                self.mgmtFeatureList[str(line[0])].append('ssh')
                        if line[12] == '1':
                            if 'telnet' not in self.mgmtFeatureList[str(line[0])]:
                                self.mgmtFeatureList[str(line[0])].append('telnet')     
        except Error as e:
            print("Error while connecting to MySQL", e)            
        finally:
            return self.mgmtFeatureList
            if connection.is_connected():
                cursor.close()
                connection.close()

    def programList(self):                
        try:
            self.uniqCustList()
            
            connection = mysql.connector.connect(host     = 'localhost',
                                                 database = 'custConfigDB',
                                                 user     = 'bjatti',
                                                 password = 'Maglev123!')
        
            cursor = connection.cursor()

            for custid in self.uniqCusIdList:                              
                query = """
                        select cust_id,prog_mdns from customerData where cust_id = %s
                        """
                cursor.execute(query,custid)        
                data = cursor.fetchall()
                  
                for line in data:
                    for val in range(0,len(line)):
                        if str(line[0]) not in self.pgmFeatureList:
                            self.pgmFeatureList[str(line[0])] = []
                        if line[1] == '1':
                            if 'mdns' not in self.pgmFeatureList[str(line[0])]:                    
                                self.pgmFeatureList[str(line[0])].append('mdns')    
        except Error as e:
            print("Error while connecting to MySQL", e)            
        finally:
            return self.pgmFeatureList
            if connection.is_connected():
                cursor.close()
                connection.close()    

    def mplsList(self):                
        try:
            self.uniqCustList()
            
            connection = mysql.connector.connect(host     = 'localhost',
                                                 database = 'custConfigDB',
                                                 user     = 'bjatti',
                                                 password = 'Maglev123!')
        
            cursor = connection.cursor()

            for custid in self.uniqCusIdList:                              
                query = """
                        select cust_id,mpls_mpls from customerData where cust_id = %s
                        """
                cursor.execute(query,custid)        
                data = cursor.fetchall()
                  
                for line in data:
                    for val in range(0,len(line)):
                        if str(line[0]) not in self.mplsFeatureList:
                            self.mplsFeatureList[str(line[0])] = []
                        if line[1] == '1':
                            if 'mpls' not in self.mplsFeatureList[str(line[0])]:                    
                                self.mplsFeatureList[str(line[0])].append('mpls')    
        except Error as e:
            print("Error while connecting to MySQL", e)            
        finally:
            return self.mplsFeatureList
            if connection.is_connected():
                cursor.close()
                connection.close()  

    def uniqCustFeaturesList(self):
        try:
            self.layer2List()
            self.layer3List()
            self.securityList()
            self.multicastList()
            self.policyList()
            self.platformList()
            self.serviceList()
            self.managementList()
            self.programList()
            self.mplsList()        
            
            for cid in self.uniqCusIdList:
                self.allFeaturesList[cid[0]] = []       
                for val in self.l2FeatureList[cid[0]]:	
                    self.allFeaturesList[cid[0]].append(val)
                for val in self.l3FeatureList[cid[0]]:		
                    self.allFeaturesList[cid[0]].append(val)
                for val in self.secFeatureList[cid[0]]:		
                    self.allFeaturesList[cid[0]].append(val)
                for val in self.mcastFeatureList[cid[0]]:		
                    self.allFeaturesList[cid[0]].append(val)
                for val in self.polFeatureList[cid[0]]:		
                    self.allFeaturesList[cid[0]].append(val)
                for val in self.platFeatureList[cid[0]]:		
                    self.allFeaturesList[cid[0]].append(val)
                for val in self.servFeatureList[cid[0]]:		
                    self.allFeaturesList[cid[0]].append(val)
                for val in self.mgmtFeatureList[cid[0]]:		
                    self.allFeaturesList[cid[0]].append(val)
                for val in self.pgmFeatureList[cid[0]]:		
                    self.allFeaturesList[cid[0]].append(val)
                for val in self.mplsFeatureList[cid[0]]:		
                    self.allFeaturesList[cid[0]].append(val)
        except Error as e:
            print("Error while connecting to MySQL", e)
        finally:
            return self.allFeaturesList                

    def insertUniqCustFeaturesRecords(self):
        try:
            recCnt = 0 
            self.uniqCustFeaturesList()
            
            connection = mysql.connector.connect(host     = 'localhost',
                                                 database = 'custConfigDB',
                                                 user     = 'bjatti',
                                                 password = 'Maglev123!')
            
            cursor = connection.cursor()
            
            # Insert Records into table     
            for cid in self.uniqCusIdList:                          
                custid = cid[0]  
                alFeat = ','.join(self.allFeaturesList[custid])
                l2Feat = ','.join(self.l2FeatureList[custid])
                l3Feat = ','.join(self.l3FeatureList[custid])
                secFea = ','.join(self.secFeatureList[custid])
                mulFea = ','.join(self.mcastFeatureList[custid])
                polFea = ','.join(self.polFeatureList[custid])
                pltFea = ','.join(self.platFeatureList[custid])
                srvFea = ','.join(self.servFeatureList[custid])
                mgtFea = ','.join(self.mgmtFeatureList[custid])
                pgmFea = ','.join(self.pgmFeatureList[custid])
                mplFea = ','.join(self.mplsFeatureList[custid]) 
                
                query  = """
                         insert into uniqCustData (cust_id,featuresList,layer2,layer3,security,\
                         multicast,policy,platform,services,management,program,mpls) values \
                         (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s);
                         """ 
            
                cursor.execute(query,(custid,alFeat,l2Feat,l3Feat,secFea,mulFea,polFea,pltFea,srvFea,mgtFea,pgmFea,mplFea))                           
                                           
                recCnt += 1                               
            
            # Commit the table after insert rows
            connection.commit()                                  
        except Error as e:
            print("Error while connecting to MySQL", e)
        finally:
            return recCnt
            if connection.is_connected():
                cursor.close()
                connection.close()

    def L2_Cust_Fin_CompList(self):
        try:
            self.layer2List()    
                
            for cid in self.uniqCusIdList:
                if cid[0] not in self.sitIntProfList:
                    self.l2_cust_fin_comp_list[cid[0]] = []             
                    for val in self.l2FeatureList[cid[0]]:	
                        if val not in self.l2FeatureList['finance']:
                            self.l2_cust_fin_comp_list[cid[0]].append(val)
                                
        except Error as e:
            print("Error while connecting to MySQL", e)
        finally:
            return self.l2_cust_fin_comp_list

    def L3_Cust_Fin_CompList(self):
        try:
            self.layer3List()    
            
            for cid in self.uniqCusIdList:
                if cid[0] not in self.sitIntProfList:
                    self.l3_cust_fin_comp_list[cid[0]] = []             
                    for val in self.l3FeatureList[cid[0]]:	
                        if val not in self.l3FeatureList['finance']:
                            self.l3_cust_fin_comp_list[cid[0]].append(val)
                                
        except Error as e:
            print("Error while connecting to MySQL", e)
        finally:
            return self.l3_cust_fin_comp_list            

    def Sec_Cust_Fin_CompList(self):
        try:
            self.securityList()    
            
            for cid in self.uniqCusIdList:
                if cid[0] not in self.sitIntProfList:
                    self.sec_cust_fin_comp_list[cid[0]] = []             
                    for val in self.secFeatureList[cid[0]]:	
                        if val not in self.secFeatureList['finance']:
                            self.sec_cust_fin_comp_list[cid[0]].append(val)
                                
        except Error as e:
            print("Error while connecting to MySQL", e)
        finally:
            return self.sec_cust_fin_comp_list  

    def Mcast_Cust_Fin_CompList(self):
        try:
            self.multicastList()    
            
            for cid in self.uniqCusIdList:
                if cid[0] not in self.sitIntProfList:
                    self.mcast_cust_fin_comp_list[cid[0]] = []             
                    for val in self.mcastFeatureList[cid[0]]:	
                        if val not in self.mcastFeatureList['finance']:
                            self.mcast_cust_fin_comp_list[cid[0]].append(val)
                                
        except Error as e:
            print("Error while connecting to MySQL", e)
        finally:
            return self.mcast_cust_fin_comp_list    

    def Policy_Cust_Fin_CompList(self):
        try:
            self.policyList()    
            
            for cid in self.uniqCusIdList:
                if cid[0] not in self.sitIntProfList:
                    self.pol_cust_fin_comp_list[cid[0]] = []             
                    for val in self.polFeatureList[cid[0]]:	
                        if val not in self.polFeatureList['finance']:
                            self.pol_cust_fin_comp_list[cid[0]].append(val)
                                
        except Error as e:
            print("Error while connecting to MySQL", e)
        finally:
            return self.pol_cust_fin_comp_list            

    def Platform_Cust_Fin_CompList(self):
        try:
            self.platformList()    
            
            for cid in self.uniqCusIdList:
                if cid[0] not in self.sitIntProfList:
                    self.plat_cust_fin_comp_list[cid[0]] = []             
                    for val in self.platFeatureList[cid[0]]:	
                        if val not in self.platFeatureList['finance']:
                            self.plat_cust_fin_comp_list[cid[0]].append(val)
                                
        except Error as e:
            print("Error while connecting to MySQL", e)
        finally:
            return self.plat_cust_fin_comp_list          

    def Service_Cust_Fin_CompList(self):
        try:
            self.serviceList()    
            
            for cid in self.uniqCusIdList:
                if cid[0] not in self.sitIntProfList:
                    self.serv_cust_fin_comp_list[cid[0]] = []             
                    for val in self.servFeatureList[cid[0]]:	
                        if val not in self.servFeatureList['finance']:
                            self.serv_cust_fin_comp_list[cid[0]].append(val)
                                
        except Error as e:
            print("Error while connecting to MySQL", e)
        finally:
            return self.serv_cust_fin_comp_list    

    def Management_Cust_Fin_CompList(self):
        try:
            self.managementList()    
            
            for cid in self.uniqCusIdList:
                if cid[0] not in self.sitIntProfList:
                    self.mgmt_cust_fin_comp_list[cid[0]] = []             
                    for val in self.mgmtFeatureList[cid[0]]:	
                        if val not in self.mgmtFeatureList['finance']:
                            self.mgmt_cust_fin_comp_list[cid[0]].append(val)
                                
        except Error as e:
            print("Error while connecting to MySQL", e)
        finally:
            return self.mgmt_cust_fin_comp_list            

    def Program_Cust_Fin_CompList(self):
        try:
            self.programList()    
            
            for cid in self.uniqCusIdList:
                if cid[0] not in self.sitIntProfList:
                    self.pgm_cust_fin_comp_list[cid[0]] = []             
                    for val in self.pgmFeatureList[cid[0]]:	
                        if val not in self.pgmFeatureList['finance']:
                            self.pgm_cust_fin_comp_list[cid[0]].append(val)
                                
        except Error as e:
            print("Error while connecting to MySQL", e)
        finally:
            return self.pgm_cust_fin_comp_list

    def Mpls_Cust_Fin_CompList(self):
        try:
            self.mplsList()    
            
            for cid in self.uniqCusIdList:
                if cid[0] not in self.sitIntProfList:
                    self.mpls_cust_fin_comp_list[cid[0]] = []             
                    for val in self.mplsFeatureList[cid[0]]:	
                        if val not in self.mplsFeatureList['finance']:
                            self.mpls_cust_fin_comp_list[cid[0]].append(val)
                                
        except Error as e:
            print("Error while connecting to MySQL", e)
        finally:
            return self.mpls_cust_fin_comp_list

    def AllFeatures_Cust_Fin_CompList(self):
        try:
            self.uniqCustFeaturesList()    
            
            for cid in self.uniqCusIdList:
                if cid[0] not in self.sitIntProfList:
                    self.tot_cust_fin_comp_list[cid[0]] = []             
                    for val in self.allFeaturesList[cid[0]]:	
                        if val not in self.allFeaturesList['finance']:
                            self.tot_cust_fin_comp_list[cid[0]].append(val)
                                
        except Error as e:
            print("Error while connecting to MySQL", e)
        finally:
            return self.tot_cust_fin_comp_list

    def Cust_Fin_Features_Percent_Coverage(self):
        try:
            self.AllFeatures_Cust_Fin_CompList()    
            
            for cid in self.uniqCusIdList:
                if cid[0] not in self.sitIntProfList:                 
                    self.cust_fin_feat_per_not_cov_list[cid[0]] = round(len(self.tot_cust_fin_comp_list[cid[0]])/len(self.allFeaturesList[cid[0]])*100)                    
                    self.cust_fin_feat_per_cov_list[cid[0]] = 100 - self.cust_fin_feat_per_not_cov_list[cid[0]]                                        
                                                       
        except Error as e:
            print("Error while connecting to MySQL", e)
        finally:
            return self.cust_fin_feat_per_cov_list,self.cust_fin_feat_per_not_cov_list            

    def L2_Cust_Edu_CompList(self):
        try:
            self.layer2List()    
            
            for cid in self.uniqCusIdList:
                if cid[0] not in self.sitIntProfList:
                    self.l2_cust_edu_comp_list[cid[0]] = []             
                    for val in self.l2FeatureList[cid[0]]:	
                        if val not in self.l2FeatureList['education']:
                            self.l2_cust_edu_comp_list[cid[0]].append(val)
                                
        except Error as e:
            print("Error while connecting to MySQL", e)
        finally:
            return self.l2_cust_edu_comp_list

    def L3_Cust_Edu_CompList(self):
        try:
            self.layer3List()    
            
            for cid in self.uniqCusIdList:
                if cid[0] not in self.sitIntProfList:
                    self.l3_cust_edu_comp_list[cid[0]] = []             
                    for val in self.l3FeatureList[cid[0]]:	
                        if val not in self.l3FeatureList['education']:
                            self.l3_cust_edu_comp_list[cid[0]].append(val)
                                
        except Error as e:
            print("Error while connecting to MySQL", e)
        finally:
            return self.l3_cust_edu_comp_list            

    def Sec_Cust_Edu_CompList(self):
        try:
            self.securityList()    
            
            for cid in self.uniqCusIdList:
                if cid[0] not in self.sitIntProfList:
                    self.sec_cust_edu_comp_list[cid[0]] = []             
                    for val in self.secFeatureList[cid[0]]:	
                        if val not in self.secFeatureList['education']:
                            self.sec_cust_edu_comp_list[cid[0]].append(val)
                                
        except Error as e:
            print("Error while connecting to MySQL", e)
        finally:
            return self.sec_cust_edu_comp_list  

    def Mcast_Cust_Edu_CompList(self):
        try:
            self.multicastList()    
            
            for cid in self.uniqCusIdList:
                if cid[0] not in self.sitIntProfList:
                    self.mcast_cust_edu_comp_list[cid[0]] = []             
                    for val in self.mcastFeatureList[cid[0]]:	
                        if val not in self.mcastFeatureList['education']:
                            self.mcast_cust_edu_comp_list[cid[0]].append(val)
                                
        except Error as e:
            print("Error while connecting to MySQL", e)
        finally:
            return self.mcast_cust_edu_comp_list    

    def Policy_Cust_Edu_CompList(self):
        try:
            self.policyList()    
            
            for cid in self.uniqCusIdList:
                if cid[0] not in self.sitIntProfList:
                    self.pol_cust_edu_comp_list[cid[0]] = []             
                    for val in self.polFeatureList[cid[0]]:	
                        if val not in self.polFeatureList['education']:
                            self.pol_cust_edu_comp_list[cid[0]].append(val)
                                
        except Error as e:
            print("Error while connecting to MySQL", e)
        finally:
            return self.pol_cust_edu_comp_list            

    def Platform_Cust_Edu_CompList(self):
        try:
            self.platformList()    
            
            for cid in self.uniqCusIdList:
                if cid[0] not in self.sitIntProfList:
                    self.plat_cust_edu_comp_list[cid[0]] = []             
                    for val in self.platFeatureList[cid[0]]:	
                        if val not in self.platFeatureList['education']:
                            self.plat_cust_edu_comp_list[cid[0]].append(val)
                                
        except Error as e:
            print("Error while connecting to MySQL", e)
        finally:
            return self.plat_cust_edu_comp_list          

    def Service_Cust_Edu_CompList(self):
        try:
            self.serviceList()    
            
            for cid in self.uniqCusIdList:
                if cid[0] not in self.sitIntProfList:
                    self.serv_cust_edu_comp_list[cid[0]] = []             
                    for val in self.servFeatureList[cid[0]]:	
                        if val not in self.servFeatureList['education']:
                            self.serv_cust_edu_comp_list[cid[0]].append(val)
                                
        except Error as e:
            print("Error while connecting to MySQL", e)
        finally:
            return self.serv_cust_edu_comp_list    

    def Management_Cust_Edu_CompList(self):
        try:
            self.managementList()    
            
            for cid in self.uniqCusIdList:
                if cid[0] not in self.sitIntProfList:
                    self.mgmt_cust_edu_comp_list[cid[0]] = []             
                    for val in self.mgmtFeatureList[cid[0]]:	
                        if val not in self.mgmtFeatureList['education']:
                            self.mgmt_cust_edu_comp_list[cid[0]].append(val)
                                
        except Error as e:
            print("Error while connecting to MySQL", e)
        finally:
            return self.mgmt_cust_edu_comp_list            

    def Program_Cust_Edu_CompList(self):
        try:
            self.programList()    
            
            for cid in self.uniqCusIdList:
                if cid[0] not in self.sitIntProfList:
                    self.pgm_cust_edu_comp_list[cid[0]] = []             
                    for val in self.pgmFeatureList[cid[0]]:	
                        if val not in self.pgmFeatureList['education']:
                            self.pgm_cust_edu_comp_list[cid[0]].append(val)
                                
        except Error as e:
            print("Error while connecting to MySQL", e)
        finally:
            return self.pgm_cust_edu_comp_list

    def Mpls_Cust_Edu_CompList(self):
        try:
            self.mplsList()    
            
            for cid in self.uniqCusIdList:
                if cid[0] not in self.sitIntProfList:
                    self.mpls_cust_edu_comp_list[cid[0]] = []             
                    for val in self.mplsFeatureList[cid[0]]:	
                        if val not in self.mplsFeatureList['education']:
                            self.mpls_cust_edu_comp_list[cid[0]].append(val)
                                
        except Error as e:
            print("Error while connecting to MySQL", e)
        finally:
            return self.mpls_cust_edu_comp_list

    def AllFeatures_Cust_Edu_CompList(self):
        try:
            self.uniqCustFeaturesList()    
            
            for cid in self.uniqCusIdList:
                if cid[0] not in self.sitIntProfList:
                    self.tot_cust_edu_comp_list[cid[0]] = []             
                    for val in self.allFeaturesList[cid[0]]:	
                        if val not in self.allFeaturesList['education']:
                            self.tot_cust_edu_comp_list[cid[0]].append(val)
                                
        except Error as e:
            print("Error while connecting to MySQL", e)
        finally:
            return self.tot_cust_edu_comp_list

    def Cust_Edu_Features_Percent_Coverage(self):
        try:
            self.AllFeatures_Cust_Edu_CompList()    
            
            for cid in self.uniqCusIdList:
                if cid[0] not in self.sitIntProfList:                 
                    self.cust_edu_feat_per_not_cov_list[cid[0]] = round(len(self.tot_cust_edu_comp_list[cid[0]])/len(self.allFeaturesList[cid[0]])*100)  
                    self.cust_edu_feat_per_cov_list[cid[0]] = 100 - self.cust_edu_feat_per_not_cov_list[cid[0]]                   
                                                   
        except Error as e:
            print("Error while connecting to MySQL", e)
        finally:
            return self.cust_edu_feat_per_cov_list,self.cust_edu_feat_per_not_cov_list         

    def L2_Cust_Ret_CompList(self):
        try:
            self.layer2List()    
            
            for cid in self.uniqCusIdList:
                if cid[0] not in self.sitIntProfList:
                    self.l2_cust_ret_comp_list[cid[0]] = []             
                    for val in self.l2FeatureList[cid[0]]:	
                        if val not in self.l2FeatureList['retail']:
                            self.l2_cust_ret_comp_list[cid[0]].append(val)
                                
        except Error as e:
            print("Error while connecting to MySQL", e)
        finally:
            return self.l2_cust_ret_comp_list

    def L3_Cust_Ret_CompList(self):
        try:
            self.layer3List()    
            
            for cid in self.uniqCusIdList:
                if cid[0] not in self.sitIntProfList:
                    self.l3_cust_ret_comp_list[cid[0]] = []             
                    for val in self.l3FeatureList[cid[0]]:	
                        if val not in self.l3FeatureList['retail']:
                            self.l3_cust_ret_comp_list[cid[0]].append(val)
                                
        except Error as e:
            print("Error while connecting to MySQL", e)
        finally:
            return self.l3_cust_ret_comp_list            

    def Sec_Cust_Ret_CompList(self):
        try:
            self.securityList()    
            
            for cid in self.uniqCusIdList:
                if cid[0] not in self.sitIntProfList:
                    self.sec_cust_ret_comp_list[cid[0]] = []             
                    for val in self.secFeatureList[cid[0]]:	
                        if val not in self.secFeatureList['retail']:
                            self.sec_cust_ret_comp_list[cid[0]].append(val)
                                
        except Error as e:
            print("Error while connecting to MySQL", e)
        finally:
            return self.sec_cust_ret_comp_list  

    def Mcast_Cust_Ret_CompList(self):
        try:
            self.multicastList()    
            
            for cid in self.uniqCusIdList:
                if cid[0] not in self.sitIntProfList:
                    self.mcast_cust_ret_comp_list[cid[0]] = []             
                    for val in self.mcastFeatureList[cid[0]]:	
                        if val not in self.mcastFeatureList['retail']:
                            self.mcast_cust_ret_comp_list[cid[0]].append(val)
                                
        except Error as e:
            print("Error while connecting to MySQL", e)
        finally:
            return self.mcast_cust_ret_comp_list    

    def Policy_Cust_Ret_CompList(self):
        try:
            self.policyList()    
            
            for cid in self.uniqCusIdList:
                if cid[0] not in self.sitIntProfList:
                    self.pol_cust_ret_comp_list[cid[0]] = []             
                    for val in self.polFeatureList[cid[0]]:	
                        if val not in self.polFeatureList['retail']:
                            self.pol_cust_ret_comp_list[cid[0]].append(val)
                                
        except Error as e:
            print("Error while connecting to MySQL", e)
        finally:
            return self.pol_cust_ret_comp_list            

    def Platform_Cust_Ret_CompList(self):
        try:
            self.platformList()    
            
            for cid in self.uniqCusIdList:
                if cid[0] not in self.sitIntProfList:
                    self.plat_cust_ret_comp_list[cid[0]] = []             
                    for val in self.platFeatureList[cid[0]]:	
                        if val not in self.platFeatureList['retail']:
                            self.plat_cust_ret_comp_list[cid[0]].append(val)
                                
        except Error as e:
            print("Error while connecting to MySQL", e)
        finally:
            return self.plat_cust_ret_comp_list          

    def Service_Cust_Ret_CompList(self):
        try:
            self.serviceList()    
            
            for cid in self.uniqCusIdList:
                if cid[0] not in self.sitIntProfList:
                    self.serv_cust_ret_comp_list[cid[0]] = []             
                    for val in self.servFeatureList[cid[0]]:	
                        if val not in self.servFeatureList['retail']:
                            self.serv_cust_ret_comp_list[cid[0]].append(val)
                                
        except Error as e:
            print("Error while connecting to MySQL", e)
        finally:
            return self.serv_cust_ret_comp_list    

    def Management_Cust_Ret_CompList(self):
        try:
            self.managementList()    
            
            for cid in self.uniqCusIdList:
                if cid[0] not in self.sitIntProfList:
                    self.mgmt_cust_ret_comp_list[cid[0]] = []             
                    for val in self.mgmtFeatureList[cid[0]]:	
                        if val not in self.mgmtFeatureList['retail']:
                            self.mgmt_cust_ret_comp_list[cid[0]].append(val)
                                
        except Error as e:
            print("Error while connecting to MySQL", e)
        finally:
            return self.mgmt_cust_ret_comp_list            

    def Program_Cust_Ret_CompList(self):
        try:
            self.programList()    
            
            for cid in self.uniqCusIdList:
                if cid[0] not in self.sitIntProfList:
                    self.pgm_cust_ret_comp_list[cid[0]] = []             
                    for val in self.pgmFeatureList[cid[0]]:	
                        if val not in self.pgmFeatureList['retail']:
                            self.pgm_cust_ret_comp_list[cid[0]].append(val)
                                
        except Error as e:
            print("Error while connecting to MySQL", e)
        finally:
            return self.pgm_cust_ret_comp_list

    def Mpls_Cust_Ret_CompList(self):
        try:
            self.mplsList()    
            
            for cid in self.uniqCusIdList:
                if cid[0] not in self.sitIntProfList:
                    self.mpls_cust_ret_comp_list[cid[0]] = []             
                    for val in self.mplsFeatureList[cid[0]]:	
                        if val not in self.mplsFeatureList['retail']:
                            self.mpls_cust_ret_comp_list[cid[0]].append(val)
                                
        except Error as e:
            print("Error while connecting to MySQL", e)
        finally:
            return self.mpls_cust_ret_comp_list

    def AllFeatures_Cust_Ret_CompList(self):
        try:
            self.uniqCustFeaturesList()    
            
            for cid in self.uniqCusIdList:
                if cid[0] not in self.sitIntProfList:
                    self.tot_cust_ret_comp_list[cid[0]] = []             
                    for val in self.allFeaturesList[cid[0]]:	
                        if val not in self.allFeaturesList['retail']:
                            self.tot_cust_ret_comp_list[cid[0]].append(val)
                                
        except Error as e:
            print("Error while connecting to MySQL", e)
        finally:
            return self.tot_cust_ret_comp_list

    def Cust_Ret_Features_Percent_Coverage(self):
        try:
            self.AllFeatures_Cust_Ret_CompList()    
            
            for cid in self.uniqCusIdList:
                if cid[0] not in self.sitIntProfList:                 
                    self.cust_ret_feat_per_not_cov_list[cid[0]] = round(len(self.tot_cust_ret_comp_list[cid[0]])/len(self.allFeaturesList[cid[0]])*100)          
                    self.cust_ret_feat_per_cov_list[cid[0]] = 100 - self.cust_ret_feat_per_not_cov_list[cid[0]]
                    
        except Error as e:
            print("Error while connecting to MySQL", e)
        finally:
            return self.cust_ret_feat_per_cov_list,self.cust_ret_feat_per_not_cov_list        

    def L2_Cust_HC_CompList(self):
        try:
            self.layer2List()    
            
            for cid in self.uniqCusIdList:
                if cid[0] not in self.sitIntProfList:
                    self.l2_cust_hc_comp_list[cid[0]] = []             
                    for val in self.l2FeatureList[cid[0]]:	
                        if val not in self.l2FeatureList['healthcare']:
                            self.l2_cust_hc_comp_list[cid[0]].append(val)
                                
        except Error as e:
            print("Error while connecting to MySQL", e)
        finally:
            return self.l2_cust_hc_comp_list

    def L3_Cust_HC_CompList(self):
        try:
            self.layer3List()    
            
            for cid in self.uniqCusIdList:
                if cid[0] not in self.sitIntProfList:
                    self.l3_cust_hc_comp_list[cid[0]] = []             
                    for val in self.l3FeatureList[cid[0]]:	
                        if val not in self.l3FeatureList['healthcare']:
                            self.l3_cust_hc_comp_list[cid[0]].append(val)
                                
        except Error as e:
            print("Error while connecting to MySQL", e)
        finally:
            return self.l3_cust_hc_comp_list            

    def Sec_Cust_HC_CompList(self):
        try:
            self.securityList()    
            
            for cid in self.uniqCusIdList:
                if cid[0] not in self.sitIntProfList:
                    self.sec_cust_hc_comp_list[cid[0]] = []             
                    for val in self.secFeatureList[cid[0]]:	
                        if val not in self.secFeatureList['healthcare']:
                            self.sec_cust_hc_comp_list[cid[0]].append(val)
                                
        except Error as e:
            print("Error while connecting to MySQL", e)
        finally:
            return self.sec_cust_hc_comp_list  

    def Mcast_Cust_HC_CompList(self):
        try:
            self.multicastList()    
            
            for cid in self.uniqCusIdList:
                if cid[0] not in self.sitIntProfList:
                    self.mcast_cust_hc_comp_list[cid[0]] = []             
                    for val in self.mcastFeatureList[cid[0]]:	
                        if val not in self.mcastFeatureList['healthcare']:
                            self.mcast_cust_hc_comp_list[cid[0]].append(val)
                                
        except Error as e:
            print("Error while connecting to MySQL", e)
        finally:
            return self.mcast_cust_hc_comp_list    

    def Policy_Cust_HC_CompList(self):
        try:
            self.policyList()    
            
            for cid in self.uniqCusIdList:
                if cid[0] not in self.sitIntProfList:
                    self.pol_cust_hc_comp_list[cid[0]] = []             
                    for val in self.polFeatureList[cid[0]]:	
                        if val not in self.polFeatureList['healthcare']:
                            self.pol_cust_hc_comp_list[cid[0]].append(val)
                                
        except Error as e:
            print("Error while connecting to MySQL", e)
        finally:
            return self.pol_cust_hc_comp_list            

    def Platform_Cust_HC_CompList(self):
        try:
            self.platformList()    
            
            for cid in self.uniqCusIdList:
                if cid[0] not in self.sitIntProfList:
                    self.plat_cust_hc_comp_list[cid[0]] = []             
                    for val in self.platFeatureList[cid[0]]:	
                        if val not in self.platFeatureList['healthcare']:
                            self.plat_cust_hc_comp_list[cid[0]].append(val)
                                
        except Error as e:
            print("Error while connecting to MySQL", e)
        finally:
            return self.plat_cust_hc_comp_list          

    def Service_Cust_HC_CompList(self):
        try:
            self.serviceList()    
            
            for cid in self.uniqCusIdList:
                if cid[0] not in self.sitIntProfList:
                    self.serv_cust_hc_comp_list[cid[0]] = []             
                    for val in self.servFeatureList[cid[0]]:	
                        if val not in self.servFeatureList['healthcare']:
                            self.serv_cust_hc_comp_list[cid[0]].append(val)
                                
        except Error as e:
            print("Error while connecting to MySQL", e)
        finally:
            return self.serv_cust_hc_comp_list    

    def Management_Cust_HC_CompList(self):
        try:
            self.managementList()    
            
            for cid in self.uniqCusIdList:
                if cid[0] not in self.sitIntProfList:
                    self.mgmt_cust_hc_comp_list[cid[0]] = []             
                    for val in self.mgmtFeatureList[cid[0]]:	
                        if val not in self.mgmtFeatureList['healthcare']:
                            self.mgmt_cust_hc_comp_list[cid[0]].append(val)
                                
        except Error as e:
            print("Error while connecting to MySQL", e)
        finally:
            return self.mgmt_cust_hc_comp_list            

    def Program_Cust_HC_CompList(self):
        try:
            self.programList()    
            
            for cid in self.uniqCusIdList:
                if cid[0] not in self.sitIntProfList:
                    self.pgm_cust_hc_comp_list[cid[0]] = []             
                    for val in self.pgmFeatureList[cid[0]]:	
                        if val not in self.pgmFeatureList['healthcare']:
                            self.pgm_cust_hc_comp_list[cid[0]].append(val)
                                
        except Error as e:
            print("Error while connecting to MySQL", e)
        finally:
            return self.pgm_cust_hc_comp_list

    def Mpls_Cust_HC_CompList(self):
        try:
            self.mplsList()    
            
            for cid in self.uniqCusIdList:
                if cid[0] not in self.sitIntProfList:
                    self.mpls_cust_hc_comp_list[cid[0]] = []             
                    for val in self.mplsFeatureList[cid[0]]:	
                        if val not in self.mplsFeatureList['healthcare']:
                            self.mpls_cust_hc_comp_list[cid[0]].append(val)
                                
        except Error as e:
            print("Error while connecting to MySQL", e)
        finally:
            return self.mpls_cust_hc_comp_list

    def AllFeatures_Cust_HC_CompList(self):
        try:
            self.uniqCustFeaturesList()    
            
            for cid in self.uniqCusIdList:
                if cid[0] not in self.sitIntProfList:
                    self.tot_cust_hc_comp_list[cid[0]] = []             
                    for val in self.allFeaturesList[cid[0]]:	
                        if val not in self.allFeaturesList['healthcare']:
                            self.tot_cust_hc_comp_list[cid[0]].append(val)
                                
        except Error as e:
            print("Error while connecting to MySQL", e)
        finally:
            return self.tot_cust_hc_comp_list

    def Cust_HC_Features_Percent_Coverage(self):
        try:
            self.AllFeatures_Cust_HC_CompList()    
            
            for cid in self.uniqCusIdList:
                if cid[0] not in self.sitIntProfList:                 
                    self.cust_hc_feat_per_not_cov_list[cid[0]] = round(len(self.tot_cust_hc_comp_list[cid[0]])/len(self.allFeaturesList[cid[0]])*100)          
                    self.cust_hc_feat_per_cov_list[cid[0]] = 100 - self.cust_hc_feat_per_not_cov_list[cid[0]]
                    
        except Error as e:
            print("Error while connecting to MySQL", e)
        finally:
            return self.cust_hc_feat_per_cov_list,self.cust_hc_feat_per_not_cov_list      

    def L2_Cust_Gov_CompList(self):
        try:
            self.layer2List()    
            
            for cid in self.uniqCusIdList:
                if cid[0] not in self.sitIntProfList:
                    self.l2_cust_gov_comp_list[cid[0]] = []             
                    for val in self.l2FeatureList[cid[0]]:	
                        if val not in self.l2FeatureList['government']:
                            self.l2_cust_gov_comp_list[cid[0]].append(val)
                                
        except Error as e:
            print("Error while connecting to MySQL", e)
        finally:
            return self.l2_cust_gov_comp_list

    def L3_Cust_Gov_CompList(self):
        try:
            self.layer3List()    
            
            for cid in self.uniqCusIdList:
                if cid[0] not in self.sitIntProfList:
                    self.l3_cust_gov_comp_list[cid[0]] = []             
                    for val in self.l3FeatureList[cid[0]]:	
                        if val not in self.l3FeatureList['government']:
                            self.l3_cust_gov_comp_list[cid[0]].append(val)
                                
        except Error as e:
            print("Error while connecting to MySQL", e)
        finally:
            return self.l3_cust_gov_comp_list            

    def Sec_Cust_Gov_CompList(self):
        try:
            self.securityList()    
            
            for cid in self.uniqCusIdList:
                if cid[0] not in self.sitIntProfList:
                    self.sec_cust_gov_comp_list[cid[0]] = []             
                    for val in self.secFeatureList[cid[0]]:	
                        if val not in self.secFeatureList['government']:
                            self.sec_cust_gov_comp_list[cid[0]].append(val)
                                
        except Error as e:
            print("Error while connecting to MySQL", e)
        finally:
            return self.sec_cust_gov_comp_list  

    def Mcast_Cust_Gov_CompList(self):
        try:
            self.multicastList()    
            
            for cid in self.uniqCusIdList:
                if cid[0] not in self.sitIntProfList:
                    self.mcast_cust_gov_comp_list[cid[0]] = []             
                    for val in self.mcastFeatureList[cid[0]]:	
                        if val not in self.mcastFeatureList['government']:
                            self.mcast_cust_gov_comp_list[cid[0]].append(val)
                                
        except Error as e:
            print("Error while connecting to MySQL", e)
        finally:
            return self.mcast_cust_gov_comp_list    

    def Policy_Cust_Gov_CompList(self):
        try:
            self.policyList()    
            
            for cid in self.uniqCusIdList:
                if cid[0] not in self.sitIntProfList:
                    self.pol_cust_gov_comp_list[cid[0]] = []             
                    for val in self.polFeatureList[cid[0]]:	
                        if val not in self.polFeatureList['government']:
                            self.pol_cust_gov_comp_list[cid[0]].append(val)
                                
        except Error as e:
            print("Error while connecting to MySQL", e)
        finally:
            return self.pol_cust_gov_comp_list            

    def Platform_Cust_Gov_CompList(self):
        try:
            self.platformList()    
            
            for cid in self.uniqCusIdList:
                if cid[0] not in self.sitIntProfList:
                    self.plat_cust_gov_comp_list[cid[0]] = []             
                    for val in self.platFeatureList[cid[0]]:	
                        if val not in self.platFeatureList['government']:
                            self.plat_cust_gov_comp_list[cid[0]].append(val)
                                
        except Error as e:
            print("Error while connecting to MySQL", e)
        finally:
            return self.plat_cust_gov_comp_list          

    def Service_Cust_Gov_CompList(self):
        try:
            self.serviceList()    
            
            for cid in self.uniqCusIdList:
                if cid[0] not in self.sitIntProfList:
                    self.serv_cust_gov_comp_list[cid[0]] = []             
                    for val in self.servFeatureList[cid[0]]:	
                        if val not in self.servFeatureList['government']:
                            self.serv_cust_gov_comp_list[cid[0]].append(val)
                                
        except Error as e:
            print("Error while connecting to MySQL", e)
        finally:
            return self.serv_cust_gov_comp_list    

    def Management_Cust_Gov_CompList(self):
        try:
            self.managementList()    
            
            for cid in self.uniqCusIdList:
                if cid[0] not in self.sitIntProfList:
                    self.mgmt_cust_gov_comp_list[cid[0]] = []             
                    for val in self.mgmtFeatureList[cid[0]]:	
                        if val not in self.mgmtFeatureList['government']:
                            self.mgmt_cust_gov_comp_list[cid[0]].append(val)
                                
        except Error as e:
            print("Error while connecting to MySQL", e)
        finally:
            return self.mgmt_cust_gov_comp_list            

    def Program_Cust_Gov_CompList(self):
        try:
            self.programList()    
            
            for cid in self.uniqCusIdList:
                if cid[0] not in self.sitIntProfList:
                    self.pgm_cust_gov_comp_list[cid[0]] = []             
                    for val in self.pgmFeatureList[cid[0]]:	
                        if val not in self.pgmFeatureList['government']:
                            self.pgm_cust_gov_comp_list[cid[0]].append(val)
                                
        except Error as e:
            print("Error while connecting to MySQL", e)
        finally:
            return self.pgm_cust_gov_comp_list

    def Mpls_Cust_Gov_CompList(self):
        try:
            self.mplsList()    
            
            for cid in self.uniqCusIdList:
                if cid[0] not in self.sitIntProfList:
                    self.mpls_cust_gov_comp_list[cid[0]] = []             
                    for val in self.mplsFeatureList[cid[0]]:	
                        if val not in self.mplsFeatureList['government']:
                            self.mpls_cust_gov_comp_list[cid[0]].append(val)
                                
        except Error as e:
            print("Error while connecting to MySQL", e)
        finally:
            return self.mpls_cust_gov_comp_list

    def AllFeatures_Cust_Gov_CompList(self):
        try:
            self.uniqCustFeaturesList()    
            
            for cid in self.uniqCusIdList:
                if cid[0] not in self.sitIntProfList:
                    self.tot_cust_gov_comp_list[cid[0]] = []             
                    for val in self.allFeaturesList[cid[0]]:	
                        if val not in self.allFeaturesList['government']:
                            self.tot_cust_gov_comp_list[cid[0]].append(val)
                                
        except Error as e:
            print("Error while connecting to MySQL", e)
        finally:
            return self.tot_cust_gov_comp_list

    def Cust_Gov_Features_Percent_Coverage(self):
        try:
            self.AllFeatures_Cust_Gov_CompList()    
            
            for cid in self.uniqCusIdList:
                if cid[0] not in self.sitIntProfList:                 
                    self.cust_gov_feat_per_not_cov_list[cid[0]] = round(len(self.tot_cust_gov_comp_list[cid[0]])/len(self.allFeaturesList[cid[0]])*100)          
                    self.cust_gov_feat_per_cov_list[cid[0]] = 100 - self.cust_gov_feat_per_not_cov_list[cid[0]]
                    
        except Error as e:
            print("Error while connecting to MySQL", e)
        finally:
            return self.cust_gov_feat_per_cov_list,self.cust_gov_feat_per_not_cov_list  

    def L2_Cust_Nge_CompList(self):
        try:
            self.layer2List()    
            
            for cid in self.uniqCusIdList:
                if cid[0] not in self.sitIntProfList:
                    self.l2_cust_nge_comp_list[cid[0]] = []             
                    for val in self.l2FeatureList[cid[0]]:	
                        if val not in self.l2FeatureList['NGE']:
                            self.l2_cust_nge_comp_list[cid[0]].append(val)
                                
        except Error as e:
            print("Error while connecting to MySQL", e)
        finally:
            return self.l2_cust_nge_comp_list

    def L3_Cust_Nge_CompList(self):
        try:
            self.layer3List()    
            
            for cid in self.uniqCusIdList:
                if cid[0] not in self.sitIntProfList:
                    self.l3_cust_nge_comp_list[cid[0]] = []             
                    for val in self.l3FeatureList[cid[0]]:	
                        if val not in self.l3FeatureList['NGE']:
                            self.l3_cust_nge_comp_list[cid[0]].append(val)
                                
        except Error as e:
            print("Error while connecting to MySQL", e)
        finally:
            return self.l3_cust_nge_comp_list            

    def Sec_Cust_Nge_CompList(self):
        try:
            self.securityList()    
            
            for cid in self.uniqCusIdList:
                if cid[0] not in self.sitIntProfList:
                    self.sec_cust_nge_comp_list[cid[0]] = []             
                    for val in self.secFeatureList[cid[0]]:	
                        if val not in self.secFeatureList['NGE']:
                            self.sec_cust_nge_comp_list[cid[0]].append(val)
                                
        except Error as e:
            print("Error while connecting to MySQL", e)
        finally:
            return self.sec_cust_nge_comp_list  

    def Mcast_Cust_Nge_CompList(self):
        try:
            self.multicastList()    
            
            for cid in self.uniqCusIdList:
                if cid[0] not in self.sitIntProfList:
                    self.mcast_cust_nge_comp_list[cid[0]] = []             
                    for val in self.mcastFeatureList[cid[0]]:	
                        if val not in self.mcastFeatureList['NGE']:
                            self.mcast_cust_nge_comp_list[cid[0]].append(val)
                                
        except Error as e:
            print("Error while connecting to MySQL", e)
        finally:
            return self.mcast_cust_nge_comp_list    

    def Policy_Cust_Nge_CompList(self):
        try:
            self.policyList()    
            
            for cid in self.uniqCusIdList:
                if cid[0] not in self.sitIntProfList:
                    self.pol_cust_nge_comp_list[cid[0]] = []             
                    for val in self.polFeatureList[cid[0]]:	
                        if val not in self.polFeatureList['NGE']:
                            self.pol_cust_nge_comp_list[cid[0]].append(val)
                                
        except Error as e:
            print("Error while connecting to MySQL", e)
        finally:
            return self.pol_cust_nge_comp_list            

    def Platform_Cust_Nge_CompList(self):
        try:
            self.platformList()    
            
            for cid in self.uniqCusIdList:
                if cid[0] not in self.sitIntProfList:
                    self.plat_cust_nge_comp_list[cid[0]] = []             
                    for val in self.platFeatureList[cid[0]]:	
                        if val not in self.platFeatureList['NGE']:
                            self.plat_cust_nge_comp_list[cid[0]].append(val)
                                
        except Error as e:
            print("Error while connecting to MySQL", e)
        finally:
            return self.plat_cust_nge_comp_list          

    def Service_Cust_Nge_CompList(self):
        try:
            self.serviceList()    
            
            for cid in self.uniqCusIdList:
                if cid[0] not in self.sitIntProfList:
                    self.serv_cust_nge_comp_list[cid[0]] = []             
                    for val in self.servFeatureList[cid[0]]:	
                        if val not in self.servFeatureList['NGE']:
                            self.serv_cust_nge_comp_list[cid[0]].append(val)
                                
        except Error as e:
            print("Error while connecting to MySQL", e)
        finally:
            return self.serv_cust_nge_comp_list    

    def Management_Cust_Nge_CompList(self):
        try:
            self.managementList()    
            
            for cid in self.uniqCusIdList:
                if cid[0] not in self.sitIntProfList:
                    self.mgmt_cust_nge_comp_list[cid[0]] = []             
                    for val in self.mgmtFeatureList[cid[0]]:	
                        if val not in self.mgmtFeatureList['NGE']:
                            self.mgmt_cust_nge_comp_list[cid[0]].append(val)
                                
        except Error as e:
            print("Error while connecting to MySQL", e)
        finally:
            return self.mgmt_cust_nge_comp_list            

    def Program_Cust_Nge_CompList(self):
        try:
            self.programList()    
            
            for cid in self.uniqCusIdList:
                if cid[0] not in self.sitIntProfList:
                    self.pgm_cust_nge_comp_list[cid[0]] = []             
                    for val in self.pgmFeatureList[cid[0]]:	
                        if val not in self.pgmFeatureList['NGE']:
                            self.pgm_cust_nge_comp_list[cid[0]].append(val)
                                
        except Error as e:
            print("Error while connecting to MySQL", e)
        finally:
            return self.pgm_cust_nge_comp_list

    def Mpls_Cust_Nge_CompList(self):
        try:
            self.mplsList()    
            
            for cid in self.uniqCusIdList:
                if cid[0] not in self.sitIntProfList:
                    self.mpls_cust_nge_comp_list[cid[0]] = []             
                    for val in self.mplsFeatureList[cid[0]]:	
                        if val not in self.mplsFeatureList['NGE']:
                            self.mpls_cust_nge_comp_list[cid[0]].append(val)
                                
        except Error as e:
            print("Error while connecting to MySQL", e)
        finally:
            return self.mpls_cust_nge_comp_list

    def AllFeatures_Cust_Nge_CompList(self):
        try:
            self.uniqCustFeaturesList()    
            
            for cid in self.uniqCusIdList:
                if cid[0] not in self.sitIntProfList:
                    self.tot_cust_nge_comp_list[cid[0]] = []             
                    for val in self.allFeaturesList[cid[0]]:	
                        if val not in self.allFeaturesList['NGE']:
                            self.tot_cust_nge_comp_list[cid[0]].append(val)
                                
        except Error as e:
            print("Error while connecting to MySQL", e)
        finally:
            return self.tot_cust_nge_comp_list

    def Cust_Nge_Features_Percent_Coverage(self):
        try:
            self.AllFeatures_Cust_Nge_CompList()    
            
            for cid in self.uniqCusIdList:
                if cid[0] not in self.sitIntProfList:                 
                    self.cust_nge_feat_per_not_cov_list[cid[0]] = round(len(self.tot_cust_nge_comp_list[cid[0]])/len(self.allFeaturesList[cid[0]])*100)          
                    self.cust_nge_feat_per_cov_list[cid[0]] = 100 - self.cust_nge_feat_per_not_cov_list[cid[0]]                    
                                                   
        except Error as e:
            print("Error while connecting to MySQL", e)
        finally:
            return self.cust_nge_feat_per_cov_list,self.cust_nge_feat_per_not_cov_list 

    def insert_CustFea_SitFea_Compare_Records(self):
        try:
            recCnt = 0 
            self.L2_Cust_Fin_CompList()
            self.L3_Cust_Fin_CompList()
            self.Sec_Cust_Fin_CompList()
            self.Mcast_Cust_Fin_CompList()
            self.Policy_Cust_Fin_CompList()
            self.Platform_Cust_Fin_CompList()
            self.Service_Cust_Fin_CompList()
            self.Management_Cust_Fin_CompList()
            self.Program_Cust_Fin_CompList()
            self.Mpls_Cust_Fin_CompList()
            self.AllFeatures_Cust_Fin_CompList()
            self.Cust_Fin_Features_Percent_Coverage()
            
            self.L2_Cust_Edu_CompList()
            self.L3_Cust_Edu_CompList()
            self.Sec_Cust_Edu_CompList()
            self.Mcast_Cust_Edu_CompList()
            self.Policy_Cust_Edu_CompList()
            self.Platform_Cust_Edu_CompList()
            self.Service_Cust_Edu_CompList()
            self.Management_Cust_Edu_CompList()
            self.Program_Cust_Edu_CompList()
            self.Mpls_Cust_Edu_CompList()
            self.AllFeatures_Cust_Edu_CompList()
            self.Cust_Edu_Features_Percent_Coverage()
            
            self.L2_Cust_Ret_CompList()
            self.L3_Cust_Ret_CompList()
            self.Sec_Cust_Ret_CompList()
            self.Mcast_Cust_Ret_CompList()
            self.Policy_Cust_Ret_CompList()
            self.Platform_Cust_Ret_CompList()
            self.Service_Cust_Ret_CompList()
            self.Management_Cust_Ret_CompList()
            self.Program_Cust_Ret_CompList()
            self.Mpls_Cust_Ret_CompList()
            self.AllFeatures_Cust_Ret_CompList()
            self.Cust_Ret_Features_Percent_Coverage()
            
            self.L2_Cust_HC_CompList()
            self.L3_Cust_HC_CompList()
            self.Sec_Cust_HC_CompList()
            self.Mcast_Cust_HC_CompList()
            self.Policy_Cust_HC_CompList()
            self.Platform_Cust_HC_CompList()
            self.Service_Cust_HC_CompList()
            self.Management_Cust_HC_CompList()
            self.Program_Cust_HC_CompList()
            self.Mpls_Cust_HC_CompList()
            self.AllFeatures_Cust_HC_CompList()
            self.Cust_HC_Features_Percent_Coverage()
            
            self.L2_Cust_Gov_CompList()
            self.L3_Cust_Gov_CompList()
            self.Sec_Cust_Gov_CompList()
            self.Mcast_Cust_Gov_CompList()
            self.Policy_Cust_Gov_CompList()
            self.Platform_Cust_Gov_CompList()
            self.Service_Cust_Gov_CompList()
            self.Management_Cust_Gov_CompList()
            self.Program_Cust_Gov_CompList()
            self.Mpls_Cust_Gov_CompList()
            self.AllFeatures_Cust_Gov_CompList()
            self.Cust_Gov_Features_Percent_Coverage()
            
            self.L2_Cust_Nge_CompList()
            self.L3_Cust_Nge_CompList()
            self.Sec_Cust_Nge_CompList()
            self.Mcast_Cust_Nge_CompList()
            self.Policy_Cust_Nge_CompList()
            self.Platform_Cust_Nge_CompList()
            self.Service_Cust_Nge_CompList()
            self.Management_Cust_Nge_CompList()
            self.Program_Cust_Nge_CompList()
            self.Mpls_Cust_Nge_CompList()
            self.AllFeatures_Cust_Nge_CompList()
            self.Cust_Nge_Features_Percent_Coverage()            
            
            connection = mysql.connector.connect(host     = 'localhost',
                                                 database = 'custConfigDB',
                                                 user     = 'bjatti',
                                                 password = 'Maglev123!')
            
            cursor = connection.cursor()
            
            # Insert Records into table              
            for cid in self.uniqCusIdList: 
                custid = cid[0]  
                if custid not in self.sitIntProfList:        
                    l2_cust_fin          = ','.join(self.l2_cust_fin_comp_list[custid])   
                    l3_cust_fin          = ','.join(self.l3_cust_fin_comp_list[custid])   
                    sec_cust_fin         = ','.join(self.sec_cust_fin_comp_list[custid])  
                    mcast_cust_fin       = ','.join(self.mcast_cust_fin_comp_list[custid])
                    pol_cust_fin         = ','.join(self.pol_cust_fin_comp_list[custid])  
                    plat_cust_fin        = ','.join(self.plat_cust_fin_comp_list[custid]) 
                    serv_cust_fin        = ','.join(self.serv_cust_fin_comp_list[custid]) 
                    mgmt_cust_fin        = ','.join(self.mgmt_cust_fin_comp_list[custid]) 
                    pgm_cust_fin         = ','.join(self.pgm_cust_fin_comp_list[custid])  
                    mpls_cust_fin        = ','.join(self.mpls_cust_fin_comp_list[custid]) 
                    tot_cust_fin         = ','.join(self.tot_cust_fin_comp_list[custid])  
                    cust_fin_per_not_cov = self.cust_fin_feat_per_not_cov_list[custid]
                    cust_fin_per_cov     = self.cust_fin_feat_per_cov_list[custid]                     

                    l2_cust_edu          = ','.join(self.l2_cust_edu_comp_list[custid])                         
                    l3_cust_edu          = ','.join(self.l3_cust_edu_comp_list[custid])     
                    sec_cust_edu         = ','.join(self.sec_cust_edu_comp_list[custid])    
                    mcast_cust_edu       = ','.join(self.mcast_cust_edu_comp_list[custid])  
                    pol_cust_edu         = ','.join(self.pol_cust_edu_comp_list[custid])    
                    plat_cust_edu        = ','.join(self.plat_cust_edu_comp_list[custid])   
                    serv_cust_edu        = ','.join(self.serv_cust_edu_comp_list[custid])   
                    mgmt_cust_edu        = ','.join(self.mgmt_cust_edu_comp_list[custid])   
                    pgm_cust_edu         = ','.join(self.pgm_cust_edu_comp_list[custid])    
                    mpls_cust_edu        = ','.join(self.mpls_cust_edu_comp_list[custid])   
                    tot_cust_edu         = ','.join(self.tot_cust_edu_comp_list[custid])    
                    cust_edu_per_not_cov = self.cust_edu_feat_per_not_cov_list[custid]
                    cust_edu_per_cov     = self.cust_edu_feat_per_cov_list[custid]

                    l2_cust_ret          = ','.join(self.l2_cust_ret_comp_list[custid])     
                    l3_cust_ret          = ','.join(self.l3_cust_ret_comp_list[custid])     
                    sec_cust_ret         = ','.join(self.sec_cust_ret_comp_list[custid])    
                    mcast_cust_ret       = ','.join(self.mcast_cust_ret_comp_list[custid])  
                    pol_cust_ret         = ','.join(self.pol_cust_ret_comp_list[custid])    
                    plat_cust_ret        = ','.join(self.plat_cust_ret_comp_list[custid])   
                    serv_cust_ret        = ','.join(self.serv_cust_ret_comp_list[custid])   
                    mgmt_cust_ret        = ','.join(self.mgmt_cust_ret_comp_list[custid])   
                    pgm_cust_ret         = ','.join(self.pgm_cust_ret_comp_list[custid])    
                    mpls_cust_ret        = ','.join(self.mpls_cust_ret_comp_list[custid])   
                    tot_cust_ret         = ','.join(self.tot_cust_ret_comp_list[custid])    
                    cust_ret_per_not_cov = self.cust_ret_feat_per_not_cov_list[custid]
                    cust_ret_per_cov     = self.cust_ret_feat_per_cov_list[custid]

                    l2_cust_hc           = ','.join(self.l2_cust_hc_comp_list[custid])     
                    l3_cust_hc           = ','.join(self.l3_cust_hc_comp_list[custid])     
                    sec_cust_hc          = ','.join(self.sec_cust_hc_comp_list[custid])    
                    mcast_cust_hc        = ','.join(self.mcast_cust_hc_comp_list[custid])  
                    pol_cust_hc          = ','.join(self.pol_cust_hc_comp_list[custid])    
                    plat_cust_hc         = ','.join(self.plat_cust_hc_comp_list[custid])   
                    serv_cust_hc         = ','.join(self.serv_cust_hc_comp_list[custid])   
                    mgmt_cust_hc         = ','.join(self.mgmt_cust_hc_comp_list[custid])   
                    pgm_cust_hc          = ','.join(self.pgm_cust_hc_comp_list[custid])    
                    mpls_cust_hc         = ','.join(self.mpls_cust_hc_comp_list[custid])   
                    tot_cust_hc          = ','.join(self.tot_cust_hc_comp_list[custid])    
                    cust_hc_per_not_cov  = self.cust_hc_feat_per_not_cov_list[custid]
                    cust_hc_per_cov      = self.cust_hc_feat_per_cov_list[custid]
                    
                    l2_cust_gov          = ','.join(self.l2_cust_gov_comp_list[custid])     
                    l3_cust_gov          = ','.join(self.l3_cust_gov_comp_list[custid])     
                    sec_cust_gov         = ','.join(self.sec_cust_gov_comp_list[custid])    
                    mcast_cust_gov       = ','.join(self.mcast_cust_gov_comp_list[custid])  
                    pol_cust_gov         = ','.join(self.pol_cust_gov_comp_list[custid])    
                    plat_cust_gov        = ','.join(self.plat_cust_gov_comp_list[custid])   
                    serv_cust_gov        = ','.join(self.serv_cust_gov_comp_list[custid])   
                    mgmt_cust_gov        = ','.join(self.mgmt_cust_gov_comp_list[custid])   
                    pgm_cust_gov         = ','.join(self.pgm_cust_gov_comp_list[custid])    
                    mpls_cust_gov        = ','.join(self.mpls_cust_gov_comp_list[custid])   
                    tot_cust_gov         = ','.join(self.tot_cust_gov_comp_list[custid])    
                    cust_gov_per_not_cov = self.cust_gov_feat_per_not_cov_list[custid]
                    cust_gov_per_cov     = self.cust_gov_feat_per_cov_list[custid]
                    
                    l2_cust_nge          = ','.join(self.l2_cust_nge_comp_list[custid])     
                    l3_cust_nge          = ','.join(self.l3_cust_nge_comp_list[custid])     
                    sec_cust_nge         = ','.join(self.sec_cust_nge_comp_list[custid])    
                    mcast_cust_nge       = ','.join(self.mcast_cust_nge_comp_list[custid])  
                    pol_cust_nge         = ','.join(self.pol_cust_nge_comp_list[custid])    
                    plat_cust_nge        = ','.join(self.plat_cust_nge_comp_list[custid])   
                    serv_cust_nge        = ','.join(self.serv_cust_nge_comp_list[custid])   
                    mgmt_cust_nge        = ','.join(self.mgmt_cust_nge_comp_list[custid])   
                    pgm_cust_nge         = ','.join(self.pgm_cust_nge_comp_list[custid])    
                    mpls_cust_nge        = ','.join(self.mpls_cust_nge_comp_list[custid])   
                    tot_cust_nge         = ','.join(self.tot_cust_nge_comp_list[custid])    
                    cust_nge_per_not_cov = self.cust_nge_feat_per_not_cov_list[custid]
                    cust_nge_per_cov     = self.cust_nge_feat_per_cov_list[custid]
                
                    query  = """
                             insert into CustDataCompare (cust_id,fin_l2_list,fin_l3_list,fin_sec_list,fin_mcast_list,fin_pol_list,fin_plat_list,\
                                                          fin_serv_list,fin_mgmt_list,fin_pgm_list,fin_mpls_list,fin_totFeat_list,fin_cust_per_cov,\
                                                          fin_cust_per_not_cov,edu_l2_list,edu_l3_list,edu_sec_list,edu_mcast_list,edu_pol_list,\
                                                          edu_plat_list,edu_serv_list,edu_mgmt_list,edu_pgm_list,edu_mpls_list,edu_totFeat_list,\
                                                          edu_cust_per_cov,edu_cust_per_not_cov,ret_l2_list,ret_l3_list,ret_sec_list,ret_mcast_list,\
                                                          ret_pol_list,ret_plat_list,ret_serv_list,ret_mgmt_list,ret_pgm_list,ret_mpls_list,\
                                                          ret_totFeat_list,ret_cust_per_cov,ret_cust_per_not_cov,hc_l2_list,hc_l3_list,hc_sec_list,\
                                                          hc_mcast_list,hc_pol_list,hc_plat_list,hc_serv_list,hc_mgmt_list,hc_pgm_list,hc_mpls_list,\
                                                          hc_totFeat_list,hc_cust_per_cov,hc_cust_per_not_cov,gov_l2_list,gov_l3_list,gov_sec_list,\
                                                          gov_mcast_list,gov_pol_list,gov_plat_list,gov_serv_list,gov_mgmt_list,gov_pgm_list,\
                                                          gov_mpls_list,gov_totFeat_list,gov_cust_per_cov,gov_cust_per_not_cov,nge_l2_list,nge_l3_list,\
                                                          nge_sec_list,nge_mcast_list,nge_pol_list,nge_plat_list,nge_serv_list,nge_mgmt_list,nge_pgm_list,\
                                                          nge_mpls_list,nge_totFeat_list,nge_cust_per_cov,nge_cust_per_not_cov) \
                                                          values (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,\
                                                          %s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,\
                                                          %s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s);
                             """ 
                    
                    cursor.execute(query,(custid,l2_cust_fin,l3_cust_fin,sec_cust_fin,mcast_cust_fin,pol_cust_fin,plat_cust_fin,serv_cust_fin,\
                                          mgmt_cust_fin,pgm_cust_fin,mpls_cust_fin,tot_cust_fin,cust_fin_per_cov,cust_fin_per_not_cov,l2_cust_edu,\
                                          l3_cust_edu,sec_cust_edu,mcast_cust_edu,pol_cust_edu,plat_cust_edu,serv_cust_edu,mgmt_cust_edu,pgm_cust_edu,\
                                          mpls_cust_edu,tot_cust_edu,cust_edu_per_cov,cust_edu_per_not_cov,l2_cust_ret,l3_cust_ret,sec_cust_ret,\
                                          mcast_cust_ret,pol_cust_ret,plat_cust_ret,serv_cust_ret,mgmt_cust_ret,pgm_cust_ret,mpls_cust_ret,tot_cust_ret,\
                                          cust_ret_per_cov,cust_ret_per_not_cov,l2_cust_hc,l3_cust_hc,sec_cust_hc,mcast_cust_hc,pol_cust_hc,plat_cust_hc,\
                                          serv_cust_hc,mgmt_cust_hc,pgm_cust_hc,mpls_cust_hc,tot_cust_hc,cust_hc_per_cov,cust_hc_per_not_cov,l2_cust_gov,\
                                          l3_cust_gov,sec_cust_gov,mcast_cust_gov,pol_cust_gov,plat_cust_gov,serv_cust_gov,mgmt_cust_gov,pgm_cust_gov,\
                                          mpls_cust_gov,tot_cust_gov,cust_gov_per_cov,cust_gov_per_not_cov,l2_cust_nge,l3_cust_nge,sec_cust_nge,\
                                          mcast_cust_nge,pol_cust_nge,plat_cust_nge,serv_cust_nge,mgmt_cust_nge,pgm_cust_nge,mpls_cust_nge,tot_cust_nge,\
                                          cust_nge_per_cov,cust_nge_per_not_cov))                           
                                           
                    recCnt += 1                               

            # Commit the table after insert rows
            connection.commit()                                  
        except Error as e:
            print("Error while connecting to MySQL", e)
        finally:
            return recCnt
            if connection.is_connected():
                cursor.close()
                connection.close()            