

import socket, struct, time
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
            time.sleep(1)
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
    
    def send_asnf(self, stream_id, descriptions_number, sequence_number):
        self.buffer += "MDC\0ASNFh=%s;fn=%d;sn=%d;\0" % (stream_id, descriptions_number, sequence_number) 
    
    def send_sreq(self, stream_id, description, du_start, du_end):
        self.buffer += "MDC\0SREQh=%s;f=%d;sb=%d;se=%d;\0" % (stream_id, description, du_start, du_end) 

    def send_asrq(self, stream_id, description, du_start, du_end):
        self.buffer += "MDC\0ASRQh=%s;f=%d;sb=%d;se=%d;\0" % (stream_id, description, du_start, du_end) 


    def send_peer(self):
        self.buffer += 'MDC\0PEER\0'

    def send_aper(self, peer_list):
        self.buffer += 'MDC\0APER'
        self.buffer += struct.pack('>I', len(peer_list))
        if len(peer_list) != 0:
            for peer in peer_list:
                self.buffer += 'a=%s;p=%d\0' % peer[0], peer[1]

    def send_alst(self, stream_list):
        self.buffer += 'MDC\0ALST'
        self.buffer += struct.pack('>I', len(stream_list))
        print "Preparing ALST: found %d entries" % len(stream_list)
        if len(stream_list) != 0:
            for stream in stream_list:
                print "Preparing ALST: %s, %s" % stream[0], stream[1]
                self.buffer += 'n=%s;h=%s\0' % stream[0], stream[1]
        print "Sent ALST message"
