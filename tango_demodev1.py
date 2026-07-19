#v1
from logging import DEBUG
from os import access

from tango.server import Device
from tango.server import attribute, command
from tango.server import device_property
from tango import AttrQuality, DispLevel, DevState

class TangoDemodev1(Device):

    demo_property = device_property(dtype=str)

    logging_level = device_property(dtype=str)
    current_logging_level = device_property(dtype=str)
    logging_target = device_property(dtype=str)
    current_logging_target = device_property(dtype=str)
    logging_rft = device_property(dtype=str)  # file size
    logging_path = device_property(dtype=str)  # file path


    @attribute(dtype=str)
    def demo_attribute(self):
        res="demo_attribute_value"
        return res

    def init_device(self):
        super().init_device()  # call first

        # setup device polling
        self.poll_attribute("demo_attribute", 300)
        self.poll_attribute("State", 300)
        self.poll_attribute("Status", 300)

        print("Starting our demo device...")

        self.debug_stream("demodev1 is initialized")

    def delete_device(self):
        #self.arduino_device.close()
        print("Deleting demo device...")
        super().delete_device()  # call last

    @command()
    def demo_command(self):
        print("Demo command!")

if __name__ == "__main__":
    TangoDemodev1.run_server()