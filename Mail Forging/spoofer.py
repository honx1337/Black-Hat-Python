import sys, socket

size =1024

def sendMessage(smtpServer, port, fromAddress, toAddress, message):
    IP = smtpServer
    PORT = int(port)

    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect((IP, PORT)) #Otwiera gniazdo
    print(s.recv(size).decode()) #wyświetla odpowiedź
    
    #HELO
    s.send(b'HELO '+ fromAddress.split('@')[1].encode() +b'\n')
    print(s.recv(size).decode())
    
    #MAIL FROM:
    s.send(b'MAIL FROM:<' + toAddress.encode() + b'>\n')
    print(s.recv(size).decode())

    #RCPT TO:
    s.send(b'RCPT TO:<' + toAddress.encode() + b'>\n')
    print(s.recv(size).decode())

    #DATA:
    s.send(b"DATA\n")
    print(s.recv(size).decode())
    s.send(message.encode() + b'\n')
    s.send(b'\r\n.\r\n')
    print(s.recv(size).decode())

    #QUIT
    s.send(b'QUIT\n')
    print(s.recv(size).decode())

    #Koniec komunikacji
    s.close()

def main(args):
    smtpServer = args[1]
    port = args[2]
    fromAddress = args[3]
    toAddress = args[4]
    message = args[5]
    sendMessage(smtpServer, port, fromAddress, toAddress, message)

if __name__ == "__main__":
    main(sys.argv)