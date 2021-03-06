#! Python3

from datetime import datetime as dt
from re import match
import meraki
import csv
import sys

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
            print(f"{org['name']}: {org['id']}")
        organization_id = input("Enter the Organization ID: ")

        temps = m.organizations.getOrganizationConfigTemplates(organization_id)
        print("\nConfiguration Template IDs")
        print("-"*25)
        for temp in temps:
            print(f"{temp['name']}: {temp['id']}")

        template_id = ""
        user_input = ""
        while True:
            user_input = input("Enter a configuration template ID: ")
            if match(r'[N_|L_]\d*', user_input):
                template_id = user_input
                break
            else:
                print("Invalid Entry.")
        
        input_file = input("Enter the file path for the input file for bulk network creation: ")

        with open(input_file, "r") as ifile:
            network_file = csv.reader(ifile, delimiter=',', quotechar='|')
            for row in network_file:
                serial = row[0].rstrip()
                network_name = row[1].rstrip()
                address = row[2].rstrip()
                # notes = row[3].rstrip()
                
                network_id = m.organizations.createOrganizationNetwork(
                    organization_id, 
                    name=network_name, 
                    productTypes=["appliance"], 
                    tags=["PRODUCTION_WFH"]
                    )["id"]

                m.networks.bindNetwork(network_id, template_id)
                m.networks.claimNetworkDevices(network_id, serials=[serial])
                m.devices.updateDevice(serial, name=network_name, address=address)

                # device_name = row[4]
                # network_id = m.devices.getDevice(serial)['networkId']
                # m.networks.updateNetwork(network_id, name=network_name, tags=["PRODUCTION_WFH"])


    except KeyboardInterrupt:
        # Except statement is to clean up keyboard interrupt output. 
        # This stops the whole call stack from being output to the CLI.
        print(f"{dt.now()} ERROR: Keyboard Interrupt.")

    # Calculating total runtime
    end_time = dt.now()
    total_runtime = end_time - start_time
    print(f"{dt.now()} INFO: Total Runtime > {total_runtime}")