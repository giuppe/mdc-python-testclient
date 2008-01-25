
import image_bmp

class ImageRepo:
    def __init__(self):
        self.images = dict()
        
    def add_descriptor(self, stream_id, flow_id, seq_id, payload):
        if(stream_id in self.images):
            curr_image = self.images[stream_id] 
            #TODO: add pixels to image
            curr_image 
        else:
            print "No image with stream_id=%s present." % stream_id
    
    def exists(self, stream_id):
        return stream_id in self.images
    
    def create(self, stream_id, width, height):
        self.images[stream_id] = image_bmp.ImageBMP()
        self.images[stream_id].create(width, height, 0, 255, 0)
             
    def save_bmp(self, stream_id, path):
        if(stream_id in self.images):
            self.images[stream_id].save(path)
        else:
            print "No image with stream_id=%s present." % stream_id
            