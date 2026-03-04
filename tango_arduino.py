#v1
import arduino_class
print("tango!")

# PyTango imports
import tango
from tango.server import run
from tango.server import Device
from tango.server import attribute, command
from tango.server import class_property, device_property
from tango import AttrQuality, DispLevel, DevState
from tango import AttrWriteType
# Additional import

class TangoArduino(Device):


    port_name=device_property(dtype=str)



    @attribute(dtype=str)
    def led_state(self):
        return 'ON'

    @command(dtype_out=str)
    def set_led_on(self):
        self.info_stream('Turning on the power supply')

# test
#myArduino=arduino_class.ArduinoDevice()
#print("Arduino state: "+myArduino.get_state())
