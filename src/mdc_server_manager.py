
import socket, struct, time
import threading


class MdcServerManager ( threading.Thread ):

    def __init__(self, host):
        threading.Thread.__init__(self)
        self.buffer = ""
        self.client = socket.socket ( socket.AF_INET, socket.SOCK_DGRAM )
        self.client.connect ( (host, 5552)  )
        
    def run ( self ):
      
        
        while(1):
            # Send some messages:
            time.sleep(1)
            if(len(self.buffer) !=0):
                sent = self.client.send ( self.buffer )
                self.buffer = self.buffer[sent:] 
                
        
    def close(self):
        # Close the connection
        self.client.close()
        
    def send_desc(self, descriptor):
        self.buffer += descriptor