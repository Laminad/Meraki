from datetime import datetime as dt
import meraki
import sys

# A function that creates a list of devices associated with a specific device template in the Meraki dashboard.
def network_device_list_generator(org_id, config_temp_ids):
    network_devices = []
    for template in config_temp_ids:
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
    with open(output_file, 'w') as f:
        for net_id in net_ids:
            try:
                serial = m.devices.getNetworkDevices(net_id)[0]['serial']
                mgmt_ip = m.devices.getNetworkDevice(net_id, serial)['lanIp']
                mgmt_ip = m.devices.getNetworkDevice(net_id, serial)['Ip']
                device_name = device_name = m.networks.getNetwork(net_id)['name']
                print("{} INFO: Writing network name and mgmt IP to the output file > {} - {}.".format(dt.now(),device_name, mgmt_ip))
                f.write("{},{}\n".format(device_name, mgmt_ip))
            except KeyError:
                print("{} ERROR: Device Offline.".format(dt.now()))
    f.close


if __name__ == "__main__":
    
    start_time = dt.now()

    try:
        # Unique Meraki API key from Meraki Dashboard
        api_key = "948df9b6f664c31b42cc4ccde2c8817e72ddf7d9"

        # LabCorp Meraki Organization ID. 
        # m.organizations.getOrganizations() 
        # Is the API method that was used to get this information.
        organization_id = "388603" 

        # The output file to export the device names and mgmt IPs after the script has completed.
        output_file = "C:\\Users\\danthompson\\Documents\\LabCorp\\wfh_z3_device_name_mgmt_ip.txt"

        # Initiating the API session and creating API object to use in API queries
        m = meraki.DashboardAPI(api_key)

        # The specific configuration templates to run the script for.
        config_template_ids = ['N_630503947831946812', 'N_630503947831949798']

        # This command was used to find the device template IDs
        # m.config_templates.getOrganizationConfigTemplates(organization_id)

        '''
                Device Configuration Template Objects Example

                {
                id: N_630503947831946812
                name: Z3C Test 11-04-2019
                productTypes: ['appliance']
                timeZone: America/New_York
                }

                {
                id: N_630503947831949798
                name:  DEFAULT TEMPLATE - WFH Z3 NO WIFI
                productTypes: ['appliance']
                timeZone: America/New_York
                }

        '''

        # Getting the network_devices using the network_device_list function
        print("{} INFO: Generating the list of network devices associated with the configuration templates.".format(dt.now()))
        print("-"*120)
        net_devices = network_device_list_generator(organization_id, config_template_ids)

        # Getting the network IDs using the network device list generated and the network_id_list function.
        print("{} INFO: Generating the list of network IDs associated with the network devices.".format(dt.now()))
        print("-"*120)
        ids = network_id_list_generator(net_devices)
        print("{} INFO: Network ID List created successfully.".format(dt.now()))

        # Creating the Network Name and Mgmt IP list using the mgmt_ip_and_device_list function.
        print("{} INFO: Generating the device name and mgmt IP objects associated for the specific network IDs.".format(dt.now()))
        print("-"*120)
        mgmt_ip_and_device_name_list_generator(ids, output_file)


    except KeyboardInterrupt:
        # Except statement is to clean up keyboard interrupt output. 
        # This stops the whole call stack from being output to the CLI.
        print("{} ERROR: Keyboard Interrupt.".format(dt.now()))


    # Calculating total runtime
    end_time = dt.now()
    total_runtime = end_time - start_time
    print("{} INFO: Total Runtime > {}".format(dt.now(), total_runtime))