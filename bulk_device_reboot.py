#! Python3

from datetime import datetime as dt
from meraki.exceptions import APIError
import meraki
import sys

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

        input_file = input("Enter the file path of the Meraki serials reboot: ") 

        with open(input_file, 'r') as ifile:
            for serial in ifile:
                try:
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