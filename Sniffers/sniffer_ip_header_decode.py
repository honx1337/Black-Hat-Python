import ipaddress
import os
import socket
import struct
import sys

class IP:
    def __init__(self, buff=None):
        header = struct.unpack('<BBHHHBBH4s4s', buff)
        self.ver = header[0] >> 4
        self.ihl = header[0] & 0xF

        self.tos = header[1]
        self.len = header[2]
        self.id = header[3]
        self.offset = header[4]
        self.ttl = header[5]
        self.protocol_num = header[6]
        self.sum = header[7]
        self.src = header[8]
        self.dst = header[9]

        #Adres IP czytelny dla człowieka
        self.src_address = ipaddress.ip_address(self.src)
        self.dst_address = ipaddress.ip_address(self.dst)

        #Powiązanie numeru z protokołem
        self.protocol_map = {1: "ICMP", 6: "TCP", 17: "UDP"}
        try:
            self.protocol = self.protocol_map[self.protocol_num]
        except Exception as e:
            print('%s Brak protokołu o kodzie %s w naszej bazie danych' % (e, self.protocol_num))
            self.protocol = str(self.protocol_num)

class ICMP:
    def __init__(self, buff):
        header = struct.unpack('<BBHHH', buff)
        self.type = header[0]
        self.code = header[1]
        self.sum = header[2]
        self.id = header[3]
        self.seq = header[4]

def sniff(host):
    #utworzenie surowego gniazda i powiązanie go z interfejsem publicznym
    if os.name == 'nt':
        socket_protocol = socket.IPPROTO_IP
    else:
        socket_protocol = socket.IPPROTO_ICMP

    sniffer = socket.socket(socket.AF_INET, socket.SOCK_RAW, socket_protocol)
    sniffer.bind(('192.168.1.4', 0))
    #Przechwytujemy też nagłówki IP
    sniffer.setsockopt(socket.IPPROTO_IP, socket.IP_HDRINCL, 1)

    if os.name == 'nt':
       sniffer.ioctl(socket.SIO_RCVALL, socket.RCVALL_ON)
    
    try:
        while True:
            #odczytywanie pakietu
            raw_buffer = sniffer.recvfrom(65535)[0]
            #utworzenie nagłówka IP na podstawie pierwszych 20B
            ip_header = IP(raw_buffer[0:20])
            if ip_header.protocol == 'ICMP':
            #wyświetlanie rozpoznanego protokołu i adresów
                print('Protokół: %s %s -> %s' % (ip_header.protocol, ip_header.src_address, ip_header.dst_address))
                print(f'Długość nagłówka: {ip_header.ihl}, TTL: {ip_header.ttl}')
                #Wyliczenie początku pakietu ICMP
                offset = ip_header.ihl *4
                buf = raw_buffer[offset:offset + 8]
                #Tworzymy strukturę ICMP
                icmp_header = ICMP(buf)
                print('ICMP -> Typ %s, kod: %s\n' % (icmp_header.type, icmp_header.code))
    except KeyboardInterrupt:
        #jeśli używany jest windows, włączamy tryb nieograniczony
        if os.name == 'nt':
            sniffer.ioctl(socket.SIO_RCVALL, socket.RCVALL_OFF)
        sys.exit()

if __name__ == '__main__':
    if len(sys.argv) == 2:
        host = sys.argv[1]
    else:
        host = '192.168.1.5'
    sniff(host)