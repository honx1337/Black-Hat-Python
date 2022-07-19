import socket
import threading

bind_ip = '0.0.0.0'
bind_port = 9998

def main():
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind((bind_ip, bind_port)) #bindujemy ip i port do nasuchu
    server.listen(5) # ustawiamy max ilosc polaczen
    print(f'[*] Nasluchiwanie na {bind_ip}:{bind_port}')

    while True:
        client, address = server.accept() #pobieranie adresu i portu klienta
        print(f'[*] Przyjeto polooczenie od {address[0]}:{address[1]}')
        client_handler = threading.Thread(target=handle_client, args=(client,))
        client_handler.start() #startujemy z watkiem obslugi klienta

def handle_client(client_socket): #odbieranie i ack tranzakcji
    with client_socket as sock:
        request = sock.recv(1024)
        print(f'[*] Odebrano: {request.decode("utf-8")}')
        sock.send(b'ACKKK')

if __name__ == '__main__':
    main()