#v1
import serial

class ArduinoDevice:

    # real communication later
    baud_rate = 9600
    led_state="OFF"

    def __init__(self, baud_rate: int =9600):
        # some initial action
        # real communication later
        self.baud_rate=baud_rate
        self.led_state="OFF"

    def get_state(self) -> str:
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

