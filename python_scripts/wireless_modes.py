#!/usr/bin/env python3

import subprocess
import argparse
import re


def get_arguments():
    parser = argparse.ArgumentParser()
    parser.add_argument("-i", "--interface", dest="interface", help="Interface to change its mode", required=True)
    parser.add_argument("-m", "--mode", dest="mode", help="mode : monitor / managed", required=True, choices=['monitor', 'managed'])
    arguments = parser.parse_args()
    return arguments


def change_mode(interface, mode):
    if (get_current_mode(arguments.interface) == str(mode).capitalize()):
        print("[-] The mode selected was allready implemented")
        return 1

    print("[+] Changing mode for " + interface + " to " + mode)

    if str(mode) == "monitor":
        subprocess.call(["ifconfig", interface, "down"])
        subprocess.call(["airmon-ng", "check", "kill"])
        subprocess.call(["iwconfig", interface, "mode", mode])
        subprocess.call(["ifconfig", interface, "up"])


    elif str(mode) == "managed":
        subprocess.call(["ifconfig", interface, "down"])
        subprocess.call(["iwconfig", interface, "mode", mode])
        subprocess.call(["ifconfig", interface, "up"])
        subprocess.call(["service", "network-manager", "restart"])

    else:
        print("[-] Please specify a good mode")

    return 0


def get_current_mode(interface):
    iwconfig_result = subprocess.check_output(["iwconfig", interface])
    old_mode = re.search(r"\w\w\w\w:\w\w\w\w\w\w\w", iwconfig_result)
    if old_mode:
        return old_mode.group(0).split(":")[1]
    else:
        print("[-] Could not implement the new mode")


arguments = get_arguments()
current_mode = get_current_mode(arguments.interface)
print("Current mode = " + str(current_mode))
change_mode(arguments.interface, arguments.mode)
current_mode = get_current_mode(arguments.interface)
if str(current_mode) == str(arguments.mode).capitalize():
    print("[+] The mode was successfully changed to  " + str(current_mode))
else:
    print("[-] The mode did not get changed into " + str(current_mode))
