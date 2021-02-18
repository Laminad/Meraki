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
        #                       Meraki MX Backup                        #
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

        # Asking the user to enter the file path of the text file of devices to apply templates updates to.
        input_file = input("Enter the file path of Meraki serial number to backup: ")
        output_file = input("Enter the file path for the file that will be used to store the backup configurations: ")

        # Creating an array of the Meraki serial numbers to backup using the input file provided.
        serial_array = []
        with open(input_file, "r") as ifile:
            for serial in ifile:
                serial_array.append(serial.rstrip())
        ifile.close()

        # Looping through the Meraki serial number array and capturing all valuable configuration elements,
        # then writing them to an output file to store the current configuration as JSON objects.
        with open(output_file, "w") as ofile:
            for serial in serial_array:

                device_config = {}
                network_id = ""
                network = ""
                traffic_analysis = ""
                syslog_servers = ""
                snmp_configuration = ""
                firmware_schedule = ""
                alerts = ""
                vlans = ""
                static_routes = ""
                l3_firewall_rules = ""
                l7_firewall_rules = ""
                vpn_bgp_settings = ""
                site_to_site_vpn = ""
                traffic_shaping_uplink_selection = ""
                traffic_shaping_bandwidth_limits = ""


                try:
                    network_id = m.devices.getDevice(serial)["networkId"]
                except APIError:
                    print(f"{get_time()}       script:    ERROR > No network with serial {serial}")
                    pass
                try:
                    network = m.networks.getNetwork(network_id)
                    device_config["network"] = network
                except APIError:
                    print(f"{get_time()}       script:    ERROR > Invalid network id {network_id}")
                    pass
                try:
                    traffic_analysis = m.networks.getNetworkTrafficAnalysis(network_id)
                    device_config["traffic_analysis"] = traffic_analysis
                except APIError:
                    print(f"{get_time()}       script:     INFO > Traffic analysis not configured or disabled on {network['name']}")
                try:
                    syslog_servers = m.networks.getNetworkSyslogServers(network_id)
                    device_config["syslog_servers"] = syslog_servers
                except APIError:
                    print(f"{get_time()}       script:     INFO > No syslog servers configured on {network['name']}")
                try:
                    snmp_configuration = m.networks.getNetworkSnmp(network_id)
                    device_config["snmp_configuration"] = snmp_configuration
                except APIError:
                    print(f"{get_time()}       script:     INFO > No snmp configuration on {network['name']}")
                try:
                    firmware_schedule = m.networks.getNetworkFirmwareUpgrades(network_id)
                    device_config["firmware_schedule"] = firmware_schedule
                except APIError:
                    print(f"{get_time()}       script:     INFO > No firmware upgrade schedule configured on {network['name']}")
                try:
                    alerts = m.networks.getNetworkAlertsSettings(network_id)
                    device_config["alerts"] = alerts
                except APIError:
                    print(f"{get_time()}       script:     INFO > No alert configurtion applied on {network['name']}")
                try:
                    vlans = m.appliance.getNetworkApplianceVlans(network_id)
                    device_config["vlans"] = vlans
                except APIError:
                    print(f"{get_time()}       script:     INFO > No vlan configuration applied on {network['name']}")
                try:
                    static_routes = m.appliance.getNetworkApplianceStaticRoutes(network_id)
                    device_config["static_routes"] = static_routes
                except APIError:
                    print(f"{get_time()}       script:     INFO > No static routes configured on {network['name']}")
                try:
                    l3_firewall_rules = m.appliance.getNetworkApplianceFirewallL3FirewallRules(network_id)
                    device_config["l3_firewall_rules"] = l3_firewall_rules
                except APIError:
                    print(f"{get_time()}       script:     INFO > No l3 firewall rules configured on {network['name']}")
                try:
                    l7_firewall_rules = m.appliance.getNetworkApplianceFirewallL7FirewallRules(network_id)
                    device_config["l7_firewall_rules"] = l7_firewall_rules
                except APIError:
                    print(f"{get_time()}       script:     INFO > No l7 Firewall rules configured on {network['name']}")
                try:
                    vpn_bgp_settings = m.appliance.getNetworkApplianceVpnBgp(network_id)
                    device_config["vpn_bgp_settings"] = vpn_bgp_settings
                except APIError:
                    print(f"{get_time()}       script:     INFO > No bgp configuration applied on {network['name']}")
                try:
                    site_to_site_vpn = m.appliance.getNetworkApplianceVpnSiteToSiteVpn(network_id)
                    device_config["site_to_site_vpn"] = site_to_site_vpn
                except APIError:
                    print(f"{get_time()}       script:     INFO > No site to site vpn configuration applied on {network['name']}")
                try:
                    traffic_shaping_uplink_selection = m.appliance.getNetworkApplianceTrafficShapingUplinkSelection(network_id)
                    device_config["traffic_shaping_uplink_selection"] = traffic_shaping_uplink_selection
                except APIError:
                    print(f"{get_time()}       script:     INFO > No traffic shaping uplink policies configured on {network['name']}")
                try:
                    traffic_shaping_bandwidth_limits = m.appliance.getNetworkApplianceTrafficShapingUplinkBandwidth(network_id)
                    device_config["traffic_shaping_bandwidth_limits"] = traffic_shaping_bandwidth_limits
                except APIError:
                    print(f"{get_time()}       script:     INFO > No traffic shaping bandwidth limited configured on {network['name']}")


                ofile.write("{\n")
                config_keys = device_config.keys()
                for key in config_keys:
                    ofile.write(f"  {key}: {device_config[key]}\n")
                ofile.write("}\n\n")


    except KeyboardInterrupt:
        # Except statement is to clean up keyboard interrupt output. 
        # This stops the whole call stack from being output to the CLI.
        print(f"{get_time()}       script:    ERROR > Keyboard Interrupt.")


    # Calculating total runtime
    end_time = dt.now()
    total_runtime = end_time - start_time
    print(f"{get_time()}       script:     INFO > Total Runtime {total_runtime}")