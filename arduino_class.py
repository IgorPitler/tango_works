# v1
import time

import py_serial_lib


class ArduinoDevice:

    # port_name="/dev/ttyUSB0"

    baud_rate = 9600
    led_state = "OFF"

    def __init__(
        self, port_name: str = "/dev/ttyUSB0", baud_rate: int = 9600, timeout: int = 1
    ):
        # some initial action
        self.real_arduino = py_serial_lib.SerialDevice(port_name, baud_rate, timeout)
        # Arduino tells "CONNECTED" on this real device
        self.port_name = port_name
        self.baud_rate = baud_rate
        self.led_state = "OFF"

    def get_led_state(self) -> str:
        self.real_arduino.send("GETSTATE.")
        self.led_state = self.real_arduino.get_response()
        # it has timeout on Arduino, need wait ?
        return self.led_state

    def set_led_on(self):
        start_time = time.perf_counter()
        self.real_arduino.send("ON.")
        end_time = time.perf_counter()
        print(f"real_arduino set_led_on Execution time: {end_time - start_time:.7f} seconds")
        self.led_state = "ON"

    def set_led_off(self):
        start_time = time.perf_counter()
        self.real_arduino.send("OFF.")
        end_time = time.perf_counter()
        print(f"real_arduino set_led_off Execution time: {end_time - start_time:.7f} seconds")
        self.led_state = "OFF"

    def close(self):
        # closing connection and stuff like that
        self.real_arduino.close()


# print('Error : '+arduino.get_error_description())

# answer=arduino.get_response() # contains CONNECTED on my Arduino

# print(answer)
