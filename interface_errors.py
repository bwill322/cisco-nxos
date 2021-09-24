"""
Look for interfaces with errors
"""

from __future__ import print_function, unicode_literals
import signal
import netmiko.ssh_exception
from netmiko import Netmiko
import login_tools

signal.signal(signal.SIGINT, signal.SIG_DFL)  # KeyboardInterrupt: Ctrl-C

hostname = login_tools.get_input("Enter hostname: ")
username, password = login_tools.get_credentials()

device = {
    'host': hostname,
    'username': username,
    'password': password,
    'device_type': 'cisco_nxos'
}

netmiko_exceptions = (netmiko.ssh_exception.NetmikoAuthenticationException,
                      netmiko.ssh_exception.NetmikoTimeoutException)

try:
    net_connect = Netmiko(**device)
    output = net_connect.send_command_timing("show interface", use_textfsm=True)

    print("-" * 160)
    print("{:35} | {:<15} | {:<15} | {:<25}".format("Interface Name",
                                                             "Input Errors",
                                                             "Output Errors",
                                                             "Description")
          )
    print("-" * 160)
    for i, element in enumerate(output):
        hardware_type = output[i]['hardware_type']

        if "Ethernet SVI" not in hardware_type or "RP Management Port" not in hardware_type:
            intf_name = output[i]['interface']
            input_errors = output[i]['input_errors']
            output_errors = output[i]['output_errors']
            description = output[i]['description']

            # To account for interfaces that don't have these counters (e.g. subintfs)
            if input_errors == '':
                input_errors = 0
            else:
                input_errors = int(input_errors)

            if output_errors == '':
                output_errors = 0
            else:
                output_errors = int(output_errors)

            intf_has_errors = input_errors > 0 or output_errors > 0

            if intf_has_errors:
                print("{:35} | {:<15} | {:<15} | {:<25}".format(
                    intf_name,
                    input_errors,
                    output_errors,
                    description)
                )

    print()
except netmiko_exceptions as e:
    print("Failed to: ", hostname, e)
