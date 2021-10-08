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
   # enter device list here
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
        output = net_connect.send_command("show interface transceiver", use_textfsm=True, strip_command=True)

        print("-" * 160)
        print(output)
        print("-" * 160)
    except netmiko_exceptions as e:
        print("Failed to: ", hostname, e)
