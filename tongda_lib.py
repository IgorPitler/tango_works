# Tongda TD-5000 console controls
#v2.0

import struct
import time

from prompt_toolkit.application import current
from pymodbus.client import ModbusTcpClient

class td5000:
    main_ip = None
    main_port = None

    detector_ip = None
    detector_port = None

    client_main = None
    client_detector = None

    positions = {
        "phi": 0.0,
        "2theta": 0.0,
        "omega": 0.0,
        "kappa": 0.0,
        #"limit": 0.0,
        "detector": 0.0
    }

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

    def connect_main(self):
        try:
            self.client_main = ModbusTcpClient(self.main_ip, port=self.main_port)
            if self.client_main.connect():
                print(f"Main TCP Connection successfully: {self.main_ip}:{self.main_port}")
                self._init_controller()
            else:
                print(f"Main Connection error: {self.main_ip}:{self.main_port}")
                self.client_main=None
        except Exception as e:
            print(f"Main connection error: {e}")
            self.client_main = None

    def connect_detector(self):
        try:
            self.client_detector = ModbusTcpClient(self.detector_ip, port=self.detector_port)
            if self.client_detector.connect():
                print(f"Detector TCP Connection successfully: {self.detector_ip}:{self.detector_port}")
            else:
                print(f"Detector Connection error: {self.detector_ip}:{self.detector_port}")
                self.client_detector = None
        except Exception as e:
            print(f"Detector connection error: {e}")
            self.client_detector = None

    def disconnect_all(self):
        self.disconnect_main()
        self.disconnect_detector()

    def disconnect_main(self):
        try:
            if self.client_main:
                self._close_controller()
                self.client_main.close()
                self.client_main = None
                print("Main client disconnected.")
            else:
                print("Main client was not connected")
        except Exception as e:
            print(f"Disconnect main exception: {e}")

    def disconnect_detector(self):
        try:
            if self.client_detector:
                self.client_detector.close()
                self.client_detector = None
                print("Detector client disconnected.")
            else:
                print("Detector client was not connected")
        except Exception as e:
            print(f"Disconnect detector exception: {e}")

    # for main only
    def _init_controller(self):
        self.process_command({'type': 'init_controller'})

    # for main only
    def _close_controller(self):
        self.process_command({'type': 'close_controller'})

    def _regs_to_float(self, r0, r1, byteorder='>'):
        try:
            b = struct.pack(byteorder + 'HH', r0, r1)
            return struct.unpack(byteorder + 'f', b)[0]
        except Exception as e:
            print(f"Exception _regs_to_float: {e}")
            return 0.0

    def _send_safe_write(self, client, reg, value):
        self.process_command({'type': 'safe_write', 'client': client, 'reg': reg, 'value': value})

    def _send_write_float(self, client, reg0, reg1, value):
        self.process_command({'type': 'write_float', 'client': client, 'reg0': reg0, 'reg1': reg1, 'value': value})

    # !!!! доработать вывод в принт
    def process_command(self, cmd: dict):
        """Process a command. All modbus read/writes go through here.

        Command examples:
            {'type': 'safe_write', 'client': 'main'|'detector', 'reg': int, 'value': int}
            {'type': 'write_float', 'client': 'main'|'detector', 'reg0': int, 'reg1': int, 'value': float}
            {'type': 'init_controller'}
            {'type': 'close_controller'}
        """
        try:
            t = cmd.get('type')
            client_name = cmd.get('client', 'main')
            client = self.client_main if client_name == 'main' else self.client_detector

            if t == 'safe_write':
                reg = int(cmd['reg'])
                value = int(cmd['value'])
                if client:
                    res = client.write_register(address=reg, value=value)
                    if hasattr(res, 'isError') and res.isError():
                        #self.log.emit(f"Write error reg {reg}: {res}")
                        print(f"Write error reg {reg}: {res}")
                    else:
                        #self.log.emit(f"Write reg {reg} = {value} ({client_name})")
                        pass
                else:
                    #self.log.emit(f"Write failed: client {client_name} not connected")
                    print(f"Write failed: client {client_name} not connected")

            elif t == 'write_float':
                reg0 = int(cmd['reg0'])
                reg1 = int(cmd['reg1'])
                val = float(cmd['value'])
                b = struct.pack('>f', val)
                regv0, regv1 = struct.unpack('>HH', b)
                # write two registers sequentially
                if client:
                    r1 = client.write_register(address=reg0, value=regv0)
                    if hasattr(r1, 'isError') and r1.isError():
                        #self.log.emit(f"Write float part1 error reg {reg0}: {r1}")
                        print(f"Write float part1 error reg {reg0}: {r1}")
                        pass
                    else:
                        #self.log.emit(f"Write reg {reg0} = {regv0} ({client_name})")
                        pass
                    r2 = client.write_register(address=reg1, value=regv1)
                    if hasattr(r2, 'isError') and r2.isError():
                        #self.log.emit(f"Write float part2 error reg {reg1}: {r2}")
                        print(f"Write float part2 error reg {reg1}: {r2}")
                        pass
                    else:
                        #self.log.emit(f"Write reg {reg1} = {regv1} ({client_name})")
                        #self.log.emit(f"Write float regs {reg0},{reg1} = {val} ({client_name})")
                        pass
                else:
                    #self.log.emit(f"Write float failed: client {client_name} not connected")
                    print(f"Write float failed: client {client_name} not connected")

            elif t == 'init_controller':
                # follow original sequence but all to main client
                if self.client_main:
                    seq = [(120, 0), (119, 2560), (120, 4096), (119, 512)]
                    for reg, val in seq:
                        r = self.client_main.write_register(address=reg, value=val)
                        time.sleep(0.05)
                    #self.log.emit("Controller init sequence executed")
                else:
                    #self.log.emit("Init failed: main client not connected")
                    print("Init failed: main client not connected")

            elif t == 'close_controller':
                if self.client_main:
                    seq = [(119, 512), (100, 1280), (35, 1280), (70, 1280), (0, 1280), (120, 512), (120, 8192)]
                    for reg, val in seq:
                        r = self.client_main.write_register(address=reg, value=val)
                        time.sleep(0.05)
                    #self.log.emit("Controller close sequence executed")
                else:
                    print("Close failed: main client not connected")

            else:
                #self.log.emit(f"Unknown command type: {t}")
                print(f"Unknown command type: {t}")
                pass
        except Exception as e:
            #self.log.emit(f"Exception processing command {cmd}: {e}")
            print(f"Exception processing command {cmd}: {e}")

    def controller_main_read_register_pair(self, address_first):
        registers_value=0.0
        try:
            if self.client_main:
                resp = self.client_main.read_holding_registers(address=address_first, count=2)
                if resp and not resp.isError():
                    regs = resp.registers
                    registers_value = self._regs_to_float(regs[0], regs[1])
                else:
                    print(f"Main modbus read error: {resp}")
            else:
                print("Main client not connected")
        except Exception as e:
            print(f"Exception polling main: {e}")
        return registers_value

    def controller_main_read_register_single(self, address_first):
        register_value=0.0
        try:
            if self.client_main:
                resp = self.client_main.read_holding_registers(address=address_first, count=1)
                if resp and not resp.isError():
                    regs = resp.registers
                    register_value = self._regs_to_float(regs[0], 0)
                else:
                    print(f"Main modbus read error: {resp}")
            else:
                print("Main client not connected")
        except Exception as e:
            print(f"Exception polling main: {e}")
        return register_value

    def controller_detector_read_register_pair(self, address_first):
        registers_value=0.0
        try:
            if self.client_detector:
                resp = self.client_detector.read_holding_registers(address=address_first, count=2)
                if resp and not resp.isError():
                    regs = resp.registers
                    registers_value = self._regs_to_float(regs[0], regs[1])
                else:
                    print(f"Detector modbus read error: {resp}")
            else:
                print("Detector client not connected")
        except Exception as e:
            print(f"Exception polling detector: {e}")
        return registers_value

    # MOVEMENT COMMANDS:

    def status(self):
        # Poll main device (read holding registers 0..124)
        try:
            if self.client_main:
                resp = self.client_main.read_holding_registers(address=0, count=125)
                if resp and not resp.isError():
                    regs = resp.registers
                    self.positions["phi"] = self._regs_to_float(regs[109], regs[110])
                    self.positions["2theta"] = self._regs_to_float(regs[15], regs[16])
                    self.positions["omega"] = self._regs_to_float(regs[50], regs[51])
                    self.positions["kappa"] = self._regs_to_float(regs[82], regs[83])
                    #self.positions["limit"] = self._regs_to_float(regs[68], 0)

                    print("phi: " + str(self.positions["phi"]))
                    print("2theta: " + str(self.positions["2theta"]))
                    print("omega: " + str(self.positions["omega"]))
                    print("kappa: " + str(self.positions["kappa"]))
                    #print("limit: " + str(self.positions["limit"]))
                else:
                    print(f"Main modbus read error: {resp}")
            else:
                print("Main client not connected")
                pass
        except Exception as e:
            print(f"Exception polling main: {e}")

        # Poll detector device (registers 13 & 14 per user)
        try:
            if self.client_detector:
                resp = self.client_detector.read_holding_registers(address=13, count=2)
                if resp and not resp.isError():
                    regs = resp.registers
                    self.positions["detector"] = self._regs_to_float(regs[0], regs[1])

                    print("detector position: " + str(self.positions["detector"]))
                else:
                    print(f"Detector modbus read error: {resp}")
            else:
                print("Detector client not connected")
        except Exception as e:
            print(f"Exception polling detector: {e}")

    # for service use only
    # use it to update postion array data without any output
    def update_positions(self):
        # Poll main device (read holding registers 0..124)
        try:
            if self.client_main:
                resp = self.client_main.read_holding_registers(address=0, count=125)
                if resp and not resp.isError():
                    regs = resp.registers
                    self.positions["phi"] = self._regs_to_float(regs[109], regs[110])
                    self.positions["2theta"] = self._regs_to_float(regs[15], regs[16])
                    self.positions["omega"] = self._regs_to_float(regs[50], regs[51])
                    self.positions["kappa"] = self._regs_to_float(regs[82], regs[83])
                    #self.positions["limit"] = self._regs_to_float(regs[68], 0)

                else:
                    print(f"Main modbus read error: {resp}")
            else:
                print("Main client not connected")
                pass
        except Exception as e:
            print(f"Exception polling main: {e}")

        # Poll detector device (registers 13 & 14 per user)
        try:
            if self.client_detector:
                resp = self.client_detector.read_holding_registers(address=13, count=2)
                if resp and not resp.isError():
                    regs = resp.registers
                    self.positions["detector"] = self._regs_to_float(regs[0], regs[1])

                else:
                    print(f"Detector modbus read error: {resp}")
            else:
                print("Detector client not connected")
        except Exception as e:
            print(f"Exception polling detector: {e}")

    # reserved, not use
    #def command_limit_reset(self):
    #    self._send_safe_write('main', 120, 1024)

    def command_shutter_open(self):
        self._send_safe_write('main', 120, 256)
        self._send_safe_write('main', 119, 2560)

    def command_shutter_close(self):
        self._send_safe_write('main', 120, 512)
        self._send_safe_write('main', 119, 512)

    # PHI

    def command_phi_abs(self, abs_value):
        try:
            self._send_safe_write('main', 100, 1280)
            self._send_write_float('main', 105, 106, float(abs_value))
            self._send_safe_write('main', 100, 2304)
        except Exception as e:
            print(f"command_phi_abs exception {e}")

    def command_phi_rel(self, rel_value):
        try:
            self._send_safe_write('main', 100, 1280)
            self._send_write_float('main', 103, 104, float(rel_value))
            self._send_safe_write('main', 100, 4352)
        except Exception as e:
            print(f"command_phi_rel exception {e}")

    def command_phi_speed(self, speed):
        try:
            self._send_safe_write('main', 100, 1280)
            self._send_write_float('main', 107, 108, float(speed))
        except Exception as e:
            print(f"command_phi_speed exception {e}")

    def command_phi_home(self):
        try:
            self._send_safe_write('main', 100, 1280)
            self._send_safe_write('main', 101, 3)
            self._send_safe_write('main', 100, 768)
        except Exception as e:
            print(f"command_phi_home exception {e}")

    def command_phi_rotate(self):
        try:
            self._send_safe_write('main', 100, 1280)
            self._send_safe_write('main', 100, 16640)
        except Exception as e:
            print(f"command_phi_rotate exception {e}")

    def command_phi_stop(self):
        try:
            self._send_safe_write('main', 100, 1280)
        except Exception as e:
            print(f"command_phi_stop exception {e}")

    # 2THETA

    def command_tetta_stop(self):
        try:
            self._send_safe_write('main', 0, 1280)
        except Exception as e:
            print(f"command_tetta_stop exception {e}")

    def command_tetta_speed(self, speed):
        try:
            self._send_safe_write('main', 0, 1280)
            self._send_write_float('main', 7, 8, float(speed))
        except Exception as e:
            print(f"command_tetta_speed exception {e}")

    def command_tetta_rel(self, rel_value):
        try:
            self._send_safe_write('main', 0, 1280)
            self._send_write_float('main', 3, 4, float(rel_value))
            self._send_safe_write('main', 0, 4352)
        except Exception as e:
            print(f"command_tetta_rel exception {e}")

    def command_tetta_home(self):
        try:
            self._send_safe_write('main', 0, 1280)
            self._send_safe_write('main', 1, 3)
            self._send_safe_write('main', 0, 768)
        except Exception as e:
            print(f"command_tetta_home exception {e}")

    def command_tetta_abs(self, abs_target):
        try:
            self._send_safe_write('main', 0, 1280)
            self._send_write_float('main', 5, 6, float(abs_target))
            self._send_safe_write('main', 0, 2304)
        except Exception as e:
            print(f"command_tetta_abs exception {e}")

    # OMEGA

    def command_omega_abs(self, abs_target):
        try:
            self._send_safe_write('main', 35, 1280)
            self._send_write_float('main', 40, 41, float(abs_target))
            self._send_safe_write('main', 35, 2304)
        except Exception as e:
            print(f"command_omega_abs exception {e}")

    def command_omega_home(self):
        try:
            self._send_safe_write('main', 35, 1280)
            self._send_safe_write('main', 36, 3)
            self._send_safe_write('main', 35, 768)
        except Exception as e:
            print(f"command_omega_home exception {e}")

    def command_omega_speed(self, speed):
        try:
            self._send_safe_write('main', 35, 1280)
            self._send_write_float('main', 42, 43, float(speed))
        except Exception as e:
            print(f"command_omega_speed exception{e}")

    def command_omega_rel(self, rel):
        try:
            self._send_safe_write('main', 35, 1280)
            self._send_write_float('main', 38, 39, float(rel))
            self._send_safe_write('main', 35, 4352)
        except Exception as e:
            print(f"command_omega_rel exception {e}")

    def command_omega_stop(self):
        try:
            self._send_safe_write('main', 35, 1280)
        except Exception as e:
            print(f"command_omega_stop exception {e}")

    # KAPPA

    def command_kappa_speed(self, speed):
        try:
            self._send_safe_write('main', 70, 1280)
            self._send_write_float('main', 76, 77, float(speed))
        except Exception as e:
            print(f"command_kappa_speed exception {e}")

    def command_kappa_home(self):
        try:
            self._send_safe_write('main', 70, 1280)
            self._send_safe_write('main', 71, 3)
            self._send_safe_write('main', 70, 768)
        except Exception as e:
            print(f"command_kappa_home exception {e}")

    def command_kappa_rel(self, rel_target):
        try:
            self._send_safe_write('main', 70, 1280)
            self._send_write_float('main', 72, 73, float(rel_target))
            self._send_safe_write('main', 70, 4352)
        except Exception as e:
            print(f"command_kappa_rel exception {e}")

    def command_kappa_abs(self, abs_target):
        try:
            self._send_safe_write('main', 70, 1280)
            self._send_write_float('main', 74, 75, float(abs_target))
            self._send_safe_write('main', 70, 2304)
        except Exception as e:
            print(f"command_kappa_abs exception {e}")

    def command_kappa_stop(self):
        try:
            self._send_safe_write('main', 70, 1280)
        except Exception as e:
            print(f"command_kappa_stop exception {e}")

    # DETECTOR POSITION

    def command_detector_stop(self):
        try:
            self._send_safe_write('detector', 0, 1280)
        except Exception as e:
            print(f"command_detector_stop exception {e}")

    def command_detector_speed(self, speed):
        try:
            self._send_safe_write('detector', 0, 1280)
            self._send_write_float('detector', 7, 8, float(speed))
        except Exception as e:
            print(f"command_detector_speed exception {e}")

    def command_detector_rel(self, rel_target):
        try:
            self._send_safe_write('detector', 0, 1280)
            self._send_write_float('detector', 3, 4, float(rel_target))
            self._send_safe_write('detector', 0, 4352)
        except Exception as e:
            print(f"command_detector_rel exception {e}")

    def command_detector_home(self):
        try:
            self._send_safe_write('detector', 0, 1280)
            self._send_safe_write('detector', 1, 3)
            self._send_safe_write('detector', 0, 768)
        except Exception as e:
            print(f"command_detector_home exception {e}")

    def command_detector_abs(self, abs_target):
        try:
            self._send_safe_write('detector', 0, 1280)
            self._send_write_float('detector', 5, 6, float(abs_target))
            self._send_safe_write('detector', 0, 2304)
        except Exception as e:
            print(f"command_detector_abs exception {e}")

    def source_on(self):
        print("source on")

    def source_off(self):
        print("source off")

    def source_warmup(self):
        print("source warmup")

    def source_status(self):
        print("source status")
        self.source_getV()
        self.source_getI()

    def source_setV(self, voltage):
        print(f"source setV {voltage}")

    def source_setI(self, current):
        print(f"source setI {current}")

    def source_getV(self) -> float:
        voltage=50000
        print(f"source getV {voltage}")
        return voltage

    def source_getI(self) -> float:
        current=12
        print(f"source getI {current}")
        return current

    def safety_check(self, theta : float = 0, omega : float = 0, kappa : float = 0, detector_pos : float = 0) -> bool:
        allow= True

        if detector_pos < 0 or detector_pos > 65 :
            return False

        if theta < -65 or theta > 90 :
            return False

        if kappa < -72 or theta > 72 :
            return False

        if kappa == 0 :
            if omega < theta-90 or omega > theta+90 :
                return False

        if kappa < 0 :
            if omega < theta-90 or omega > theta+30 :
                return False

        if kappa > 0 :
            if omega < theta-30 or omega > theta+90 :
                return False

        return allow

    # TODO, return 4 values!
    def safety_rel_to_abs(self):
        res=1
        return res