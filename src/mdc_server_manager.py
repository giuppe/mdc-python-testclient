
import socket, struct, time
import threading

import globals


class MdcServerManager ( threading.Thread ):

    def __init__(self, host):
        threading.Thread.__init__(self)
        self.buffer = ""
        self.client = socket.socket ( socket.AF_INET, socket.SOCK_DGRAM )
        self.client.connect ( (host, 5552)  )
        self.descriptors_schedule = list()
        
    def run ( self ):
      

        global g_sequences_cache
        
        while(1):
            # this should prevent CPU chocking
            time.sleep(1)
            
            if(len(self.buffer) !=0):
                sent = self.client.send ( self.buffer )
                self.buffer = self.buffer[sent:] 
            else:
                curr_desc = self.descriptors_schedule.pop()
                self.buffer += globals.g_sequences_cache.get_descriptor(curr_desc[0], curr_desc[1], curr_desc[2])  
        
    def close(self):
        self.client.close()
        
    def send_desc(self, stream_id, description_id, seq_start, seq_end):
        for index in range(seq_start, seq_end+1):
            self.descriptors_schedule.insert(0, (stream_id, description_id, index))
        