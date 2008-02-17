import SocketServer, threading
import struct, time
from image_repository import ImageRepo
import globals
from mdc_client_manager import MdcClientManager

    

class MdcMessageHandler(SocketServer.DatagramRequestHandler):
    def handle(self):
        global g_sequences_cache
        global g_peers_cache
        global g_stream_name_cache
        global g_last_stream_name_search
        header = self.request[0][0:3]
        version = self.request[0][3]
        type = self.request[0][4:8]  
        print "Peer %s sent message %s of type %s" % (self.client_address[0], header, type)
        #print "%s" % self.request[0][8:]
        
        if type == "LIST":
            searched_stream_name = ""
            for key, value in self.split_parameters(str(self.request[0][8:])).iteritems():
                if(key == "n"):
                    searched_stream_name = value
            
            streams_list = list()
            for stream_i_have in globals.g_sequences_cache.get_stream_ids():
                stream_name_i_have = globals.g_stream_name_cache.get(stream_i_have)
                if(stream_name_i_have.find(searched_stream_name) != -1):
                    streams_list.append((stream_name_i_have, stream_i_have))
                
            peer_connection = globals.g_peers_cache.get_control_connection(self.client_address[0])
            
            peer_connection.send_alst(streams_list)
            time.sleep(2)
            return
        
        if type == "ALST":
            globals.g_stream_name_last_search.clear()
            for single_parameters in self.split_multiple_parameters(str(self.request[0][9:])).iteritems():
                
                for key, value in self.split_parameters(single_parameters).iteritems():
                    if(key=="n"):
                        searched_stream_name = value
                    if(key=="h"):
                        stream_id = value
                globals.g_stream_name_cache.add_name(stream_id, searched_stream_name)
                globals.g_last_stream_name_search.add_name(stream_id, searched_stream_name)        
                
            return
        
        if type == "SINF":
            stream_id=""
            
            # first extract parameter
            for key, value in self.split_parameters(str(self.request[0][8:])).iteritems():
                if(key == "h"):
                    stream_id = value
                
                    
            #second retrieve information on the stream
            descriptions_number, sequence_number = globals.g_stream_name_cache.get_info(stream_id)
            
            #finally send ASNF message with these info
            
            peer_connection = globals.g_peers_cache.get_control_connection(self.client_address[0])
            
            peer_connection.send_asnf(stream_id, descriptions_number, sequence_number)
            
            return

        if type == "ASNF":
            stream_id = ""
            flows_number = 0
            sequences = 0
            for key, value in self.split_parameters(str(self.request[0][8:])).iteritems():
                if(key=="h"):
                    stream_id = value
                if(key=="fn"):
                    flows_number = int(value)
                if(key=="dn"):
                    sequences = int(value)
            global image_repo
            globals.image_repo.set_flows_number(stream_id, flows_number)
            
            global g_stream_name_cache
            
            globals.g_stream_name_cache.add_info(stream_id, flows_number, sequences)
            
            return

        
        if type == "SREQ":
            stream_id = ""
            description_id = 0
            sequence_start = 0
            sequence_end = 0
            #first extract parameters
            for key, value in self.split_parameters(str(self.request[0][8:])).iteritems():
                if(key=="h"):
                    stream_id = value
                if(key=="fn"):
                    description_id = int(value)
                if(key=="sb"):
                    sequence_begin = int(value)
                if(key=="se"):
                    sequence_end = int(value)
            
            #check for descriptors presence
            
            real_seq_begin, real_seq_end = globals.g_sequences_cache.get_descriptors_index(stream_id, description_id, sequence_begin, sequence_end)
            
            #third, send an ASRQ with descriptors we have
            
            peer_connection = globals.g_peers_cache.get_control_connection(self.client_address[0])
            
            peer_connection.send_asrq(stream_id, description_id, real_seq_start, real_seq_end)
            
            #finally, schedule for sending those descriptors 
            
            if(real_seq_end != 0):
                data_connection = globals.g_peers_cache.get_data_connection(self.client_address[0])
                data_connection.send_desc(stream_id, description_id, real_seq_start, real_seq_end)
            
            print "ERROR: We still cannot handle SREQ messages";
            return
        
        if type == "ASRQ":
            print "Received ASRQ: expecting descriptors..."
            return            
        
        if type == "PEER":
            
            peers_list = globals.g_peers_cache.get_peers()
            
            peer_connection = globals.g_peers_cache.get_control_connection(self.client_address[0])
            
            peer_connection.send_aper(peers_list)
            return
        
        if type == "APER":
                        
            for single_parameters in self.split_multiple_parameters(str(self.request[0][9:])).iteritems():
                
                for key, value in self.split_parameters(single_parameters).iteritems():
                    if(key=="a"):
                        address = value
                    if(key=="p"):
                        port = value
                globals.g_peers_cache.add(address, port)
                
            return
            
        

        
                    
        
        for key, value in self.split_parameters(str(self.request[0][8:])).iteritems():
            print key, value
            #print param["h"]
        
    def split_parameters(self, parameters):
        result_array = {}
        list_parameters = parameters.split(";")
        for string_parameter in list_parameters[0:len(list_parameters)-1]:
            if string_parameter is not '':
                parameter = string_parameter.split("=")
                result_array[parameter[0]] = parameter[1]
            
        return result_array
    
    def split_multiple_parameters(self, multi_parameters):
        return multi_parameters.split("\0");
         
           

class MdcControlReceiver(threading.Thread, SocketServer.UDPServer):
    def __init__(self):
        threading.Thread.__init__(self)
        SocketServer.UDPServer.__init__(self, ('',5551), MdcMessageHandler)
        
    def run(self):
        print "Starting control listening on port 5551"
        while True:
            self.serve_forever()
            

class MdcDataReceiver(threading.Thread, SocketServer.UDPServer):
    def __init__(self):
        threading.Thread.__init__(self)
        SocketServer.UDPServer.__init__(self, ('',5552), DescriptorHandler)
        
    def run(self):
        print "Starting data listening on port 5552"
        while True:
            self.serve_forever()

class DescriptorHandler(SocketServer.DatagramRequestHandler):

        
    def handle(self):
        header = self.request[0][0:2]
        version = self.request[0][3]
        type = self.request[0][4:8]  
        print "Peer %s sent data message of type %s" % (self.client_address[0], type)
        descriptor = self.request[0][8:]
        #print descriptor
        
        stream_id = descriptor[0:32]
        flow_id, sequence_id = struct.unpack(">bI", descriptor[32:37])
       
        codec_type, codec_param_size = struct.unpack(">bI", descriptor[37:42])
        
        #sequence_id = descriptor[33:37]
        
        print "stream_id: %s\n flow_id: %s\n sequence_id: %s" % (stream_id, flow_id, sequence_id)
        
        if(codec_type != 2):
            print "Current version can manage only images"
            return
        
        print "Codec type 'image', param size %s" % codec_param_size
        width, height, bpp = struct.unpack(">HHb", descriptor[42:47])
        if(bpp != 24):
            print "Images with bpp != 24 are not supported"
            return
        
        print "Image size: %s*%s*%s" % (width, height, bpp)
        
        payload_size = struct.unpack(">H", descriptor[47:49])
        
        global image_repo
        
        if(not globals.image_repo.is_init(stream_id)):
            globals.image_repo.set_size(stream_id, width, height)
            
        
        payload_ends = 49 + int(payload_size[0])
        globals.image_repo.add_descriptor(stream_id, flow_id, sequence_id, descriptor[49:payload_ends])
        
        
        
        