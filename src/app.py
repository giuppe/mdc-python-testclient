
import struct, mdc_client_manager, mdc_receiver, asyncore
from image_repo import ImageRepo


#mdcmessage = struct.pack("3sb4s", "MDC", 0, "LIST")

#mdcmessage += struct.pack("1s1s5s10s", "n", "=","la_gi",";")

#arraymessage = struct.unpack("3sb4s", mdcmessage)

#print arraymessage[2]

#print (mdcmessage)

c = mdc_client_manager.MdcClientManager('192.168.0.30')

#c.send_list("capo")

#c.send_sinf("5e9f88e7ed612d6129b771d7e2d49bd0")

c.send_sreq("5e9f88e7ed612d6129b771d7e2d49bd0", 0, 0, 20)

control_listener = mdc_receiver.MdcControlReceiver()

control_listener.start()

image_repo = ImageRepo()

data_listener = mdc_receiver.MdcDataReceiver(image_repo)

data_listener.start()


asyncore.loop()



