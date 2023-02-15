import socketserver

class BotHandler(socketserver.BaseRequestHandler):

    def handle(self):
        self.data = self.request.recv(1024).strip()
        print("Bot with IP {} sent:".format(self.client_address[0]))
        f = open(command.txt)
        self.request.sendall(f.read())

    if __name__ == "__main__":
        HOST, PORT = "", 8000
        tcpServer = socketserver.TCPServer((HOST, PORT), BotHandler)
        try:
            tcpServer.serve_forever()
        except:
            print("There was an error")