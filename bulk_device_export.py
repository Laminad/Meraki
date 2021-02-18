#! Python3
from datetime import datetime as dt
from re import match
import meraki
import sys

if __name__ == "__main__":
    
    start_time = dt.now()
    network_id_list = []

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
            print("{}: {}".format(org['name'], org['id']))
        organization_id = input("Enter the Organization ID: ")

        # Outputting the organization config templates and asking the user to select the
        # specific templates they want the client information from.
        temps = m.organizations.getOrganizationConfigTemplates(organization_id)
        print("\nConfiguration Template IDs")
        print("-"*25)
        for temp in temps:
            print("{}: {}".format(temp['name'], temp['id']))

        config_template_ids = []
        user_input = "L_123"
        while user_input != "0":
            user_input = input("Enter a configuration template ID or 0 to end: ")
            if user_input !="0" and match(r'[N_|L_]\d*', user_input):
                config_template_ids.append(user_input)
            elif user_input ==  "0":
                pass
            else:
                print("Invalid Entry.")
        
        output_file = input("Enter the file to export the device data to: ") 

        with open(output_file, 'w') as ofile:

            for template in config_template_ids:
                organization_network_objects = m.organizations.getOrganizationNetworks(organization_id, configTemplateId=template)

            for network_object in organization_network_objects:
                network_id_list.append(network_object['id'])

            for network_id in network_id_list:
                network_id = network_id
                network = m.networks.getNetwork(network_id)
                devices = m.networks.getNetworkDevices(network_id)
                network_tags = str(network['tags'])
                network_name = network['name']
                mx68_serial = ''
                mx68_name = ''
                mr33_serial = ''
                mr33_name = ''
                for device in devices:
                    if device['model'] == 'MX68':
                        street_address = device['address']
                        mx68_serial = device['serial']
                        try:
                            mx68_name = device['name']
                        except:
                            pass
                    elif device['model'] == 'MR33':
                        mr33_serial = device['serial']
                        try:
                            mr33_name = device['name']
                        except:
                            pass   
                ofile.write(f"{network_name},{network_tags},{mx68_name},{mx68_serial},{mr33_name},{mr33_serial},{street_address}\n")
                
    except KeyboardInterrupt:
        # Except statement is to clean up keyboard interrupt output. 
        # This stops the whole call stack from being output to the CLI.
        print("{} ERROR: Keyboard Interrupt.".format(dt.now()))

    # Calculating total runtime
    end_time = dt.now()
    total_runtime = end_time - start_time
    print("{} INFO: Total Runtime > {}".format(dt.now(), total_runtime))
    