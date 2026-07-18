#v1
from logging import DEBUG
from os import access

from tango.server import Device
from tango.server import attribute, command
from tango.server import device_property
from tango import AttrQuality, DispLevel, DevState

class tango_demodev1(Device):

    demo_property = device_property(dtype=str)

    logging_level = device_property(dtype=str)
    current_logging_level = device_property(dtype=str)
    logging_target = device_property(dtype=str)
    current_logging_target = device_property(dtype=str)
    logging_rft = device_property(dtype=str)  # file size
    logging_path = device_property(dtype=str)  # file path


    @attribute(dtype=str)
    def demo_attribute(self):
        return "demo_attribute_value"

    def init_device(self):
        super().init_device()  # call first
        print("Starting our demo device...")

    def delete_device(self):
        #self.arduino_device.close()
        print("Deleting demo device...")
        super().delete_device()  # call last

if __name__ == "__main__":
    tango_demodev1.run_server()