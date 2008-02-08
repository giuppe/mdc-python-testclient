import socket

#class MdcClientManager(asyncore.dispatcher):
#
#    def __init__(self, host):
#        asyncore.dispatcher.__init__(self)
#        self.create_socket(socket.AF_INET, socket.SOCK_DGRAM)
#        self.connect( (host, 5551) )
#        self.buffer = ""
#    
#    def start(self):
#        self.loop()
#
#    def handle_connect(self):
#        pass
#
#    def handle_close(self):
#        self.close()
#
#    def handle_read(self):
#        print self.recv(8192)
#
#    def writable(self):
#        return (len(self.buffer) > 0)
#
#    def handle_write(self):
#        sent = self.send(self.buffer)
#        self.buffer = self.buffer[sent:]
#
#    def send_list(self, name):
#        self.buffer += 'MDC\0LISTn=%s;\0' % name
#        
#    def send_sinf(self, stream_id):
#        self.buffer += 'MDC\0SINFh=%s;\0' % stream_id
#        
#    def send_sreq(self, stream_id, description, du_start, du_end):
#        self.buffer += "MDC\0SREQh=%s;f=%d;sb=%d;se=%d;\0" % (stream_id, description, du_start, du_end) 

import pickle
import socket
import threading


class MdcClientManager ( threading.Thread ):

    def __init__(self, host):
        threading.Thread.__init__(self)
        self.buffer = ""
        self.client = socket.socket ( socket.AF_INET, socket.SOCK_DGRAM )
        self.client.connect ( (host, 5551)  )
        
    def run ( self ):
      
        
        while(1):
            # Send some messages:
            if(len(self.buffer) !=0):
                sent = self.client.send ( self.buffer )
                self.buffer = self.buffer[sent:]
        
    def close(self):
        # Close the connection
        self.client.close()

    def send_list(self, name):
        self.buffer += 'MDC\0LISTn=%s;\0' % name
        
    def send_sinf(self, stream_id):
        self.buffer += 'MDC\0SINFh=%s;\0' % stream_id
        
    def send_sreq(self, stream_id, description, du_start, du_end):
        self.buffer += "MDC\0SREQh=%s;f=%d;sb=%d;se=%d;\0" % (stream_id, description, du_start, du_end) 

#class mdc_control_receiver(UDPServer):
#    def __init__(self):
#        asyncore.dispatcher.__init__(self)
#        self.create_socket(socket.AF_INET, socket.SOCK_DGRAM)
#        self.bind(('', 5551))
#        self.listen(1)
#
#    def handle_connect(self):
#        pass
#    
#    def handle_accept(self):
#        print self.socket
#        
#    def handle_read(self):
#        print self.recv(8192)
