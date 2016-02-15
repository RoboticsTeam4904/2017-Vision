import SocketServer
import subprocess

class MyTCPHandler(SocketServer.BaseRequestHandler):
    """
    Responds to requests for the view of the goal.
    """

    def handle(self):
        # self.request is the TCP socket connected to the client
        process = subprocess.Popen(["./highgoal.bin", "latest"], stdout=subprocess.PIPE)

        response = process.stdout.read()
        # just send back the same data, but upper-cased
        self.request.sendall(response)

if __name__ == "__main__":
    HOST, PORT = "0.0.0.0", 9999

    # Create the server, binding to localhost on port 9999
    server = SocketServer.TCPServer((HOST, PORT), MyTCPHandler)

    # Activate the server; this will keep running until you
    # interrupt the program with Ctrl-C
    server.serve_forever()
