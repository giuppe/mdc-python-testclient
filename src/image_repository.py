
from image_bmp import ImageBmp

class ImageRepo:
    def __init__(self):
        self.images = dict()
        self.flows_number = dict()
        self.max_payload = dict()
    
    def _set_max_payload(self, stream_id, max_payload):
        self.max_payload[stream_id] = max_payload
    
    def add_descriptor(self, stream_id, flow_id, seq_id, payload):
        if(stream_id in self.images):
            curr_image = self.images[stream_id] 
            
            print "Adding received pixels"
            if seq_id <= 1:
                self.max_payload[stream_id] = len(payload)
            
            #payload_max_len = len(payload)
            pixel_number = len(payload)/3
            for k in range(0, pixel_number):
                #pixel_pos=flow_id +payload_max_len*seq_id*self.flows_number[stream_id]+ k*self.flows_number[stream_id] 
                pixel_pos=((self.max_payload[stream_id]/3)*seq_id+k)*self.flows_number[stream_id]+flow_id
                y=int((pixel_pos)/curr_image.width)
                x=int((pixel_pos)%curr_image.width)
            
                r=ord(payload[k*3])
                g=ord(payload[k*3+1])
                b=ord(payload[k*3+2])    
                curr_image.set_pixel(x, y, r, g, b)
        else:
            print "No image with stream_id=%s present." % stream_id
    
    def exists(self, stream_id):
        return stream_id in self.images
    
    def is_init(self, stream_id):
        return self.exists(stream_id) and self.images[stream_id].width != 0
    
    def create(self, stream_id):
        self.images[stream_id] = ImageBmp()
        
    def set_size(self, stream_id, width, height):
        self.images[stream_id].create(width, height, 0, 255, 0)
    
    
    def set_flows_number(self, stream_id, flows_number):
        self.flows_number[stream_id] = flows_number
    
    def save_bmp(self, stream_id, path):
        if(stream_id in self.images):
            image_to_save = self.images[stream_id].subst_transparent()
#            image_to_save = self.images[stream_id]
            image_to_save.save(path)
        else:
            print "No image with stream_id=%s present." % stream_id
            