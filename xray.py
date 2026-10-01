#v1
import time
import py_serial_lib

class XraySource:

    port_name="/dev/ttyUSB0"
    baud_rate = 9600
    timeout: int = 1

    def __init__(self, port_name : str ="/dev/ttyUSB0", baud_rate : int = 9600, timeout : int = 1):
        self.port_name=port_name
        self.baud_rate=baud_rate
        self.timeout=timeout

    def connect(self):
        self.xray_device = py_serial_lib.SerialDevice(self.port_name, self.baud_rate, self.timeout)

    def disconnect(self):
        self.xray_device.close()

    def send_command(self, command : str =""):
        self.xray_device.send(command)

    def get_response(self) -> str :
        r = self.xray_device.get_response()
        return r

    def get_status(self):
        res=""
        return res

    def test1(self) -> str :
        self.send_command("ON.")
        # read response
        self.send_command("GETSTATE.")
        r = self.get_response()
        print(r)

        time.sleep(2)
        self.send_command("OFF.")
        # read response
        self.send_command("GETSTATE.")
        r = self.get_response()
        print(r)

    # only positive
    def get_12bit_value(self, value : int = 0, hardware_max : int = 1):
        if value > hardware_max:
            return 4095
        if value < 0:
            return 0
        res=round((value/hardware_max)*4095)
        return res

    def get_real_value_of_12bit(self, value: int = 0, hardware_max: int = 1) -> int:
        if value > 4095:
            return hardware_max
        if value < 0:
            return 0
        res=round((value/4095)*hardware_max)
        return res

    def prepare_command(self, p1 : int, p2 : int, p3 : int, p4 : int) -> str:
        res=str(p1)+","+str(p2)+","+str(p3)+","+str(p4)
        res=res+bytes.fromhex("03").decode()
        return res

    def trim_incoming(self, data_string : str) -> str:
        res=""

        # strip start and end symbols from string-list
        # s = txt.strip(",.grt")

        return res
# test !
x=XraySource("/dev/ttyUSB0", 9600, 2)
#x.connect()
#x.test1()
#x.disconnect()
print(x.get_12bit_value(49999, 50000))
print(x.get_real_value_of_12bit(4095, 50000))

print(x.prepare_command(1,2,3,4))




