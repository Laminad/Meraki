from datetime import datetime as dt
from re import search
import meraki
import sys

def network_search(site_name, org_id):
    organization_networks = m.networks.getOrganizationNetworks(org_id)
    for network in organization_networks:
        if search(site_name, network['name']):
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

        network_ids_to_update = []

        input_file = ("Enter the file of network names to update: ")
        with open(input_file, "r") as ifile:
            for network_name in ifile:
                site_name = network_name
                network_id = network_search(site_name, organization_id)
                network_ids_to_update.append(network_id)
        ifile.close()

        for network_id in network_ids_to_update:
            network_name = m.networks.getNetwork(network_id)['name']
            response = m.networks.updateNetwork(network_id, name=network_name+'-Migrated')

    except KeyboardInterrupt:
        # Except statement is to clean up keyboard interrupt output. 
        # This stops the whole call stack from being output to the CLI.
        print("{} ERROR: Keyboard Interrupt.".format(dt.now()))

    # Calculating total runtime
    end_time = dt.now()
    total_runtime = end_time - start_time
    print("{} INFO: Total Runtime > {}".format(dt.now(), total_runtime))