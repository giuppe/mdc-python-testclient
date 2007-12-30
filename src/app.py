
import struct, mdc_client_manager, mdc_receiver, asyncore


#mdcmessage = struct.pack("3sb4s", "MDC", 0, "LIST")

#mdcmessage += struct.pack("1s1s5s10s", "n", "=","la_gi",";")

#arraymessage = struct.unpack("3sb4s", mdcmessage)

#print arraymessage[2]

#print (mdcmessage)

c = mdc_client_manager.MdcClientManager('192.168.0.30')

c.send_list("undi")

#c.send_sinf("5bccec356d2b9ca4685ba415d0706f44")

control_listener = mdc_receiver.MdcControlReceiver()

control_listener.start()

data_listener = mdc_receiver.MdcDataReceiver()

data_listener.start()


asyncore.loop()



