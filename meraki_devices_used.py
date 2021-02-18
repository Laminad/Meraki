#! Python3

from datetime import datetime as dt
from time import sleep
from re import search
import meraki
import sys

if __name__ == "__main__":
    
    start_time = dt.now()

    try:
        # Unique Meraki API key from the Meraki Dashboard
        api_key = "7e1b8674f0cd64850602befdc8b4941bab1e28a7"

        # Initiating the API session and creating API object to use in API queries
        m = meraki.DashboardAPI(api_key)

        output_file = "C:\\Users\\lamin\\OneDrive\\Documents\\Repos\\Meraki\\devices_report.csv"

        with open(output_file, "w") as ofile:

            orgs = m.organizations.getOrganizations()
            stats = {}

            for org in orgs:
                count = 0
                devices = m.organizations.getOrganizationInventoryDevices(
                    org['id'],
                    total_pages="all",
                    startingAfter="2020-03-01T00:00:00.000000Z",
                    usedState="used"
                )
                
                org_name = org['name']

                for device in devices:
                    serial = device['serial']
                    model = device['model']
                    claimed_date = device["claimedAt"]
                    if claimed_date >= "2020-03-01T00:00:00.000000Z":
                        network = m.networks.getNetwork(device["networkId"])['name']
                        if not search("SPARE", network):
                            ofile.write(f"{org_name},{network},{serial},{model},{claimed_date}\n")
                            count += 1
                    sleep(.02)

                stats[org_name] = count

            print("\n")
            for key in stats:
                print(f"{key}: {stats[key]}")


    except KeyboardInterrupt:
        # Except statement is to clean up keyboard interrupt output. 
        # This stops the whole call stack from being output to the CLI.
        print(f"{dt.now()} ERROR: Keyboard Interrupt.")

    # Calculating total runtime
    end_time = dt.now()
    total_runtime = end_time - start_time
    print(f"\n{dt.now()} INFO: Total Runtime > {total_runtime}\n")