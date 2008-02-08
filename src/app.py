
import struct, mdc_client_manager, mdc_receiver, time, globals

from image_repository import ImageRepo




control_listener = mdc_receiver.MdcControlReceiver()

control_listener.start()

data_listener = mdc_receiver.MdcDataReceiver()

data_listener.start()



c = mdc_client_manager.MdcClientManager('192.168.0.30')

c.start()



stream_id = "5e9f88e7ed612d6129b771d7e2d49bd0"

c.send_sinf(stream_id)

if(not globals.image_repo.exists(stream_id)):
     globals.image_repo.create(stream_id)

time.sleep(5)


c.send_sreq(stream_id, 0, 0, 10)

time.sleep(2)

c.send_sreq(stream_id, 0, 11, 20)

time.sleep(2)

c.send_sreq(stream_id, 0, 21, 31)


time.sleep(10)

c.send_sreq(stream_id, 1, 0, 31)

time.sleep(10)

global image_repo

globals.image_repo.save_bmp(stream_id, "/home/giuppe/capodanno3.bmp")

print "Saved image, exiting."

exit()
