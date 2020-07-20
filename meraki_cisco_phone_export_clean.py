from datetime import datetime as dt
from re import search
import meraki
import sys

# A pretty print method for simple JSON objects.
def object_pprint(objects):
    for obj in objects:
        print('\n{')
        for key in obj:
            print('    {}: {}'.format(key, obj[key]))
        print('}\n') 

# A function that creates a list of devices associated with a specific device template in the Meraki dashboard.
def network_device_list_generator(org_id, template):
    network_devices = []
    network_devices = m.networks.getOrganizationNetworks(org_id, configTemplateId=template)
    return network_devices

# A function that takes a list network devices and creates a list of their network IDs.
def network_id_list_generator(net_devices):
    network_ids = []
    for device in net_devices:
        network_ids.append(device['id'])
    return network_ids

# A functions that takes a network id list and output file and exports 
# the Cisco clients, network name, Meraki serial, and client MAC address to the output file.
def cisco_device_export(net_ids, output_file):
    with open(output_file, "r+") as f:
        f.write("Network Name, Serial #, Manufacturer, MAC Address\n")
        for net_id in net_ids:
            serial = m.devices.getNetworkDevices(net_id)[0]['serial']
            network_name = m.networks.getNetwork(net_id)['name']
            site_clients = m.clients.getNetworkClients(net_id)
            for client in site_clients:
                if search(client["manufacturer"], "Cisco Systems"):
                    f.write("{}, {}, {}, {}\n".format(network_name, serial, client["manufacturer"], client["mac"]))
    f.close()


if __name__ == "__main__":
    
    start_time = dt.now()

    try:
        # Unique Meraki API key from the Meraki Dashboard
        api_key = input("Enter your Meraki API Key: ")

        # Initiating the API session and creating API object to use in API queries
        m = meraki.DashboardAPI(api_key)
 
        orgs = m.organizations.getOrganizations()
        object_pprint(orgs)
        organization_id = input("Enter the Organization ID: ") 

        # The output file to export the device names and mgmt IPs after the script has completed.
        output_file = input("Enter the file path for the cisco device output file: ")

        # m.config_templates.getOrganizationConfigTemplates(organization_id)
        # This command was used to find the device template IDs below.
        """
            {
                'id': 'N_630503947831923190', 
                'name': 'CLS-PROD-MX250-Template', 
                'productTypes': ['appliance'], 
                'timeZone': 'US/Central'
            }
            {
                'id': 'N_630503947831946699', 
                'name': 'CLS-EMEA-MX100-Template', 
                'productTypes': ['appliance'], 
                'timeZone': 'Greenwich'
            }
        """

        # The specific configuration templates IDs to use in the script.
        config_template_ids = ['N_630503947831923190', 'N_630503947831946699']
        
        for template in config_template_ids:
            
            # Getting the network_devices using the network_device_list function
            print("{} INFO: Generating the list of network devices associated with the configuration templates.".format(dt.now()))
            print("-"*120)
            net_devices = network_device_list_generator(organization_id, template)

            # Getting the network IDs using the network device list generated and the network_id_list function.
            print("{} INFO: Generating the list of network IDs associated with the network devices.".format(dt.now()))
            print("-"*120)
            ids = network_id_list_generator(net_devices)
            print("{} INFO: Network ID List created successfully.".format(dt.now()))

            # Creating the Network Name, Serial, Client MAC list using the cisco_device_export function.
            print("{} INFO: Generating the device name and mgmt IP objects associated for the specific network IDs.".format(dt.now()))
            print("-"*120)
            cisco_device_export(ids, output_file)


    except KeyboardInterrupt:
        # Except statement is to clean up keyboard interrupt output. 
        # This stops the whole call stack from being output to the CLI.
        print("{} ERROR: Keyboard Interrupt.".format(dt.now()))


    # Calculating total runtime
    end_time = dt.now()
    total_runtime = end_time - start_time
    print("{} INFO: Total Runtime > {}".format(dt.now(), total_runtime))
