#v1
import arduino_class
print("Tango!")

# PyTango imports

from tango.server import Device
from tango.server import attribute, command
from tango.server import device_property
from tango import AttrQuality, DispLevel, DevState
from tango import AttrWriteType
# Additional import

class tango_arduino(Device):

    #arduino_device=arduino_class.ArduinoDevice()


    port_name=device_property(dtype=str)



    @attribute(dtype=str)
    def led_state(self):
        # temp
        arduino_state=self.arduino_device.get_led_state()
        return arduino_state

    # built-in attributes State and Status

    @command()
    def set_led_on(self):
        self.arduino_device.set_led_on()
        print('Turning on the LED')
        print("LED is "+self.arduino_device.get_led_state()+" Port is: "+self.arduino_device.port_name)

    @command()
    def set_led_off(self):
        self.arduino_device.set_led_off()
        print('Turning off the LED')

    def init_device(self):
        super().init_device() # call first
        # runs on device initialization
        print("Starting our device...")

        self.arduino_device=arduino_class.ArduinoDevice(self.port_name, 9600)

        #test!
        self.set_state(DevState.ON)
        self.set_status("Running OK")

    def delete_device(self):
        pass
        self.arduino_device.close()
        print("Deleting device...")
        super().delete_device() # call last


# test
#myArduino=arduino_class.ArduinoDevice()
#print("Arduino state: "+myArduino.get_state())


if __name__ == "__main__":
    tango_arduino.run_server()