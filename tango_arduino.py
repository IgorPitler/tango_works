#v1
from os import access
import arduino_class
#print("Tango!")

from tango.server import Device
from tango.server import attribute, command
from tango.server import device_property
from tango import AttrQuality, DispLevel, DevState
from tango import AttrWriteType


class tango_arduino(Device):

    port_name=device_property(dtype=str)

    @attribute(dtype=str)
    def led_state(self):
        return self.arduino_device.get_led_state()

    #led_state=attribute(label="LED state attribute", dtype=str, fget="read_led_state", access=AttrWriteType.READ)

    #@led_state.getter
    #def read_led_state(self) -> str:
    #    return self.arduino_device.get_led_state()

    @command()
    def set_led_on(self):
        self.arduino_device.set_led_on()

        self.set_status("Status: LED is ON")
        self.set_state(DevState.ON)

        print('Turning on the LED')
        #print("LED is "+self.arduino_device.get_led_state()+" Port is: "+self.arduino_device.port_name+" Device status is "+self.get_status())
        #print(self.get_state())
        #print(self.led_state)

    @command()
    def set_led_off(self):
        self.arduino_device.set_led_off()

        self.set_status("Status: LED is OFF")
        self.set_state(DevState.OFF)

        print('Turning off the LED')
        #print("LED is " + self.arduino_device.get_led_state() + " Port is: " + self.arduino_device.port_name+" Device status is "+self.get_status())
        #print(self.get_state())
        #print(self.led_state.read(fget=))

    def init_device(self):
        super().init_device() # call first
        # runs on device initialization
        print("Starting our device...")

        self.arduino_device=arduino_class.ArduinoDevice(self.port_name, 9600)

        self.set_state(DevState.INIT)
        self.set_status("Status: Init")

    def delete_device(self):
        pass
        self.arduino_device.close()
        print("Deleting device...")
        super().delete_device() # call last


if __name__ == "__main__":
    tango_arduino.run_server()