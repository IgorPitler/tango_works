#v1
import serial

class ArduinoDevice:

    # real communication later
    #port_name="/dev/ttyUSB0"
    port_name = "no_port"
    baud_rate = 9600
    led_state="OFF"

    #def __init__(self, port_name: str="/dev/ttyUSB0", baud_rate: int =9600):
    def __init__(self, port_name: str = "no_port", baud_rate: int = 9600):
        # some initial action
        # real communication later
        self.port_name=port_name
        self.baud_rate=baud_rate
        self.led_state="OFF"

    def get_led_state(self) -> str:
        return self.led_state

    def set_led_on(self):
        # add real communication later
        self.led_state="ON"

    def set_led_off(self):
        # add real communication later
        self.led_state="OFF"

    def close(self):
        # closing connection and stuff like that
        pass

