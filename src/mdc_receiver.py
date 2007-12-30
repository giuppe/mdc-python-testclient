import SocketServer, threading

class MdcMessageHandler(SocketServer.DatagramRequestHandler):
    def handle(self):
        header = self.request[0][0:2]
        version = self.request[0][3]
        type = self.request[0][4:8]  
        print "Peer %s sent message of type %s" % (self.client_address[0], type)
        
        for param in self.split_parameters(self.request[9:]):
            print param["n"]
            print param["h"]
        
    def split_parameters(self, parameters):
        result_array = dict
        list_parameters = parameters.split(";")
        for string_parameter in list_parameters:
            parameter = string_parameter.split("=")
            result_array.update({parameter[0]: parameter[1]})
            
        return result_array
        
           

class MdcControlReceiver(threading.Thread, SocketServer.UDPServer):
    def __init__(self):
        threading.Thread.__init__(self)
        SocketServer.UDPServer.__init__(self, ('',5551), MdcMessageHandler)
        
    def run(self):
        while True:
            self.serve_forever()
            

class MdcDataReceiver(threading.Thread, SocketServer.UDPServer):
    def __init__(self):
        threading.Thread.__init__(self)
        SocketServer.UDPServer.__init__(self, ('',5552), DescriptorHandler)
        
    def run(self):
        while True:
            self.serve_forever()

class DescriptorHandler(SocketServer.DatagramRequestHandler):
    def handle(self):
        header = self.request[0][0:2]
        version = self.request[0][3]
        type = self.request[0][4:8]  
        print "Peer %s sent data message of type %s" % (self.client_address[0], type)
        descriptor = self.request[0][9:]
        print descriptor
        current_string = descriptor.split("\0", 1)[0]
        stream_id = current_string[0]
        flow_id = int(current_string[1][0])
        sequence_id = int(current_string[1][1:4])
        
        print "stream_id: %s\n flow_id: %d\n sequence_id: %d" % stream_id, flow_id, sequence_id
        
