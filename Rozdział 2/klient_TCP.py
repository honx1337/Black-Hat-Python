import socket

target_host = "0.0.0.0"
target_port = 9998
data = input(str("Jaka wiadomosc masz do admina? "))

#tworzenie gniazda
client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
#AF_INET oznacza IPv4, SOCK_STREAM oznacza uzywanie TCP

#polaczenie z serwerem
client.connect((target_host, target_port))

#wyslanie danych
client.send(data.encode('utf-8'))

#odebranie danych 
response = client.recv(4096)
print(response.decode())
client.close()