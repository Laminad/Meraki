from datetime import datetime as dt
from re import match
import meraki
import sys

def network_search(site_name, org_id):
    organization_networks = m.networks.getOrganizationNetworks(org_id)
    for network in organization_networks:
        if match(site_name, network['name']):
            return network['id']

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

        device_serial = input("Enter the Device Serial number to remove: ")
        site_name = input("Enter the Network name the device is associated with: ")
        print(site_name)
        network_id = network_search(site_name, organization_id)
        print(network_id)

        m.devices.removeNetworkDevice(network_id, device_serial)


    except KeyboardInterrupt:
        # Except statement is to clean up keyboard interrupt output. 
        # This stops the whole call stack from being output to the CLI.
        print("{} ERROR: Keyboard Interrupt.".format(dt.now()))


    # Calculating total runtime
    end_time = dt.now()
    total_runtime = end_time - start_time
    print("{} INFO: Total Runtime > {}".format(dt.now(), total_runtime))