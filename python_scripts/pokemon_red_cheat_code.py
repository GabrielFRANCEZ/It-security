import sys
import argparse
import math 

def get_arguments():
    parser = argparse.ArgumentParser()
    parser.add_argument("-p", "--path", dest="savepath", help="Specify path to the save file", required=True)
    parser.add_argument("-m", "--money", dest="money", help="Specify the amount of money", required=False)
    parser.add_argument("-b", "--badge", dest="badge", help="Specify the number of badge", required=False)

    arguments = parser.parse_args()
    return arguments

def fix_checksum(ram):
    checksum = 0xff
    for c in ram [0x2598:0x3523]:
        checksum -= c
    
    ram[0x3523] = checksum&0xff
    #print("[+] Checksum {} written".format(checksum&0xff))

def get_hex(number):
    unit = number % 10
    dec = number // 10

    return 16 * dec + unit 

def change_money (ram, money):
    amount = int(money)
    if amount > 999999:
         print("[-] ERROR MAXIMUM IS 999,999 and you enter : {}".format( amount))
         return 1
    else :
        value = amount % 100
        addr_memoire = 0x25F5
        ram[addr_memoire] = get_hex(value)
        amount = amount // 100
        value = amount % 100
        addr_memoire = 0x25F4
        ram[addr_memoire] = get_hex(value)
        amount = amount // 100
        value = amount % 100
        addr_memoire = 0x25F3
        ram[addr_memoire] = get_hex(value)
        amount = amount // 100
        print("[+] Now, you have {} P$".format(money))
    
def change_badge(ram, badge) : 
    value = pow(2,int(badges)) - 1
    res = int(hex(value),16)
    ram[0x2602] = res
    print("[+] Now, you have {} badges".format(badge))

arguments = get_arguments()
with open(arguments.savepath,'rb+') as hex_file :
    ram = bytearray(hex_file.read())
    #fix_checksum(hex_file)
    if arguments.money != None : 
        change_money(ram,arguments.money)
    if arguments.badge != None : 
        change_badge(ram,arguments.badge)
    fix_checksum(ram)
    hex_file.seek(0,0)
    hex_file.write(ram)
    