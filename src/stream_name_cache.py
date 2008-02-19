class StreamNameCache:
    def __init__(self):
        self.name_cache = dict()
        self.desc = dict()
        self.seq = dict()
    
    def add_name(self, stream_id, stream_name):
        self.name_cache[stream_id] = stream_name
        
    def get_names(self):
        result = list()
        for stream_id, stream_name in self.name_cache.iteritems():
            result.append((stream_id, stream_name))
        return result
    
    def add_info(self, stream_id, descriptions, sequences):
        self.desc[stream_id] =descriptions
        self.seq[stream_id] = sequences
    
    def clear(self):
        self.name_cache.clear()
        
    def get_info(self, stream_id):
        return (self.desc[stream_id], self.seq[stream_id])
    
    