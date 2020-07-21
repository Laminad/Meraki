from datetime import datetime as dt
from re import search
import meraki
import sys


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

# A functions that takes a network id list and output file object and exports 
# the network name, Meraki serial, manufacturer (Cisco Systems) and client MAC to the output file.
def device_export(net_ids, output_file):
        for net_id in net_ids:
            try:
                serial = m.devices.getNetworkDevices(net_id)[0]['serial']
                network_name = m.networks.getNetwork(net_id)['name']
                site_clients = m.clients.getNetworkClients(net_id)
                for client in site_clients:
                    if search(client["manufacturer"], "Cisco Systems"):
                        output_file.write("{}, {}, {}, {}\n".format(network_name, serial, client["manufacturer"], client["mac"]))
            except:
                print("{} ERROR: Either no Meraki device or client associated with this network.".format(dt.now()))


if __name__ == "__main__":
    
    start_time = dt.now()

    try:
        # Unique Meraki API key from the Meraki Dashboard
        api_key = input("Enter your Meraki API key: ")

        # Initiating the API session and creating API object to use in API queries
        m = meraki.DashboardAPI(api_key)
        
        # Outputting the Organization IDs and asking the user to input the organization they are working on.
        print("\nOrganization IDs")
        print("-"*25)
        orgs = m.organizations.getOrganizations()
        for org in orgs:
            print("Name: {}".format(org['name']))
            print("ID: {}\n".format(org['id']))

        organization_id = input("Enter the Organization ID: ") 

        # The output file to export the site names and device info after the script has completed.
        output_file = input("Enter the file path for the output file: ")
        
        # Outputting the organization config templates and asking the user to select the
        # specific templates they want the client information from.
        print("\nConfiguration Template IDs")
        print("-"*25)
        temps = m.config_templates.getOrganizationConfigTemplates(organization_id)
        for temp in temps:
            print("Name: {}".format(temp['name']))
            print("ID: {}\n".format(temp['id']))

        config_template_ids = []
        user_input = "L_123"
        while user_input != "0":
            user_input = input("Enter a configuration template ID or 0 to end: ")
            if user_input !="0":
                config_template_ids.append(user_input)
        
        with open(output_file, "w") as ofile:
            
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

                # Creating the Network Name, Serial, Manufacturer, and MAC list using the device_export function.
                print("{} INFO: Generating the device name and mgmt IP objects associated for the specific network IDs.".format(dt.now()))
                print("-"*120)
                device_export(ids, ofile)
                
        ofile.close()


    except KeyboardInterrupt:
        # Except statement is to clean up keyboard interrupt output. 
        # This stops the whole call stack from being output to the CLI.
        print("{} ERROR: Keyboard Interrupt.".format(dt.now()))


    # Calculating total runtime
    end_time = dt.now()
    total_runtime = end_time - start_time
    print("{} INFO: Total Runtime > {}".format(dt.now(), total_runtime))