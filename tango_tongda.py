#v1

import diffractometer_commands

from logging import DEBUG
from os import access

from tango.server import Device
from tango.server import attribute, command
from tango.server import device_property
from tango import AttrQuality, DispLevel, DevState

class tango_tongda(Device):

    port_name = device_property(dtype=str)

    logging_level = device_property(dtype=str)
    current_logging_level = device_property(dtype=str)
    logging_target = device_property(dtype=str)
    current_logging_target = device_property(dtype=str)
    logging_rft = device_property(dtype=str)  # file size
    logging_path = device_property(dtype=str)  # file path

    @attribute(dtype=str)
    def led_state(self):
        return self.arduino_device.get_led_state()

    @command(dtype_in=str)
    def set_led_on(self, par1):
        self.arduino_device.set_led_on()
        self.set_status("Status: LED is ON")
        self.set_state(DevState.ON)
        print("Turning ON the LED")

        #self.debug_stream("Turning ON the LED")

    @command()
    def set_led_off(self):
        self.arduino_device.set_led_on()
        self.set_status("Status: LED is ON")
        self.set_state(DevState.ON)
        print("Turning ON the LED")

        #self.debug_stream("Turning ON the LED")

    def init_device(self):
        super().init_device()  # call first
        print("Starting our device...")

    def delete_device(self):
        #self.arduino_device.close()
        print("Deleting device...")
        super().delete_device()  # call last

if __name__ == "__main__":
    tango_tongda.run_server()