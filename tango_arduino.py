# v1
from logging import DEBUG
from os import access

import arduino_class

from tango.server import Device
from tango.server import attribute, command
from tango.server import device_property
from tango import AttrQuality, DispLevel, DevState


class tango_arduino(Device):

    port_name = device_property(dtype=str)

    logging_level = device_property(dtype=str)
    current_logging_level = device_property(dtype=str)
    logging_target = device_property(dtype=str)
    current_logging_target = device_property(dtype=str)
    logging_rft = device_property(dtype=str) # file size
    logging_path = device_property(dtype=str) # file path

    @attribute(dtype=str)
    def led_state(self):
        return self.arduino_device.get_led_state()

    # led_state=attribute(label="LED state attribute", dtype=str, fget="read_led_state", access=AttrWriteType.READ)
    # @led_state.getter
    # def read_led_state(self) -> str:
    #    return self.arduino_device.get_led_state()

    @command()
    def set_led_on(self):
        self.arduino_device.set_led_on()
        self.set_status("Status: LED is ON")
        self.set_state(DevState.ON)
        print("Turning ON the LED")

        self.debug_stream("Turning ON the LED")

    @command()
    def set_led_off(self):
        self.arduino_device.set_led_off()
        self.set_status("Status: LED is OFF")
        self.set_state(DevState.OFF)
        print("Turning OFF the LED")

        self.debug_stream("Turning OFF the LED")

    def init_device(self):
        super().init_device()  # call first
        print("Starting our device...")

        self.arduino_device = arduino_class.ArduinoDevice(self.port_name, 9600)
        self.set_state(DevState.INIT)
        self.set_status("Status: Init")

        # setting up logging
        #self.logging_target = "device::lab1/table1/dev2"
        #self.current_logging_target="device::lab1/table1/dev2"
        #self.logging_level = 4  # DEBUG
        #self.current_logging_level = 4# DEBUG



    def delete_device(self):
        self.arduino_device.close()
        print("Deleting device...")
        super().delete_device()  # call last


if __name__ == "__main__":
    tango_arduino.run_server()
