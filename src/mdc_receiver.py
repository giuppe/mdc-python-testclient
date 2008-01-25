import SocketServer, threading
import struct

class MdcMessageHandler(SocketServer.DatagramRequestHandler):
    def handle(self):
        header = self.request[0][0:3]
        version = self.request[0][3]
        type = self.request[0][4:8]  
        print "Peer %s sent message %s of type %s" % (self.client_address[0], header, type)
        print "%s" % self.request[0][8:]
        if type != "ALST":
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
        
           

class MdcControlReceiver(threading.Thread, SocketServer.UDPServer):
    def __init__(self):
        threading.Thread.__init__(self)
        SocketServer.UDPServer.__init__(self, ('',5551), MdcMessageHandler)
        
    def run(self):
        print "Starting control listening on port 5551"
        while True:
            self.serve_forever()
            

class MdcDataReceiver(threading.Thread, SocketServer.UDPServer):
    def __init__(self, image_repo):
        threading.Thread.__init__(self)
        desc_handle = DescriptorHandler
#        desc_handle.set_image_repo(desc_handle, image_repo)
        SocketServer.UDPServer.__init__(self, ('',5552), desc_handle)
        
    def run(self):
        print "Starting data listening on port 5552"
        while True:
            self.serve_forever()

class DescriptorHandler(SocketServer.DatagramRequestHandler):
    def set_image_repo(self, image_repo):
        self.img_repo = image_repo
        
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
        height, width, bpp = struct.unpack(">HHb", descriptor[42:47])
        if(bpp != 24):
            print "Images with bpp != 24 are not supported"
            return
        
        print "Image size: %s*%s*%s" % (width, height, bpp)
        
        payload_size = struct.unpack(">H", descriptor[47:49])
        
        
        
        