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

        # Outputting the organization config templates and asking the user to select the
        # specific templates they want the client information from.
        temps = m.config_templates.getOrganizationConfigTemplates(organization_id)
        print("\nConfiguration Template IDs")
        print("-"*25)
        for temp in temps:
            print("{}: {}".format(temp['name'], temp['id']))

        config_template_id = ""
        user_input = "L_123"
        while True:
            user_input = input("Enter a configuration template ID or 0 to end: ")
            if user_input !="0" and match(r'[N_|L_]\d*', user_input):
                config_template_id = user_input
                break
            else:
                print("Invalid Entry.")

        site_name = input("Enter the Network name the device is associated with: ")
        network_id = network_search(site_name, organization_id)
        status = m.networks.bindNetwork(network_id, config_template_id)


    except KeyboardInterrupt:
        # Except statement is to clean up keyboard interrupt output. 
        # This stops the whole call stack from being output to the CLI.
        print("{} ERROR: Keyboard Interrupt.".format(dt.now()))

    # Calculating total runtime
    end_time = dt.now()
    total_runtime = end_time - start_time
    print("{} INFO: Total Runtime > {}".format(dt.now(), total_runtime))