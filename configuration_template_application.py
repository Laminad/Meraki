from datetime import datetime as dt
from meraki.exceptions import APIError
from re import match
import meraki


def get_time():
    return dt.now().replace(microsecond=0)


if __name__ == "__main__":
    
    start_time = dt.now()
    print(
        """
        #################################################################
        #                                                               #
        #                Meraki Config Template Rebind                  #
        #                                                               #
        #################################################################
        """
    )

    try:
        # Asking the user to enter their unique Meraki API key from the Meraki Dashboard
        api_key = input("Enter your Meraki API key: ")


        # Initiating the API session and creating API object to use in API queries with the API provided.
        m = meraki.DashboardAPI(api_key)

        
        # Outputting the Organization IDs and asking the user to input the organization they are working on.
        orgs = m.organizations.getOrganizations()
        print("\nOrganization IDs")
        print("-"*25)
        for org in orgs:
            print(f"{org['name']}: {org['id']}")
        organization_id = input("Enter the Organization ID: ")


        # Outputting the organization config templates and asking the user to select the
        # specific templates they want the want to rebind the devices to.
        temps = m.organizations.getOrganizationConfigTemplates(organization_id)
        print("\nConfiguration Template IDs")
        print("-"*25)
        for temp in temps:
            print(f"{temp['name']}: {temp['id']}")

        config_template_id = ""
        user_input = "L_123"
        while True:
            user_input = input("Enter the configuration template ID to rebind the networks to: ")
            if user_input !="0" and match(r'[N_|L_]\d*', user_input):
                config_template_id = user_input
                break
            else:
                print("Invalid Entry.")


        # Asking the user to enter the file path of the text file of devices to apply templates updates to.
        input_file = input("Enter the file path to the file of serial numbers to complete a template rebind on: ")


        # This loop uses a list of serial numbers to unbinds the old template if it exists 
        # and then applies the new template that was provided previously.
        # This is the fastest and most reliable method to update templates.
        with open(input_file, "r") as ifile:
            for serial in ifile:
                network_id = m.devices.getDevice(serial.rstrip())["networkId"]
                try:
                    m.networks.unbindNetwork(network_id)
                except APIError:
                    print(f"{get_time}       script:   ERROR > No template bound to device {serial}.")
                try:
                    m.networks.bindNetwork(network_id, config_template_id)
                except APIError:
                    print(f"{get_time}       script:   ERROR > Failed to bind new template for serial {serial}.")


        # These loops are useful if you need to find network IDs based on network name instead of serial number.
        # This method should only be used as a last resort. It is slower and less reliable than using a list of serial numbers.
        """
        search_list = {}
        network_list = m.organizations.getOrganizationNetworks(organization_id, total_pages='all', configTemplateId=config_template_id)
        for network in network_list:
            search_list[network["name"].rstrip()] = network["id"]

        with open(input_file, "r") as ifile:
            for network in network_list:
                network_id = search_list[network.rstrip()]
                try:
                    m.networks.unbindNetwork(network_id)
                except APIError:
                    print(f"{get_time}       script:   ERROR > No template bound to device {serial}.")
                try:
                    m.networks.bindNetwork(network_id, config_template_id)
                except APIError:
                    print(f"{get_time}       script:   ERROR > Failed to bind new template for serial {serial}.")
        """


    except KeyboardInterrupt:
        # Except statement is to clean up keyboard interrupt output. 
        # This stops the whole call stack from being output to the CLI.
        print(f"{get_time}       script:   ERROR > Keyboard Interrupt.")


    # Calculating total runtime
    end_time = dt.now()
    total_runtime = end_time - start_time
    print(f"{get_time}       script:    INFO > Total Runtime {total_runtime}")