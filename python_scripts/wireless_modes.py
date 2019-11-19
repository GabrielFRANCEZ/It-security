#!/usr/bin/env python

import subprocess
import optparse
import re


def get_arguments():
    parser = optparse.OptionParser()
    parser.add_option("-i", "--interface", dest="interface", help="Interface to change its MAC address")
    parser.add_option("-m", "--mode", dest="mode", help="mode : monitor / managed")
    (options, arguments) = parser.parse_args()
    if not options.interface:
        parser.error("[-] Please specify an interface, use --help for more info")
    if not options.mode:
        parser.error("[-] Please specify a mode, use --help for more info")
    return options


def change_mode(interface, mode):
    if (get_current_mode(options.interface) == str(mode).capitalize()):
        print("[-] The mode selected was allready implemented")
        return 1

    print("[+] Changing mode for " + interface + " to " + mode)
    subprocess.call(["ifconfig", interface, "down"])

    if str(mode) == "monitor":
        subprocess.call(["airmon-ng", "check", "kill"])
        subprocess.call(["iwconfig", interface, "mode", mode])
	subprocess.call(["ifconfig", interface, "up"])
	

    elif str(mode) == "managed":
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


options = get_arguments()
current_mode = get_current_mode(options.interface)
print("Current Mac addresse = " + str(current_mode))
change_mode(options.interface, options.mode)
current_mode = get_current_mode(options.interface)
if str(current_mode) == str(options.mode).capitalize():
    print("[+] The mode was successfully changed to  " + str(current_mode))
else:
    print("[-] The mode did not get changed into " + str(current_mode))


