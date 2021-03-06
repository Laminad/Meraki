#! Python3

from datetime import datetime as dt
from meraki.exceptions import APIError
from re import match
import meraki


if __name__ == "__main__":
    
    start_time = dt.now()

    try:
        # Unique Meraki API key from the Meraki Dashboard
        api_key = input("Enter your Meraki API key: ")

        # Initiating the API session and creating API object to use in API queries
        m = meraki.DashboardAPI(api_key)
        
        # Outputting the Organization IDs and asking the user to 
        # input the organization they are working on.
        orgs = m.organizations.getOrganizations()
        print("\nOrganization IDs")
        print("-"*25)
        for org in orgs:
            print(f"{org['name']}: {org['id']}")     
        organization_id = input("Enter the Organization ID: ")

        # Outputting the organization config templates and asking the user to select the
        # specific templates they want the want to rebind the devices to.
        temps = m.organizations.getOrganizationConfigTemplates(organization_id)
        print("\nConfiguration Template IDs")
        print("-"*25)
        for temp in temps:
            print(f"{temp['name']}: {temp['id']}")

        config_template_id = ""
        user_input = "L_123"
        while True:
            user_input = input("Enter the configuration template ID to rebind the networks to: ")
            if user_input !="0" and match(r'[N_|L_]\d*', user_input):
                config_template_id = user_input
                break
            else:
                print("Invalid Entry.")

        template_networks = m.organizations.getOrganizationNetworks(organization_id, configTemplateId=config_template_id)

        for network in template_networks:
            network_id = network["id"]
            try:
                serial = m.networks.getNetworkDevices(network_id)[0]["serial"]
                m.devices.rebootDevice(serial.rstrip())
            except APIError:
                pass
                
    except KeyboardInterrupt:
        # Except statement is to clean up keyboard interrupt output. 
        # This stops the whole call stack from being output to the CLI.
        print(f"{dt.now()} ERROR: Keyboard Interrupt.")

    # Calculating total runtime
    end_time = dt.now()
    total_runtime = end_time - start_time
    print(f"{dt.now()} INFO: Total Runtime > {total_runtime}")