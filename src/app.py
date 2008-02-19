
import struct, mdc_client_manager, mdc_receiver, time, globals

from image_repository import ImageRepo




control_listener = mdc_receiver.MdcControlReceiver()

control_listener.start()

data_listener = mdc_receiver.MdcDataReceiver()

data_listener.start()

global g_last_stream_name_search

c = mdc_client_manager.MdcClientManager('192.168.0.30')

c.start()

stream_id = ""

while(stream_id == ""):
    
    c.send_list("lena")

    time.sleep(5)

    

    found_list = globals.g_last_stream_name_search.get_names()

    print found_list

    if len(found_list)>0:
        stream_id = found_list[0][0]

#stream_id = "5e9f88e7ed612d6129b771d7e2d49bd0"

c.send_sinf(stream_id)

if(not globals.image_repo.exists(stream_id)):
     globals.image_repo.create(stream_id)

time.sleep(5)

descriptions, sequences = globals.g_stream_name_cache.get_info(stream_id)

old_seq_block = 0
for seq_block in range(10, sequences, 10):
    c.send_sreq(stream_id, 0, old_seq_block, seq_block)
    old_seq_block = seq_block+1
    time.sleep(2)


c.send_sreq(stream_id, 1, 0, 31)

time.sleep(10)

global image_repo

globals.image_repo.save_bmp(stream_id, "/home/giuppe/mdclena511-interp.bmp", True)

print "Saved image, exiting."

exit()
