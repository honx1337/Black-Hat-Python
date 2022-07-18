import argparse
import socket
import shlex
import subprocess
import sys
import textwrap
import threading

def execute(cmd):
        cmd = cmd.strip()
        if not cmd:
            return
        output = subprocess.check_output(shlex.split(cmd), stderr=subprocess.STDOUT)
        return output.decode()

class NetCat:
    def __init__(self, args, buffer=None):
        self.args = args
        self.buffer = buffer
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.socker.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    
    def run(self):
        if self.args.listen:
            self.listen()
        else:
            self.send()

   
if __name__ == '__main__':
    parser = argparse.ArgumentParser(
        description = 'Narzędzie netcat, ale w pythonie'
        formatter_class = argparse.RawDescriptionHelpFormatter,
        epilog = textwrap.dedent('''Przykład uzycia
            netcat.py -t 192.168.1.108 -p 5555 -l -c #powłoka systemu
            netcat.py -t 192.168.1.108 -p 5555 -l -u=mytest.whatisup #załadowanie polecenia
            netcat.py -t 192.168.1.108 -p 5555 -l -e=\"cat /etc/passwd\"

            echo 'ABCDEFGHI' | ./netcat.py -t 192.168.1.108 -p 135 #wysyłanie tekstu do serwera na porcie 135
            netcat.py -t 192.168.1.108 -p 5555 #połączenie z serwerem
            '''))
    parser.add_argument('-c', '--command', action='store_true', help='otwarcie powłoki')
    parser.add_argument('-e', '--execute', help='wykonanie polecenia')
    parser.add_argument('-l', '--listen', action='store_true', help='nasłuchiwanie')
    parser.add_argument('-p', '--port', type=int, default=5555, help='docelowy port')
    parser.add_argument('-t', '--target', default='0.0.0.0', help='docelowy adres IP')
    parser.add_argument('-u', '--upload', help='załadowanie pliku')
    args = parser.parse_args()
    if args.listen:
        buffer = ''
    else:
        buffer = sys.stdin.read()

nc = NetCat(args, buffer.encode('utf-8'))
nc.run