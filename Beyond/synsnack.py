from scapy.all import IP, TCP, ICMP, srl
import sys

def icmp_probe(ip):
    icmp_packet = IP(dst=ip)/ICMP()
    resp_packet = srl(icmp_packet, timeout=10)
    return resp_packet != None

def syn_scan(ip, port):
    syn_packet = IP(dst=ip) / TCP(dport=port, flags='S')
    resp_syn_packet = srl(syn_packet, timeout=10)
    if resp_syn_packet.getlayer('TCP').flags == 0x12:
        print("Host " + ip + " open on port " + port)

if __name__ == "__main__":
    ip = sys.argv[1]
    port = sys.argv[2]
    if icmp_probe(ip):
        syn_ack_packet = syn_scan(ip, port)
        syn_ack_packet.show()
    else:
        print("ICMP probe failed")