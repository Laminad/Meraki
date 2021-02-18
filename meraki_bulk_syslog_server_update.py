#! Python3

from datetime import datetime as dt
from re import match
import meraki
import csv
import sys


if __name__ == "__main__":
    
    start_time = dt.now()

    try:
        m = meraki.DashboardAPI("7e1b8674f0cd64850602befdc8b4941bab1e28a7")
        organization_id = "630503947831870169"
        networks = m.organizations.getOrganizationNetworks(organization_id, perPage=10000, total_pages="all")
        input_file = "C:\\Users\\lamin\\OneDrive\\Documents\\Repos\\Meraki\\network_names_and_syslog_server_role.csv"

        search_list = {}
        for network in networks:
            search_list[network["name"]] = network["id"]

        with open(input_file, "r") as ifile:
            network_file = csv.reader(ifile, delimiter=',', quotechar='|')
            for line in network_file:
                network_name = line[0]
                server_role = line[1]
                network_id = search_list[network_name.rstrip()]
                syslog_servers = [
                    {
                        "host": "172.19.35.245", 
                        "port": 514, 
                        "roles": [server_role]
                    },
                    {
                        "host":"172.19.34.21",
                        "port":514,
                        "roles":["Flows","URLs","Security events","Appliance event log"]
                    }
                ]
                m.networks.updateNetworkSyslogServers(network_id, syslog_servers)
                    
                    
    except KeyboardInterrupt:
        # Except statement is to clean up keyboard interrupt output. 
        # This stops the whole call stack from being output to the CLI.
        print(f"{dt.now()} ERROR: Keyboard Interrupt.")

    # Calculating total runtime
    end_time = dt.now()
    total_runtime = end_time - start_time
    print(f"{dt.now()} INFO: Total Runtime > {total_runtime}")