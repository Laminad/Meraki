from datetime import datetime as dt
import re
import meraki
import sys

def network_search(site_name, org_networks):
    for network in org_networks:
        if re.match(site_name, network['name']):
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
        input_file = input("Enter the file of network names to update: ")
        organization_networks = m.networks.getOrganizationNetworks(organization_id)
        networks_to_update = []

        with open(input_file, "r", encoding="UTF-8") as ifile:
            for network in ifile:
                print(network)
                network_id = network_search(network, organization_networks)
                print(network_id)
                network_name = m.networks.getNetwork(network_id)['name']
                print(network_name)
                response = m.networks.updateNetwork(network_id, name=network_name+'-Migrating')
        ifile.close()

    except KeyboardInterrupt:
        # Except statement is to clean up keyboard interrupt output. 
        # This stops the whole call stack from being output to the CLI.
        print("{} ERROR: Keyboard Interrupt.".format(dt.now()))

    # Calculating total runtime
    end_time = dt.now()
    total_runtime = end_time - start_time
    print("{} INFO: Total Runtime > {}".format(dt.now(), total_runtime))