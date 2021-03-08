from datetime import datetime as dt
from meraki.exceptions import APIError
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

        # Asking the user to enter the file path of the text file of devices to apply templates updates to.
        input_file = input("Enter the file path to the file of serial numbers to complete a template rebind on: ")
        search_space = {}
        config_template_ids = ["N_630503947831922447", "N_630503947831954623", "N_630503947831959324"]

        for template_id in config_template_ids:
            networks = m.organizations.getOrganizationNetworks("388603", total_pages="all", configTemplateId=template_id)
            for network in networks:
                network_id = network["id"]
                search_space[network_id] = template_id


        with open(input_file, "r") as ifile:
            for serial in ifile:
                try:
                    network_id = m.devices.getDevice(serial.rstrip())["networkId"]
                except APIError:
                    print(f"{get_time()}       script:    ERROR > No network id found for device {serial}.")
                    pass
                try:
                    m.networks.unbindNetwork(network_id)
                except APIError:
                    print(f"{get_time()}       script:    ERROR > No template bound to device {serial}.")
                try:
                    config_template_id = search_space[network_id]

                    if config_template_id == "N_630503947831954623":
                        # DEFAULT TEMPLATE - WFH ALT CALL CTR: N_630503947831954623 -> RCM_CCC_Cluster 2: N_762797186885880884
                        m.networks.bindNetwork(network_id, "N_762797186885880884")

                    elif config_template_id == "N_630503947831922447" or config_template_id == "N_630503947831959324":
                        # DEFAULT TEMPLATE - WFH Z3 NO WIFI: N_630503947831959324 -> RCM_CCC_Cluster 1: N_762797186885880895
                        # DEPRECTED - WFH Z3 NO WIFI: N_630503947831922447 -> RCM_CCC_Cluster 1: N_762797186885880895
                        m.networks.bindNetwork(network_id, "N_762797186885880895")

                except APIError:
                    print(f"{get_time()}       script:    ERROR > Failed to bind new template for serial {serial}.")



    except KeyboardInterrupt:
        # Except statement is to clean up keyboard interrupt output. 
        # This stops the whole call stack from being output to the CLI.
        print(f"{get_time()}       script:    ERROR > Keyboard Interrupt.")


    # Calculating total runtime
    end_time = dt.now()
    total_runtime = end_time - start_time
    print(f"{get_time()}       script:     INFO > Total Runtime {total_runtime}")