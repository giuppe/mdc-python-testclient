
import struct, mdc_client_manager, mdc_receiver, time, globals

from image_repository import ImageRepo




control_listener = mdc_receiver.MdcControlReceiver()

control_listener.start()

data_listener = mdc_receiver.MdcDataReceiver()

data_listener.start()

time.sleep(120)

exit()