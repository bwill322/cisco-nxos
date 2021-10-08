"""
Look for interfaces with errors
"""

from __future__ import print_function, unicode_literals
import signal
import netmiko.ssh_exception
from netmiko import Netmiko
import login_tools

signal.signal(signal.SIGINT, signal.SIG_DFL)  # KeyboardInterrupt: Ctrl-C

username, password = login_tools.get_credentials()

hostnames = [
    #enter all hostnames here
]
for hostname in hostnames:
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
        output = net_connect.send_command("show interface status", use_textfsm=True, strip_command=True)

        print("-" * 160)
        print("100M Interfaces on: ", hostname)
        print("-" * 160)
        print("{:35} | {:<20} | {:<20} |".format("Interface Name", "Status", "Speed"))
        print("-" * 160)

        for i, element in enumerate(output):

            intf_name = output[i]['port']
            status = output[i]['status']
            speed = output[i]['speed']

            if status == "connected" and speed == "100":
                print("{:35} | {:<20} | {:<20} |".format(
                    intf_name,
                    status,
                    speed
                    )
                )

        print()

    except netmiko_exceptions as e:
        print("Failed to: ", hostname, e)
