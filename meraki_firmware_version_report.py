from datetime import datetime as dt
from time import sleep
from re import match
import meraki

if __name__ == "__main__":
    
    start_time = dt.now()
    orgs = ["388603", "630503947831870169", "630503947831871207"]
    data = {}
    models =  []
    firmware = {}

    try:
        # Unique Meraki API key from the Meraki Dashboard
        api_key = "7e1b8674f0cd64850602befdc8b4941bab1e28a7"

        # Initiating the API session and creating API object to use in API queries
        m = meraki.DashboardAPI(api_key)

        output_file = "C:\\Users\\lamin\\OneDrive\\Documents\\Repos\\Meraki\\firmware_version_report.txt"

        with open(output_file, "w") as ofile:
            ofile.write("Organization,Network,Model,Serial,Firmware\n")
            for org in orgs:
                devices = m.organizations.getOrganizationDevices(org, total_pages="all")
                org_name = m.organizations.getOrganization(org)["name"]
                data[org_name] = models
                for device in devices:
                    model = device["model"]
                    serial = device["serial"]
                    firmware = device["firmware"]
                    if match(firmware, "Not running configured version"):
                        pass
                    else:
                        # Need to create a relational data structure here to associate the organization name with
                        # It's device types, firmware versions, and total counts of those firmware versions
                        sleep(.01)


    except KeyboardInterrupt:
        # Except statement is to clean up keyboard interrupt output. 
        # This stops the whole call stack from being output to the CLI.
        print(f"{dt.now()} ERROR: Keyboard Interrupt.")

    # Calculating total runtime
    end_time = dt.now()
    total_runtime = end_time - start_time
    print(f"\n{dt.now()} INFO: Total Runtime > {total_runtime}\n")
    