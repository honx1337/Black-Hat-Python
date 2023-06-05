from scapy.all import (ARP, Ether, conf, send, get_if_hwaddr, RandMAC, RandIP)
import socket

print(RandIP())
def main():
    comp = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
#    comp.setsockopt(socket.SOL_SOCKET)
    def whohas():
        ip = str(RandIP())
        bindport = 219
        comp.bind((ip, bindport))
        packet= Ether(ARP(op=2, hwdst="ff:ff:ff:ff:ff:ff", hwsrc=RandMAC()))
        send(packet)
    while True:
        whohas()

main()