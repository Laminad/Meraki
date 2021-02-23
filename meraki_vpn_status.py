from datetime import datetime as dt
from os import P_NOWAIT
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
        #                      Meraki VPN Status                        #
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
        print("\n")

        serial = input("Enter the serial number of the device to check VPN status on: ")
        network_id = m.devices.getDevice(serial)["networkId"]
        vpn_status = m.appliance.getOrganizationApplianceVpnStatuses(organization_id, networkIds=[network_id])

        print(vpn_status)

    except KeyboardInterrupt:
        # Except statement is to clean up keyboard interrupt output. 
        # This stops the whole call stack from being output to the CLI.
        print(f"{get_time()}       script:    ERROR > Keyboard Interrupt.")


    # Calculating total runtime
    end_time = dt.now()
    total_runtime = end_time - start_time
    print(f"{get_time()}       script:     INFO > Total Runtime {total_runtime}")