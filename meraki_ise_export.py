from datetime import datetime as dt
import meraki
import sys

# A function that creates a list of devices associated with a specific device template in the Meraki dashboard.
def network_device_list_generator(org_id, config_temp_ids):
    network_devices = []
    network_devices = m.networks.getOrganizationNetworks(org_id, configTemplateId=template)
    return network_devices

# A function that takes a list network devices and creates a list of their network IDs.
def network_id_list_generator(net_devices):
    network_ids = []
    for device in net_devices:
        network_ids.append(device['id'])
    return network_ids

# A function that takes in a list of network IDs and creates objects of the corresponding network name and mgmt IP.
def mgmt_ip_and_device_name_list_generator(net_ids, output_file):
    mgmt_ip = ''
    device_name = ''
    for net_id in net_ids:
        try:
            serial = m.devices.getNetworkDevices(net_id)[0]['serial']
            mgmt_ip = m.devices.getNetworkDevice(net_id, serial)
            # mgmt_ip = m.devices.getNetworkDevice(net_id, serial)['lanIp']
            # mgmt_ip = m.devices.getNetworkDevice(net_id, serial)['Ip']
            device_name = device_name = m.networks.getNetwork(net_id)['name']
            print("{} INFO: Writing network name and mgmt IP to the output file > {} - {}.".format(dt.now(),device_name, mgmt_ip))
            output_file.write("{},{}\n".format(device_name, mgmt_ip))
        except KeyError:
            print("{} ERROR: Device Offline.".format(dt.now()))


if __name__ == "__main__":
    
    start_time = dt.now()

    try:
        # Unique Meraki API key from Meraki Dashboard
        api_key = input("Enter you Meraki API key: ")

        # Initiating the API session and creating API object to use in API queries
        m = meraki.DashboardAPI(api_key)

        # Outputting the Organization IDs and asking the user to input the organization they are working on. 
        orgs = m.organizations.getOrganizations() 
        print("\nOrganization IDs")
        print("-"*25)
        for org in orgs:
            print("Name: {}".format(org['name']))
            print("ID: {}\n".format(org['id']))
        organization_id = input("Enter the Organization ID: ")

        # The output file to export the device names and mgmt IPs after the script has completed.
        output_file = input("Enter the file path of the output file: ")

        # Outputting the organization config templates and asking the user to select the
        # specific templates they want the device information from.
        temps = m.config_templates.getOrganizationConfigTemplates(organization_id)
        print("\nConfiguration Template IDs")
        print("-"*25)
        for temp in temps:
            print("Name: {}".format(temp['name']))
            print("ID: {}\n".format(temp['id']))

        config_template_ids = []
        user_input = "L_123"
        while user_input != "0":
            user_input = input("Enter a configuration template ID or 0 to end: ")
            if user_input !="0":
                config_template_ids.append(user_input)

        with open(output_file, 'w') as ofile:

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

                # Creating the Network Name and Mgmt IP list using the mgmt_ip_and_device_list function.
                print("{} INFO: Generating the device name and mgmt IP objects associated for the specific network IDs.".format(dt.now()))
                print("-"*120)
                mgmt_ip_and_device_name_list_generator(ids, ofile)

        ofile.close


    except KeyboardInterrupt:
        # Except statement is to clean up keyboard interrupt output. 
        # This stops the whole call stack from being output to the CLI.
        print("{} ERROR: Keyboard Interrupt.".format(dt.now()))


    # Calculating total runtime
    end_time = dt.now()
    total_runtime = end_time - start_time
    print("{} INFO: Total Runtime > {}".format(dt.now(), total_runtime))