import socketserver

class ClientHandler(socketserver.BaseRequestHandler):

    def handle(self):
        encrypted_key = self.request.recv(1024).strip()
        print("Implement decryption of data" + encrypted_key)
        #kod deszyfrujący
        self.request.sendall("send key back")

if __name__ == "__main__":
    HOST, PORT = "", 8000

    tcpServer = socketserver.TCPServer((HOST, PORT), ClientHandler)
    try: 
        tcpServer.serve_forever()
    except:
        print("There was an error")

#unfinished