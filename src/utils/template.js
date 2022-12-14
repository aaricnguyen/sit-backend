export const template = {
  // ============ without ============
  isis: /^router isis.*\r?\n(\s+.*\r?\n)*!/gm,
  l3_bgp: /^router bgp.*\r?\n(\s+.*\r?\n)*!/gm, // duplicate
  trunk: /^interface.*\r?\n(\s+.*\r?\n)*!/gm,
  tunnel: /^interface Tunnel.*\r?\n(\s+.*\r?\n)*!/gm,
  l3dot1q: /^interface.*\r?\n(\s+.*\r?\n)*!/gm,
  svi: /^interface Vlan.*\r?\n(\s+.*\r?\n)*!/gm,
  ospfv6: /^ipv6 router.*\r?\n(\s+.*\r?\n)*!/gm,

  // ============ default true ============
  vtp: /.*(vtp version 2|vtp version 3).*/gm,
  cdp: /.*no cdp run.*/gm,
  lldp: /.*no lldp run.*/gm,
  l2_udld: /.*no udld enable.*/gm, // duplicate
  // ============ config ============
  udldAgg: /udld aggressive/gm,
  pagp: /^interface .*\r?\n(\s+.*\r?\n)*\s+.*(mode desirable|mode auto).*\r?\n(\s+.*\r?\n)*!/gm,
  lacp: /^interface .*\r?\n(\s+.*\r?\n)*\s+.*(mode active|mode passive).*\r?\n(\s+.*\r?\n)*!/gm,
  on: /^interface .*\r?\n(\s+.*\r?\n)*\s+.*mode on.*\r?\n(\s+.*\r?\n)*!/gm,
  l2ec: /^interface .*\r?\n(\s+.*\r?\n)*\s+switchport mode.*\r?\n(\s+.*\r?\n)*\s+channel-group.*(\s+.*\r?\n)*!/gm,
  pvst: /.*spanning-tree mode pvst.*/gm,
  rstp: /.*spanning-tree mode rapid.*/gm,
  mst: /.*spanning-tree mode mst.*/gm,
  stormBcast:
    /^(interface|template) .*\r?\n(\s+.*\r?\n)*\s+.*(storm-control broadcast).*\r?\n(\s+.*\r?\n)*!/gm,
  stormMcast:
    /^(interface|template) .*\r?\n(\s+.*\r?\n)*\s+.*(storm-control multicast).*\r?\n(\s+.*\r?\n)*!/gm,
  uufb: /^interface .*\r?\n(\s+.*\r?\n)*\s+.*(switchport block unicast).*\r?\n(\s+.*\r?\n)*!/gm,
  access:
    /^interface .*\r?\n(\s+.*\r?\n)*\s+.*(switchport mode access).*\r?\n(\s+.*\r?\n)*!/gm,
  vlan: /^vlan .*\r?\n(\s+.*\r?\n)*!/gm,
  errdisableRec: /.*errdisable recovery cause.*/gm,
  macacl: /.*mac access.*/gm,
  l3ec: /^interface .*\r?\n(\s+.*\r?\n)*\s+no switchport.*\r?\n(\s+.*\r?\n)*\s+channel-group .*(\s+.*\r?\n)*!/gm,
  l3if: /^interface .*\r?\n(\s+.*\r?\n)*\s+no switchport.*\r?\n(\s+.*\r?\n)*!/gm,
  ospfv4:
    /^router ospf .*\r?\n(\s+.*\r?\n)*\s+.*(network).*\r?\n(\s+.*\r?\n)*!/gm,
  eigrpv4:
    /^router eigrp .*\r?\n(\s+.*\r?\n)*\s+.*(network).*\r?\n(\s+.*\r?\n)*!/gm,
  ripv4: /^router rip.*\r?\n(\s+.*\r?\n)*\s+.*(network).*\r?\n(\s+.*\r?\n)*!/gm,
  static: /.*(ip route ).*\r?\n(\s+.*\r?\n)*/gm,
  ipacl: /(ip access.*\r?\n(\s+.*\r?\n)*)+!/gm,
  bfdv4:
    /^(router )([ .\d\w\-\r?\n]+)(bfd all-interfaces).*\r?\n(\s+.*\r?\n)*!/gm,
  ipv6acl: /^ipv6 access.*\r?\n(\s+.*\r?\n)*!/gm,
  eigrpv6:
    /^(router eigrp).*\r?\n(\s+.*\r?\n)*\s+.*(address-family ipv6).*\r?\n(\s+.*\r?\n)*!/gm,
  bfdv6:
    /^(ipv6 router )([ .\d\w\-\r?\n]+)(bfd all-interfaces).*\r?\n(\s+.*\r?\n)*!/gm,
  portsec:
    /^(interface|template) .*\r?\n(\s+.*\r?\n)*\s+.*(switchport port-sec).*\r?\n(\s+.*\r?\n)*!/gm,
  dot1x:
    /^(interface) .*\r?\n(\s+.*\r?\n)*\s+.*(dot1x pae auth).*\r?\n(\s+.*\r?\n)*!/gm,
  mab: /^(interface) .*\r?\n(\s+.*\r?\n)*\s+.*(mab).*\r?\n(\s+.*\r?\n)*!/gm,
  webauth:
    /^(interface) .*\r?\n(\s+.*\r?\n)*\s+.*(webauth).*\r?\n(\s+.*\r?\n)*!/gm,
  vvlan:
    /^(interface) .*\r?\n(\s+.*\r?\n)*\s+.*(voice vlan).*\r?\n(\s+.*\r?\n)*!/gm,
  ctsSAP:
    /^(interface) .*\r?\n(\s+.*\r?\n)*\s+.*(cts man).*\r?\n(\s+.*\r?\n)*!/gm,
  radiusv4:
    /^(radius server) .*\r?\n(\s+.*\r?\n)*\s+.*(address ipv4).*\r?\n(\s+.*\r?\n)*!/gm,
  radiusv6:
    /^(radius server) .*\r?\n(\s+.*\r?\n)*\s+.*(address ipv6).*\r?\n(\s+.*\r?\n)*!/gm,
  tacac: /(^tacac.*\r?\n(\s+.*\r?\n)*!)|(.*tacac.*\r?\n)/gm,
  dhcpSnoop:
    /(^ip dhcp snooping.*\r?\n(\s+.*\r?\n)*!)|(.*ip dhcp snooping.*\r?\n)/gm,
  mcast: /ip multicast-routing/gm,
  mcastv6: /ipv6 multicast-routing/gm,
  igmp: /^interface .*\r?\n(\s+.*\r?\n)*\s+ip igmp.*\r?\n(\s+.*\r?\n)*!/gm,
  pim: /^interface .*\r?\n(\s+.*\r?\n)*\s+ip pim.*\r?\n(\s+.*\r?\n)*!/gm,
  pimv6:
    /^interface .*\r?\n(\s+.*\r?\n)*\s+ip pim.*\r?\n(\s+.*\r?\n)*\s+ipv6 address .*(\s+.*\r?\n)*!/gm,
  mld: /ipv6 mld snooping/gm,
  msdp: /ip msdp.*/gm,
  qos: /^interface .*\r?\n(\s+.*\r?\n)*\s+service-policy.*\r?\n(\s+.*\r?\n)*!/gm,
  police: /^policy-map.*\r?\n(\s+.*\r?\n)*\s+police.*\r?\n!/gm,
  mark: /^policy-map.*\r?\n(\s+.*\r?\n)*\s+set.*\r?\n!/gm,
  shape: /^policy-map.*\r?\n(\s+.*\r?\n)*\s+shape.*\r?\n!/gm,
  fnf: /^flow .*\r?\n(\s+.*\r?\n)*!/gm,
  autoconf: /autoconf enable/gm,
  template:
    /^interface .*\r?\n(\s+.*\r?\n)*\s+source template.*\r?\n(\s+.*\r?\n)*!/gm,
  asp: /^interface .*\r?\n(\s+.*\r?\n)*\s+macro auto.*\r?\n(\s+.*\r?\n)*!/gm,
  svl: /stackwise-virtual.*/gm,
  stack: /switch.*provi.*/gm,
  len_stk: /switch.*provi.*/gm,
  dhcpServer: /^ip dhcp pool.*\r?\n(\s+.*\r?\n)*!/gm,
  dns: /^ip domain.*/gm,
  span: /^monitor session.*destination interface.*/gm,
  rspan: /^monitor session.*remote vlan.*/gm,
  erspan: /erspan/gm,
  http: /^ip http server/gm,
  https: /^ip http secure-server/gm,
  callhome: /^call-home.*/gm,
  tftp: /^tftp-server.*/gm,
  ftp: /^ip ftp.*/gm,
  mgmt: /^interface .*\r?\n(\s+.*\r?\n)*\s+ip vrf forwarding .*\r?\n(\s+.*\r?\n)*!/gm,
  archiveLogging: /^archive.*\r?\n(\s.*\r?\n)*!/gm,
  snmpv1: /^snmp-server.*v1.*/gm,
  snmpv2: /^snmp-server.*v2c.*/gm,
  snmpv3: /^snmp-server.*v3.*/gm,
  snmp: /^snmp-server.*/gm,
  snmpTrap:
    /^interface .*\r?\n(\s+.*\r?\n)*\s+snmp trap.*\r?\n(\s+.*\r?\n)*!/gm,
  syslog: /^logging host.*/gm,
  ssh: /^ip ssh .*/gm,
  telnet: /transport input .*(all|telnet).*/gm,
  mdns: /.*mdns.*/gm,
  mpls: /^interface .*\r?\n(\s+.*\r?\n)*\s+mpls ip.*\r?\n(\s+.*\r?\n)*!/gm,

  // new policy
  autoQos: /^interface .*\r?\n(\s+.*\r?\n)*\s+auto qos.*\r?\n(\s+.*\r?\n)*!/gm,
  Copp: /service-policy input system-cpp-policy/gm,
  ecIngressQos:
    /^interface Port-channel .*\r?\n(\s+.*\r?\n)*\s+service-policy input.*\r?\n(\s+.*\r?\n)*!/gm,
  ecEgressQos:
    /^interface Port-channel .*\r?\n(\s+.*\r?\n)*\s+service-policy output.*\r?\n(\s+.*\r?\n)*!/gm,
  ingressPolicing:
    /^policy-map .*\r?\n(\s+.*\r?\n)*\s+police rate.*\r?\n(\s+.*\r?\n)*!/gm,
  egressPolicing:
    /^policy-map .*\r?\n(\s+.*\r?\n)*\s+police rate.*\r?\n(\s+.*\r?\n)*!/gm,
  egressShping:
    /^policy-map .*\r?\n(\s+.*\r?\n)*\s+shape.*\r?\n(\s+.*\r?\n)*!/gm,
  WRED: /^policy-map .*\r?\n(\s+.*\r?\n)*\s+random-detect.*\r?\n(\s+.*\r?\n)*!/gm,
  QoSSharing:
    /^policy-map .*\r?\n(\s+.*\r?\n)*\s+bandwidth.*\r?\n(\s+.*\r?\n)*!/gm,
  Inv4Acl:
    /^interface .*\r?\n(\s+.*\r?\n)*\s+ip access-group.*in.*\r?\n(\s+.*\r?\n)*!/gm,
  Egressv4Acl:
    /^interface .*\r?\n(\s+.*\r?\n)*\s+ip access-group.*out.*\r?\n(\s+.*\r?\n)*!/gm,
  Inv6Acl:
    /^interface .*\r?\n(\s+.*\r?\n)*\s+ipv6 traffic-filter.*in.*\r?\n(\s+.*\r?\n)*!/gm,
  Egressv6Acl:
    /^interface .*\r?\n(\s+.*\r?\n)*\s+ipv6 traffic-filter.*out.*\r?\n(\s+.*\r?\n)*!/gm,
  v4OGACL:
    /^ip access-list .*\r?\n(\s+.*\r?\n)*\s+object-group.*\r?\n(\s+.*\r?\n)*!/gm,
  v6OGACL:
    /^ipv6 access-list .*\r?\n(\s+.*\r?\n)*\s+object-group.*\r?\n(\s+.*\r?\n)*!/gm,
  fnfSGT:
    /^flow record .*\r?\n(\s+.*\r?\n)*\s+match flow cts.*\r?\n(\s+.*\r?\n)*!/gm,
  fnfV6: /.*ipv6 flow monitor.*/gm,

  // new mpls
  ldp: /^interface .*\r?\n(\s+.*\r?\n)*\s+mpls ip.*\r?\n(\s+.*\r?\n)*!/gm,
  mplsTE:
    /^interface Tunnel .*\r?\n(\s+.*\r?\n)*\s+tunnel mode mpls traffic-eng.*\r?\n(\s+.*\r?\n)*!/gm,
  vpnv4:
    /^router bgp .*\r?\n(\s+.*\r?\n)*\s+address-family vpnv4.*\r?\n(\s+.*\r?\n)*!/gm,
  vpnv6:
    /^router bgp .*\r?\n(\s+.*\r?\n)*\s+address-family vpnv6.*\r?\n(\s+.*\r?\n)*!/gm,
  l2vpn:
    /^router bgp .*\r?\n(\s+.*\r?\n)*\s+address-family l2vpn vpls.*\r?\n(\s+.*\r?\n)*!/gm,
  '6pe':
    /^router bgp .*\r?\n(\s+.*\r?\n)*\s+template peer-policy.*\r?\n(\s+.*\r?\n)*!/gm,
  bgpLU:
    /^router bgp .*\r?\n(\s+.*\r?\n)*\s+template peer-policy.*\r?\n(\s+.*\r?\n)*!/gm,
  mvpn: /^router bgp .*\r?\n(\s+.*\r?\n)*\s+address-family ipv4 mdt.*\r?\n(\s+.*\r?\n)*!/gm,
  ngMvpn:
    /^router bgp .*\r?\n(\s+.*\r?\n)*\s+address-family ipv4 mvpn.*\r?\n(\s+.*\r?\n)*!/gm,

  // new security
  qnq: /^interface .*\r?\n(\s+.*\r?\n)*\s+switchport vlan mapping.*\r?\n(\s+.*\r?\n)*!/gm,
  macsec: /^interface .*\r?\n(\s+.*\r?\n)*\s+mka policy.*\r?\n(\s+.*\r?\n)*!/gm,
  ctsSGTMAP: /.*cts role-based sgt-map.*/gm,
  httpLocalAuth: /.*ip http authentication local.*/gm,
  SXP: /.*cts sxp enable.*/gm,
  CoA: /.*aaa server radius dynamic-author.*/gm,
  accounting: /.*aaa accounting.*/gm,
  v6RAGuard:
    /^interface .*\r?\n(\s+.*\r?\n)*\s+ipv6 nd raguard.*\r?\n(\s+.*\r?\n)*!/gm,

  // new layer 3
  bfd: /^interface .*\r?\n(\s+.*\r?\n)*\s+bfd interval.*\r?\n(\s+.*\r?\n)*!/gm,
  l3_udld: /^interface .*\r?\n(\s+.*\r?\n)*\s+udld.*\r?\n(\s+.*\r?\n)*!/gm, // duplicate
  hsrp: /^interface .*\r?\n(\s+.*\r?\n)*\s+standby.*\r?\n(\s+.*\r?\n)*!/gm,
  'bfd-template':
    /^bfd-template .*\r?\n(\s+.*\r?\n)*\s+interval min-tx.*\r?\n(\s+.*\r?\n)*!/gm,

  // new layer 2
  dhcpSnooping:
    /^interface .*\r?\n(\s+.*\r?\n)*\s+ip dhcp snooping.*\r?\n(\s+.*\r?\n)*!/gm,

  // new mcast
  igmpStaticJoin:
    /^interface .*\r?\n(\s+.*\r?\n)*\s+ip igmp join-group.*\r?\n(\s+.*\r?\n)*!/gm,

  // new program
  netconf: /.*netconf-yang.*/gm,

  // =============== new category ===============
  // misc
  snmp_trap: /.*snmp-server enable traps.*/gm,
  // evpn
  evpnEnable: /.*l2vpn evpn.*/gm,
  evpn_bgp:
    /^router bgp .*\r?\n(\s+.*\r?\n)*\s+address-family l2vpn evpn.*\r?\n(\s+.*\r?\n)*!/gm, // duplicate
  l2vni:
    /^l2vpn evpn instance .*\r?\n(\s+.*\r?\n)*\s+encapsulation vxlan.*\r?\n(\s+.*\r?\n)*!/gm,
  l3vni:
    /^vlan configuration .*\r?\n(\s+.*\r?\n)*\s+member vni.*\r?\n(\s+.*\r?\n)*!/gm,
  l3trmV4:
    /^vrf definition .*\r?\n(\s+.*\r?\n)*\s+mdt auto-discovery vxlan.*\r?\n(\s+.*\r?\n)*!/gm,
  l3trmV6:
    /^router bgp .*\r?\n(\s+.*\r?\n)*\s+address-family ipv6 mvpn.*\r?\n(\s+.*\r?\n)*!/gm,
  // sda
  ipv4Overlay:
    /^router lisp .*\r?\n(\s+.*\r?\n)*\s+service ipv4.*\r?\n(\s+.*\r?\n)*!/gm,
  ipv6Overlay:
    /^router lisp .*\r?\n(\s+.*\r?\n)*\s+service ipv6.*\r?\n(\s+.*\r?\n)*!/gm,
  l2Overlay:
    /^router lisp .*\r?\n(\s+.*\r?\n)*\s+service ethernet.*\r?\n(\s+.*\r?\n)*!/gm,
  multicast:
    /^interface LISP0 .*\r?\n(\s+.*\r?\n)*\s+ip pim.*\r?\n(\s+.*\r?\n)*!/gm,
  controlPlane:
    /^router lisp .*\r?\n(\s+.*\r?\n)*\s+eid-record instance-id.*\r?\n(\s+.*\r?\n)*!/gm,
};

export const confDefaultTrueList = ['vtp', 'cdp', 'lldp', 'l2_udld'];

export const withoutConfList = {
  isis: 'shut',
  l3_bgp: 'shut',
  tunnel: 'shutdown',
  l3dot1q: 'shutdown',
  svi: 'shutdown',
  ospfv6: 'shut',
  trunk: 'switchport mode access',
};
