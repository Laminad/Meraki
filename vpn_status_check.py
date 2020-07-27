from datetime import datetime as dt
from re import match
import meraki
import sys

# A function that creates a list of devices associated with a specific device template in the Meraki dashboard.
def network_device_list_generator(org_id):
    network_devices = []
    network_devices = m.networks.getOrganizationNetworks(org_id)
    return network_devices

# A function that takes a list network devices and creates a list of their network IDs.
def network_id_list_generator(net_devices, site_name):
    network_ids = []
    for device in net_devices:
        if match(site_name, device['name']):
            network_ids.append(device['id'])
    return network_ids

def get_vpn_status(net_ids):
    vpn_status = []
    vpn_status.append(m.networks.getNetworkSiteToSiteVpn(net_ids))
    return vpn_status


if __name__ == "__main__":
    
    start_time = dt.now()

    try:
        # Unique Meraki API key from the Meraki Dashboard
        api_key = input("Enter your Meraki API key: ")

        # Initiating the API session and creating API object to use in API queries
        m = meraki.DashboardAPI(api_key)
        
        # Outputting the Organization IDs and asking the user to input the organization they are working on.
        orgs = m.organizations.getOrganizations()
        print("\nOrganization IDs")
        print("-"*25)
        for org in orgs:
            print("{}: {}".format(org['name'], org['id']))
        organization_id = input("Enter the Organization ID: ")
        site_name = input("Enter the name of the site to check VPN status for: ") 
            
        # Getting the network_devices using the network_device_list function
        print("{} INFO: Finding the specific network".format(dt.now()))
        print("-"*120)
        net_devices = network_device_list_generator(organization_id)

        # Getting the network IDs using the network device list generated and the network_id_list function.
        print("{} INFO: Generating the list of network IDs associated with the network devices.".format(dt.now()))
        print("-"*120)
        net_ids = network_id_list_generator(net_devices, site_name)
        print("{} INFO: Network ID List created successfully.".format(dt.now()))

        # Creating the Network Name, Serial, Manufacturer, and MAC list using the device_export function.
        print("{} INFO: Generating the device name and mgmt IP objects associated for the specific network IDs.".format(dt.now()))
        print("-"*120)
        get_vpn_status(net_ids)

    except KeyboardInterrupt:
        # Except statement is to clean up keyboard interrupt output. 
        # This stops the whole call stack from being output to the CLI.
        print("{} ERROR: Keyboard Interrupt.".format(dt.now()))


    # Calculating total runtime
    end_time = dt.now()
    total_runtime = end_time - start_time
    print("{} INFO: Total Runtime > {}".format(dt.now(), total_runtime))