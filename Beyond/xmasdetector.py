from scapy.all import IP, sniff, TCP

def flagCheck(flag):
    flag = resp_packet.getlayer('TCP').flags
    if flag == 0x01:
        return "FIN"
    elif flag ==  0x08:
        return "PSH"
    elif flag ==0x20:
        return "URG"
    else:
        return 0

sniff(count=0, filter="tcp", store=0, prn = flagCheck(flag))
if flagCheck(flag) != 0:
    print("Possible XMAS scan")

#I fucked up something and I don't know what