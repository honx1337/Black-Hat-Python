import ipaddress
import os
import socket
import struct
import sys
import threading
import time

#Docelowa podsieć
SUBNET = '192.168.1.0/24'
#Zaklęcie którym będziemy sprawdzać czy host jest dostępny przez ICMP
MESSAGE = 'CTHULHUFHTAGN!'

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

#Funkcja rozsyłająca datagramy UDP z zaklęciem
def udp_sender():
    with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as sender:
        for ip in ipaddress.ip_network(SUBNET).hosts():
            sender.sendto(bytes(MESSAGE, 'utf-8'), str(str(ip), 65212))

class Scanner:
    def __init__(self, host):
        self.host = host
        if os.name == 'nt':
            socket_protocol = socket.IPPROTO_IP
        else:
            socket_protocol = socket.IPPROTO_ICMP

        sniffer = socket.socket(socket.AF_INET, socket.SOCK_RAW, socket_protocol)
        sniffer.bind((host, 0))
        sniffer.setsockopt(socket.IPPROTO_IP, socket.IP_HDRINCL, 1)
        if os.name == 'nt':
            sniffer.ioctl(socket.SIO_RCVALL, socket.RCVALL_ON)
    
    def sniff(self):
        hosts_up = set([f'{str(self.host)} *'])
        try:
            while True:
                #Odczytanie pakietu
                raw_buffer = self.socket.recvfrom(65535)[0]
                #Utworzenie nagłówka IP na podstawie pierwszych 20 bajtów
                ip_header = IP(raw_buffer[0:20])
                if ip_header.protocol == 'ICMP':
                    offset = ip_header.ihl * 4
                    buf = raw_buffer[offset:offset +8]
                    icmp_header = ICMP(buf)
                    #Sprawdzenie kodu i typu komunikatu
                    if icmp_header.code == 3 and icmp_header.type == 3:
                        if ipaddress.ip_address(ip_header.src_address) in ipaddress.IPv4Network(SUBNET):
                            #Sprawdzamy czy komunikat ma zaklęcie
                            if raw_buffer[len(raw_buffer) - len(MESSAGE): ] == bytes(MESSAGE, 'utf-8'):
                                tgt = str(ip_header.src_address)
                                if tgt != self.host and tgt not in hosts_up:
                                    hosts_up.add(str(ip_header.src_address))
                                    print(f'Aktywny host:{str(ip_header.src_address)}')
        except KeyboardInterrupt:
            if os.name == 'nt':
                self.socket.ioctl(socket.SIO_RCVALL, socket.RCVALL_OFF)

            print('\n Przerwane przez użytkownika.')
            if hosts_up:
                print(f'\n\n Podsumowanie: Wykryte aktywne hosty w podsieci {SUBNET}')
                for host in hosts_up:
                    print(f'{host}')
                    print('')
                    sys.exit()

if __name__ == "__main__":
    if len(sys.argv) == 2:
        host = sys.argv[1]
    else:
        host = '192.168.1.4'
    s = Scanner(host)
    time.sleep(5)
    t = threading.Thread(target=udp_sender())
    t.start()
    s.sniff()