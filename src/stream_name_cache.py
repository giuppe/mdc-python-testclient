class StreamNameCache:
    def __init__(self):
        self.name_cache = dict()
        self.desc = dict()
        self.seq = dict()
    
    def add_name(self, stream_id, stream_name):
        self.name_cache[stream_id] = stream_name
    
    def add_info(self, stream_id, descriptions, sequences):
        self.desc[stream_id] =descriptions
        self.seq[stream_id] = sequences
    
    def clear(self):
        self.name_cache.clear()
    
    