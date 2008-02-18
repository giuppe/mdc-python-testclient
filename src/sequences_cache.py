class SequencesCache:
    def __init__(self):
        self.sequences = dict()
        self.stream_ids = list()
        
    def add(self, stream_id, description_id, sequence_id, desc_unit):
        
        if not self.sequences.has_key(stream_id):
            self.sequences[stream_id] = list()
        
        if not self.sequences[stream_id].has_key(description_id):
            self.sequences[stream_id][description_id] =list()
            
        self.sequences[stream_id][description_id][sequence_id] = desc_unit
        self.stream_ids.append(stream_id)
            
    def get_descriptor(self, stream_id, description_id, sequence_id):
       
                
        return self.sequences[stream_id][description_id][sequence_id]
        
    def get_stream_ids(self):
        return self.stream_ids
    
    
    def get_descriptors_index(self, stream_id, description_id, sequence_start, sequence_end):
        #TODO should find descriptors we have
        
        print "ERROR: Missing function get_descriptors_index in SequencesCache"
        return (0, 0)