
from mdc_client_manager import MdcClientManager

class PeersCache:
    def __init__(self):
        self.peer_names = dict()
        self.connections = dict()
        
    def add(self, ip_address, port):
        self.peer_names[ip_address] = (ip_address, port)
    
    def _add_control_connection(self, ip_address, connection):
        self.connections[ip_address] = connection
    
    def get_control_connection(self, ip_address):
        if self.connections.has_key(ip_address):
            return self.connections[ip_address]
        else:
            peer_connection = MdcClientManager(ip_address)
            peer_connection.start()
            self._add_control_connection(ip_address, peer_connection)
            return peer_connection
    
    def _add_data_connection(self, ip_address, connection):
        self.connections[ip_address] = connection
    
    def get_data_connection(self, ip_address):
        if self.connections.has_key(ip_address):
            return self.connections[ip_address]
        else:
            peer_connection = MdcServerManager(ip_address)
            peer_connection.start()
            self._add_data_connection(ip_address, peer_connection)
            return peer_connection    
    
    def get_peers(self):
        return self.peer_names
    