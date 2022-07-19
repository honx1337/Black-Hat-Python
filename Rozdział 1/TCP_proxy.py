import sys
import threading
import socket


#blokujemy wszystko co nie jest znakami alfabetu
HEX_FILTER = ''.join([(len(repr(chr(i))) == 3) and chr(i) or '.' for i in range(256)])

#tłumaczenie znaków na hex i na alfabet
def hexdump(src, length=16, show=True):
    if isinstance(src, bytes):
        src = src.decode()
    results = list()
    for i in range(0, len(src), length):
        word = str(src[i:i+length])
        printable = word.translate(HEX_FILTER)
        hexa = ' '.join([f'{ord(c):02X}' for c in word])
        hexwidth = length*3
        results.append(f'{i:04x} {hexa:<{hexwidth}} {printable}')
    if show:
        for line in results:
            print(line)
    else:
        return results #SKOŃCZONO TUTAJ CZYTANIE

#zapisywanie przyjętych danych
def receive_from(connection):
    buffer = b""
    connection.settimeout(5)
    try:
        while True:
            data = connection.recv(4096)
            if not data:
                break
            buffer += data
    except Exception as e:
        print('Błąd', e)
        pass
    return buffer

def request_handler(buffer):
    #Modyfikacja pakietu
    return buffer

def response_handler(buffer):
    #Modyfikacja pakietu
    return buffer

#montowanie proxy
def proxy_handler(client_socket, remote_host, remote_port, receive_first):
    remote_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    remote_socket.connect((remote_host, remote_port))

    if receive_first:
        remote_buffer = receive_from(remote_socket)
        hexdump(remote_buffer)

    remote_buffer = response_handler(remote_buffer)
    if len(remote_buffer):
        print("[<===] Wysłano %d bajtów do lokalnego hosta." % len(remote_buffer))
        client_socket.send(remote_buffer)

    while True:
        local_buffer = receive_from(client_socket)
        if len(local_buffer):
            print("[<===] Odebrano %d bajtów od lokalnego hosta." % len(local_buffer))
            hexdump(local_buffer)

            local_buffer = request_handler(local_buffer)
            remote_socket.send(local_buffer)
            print("[<===] Wysłano do zdalnego hosta.")

        remote_buffer = receive_from(remote_socket)
        if len(remote_buffer):
            print("[<===] Odebrano %d bajtów od zdalnego hosta." % len(remote_buffer))
            hexdump(remote_buffer)

            remote_buffer = request_handler(remote_buffer)
            remote_socket.send(remote_buffer)
            print("[<===] Wysłano do lokalnego hosta.")

        if not len(local_buffer) or not len(remote_buffer):
            client_socket.close()
            remote_socket.close()
            print("[#] Nie ma więcej danych, zamykanie połączenia.")
            break

def server_loop(local_host: str, local_port: int, remote_host: str, remote_port: int, receive_first: bool):
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        server.bind((local_host, local_port))
    except Exception as e:
         print("Problem z utworzeniem gniazda: $r" % e)
         print("[!] Brak możliwości nasłuchu na %s:%d" % (local_host, local_port))
         print("[!] Sprawdź inne gniazda nasłuchu lub zmień uprawnienia.")
         sys.exit(0)

    print("[*] Nasłuch na %s:%d" % (local_host, local_port))
    server.listen(5)
    while True:
        client_socket, addr = server.accept()
        #wyświetlenie informacji o połączeniu
        print("> Odebrane połączenie przychodzące od %s:%d" % (local_host, local_port))
        #uruchomienie komunikacji ze zdalnym hostem 
        proxy_thread = threading.Thread(
            target = proxy_handler(client_socket, remote_host, remote_port, receive_first))
        proxy_thread.start()

def main():
    if len(sys.argv[1:]) != 5:
        print("Użycie ./TCP_proxy.py [lokalny host] [lokalny port]", end="")
        print("[zdalny host] [zdalny port] [najpierw odbieranie]")
        print("Przykład: python3 TCP_proxy.py 127.0.0.1 9000 10.12.132.1 9000 True")
        sys.exit(0)

    local_host = sys.argv[1]
    local_port = int(sys.argv[2])

    remote_host = sys.argv[3]
    remote_port = int(sys.argv[4])

    receive_first = bool(sys.argv[5])

    if receive_first == True:
        receive_first = True
    else:
        receive_first = False

    server_loop(local_host, local_port, remote_host, remote_port, receive_first)

if __name__ == '__main__':
    main()