from datetime import datetime as dt
from time import sleep
from re import match
import meraki
import sys

if __name__ == "__main__":
    
    start_time = dt.now()

    try:
        # Unique Meraki API key from the Meraki Dashboard
        api_key = "7e1b8674f0cd64850602befdc8b4941bab1e28a7"

        # Initiating the API session and creating API object to use in API queries
        m = meraki.DashboardAPI(api_key)
        
        organization_id = "630503947831870169"
        template_id = "N_630503947831950784"
        output_file = "C:\\Users\\lamin\\OneDrive\\Documents\\Repos\\Meraki\\network_names_and_serials.txt"
        input_file = "C:\\Users\\lamin\\OneDrive\\Documents\\Repos\\Meraki\\Prod2_Offline_Networks.txt"

        networks = m.organizations.getOrganizationNetworks(organization_id, perPage=10000, configTemplateId=template_id)
        org_devices = m.organizations.getOrganizationDevicesStatuses(organization_id, total_pages="All")

        search_list = {}
        for network in networks:
            search_list[network["name"]] = network["id"]
        
        last_reported_data = {}
        for device in org_devices:
            last_reported_data[device["serial"]] = device["lastReportedAt"]

        offline_networks = []
        with open(input_file, "r") as ifile:
            for network in ifile:
                network_id = search_list[network.rstrip()]
                offline_networks.append(network_id)
        ifile.close()
        
        with open(output_file, "w") as ofile:
            for network in offline_networks:
                device_serial = m.networks.getNetworkDevices(network)[0]["serial"]
                last_seen = last_reported_data[device_serial]
                ofile.write(f"{device_serial},{last_seen}\n")
                sleep(.001)
        ofile.close()

    except KeyboardInterrupt:
        # Except statement is to clean up keyboard interrupt output. 
        # This stops the whole call stack from being output to the CLI.
        print(f"{dt.now()} ERROR: Keyboard Interrupt.")

    # Calculating total runtime
    end_time = dt.now()
    total_runtime = end_time - start_time
    print(f"{dt.now()} INFO: Total Runtime > {total_runtime}")