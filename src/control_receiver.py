import SocketServer, threading

class handler(SocketServer.DatagramRequestHandler):
    def handle(self):
        header = self.request[0][0:2]
        version = self.request[0][3]
        type = self.request[0][4:8]  
        print "Peer %s sent message of type %s" % (self.client_address[0], type)
        
           

class mdc_control_receiver(threading.Thread, SocketServer.UDPServer):
    def __init__(self):
        threading.Thread.__init__(self)
        SocketServer.UDPServer.__init__(self, ('',5551), handler)
        
    def run(self):
        while True:
            self.serve_forever()
            
