from meraki_sdk.meraki_sdk_client import MerakiSdkClient
from meraki_sdk.exceptions.api_exception import APIException
from datetime import datetime
from re import search
import meraki as m
import sys

rules = [

    {
        'comment': 'Allow ATL DNS',
        'policy': 'allow',
        'protocol': 'TCP',
        'destPort': '53',
        'destCidr': '8.8.8.8'
    },

    {
        'comment': 'Allow ATL DNS',
        'policy': 'allow',
        'protocol': 'UDP',
        'destPort': '53',
        'destCidr': '8.8.8.8'
    },

    {
        'comment': 'Allow ATL DNS',
        'policy': 'allow',
        'protocol': 'TCP',
        'destPort': '53',
        'destCidr': '8.8.4.4'
    },

    {
        'comment': 'Allow ATL DNS',
        'policy': 'allow',
        'protocol': 'UDP',
        'destPort': '53',
        'destCidr': '8.8.4.4'
    },

    {
        'comment': 'Allow ATL NTP',
        'policy': 'allow',
        'protocol': 'UDP',
        'destPort': '123',
        'destCidr': '1.1.1.1'
    },

    {
        'comment': 'Allow ATL NTP',
        'policy': 'allow',
        'protocol': 'UDP',
        'destPort': '123',
        'destCidr': '1.1.2.2'
    },

    {
        'comment': 'Allow ATL SNMP',
        'policy': 'allow',
        'protocol': 'UDP',
        'destPort': '161',
        'destCidr': '8.8.4.45'
    },

    {
        'comment': 'Allow ATL SNMP',
        'policy': 'allow',
        'protocol': 'TCP',
        'destPort': '161',
        'destCidr': '8.8.4.45'
    },

    {
        'comment': 'Allow ATX DNS',
        'policy': 'allow',
        'protocol': 'TCP',
        'destPort': '53',
        'destCidr': '4.4.4.4'
    },

    {
        'comment': 'Allow ATX DNS',
        'policy': 'allow',
        'protocol': 'UDP',
        'destPort': '53',
        'destCidr': '4.4.4.4'
    },

    {
        'comment': 'Allow ATX DNS',
        'policy': 'allow',
        'protocol': 'TCP',
        'destPort': '53',
        'destCidr': '4.4.8.8'
    },

    {
        'comment': 'Allow ATX DNS',
        'policy': 'allow',
        'protocol': 'UDP',
        'destPort': '53',
        'destCidr': '4.4.8.8'
    },

    {
        'comment': 'Allow ATX NTP',
        'policy': 'allow',
        'protocol': 'UDP',
        'destPort': '123',
        'destCidr': '4.4.5.5'
    },

    {
        'comment': 'Allow ATX NTP',
        'policy': 'allow',
        'protocol': 'UDP',
        'destPort': '123',
        'destCidr': '4.4.6.6'
    },

    {
        'comment': 'Allow LAN',
        'policy': 'allow',
        'protocol': 'Any',
        'destPort': 'Any',
        'destCidr': '10.0.26.0/24'
    },

    {
        'comment': 'Deny Internal 10.0.0.0/8',
        'policy': 'deny',
        'protocol': 'Any',
        'destPort': 'Any',
        'destCidr': '10.0.0.0/8'
    },

    {
        'comment': 'Deny Internal 192.168.0.0/16',
        'policy': 'deny',
        'protocol': 'Any',
        'destPort': 'Any',
        'destCidr': '192.168.0.0/16'
    },

    {
        'comment': 'Deny Internal 172.16.0.0/12',
        'policy': 'deny',
        'protocol': 'Any',
        'destPort': 'Any',
        'destCidr': '172.16.0.0/12'
    }
]

def get_site_name(network_id): 
    return meraki.networks.get_network(network_id)['name']

def get_all_site_vlans(network_id):
    return meraki.vlans.get_network_vlans(network_id)

def get_all_site_ssids(network_id):
    return meraki.ssids.get_network_ssids(network_id)

def firewall_rule_add(site, rules):
    mk.mr_l3_firewall.updateNetworkSsidL3FirewallRules(site['network_id'], site['ssid_number'], rules)

def network_id_list_creation(network_object_list, network_id_list):
    for network_object in network_object_list:
        if search(r'\bSITE-NAME\b', network_object['name']): # This is only needed if you need to filter out certain sites.
            network_id_list.append(network_object['id'])

def new_ssid_creation(network_id_list):
    for network_id in network_id_list:
        mk.ssids.updateNetworkSsid(
            network_id, 
            3,  # SSID Number
            name='SSID-NAME', 
            enabled=False,
            splashPage=None,
            authMode='open-with-radius',
            ipAssignmentMode='Bridge mode', 
            radiusServers=[{'host': '10.1.1.1', 'port': 1812, 'secret': 'password'}, {'host': '10.1.1.2', 'port': 1812, 'secret': 'password'}],
            radiusCoaEnabled=True, 
            radiusAccountingEnabled=True,
            radiusAccountingServers= [{'host': '10.1.1.1', 'port': 1813, 'secret': 'password'}, {'host': '10.1.1.2', 'port': 1813, 'secret': 'password'}],
            radiusAttributeForGroupPolicies='Airespace-ACL-Name',
            radiusFailoverPolicy=None,
            useVlanTagging=True,
            defaultVlanId=19,
            radiusOverride=False,
            minBitrate=11,
            bandSelection='Dual band operation with Band Steering',
            perClientBandwidthLimitUp=0,
            perClientBandwidthLimitDown=0
        )
        print('{}: INFO: Created SSID-NAME SSID for {}...'.format(datetime.now(), get_site_name(network_id)))

def ssid_filter(ssid_object):
    for ssid in ssid_object:
        if search(r'\bSSID-NAME\b', ssid['name']): # Update the regex string to whatever SSID name you are trying to find.
            return ssid

def vlan_filter(vlan_object):
    for vlan in vlan_object: 
        if search(r'\bVLAN-NAME\b', vlan['name']): # Update the regex string to whatever VLAN name you are trying to find.
            return vlan

def site_parser(network_id_list):
    for network_id in network_id_list:
        try:
            site_vlans = get_all_site_vlans(network_id)
            site_ssids = get_all_site_ssids(network_id)
        except:
            pass
        print('{}: INFO: Parsing {} for SSID and VLAN information...'.format(datetime.now(), get_site_name(network_id)))
        ssid = ssid_filter(site_ssids)
        vlan = vlan_filter(site_vlans)
        site_object_creation(network_id, ssid, vlan)

def site_object_creation(network_id, ssid, vlan):
    try:
        obj = {}
        obj['network_id'] = network_id
        obj['site_name'] = get_site_name(network_id)
        obj['subnet'] = vlan['subnet']
        obj['vlan_name'] = vlan['name']
        obj['vlan_id'] = vlan['id']
        obj['ssid_name'] = ssid['name']
        obj['ssid_number'] = ssid['number']
        site_objects.append(obj)
        print('{}: INFO: Successfully created {} site object...'.format(datetime.now(), get_site_name(network_id))) 
    except:
        pass

def rules_update(site_objects, rules):
    for site in site_objects:
        for rule in rules:
            if rule['comment'] == 'Allow LAN': # This updates the Allow LAN firewall rule to the VLAN subnet for that specific site.
                rule['destCidr'] = site['subnet']
        print('{}: INFO: Firewall Rules for {} are being processed'.format(datetime.now(), site['site_name']))
        firewall_rule_add(site, rules)
    
def object_pprint(objects): # This is just a pretty print method for troubleshooting.
    for obj in objects:
        print('\n{')
        for key in obj:
            print('    {}: {}'.format(key, obj[key]))
        print('}\n') 

if __name__ == '__main__':
    starttime = datetime.now()
    api_key = input("Enter your Meraki Dashboard API Key: ")
    organization_id = input("Enter your Meraki Organization ID: ")
    site_objects = []
    network_id_list = []
    print('{}: INFO: Initiating API session...'.format(datetime.now()))
    meraki = MerakiSdkClient(x_cisco_meraki_api_key = api_key)
    mk = m.DashboardAPI(api_key)
    network_object_list = meraki.networks.get_organization_networks({'organization_id': organization_id})
    print('{}: INFO: Creating Network ID list...'.format(datetime.now()))
    network_id_list_creation(network_object_list, network_id_list)
    print('{}: INFO: Creating New SSID-NAME SSIDs...'.format(datetime.now()))
    new_ssid_creation(network_id_list)
    print('{}: INFO: Parsing Network ID list to create site objects...'.format(datetime.now()))
    site_parser(network_id_list)
    print('{}: INFO: Finished creating site objects...'.format(datetime.now()))
    rules_update(site_objects, rules)
    endtime = datetime.now()
    runtime = endtime - starttime
    print("Total Runtime: {}".format(runtime))


# Devnet sandbox organization id: '549236'