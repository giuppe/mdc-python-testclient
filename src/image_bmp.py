import struct

class ImageBmp:
    
    def __init__(self): pass
        
    def create(self, width, height, trans_r, trans_g, trans_b):
        self.header_size = 54
        self.width= width
        self.height = height
        self.img_size = width*height*3
        self._pixels=[(trans_r,trans_g,trans_b)]
        
        for i in range(self.img_size-1):
            self._pixels.append((trans_r,trans_g,trans_b))

    def set_pixel(self, x, y, r, g, b):
        self._pixels[x+(self.height-y-1)*self.width]=(r,g,b)
        
    def get_pixel(self, x, y):
        return self._pixels[x+(self.height-y-1)*self.width]


    def median(self):
    
        median_img = ImageBmp()
        median_img.create(self.width, self.height)
        
        for x in range(1, self.width-1):
            med_r = (self.get_pixel(x-1,0)[0]+self.get_pixel(x,1)[0]+self.get_pixel(x+1,0)[0])/3
            med_g = (self.get_pixel(x-1,0)[1]+self.get_pixel(x,1)[1]+self.get_pixel(x+1,0)[1])/3
            med_b = (self.get_pixel(x-1,0)[2]+self.get_pixel(x,1)[2]+self.get_pixel(x+1,0)[2])/3
            median_img.set_pixel(x, 0, med_r, med_g, med_b)
            
            med_r = (self.get_pixel(x-1,self.height-1)[0]+self.get_pixel(x,self.height-2)[0]+self.get_pixel(x+1,self.height-1)[0])/3
            med_g = (self.get_pixel(x-1,self.height-1)[1]+self.get_pixel(x,self.height-2)[1]+self.get_pixel(x+1,self.height-1)[1])/3
            med_b = (self.get_pixel(x-1,self.height-1)[2]+self.get_pixel(x,self.height-2)[2]+self.get_pixel(x+1,self.height-1)[2])/3
            median_img.set_pixel(x, self.height-1, med_r, med_g, med_b)    
        
        for x in range(1, self.width-1):
            for y in range(1, self.height-1):    
                med_r, med_g, med_b = self._calc_full_median(x, y)
                median_img.set_pixel(x, y, med_r, med_g, med_b)
        
        return median_img

    def subst_transparent(self, trans_r, trans_g, trans_b):
        final_img = ImageBmp()
        final_img.create(self.width, self.height)
        
        for x in range(1, self.width-1):
            for y in range(1, self.height-1):    
                if self.get_pixel(x, y)[0] == trans_r and self.get_pixel(x, y)[1] == trans_g and self.get_pixel(x, y)[2] == trans_b:
                    med_r, med_g, med_b = self._calc_full_median(x, y)
                    final_img.set_pixel(x, y, med_r, med_g, med_b)
                else:
                    final_img.set_pixel(x, y, self.get_pixel(x, y)[0], self.get_pixel(x, y)[1], self.get_pixel(x, y)[2])
        return final_img
        

    def save(self, path):
        file_header = struct.pack("<2sihhi", "BM",self.header_size+self.img_size, 0, 0, self.header_size)
        info_header = struct.pack("<iiihhiiiiii", self.header_size-14, self.width, self.height, 1, 24, 0, self.img_size, 0, 0, 0, 0)
        img_bmp = ""
        pixel_on_row_count = 0
        curr_row =""
        for (r, g, b) in self._pixels:
            curr_row += struct.pack("<BBB", b, g, r)
            pixel_on_row_count+=3
            if(pixel_on_row_count == self.width*3):
                modulus = (self.width*3)%4
                if modulus==0:
                    padding_num = 0
                else:
                    padding_num = 4-modulus
                for i in range(0, padding_num):
                    curr_row += struct.pack("<B", 0)
                img_bmp+=curr_row
                pixel_on_row_count = 0
                curr_row = ""
                
            
        
        final_file = file_header + info_header+ str(img_bmp)
        
        f = open(path, "w+")
        f.write(final_file)
        file.close(f)

    def _calc_full_median(self, x, y):
        up_right = self.get_pixel(x + 1, y - 1)
        up_center = self.get_pixel(x, y - 1)
        up_left = self.get_pixel(x - 1, y - 1)
        center_right = self.get_pixel(x + 1, y)
        center_center = self.get_pixel(x, y)
        center_left = self.get_pixel(x - 1, y)
        down_right = self.get_pixel(x + 1, y + 1)
        down_center = self.get_pixel(x, y + 1)
        down_left = self.get_pixel(x - 1, y + 1)
        med_r = (up_right[0] + up_left[0] + up_center[0] + center_left[0] + center_center[0] + center_right[0] + down_left[0] + down_center[0] + down_right[0]) / 9
        med_g = (up_right[1] + up_left[1] + up_center[1] + center_left[1] + center_center[1] + center_right[1] + down_left[1] + down_center[1] + down_right[1]) / 9
        med_b = (up_right[2] + up_left[2] + up_center[2] + center_left[2] + center_center[2] + center_right[2] + down_left[2] + down_center[2] + down_right[2]) / 9
        return med_r, med_g, med_b




def test_imagebmp(save_path):
    pippo = ImageBmp()
    pippo.create(33, 33)
    for i in range(0, 33):
        for k in range(0, 33):
            pippo.set_pixel(i * 2, k * 2, 255, 255, 255)
        
    
    for i in range(0, 33):
        pippo.set_pixel(i * 2, i, 0, 255, 0)
    
    #pappo = pippo.subst_transparent(0, 255, 0)
    
    pappo = pippo.median()
    
    pappo.save(save_path)


