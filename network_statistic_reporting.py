#! Python3

from datetime import datetime as dt
from time import sleep
import meraki


if __name__ == "__main__":
    
    start_time = dt.now()
    organization_ids = ["388603", "630503947831870169"]

    try:
        # Unique Meraki API key from the Meraki Dashboard
        api_key = "7e1b8674f0cd64850602befdc8b4941bab1e28a7"

        # Initiating the API session and creating API object to use in API queries
        m = meraki.DashboardAPI(api_key)

        output_file = "C:\\Users\\lamin\\OneDrive - Presidio Networked Solutions, Inc\\LabCorp\\network_statistics.txt"

        with open(output_file, "w") as ofile:
            ofile.write("Organization Name:Network Name:Packet Loss:Latency\n")
            for organization_id in organization_ids:
                organization_statistics = m.organizations.getOrganizationDevicesUplinksLossAndLatency(organization_id, timespan=90)
                organization_name = m.organizations.getOrganization(organization_id)["name"]
                for network in organization_statistics:
                    network_id = network["networkId"]
                    network_name = m.networks.getNetwork(network_id)["name"]
                    network_loss = network["timeSeries"][0]["lossPercent"]
                    network_latency = network["timeSeries"][0]["latencyMs"]
                    ofile.write(f"{organization_name}:{network_name}:{network_loss}:{network_latency}\n")
                    sleep(.1)

        
    except KeyboardInterrupt:
        # Except statement is to clean up keyboard interrupt output. 
        # This stops the whole call stack from being output to the CLI.
        print(f"{dt.now()} ERROR: Keyboard Interrupt.")

    # Calculating total runtime
    end_time = dt.now()
    total_runtime = end_time - start_time
    print(f"{dt.now()} INFO: Total Runtime > {total_runtime}")