"""Модуль для работы с последовательным портом"""

# version 1.26
# by Igor Pitler
# uses pyserial
# install command: sudo apt install python3-serial

# TO DO list:
# 1. add error logging to files?

import serial


class SerialDevice:
    """Класс для работы с последовательным портом. Отправка и чтение данных происходят в строковом виде."""

    port = ""
    baudrate = 9600
    timeout = 1
    encoding = "utf-8"
    # serial_dev

    # 0 no error, 1 timeout, 2 common serial error 3 obj not initialised
    err_code = 0
    err_description = ""

    def get_error_code(self) -> int:
        """Получение сохраненного в объекте кода ошибки в целочисленном виде"""

        return self.err_code

    def get_error_description(self) -> str:
        """Получение сохраненного в объекте описания ошибки в виде строки"""

        return self.err_description

    def set_error(self, code: int, description: str = ""):
        """Сохранение кода и описания ошибки во внутренней переменной класса"""
        self.err_code = code
        self.err_description = description

    def __init__(
        self, port: str = "/dev/ttyUSB0", baudrate: int = 9600, timeout: int = 3
    ):

        self.port = port
        self.baudrate = baudrate
        self.timeout = timeout
        try:
            self.serial_dev = serial.Serial(
                port=self.port,
                baudrate=self.baudrate,
                bytesize=serial.EIGHTBITS,
                parity=serial.PARITY_NONE,
                stopbits=serial.STOPBITS_ONE,
                timeout=self.timeout,
            )

        except serial.SerialTimeoutException as te:
            self.set_error(1, te.strerror)
            print("Serial timeout exception!")
        except serial.SerialException as e:
            self.set_error(2, e.strerror)
            print("Serial exception!")

    def close(self):
        """Закрыть порт"""
        try:
            self.serial_dev.close()
        except AttributeError as ae:
            self.set_error(3, ae.name)
            print(
                "Attribute error exception!"
            )  # возникает при неудачной инициализации порта

    def send(self, str_data: str):
        """Отправка строки в порт"""
        command = str_data.encode(self.encoding)
        self.set_error(0)
        try:
            self.serial_dev.write(command)
        except serial.SerialTimeoutException as te:
            self.set_error(1, te.strerror)
            print("Serial timeout exception!")
        except serial.SerialException as e:
            self.set_error(2, e.strerror)
            print("Serial exception!")
        except AttributeError as ae:
            self.set_error(3, ae.name)
            print("Attribute error exception!")

    def get_response(self) -> str:
        """Чтение строки из порта"""
        response = ""
        self.set_error(0)
        try:
            response = (
                self.serial_dev.readline().decode(self.encoding).strip()
            )  # arduino finish string with \n !
        except serial.SerialTimeoutException as te:
            self.set_error(1, te.strerror)
            print("Serial timeout exception!")
        except serial.SerialException as e:
            self.set_error(2, e.strerror)
            print("Serial exception!")
        except AttributeError as ae:
            self.set_error(3, ae.name)
            print("Attribute error exception!")
        return response
