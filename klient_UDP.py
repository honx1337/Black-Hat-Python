import socket

target_host = "127.0.0.1"
target_port = 9997
strim = "AAABBBCCC"

#obiekt gniazda
client = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

#wysylka
client.sendto(strim.encode('utf-8'), (target_host, target_port))

#odebranie
data, adddr = client.recvfrom(4096)
print(data.decode())
client.close()
#no worky????