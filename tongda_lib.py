from pymodbus.client import ModbusTcpClient

class td5000:
    main_ip = None
    main_port = None

    detector_ip = None
    detector_port = None

    client_main = None
    client_detector = None

    #main_connected = False
    #detector_connected = False

    def __init__(self, main_ip: str, main_port: int, detector_ip: str, detector_port: int):
        self.main_ip = main_ip
        self.main_port = main_port
        self.detector_ip = detector_ip
        self.detector_port = detector_port

    def connect_all(self):
        self.connect_main()
        self.connect_detector()
        print("connect all sent")

    def connect_main(self):
        try:
            self.client_main = ModbusTcpClient(self.main_ip, port=self.main_port)
            if self.client_main.connect():
                print(f"Main TCP Connection successfully: {self.main_ip}:{self.main_port}")
                self._init_controller()
            else:
                print(f"Main Connection error: {self.main_ip}:{self.main_port}")
        except Exception as e:
            print(f"Main connection error: {e}")
        print("connect main sent")

    def connect_detector(self):
        try:
            self.client_detector = ModbusTcpClient(self.detector_ip, port=self.detector_port)
            if self.client_detector.connect():
                print(f"Detector TCP Connection successfully: {self.detector_ip}:{self.detector_port}")
            else:
                print(f"Detector Connection error: {self.detector_ip}:{self.detector_port}")
        except Exception as e:
            print(f"Detector connection error: {e}")
        print("connect detector sent")

    def disconnect_all(self):
        self.disconnect_main()
        self.disconnect_detector()
        print("disconnect all OK")

    def disconnect_main(self):
        try:
            pass
        except Exception as e:
            pass
        print("disconnect main sent")

    def disconnect_detector(self):
        try:
            pass
        except Exception as e:
            pass
        print("disconnect detector sent")

    def _init_controller(self):
        # for Main only!
        pass

    def _close_controller(self):
        pass

    # Доработать позже!
    def check_limits(phi, theta, omega, kappa, detector_pos):
        allow = True
        # here we will check if the axis positions are dangerous
        return allow