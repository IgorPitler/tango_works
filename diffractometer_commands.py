# v1 15.07.2026

import struct
import time

from pymodbus.client import ModbusTcpClient

class DiffractometerCommands:

    main_ip = None
    main_port= None

    detector_ip= None
    detector_port = None

    client_main = None
    client_detector = None

    main_connected= False
    detector_connected = False

    # reserved
    # updated only from update_position_data() !!!!
    positions = {
        "phi": 0.0,
        "tetta": 0.0,
        "omega": 0.0,
        "kappa": 0.0,
        "limit_switch": 0.0,
        "detector": 0.0
    }

    # error logging...

    errors_count = 0
    error_descriptions=""

    def get_error_counts(self):
        res=self.errors_count

        # reset error counter
        self.errors_count=0
        return res

    def get_error_descriptions(self):
        desc=self.error_descriptions

        #reset error descriptions
        self.error_descriptions=""
        return desc

    def set_error(self, error_description):
        self.errors_count=self.errors_count+1
        self.error_descriptions=self.error_descriptions+"\n"+error_description

    # end error logging

    def __init__(self, main_ip: str, main_port: str, detector_ip: str, detector_port: str):

        self.main_ip = main_ip
        self.main_port = main_port
        self.detector_ip = detector_ip
        self.detector_port = detector_port

        self.start_clients(self.main_ip, self.main_port, self.detector_ip, self.detector_port)

    def start_clients(self, ip_main, port_main, ip_detector, port_detector):
        try:
            self.client_main = ModbusTcpClient(ip_main, port=port_main)
            if not self.client_main.connect():
                #self.log.emit(f"Failed to connect main: {ip_main}:{port_main}")
                self.set_error(f"Failed to connect main: {ip_main}:{port_main}")
                self.client_main.close()
                self.client_main = None
                self.main_connected= False
            else:
                #self.log.emit(f"Connected main: {ip_main}:{port_main}")
                self.main_connected=True
                # send command to init controller
                self.command_init_controller()

        except Exception as e:
            self.client_main = None
            self.main_connected=False
            self.set_error("start_clients exception")

        try:
            self.client_detector = ModbusTcpClient(ip_detector, port=port_detector)
            if not self.client_detector.connect():
                #self.log.emit(f"Failed to connect detector: {ip_detector}:{port_detector}")
                self.set_error(f"Failed to connect detector: {ip_detector}:{port_detector}")
                self.client_detector.close()
                self.client_detector = None
                self.detector_connected=False
            else:
                #self.log.emit(f"Connected detector: {ip_detector}:{port_detector}")
                self.detector_connected=True
        except Exception as e:
            self.client_detector = None
            self.detector_connected=False
            self.set_error("start_clients detector exception")

    def stop_clients(self):
        try:
            if self.client_main:
                # send command to close
                self.command_close_controller()

                self.client_main.close()
                self.client_main = None
                self.main_connected=False
        except Exception as e:
            self.set_error("stop_clients main exception")
        try:
            if self.client_detector:
                self.client_detector.close()
                self.client_detector = None
                self.detector_connected=False
        except Exception as e:
            self.set_error("stop_clients detector exception")

    def _regs_to_float(self, r0, r1, byteorder='>'):
        try:
            b = struct.pack(byteorder + 'HH', r0, r1)
            return struct.unpack(byteorder + 'f', b)[0]
        except Exception as e:
            self.set_error("_regs_to_float exception")
            return 0.0

    def read_position_phi(self):
        # 109 110
        pos=self.controller_main_read_register_pair(109)
        return pos

    def read_position_tetta(self):
        # 15 16
        pos = self.controller_main_read_register_pair(15)
        return pos

    def read_position_omega(self):
        # 50 51
        pos = self.controller_main_read_register_pair(50)
        return pos

    def read_position_kappa(self):
        # 82 83
        pos = self.controller_main_read_register_pair(82)
        return pos

    def read_position_limit_switch(self):
        # 68
        pos=self.controller_main_read_register_single(68)
        return pos

    def read_position_detector(self):
        # 13 14
        detector_pos=self.controller_detector_read_register_pair(13)
        return detector_pos

    def controller_main_read_register_pair(self, address_first):
        registers_value=0.0
        try:
            if self.client_main:
                resp = self.client_main.read_holding_registers(address=address_first, count=2)
                if resp and not resp.isError():
                    regs = resp.registers
                    registers_value = self._regs_to_float(regs[0], regs[1])
                else:
                    #self.log.emit(f"Main modbus read error: {resp}")
                    self.set_error(f"Main modbus read error: {resp}")
                    pass
            else:
                #self.log.emit("Main client not connected")
                self.set_error("Main client not connected")
                pass
        except Exception as e:
            #self.log.emit(f"Exception polling main: {e}")
            self.set_error(f"Exception polling main: {e}")
            pass
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
                    #self.log.emit(f"Main modbus read error: {resp}")
                    self.set_error(f"Main modbus read error: {resp}")
                    pass
            else:
                #self.log.emit("Main client not connected")
                self.set_error("Main client not connected")
                pass
        except Exception as e:
            #self.log.emit(f"Exception polling main: {e}")
            self.set_error(f"Exception polling main: {e}")
            pass
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
                    # self.log.emit(f"Detector modbus read error: {resp}")
                    self.set_error(f"Detector modbus read error: {resp}")
                    pass
            else:
                # self.log.emit("Detector client not connected")
                self.set_error("Detector client not connected")
                pass
        except Exception as e:
            # self.log.emit(f"Exception polling detector: {e}")
            self.set_error(f"Exception polling detector: {e}")
            pass
        return registers_value

    # reserved, no error reporting!
    def update_position_data(self):
        # Poll main device (read holding registers 0..124)
        try:
            if self.client_main:
                resp = self.client_main.read_holding_registers(address=0, count=125)
                if resp and not resp.isError():
                    regs = resp.registers
                    self.positions["phi"] = self._regs_to_float(regs[109], regs[110])
                    self.positions["tetta"] = self._regs_to_float(regs[15], regs[16])
                    self.positions["omega"] = self._regs_to_float(regs[50], regs[51])
                    self.positions["kappa"] = self._regs_to_float(regs[82], regs[83])
                    self.positions["limit_switch"] = self._regs_to_float(regs[68], 0)
                else:
                    #self.log.emit(f"Main modbus read error: {resp}")
                    pass
            else:
                #self.log.emit("Main client not connected")
                pass
        except Exception as e:
            #self.log.emit(f"Exception polling main: {e}")
            pass

        # Poll detector device (registers 13 & 14 per user)
        try:
            if self.client_detector:
                resp = self.client_detector.read_holding_registers(address=13, count=2)
                if resp and not resp.isError():
                    regs = resp.registers
                    self.positions["detector"] = self._regs_to_float(regs[0], regs[1])
                else:
                    #self.log.emit(f"Detector modbus read error: {resp}")
                    pass
            else:
                #self.log.emit("Detector client not connected")
                pass
        except Exception as e:
            #self.log.emit(f"Exception polling detector: {e}")
            pass

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
                        self.set_error(f"Write error reg {reg}: {res}")
                    else:
                        #self.log.emit(f"Write reg {reg} = {value} ({client_name})")
                        pass
                else:
                    #self.log.emit(f"Write failed: client {client_name} not connected")
                    self.set_error(f"Write failed: client {client_name} not connected")
                    pass

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
                        self.set_error(f"Write float part1 error reg {reg0}: {r1}")
                        pass
                    else:
                        #self.log.emit(f"Write reg {reg0} = {regv0} ({client_name})")
                        pass
                    r2 = client.write_register(address=reg1, value=regv1)
                    if hasattr(r2, 'isError') and r2.isError():
                        #self.log.emit(f"Write float part2 error reg {reg1}: {r2}")
                        self.set_error(f"Write float part2 error reg {reg1}: {r2}")
                        pass
                    else:
                        #self.log.emit(f"Write reg {reg1} = {regv1} ({client_name})")
                        #self.log.emit(f"Write float regs {reg0},{reg1} = {val} ({client_name})")
                        pass
                else:
                    #self.log.emit(f"Write float failed: client {client_name} not connected")
                    self.set_error(f"Write float failed: client {client_name} not connected")
                    pass

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
                    self.set_error("Init failed: main client not connected")
                    pass

            elif t == 'close_controller':
                if self.client_main:
                    seq = [(119, 512), (100, 1280), (35, 1280), (70, 1280), (0, 1280), (120, 512), (120, 8192)]
                    for reg, val in seq:
                        r = self.client_main.write_register(address=reg, value=val)
                        time.sleep(0.05)
                    #self.log.emit("Controller close sequence executed")
                else:
                    #self.log.emit("Close failed: main client not connected")
                    self.set_error("Close failed: main client not connected")
                    pass

            else:
                #self.log.emit(f"Unknown command type: {t}")
                self.set_error(f"Unknown command type: {t}")
                pass
        except Exception as e:
            #self.log.emit(f"Exception processing command {cmd}: {e}")
            self.set_error(f"Exception processing command {cmd}: {e}")
            pass

    # helpers

    def _send_safe_write(self, client, reg, value):
        self.process_command({'type': 'safe_write', 'client': client, 'reg': reg, 'value': value})

    def _send_write_float(self, client, reg0, reg1, value):
        self.process_command({'type': 'write_float', 'client': client, 'reg0': reg0, 'reg1': reg1, 'value': value})

    # commands:

    # reserved, not use
    def command_limit_reset(self):
        try:
            self._send_safe_write('main', 120, 1024)
        except Exception as e:
            self.set_error("command_limit_reset exception")

    #later add call to it at connect
    def command_init_controller(self):
        self.process_command({'type': 'init_controller'})

    # later add call to it at disconnect (close)
    def command_close_controller(self):
        self.process_command({'type': 'close_controller'})

    def command_shutter_open(self):
        self._send_safe_write('main', 120, 512)
        self._send_safe_write('main', 119, 512)

    def command_shutter_close(self):
        self._send_safe_write('main', 120, 512)
        self._send_safe_write('main', 119, 512)

    ### PHI

    def command_phi_abs(self, abs_value):
        try:
            self._send_safe_write('main', 100, 1280)
            self._send_write_float('main', 105, 106, float(abs_value))
            self._send_safe_write('main', 100, 2304)
        except Exception as e:
            self.set_error("command_phi_abs exception")

    def command_phi_rel(self, rel_value):
        try:
            self._send_safe_write('main', 100, 1280)
            self._send_write_float('main', 103, 104, float(rel_value))
            self._send_safe_write('main', 100, 4352)
        except Exception as e:
            self.set_error("command_phi_rel exception")

    def command_phi_speed(self, speed):
        try:
            self._send_safe_write('main', 100, 1280)
            self._send_write_float('main', 107, 108, float(speed))
        except Exception as e:
            self.set_error("command_phi_speed exception")

    def command_phi_home(self):
        try:
            self._send_safe_write('main', 100, 1280)
            self._send_safe_write('main', 101, 3)
            self._send_safe_write('main', 100, 768)
        except Exception as e:
            self.set_error("command_phi_home exception")

    def command_phi_rotate(self):
        try:
            self._send_safe_write('main', 100, 1280)
            self._send_safe_write('main', 100, 16640)
        except Exception as e:
            self.set_error("command_phi_rotate exception")

    def command_phi_stop(self):
        try:
            self._send_safe_write('main', 100, 1280)
        except Exception as e:
            self.set_error("command_phi_stop exception")

    ### TETTA

    def command_tetta_stop(self):
        try:
            self._send_safe_write('main', 0, 1280)
        except Exception as e:
            self.set_error("command_tetta_stop exception")

    def command_tetta_speed(self, speed):
        try:
            self._send_safe_write('main', 0, 1280)
            self._send_write_float('main', 7, 8, float(speed))
        except Exception as e:
            self.set_error("command_tetta_speed exception")

    def command_tetta_rel(self, rel_value):
        try:
            self._send_safe_write('main', 0, 1280)
            self._send_write_float('main', 3, 4, float(rel_value))
            self._send_safe_write('main', 0, 4352)
        except Exception as e:
            self.set_error("command_tetta_rel exception")

    def command_tetta_home(self):
        try:
            self._send_safe_write('main', 0, 1280)
            self._send_safe_write('main', 1, 3)
            self._send_safe_write('main', 0, 768)
        except Exception as e:
            self.set_error("command_tetta_home exception")

    def command_tetta_abs(self, abs_target):
        try:
            self._send_safe_write('main', 0, 1280)
            self._send_write_float('main', 5, 6, float(abs_target))
            self._send_safe_write('main', 0, 2304)
        except Exception as e:
            self.set_error("command_tetta_abs exception")

    ### OMEGA

    def command_omega_abs(self, abs_target):
        try:
            self._send_safe_write('main', 35, 1280)
            self._send_write_float('main', 40, 41, float(abs_target))
            self._send_safe_write('main', 35, 2304)
        except Exception as e:
            self.set_error("command_omega_abs exception")

    def command_omega_home(self):
        try:
            self._send_safe_write('main', 35, 1280)
            self._send_safe_write('main', 36, 3)
            self._send_safe_write('main', 35, 768)
        except Exception as e:
            self.set_error("command_omega_home exception")

    def command_omega_speed(self, speed):
        try:
            self._send_safe_write('main', 35, 1280)
            self._send_write_float('main', 42, 43, float(speed))
        except Exception as e:
            self.set_error("command_omega_speed exception")

    def command_omega_rel(self, rel):
        try:
            self._send_safe_write('main', 35, 1280)
            self._send_write_float('main', 38, 39, float(rel))
            self._send_safe_write('main', 35, 4352)
        except Exception as e:
            self.set_error("command_omega_rel exception")

    def command_omega_stop(self):
        try:
            self._send_safe_write('main', 35, 1280)
        except Exception as e:
            self.set_error("command_omega_stop exception")

    # KAPPA

    def command_kappa_speed(self, speed):
        try:
            self._send_safe_write('main', 70, 1280)
            self._send_write_float('main', 76, 77, float(speed))
        except Exception as e:
            self.set_error("command_kappa_speed exception")

    def command_kappa_home(self):
        try:
            self._send_safe_write('main', 70, 1280)
            self._send_safe_write('main', 71, 3)
            self._send_safe_write('main', 70, 768)
        except Exception as e:
            self.set_error("command_kappa_home exception")

    def command_kappa_rel(self, rel_target):
        try:
            self._send_safe_write('main', 70, 1280)
            self._send_write_float('main', 72, 73, float(rel_target))
            self._send_safe_write('main', 70, 4352)
        except Exception as e:
            self.set_error("command_kappa_rel exception")

    def command_kappa_abs(self, abs_target):
        try:
            self._send_safe_write('main', 70, 1280)
            self._send_write_float('main', 74, 75, float(abs_target))
            self._send_safe_write('main', 70, 2304)
        except Exception as e:
            self.set_error("command_kappa_abs exception")

    def command_kappa_stop(self):
        try:
            self._send_safe_write('main', 70, 1280)
        except Exception as e:
            self.set_error("command_kappa_stop exception")

    ### DETECTOR

    def command_detector_stop(self):
        try:
            self._send_safe_write('detector', 0, 1280)
        except Exception as e:
            self.set_error("command_detector_stop exception")

    def command_detector_speed(self, speed):
        try:
            self._send_safe_write('detector', 0, 1280)
            self._send_write_float('detector', 7, 8, float(speed))
        except Exception as e:
            self.set_error("command_detector_speed exception")

    def command_detector_rel(self, rel_target):
        try:
            self._send_safe_write('detector', 0, 1280)
            self._send_write_float('detector', 3, 4, float(rel_target))
            self._send_safe_write('detector', 0, 4352)
        except Exception as e:
            self.set_error("command_detector_rel exception")

    def command_detector_home(self):
        try:
            self._send_safe_write('detector', 0, 1280)
            self._send_safe_write('detector', 1, 3)
            self._send_safe_write('detector', 0, 768)
        except Exception as e:
            self.set_error("command_detector_home exception")

    def command_detector_abs(self, abs_target):
        try:
            self._send_safe_write('detector', 0, 1280)
            self._send_write_float('detector', 5, 6, float(abs_target))
            self._send_safe_write('detector', 0, 2304)
        except Exception as e:
            self.set_error("command_detector_abs exception")

