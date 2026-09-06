import socket

class DectrisCamserver:

    # seconds
    operation_timeout=200

    def __init__(self, camserver_ip="127.0.0.1", camserver_port : int = 8002):
        self.camserver_ip=camserver_ip
        self.camserver_port=camserver_port
        try:
            self.soc=socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            # operation timeout in seconds
            self.soc.settimeout(self.operation_timeout)
        except Exception as e:
            print(f"Error creating socket {e}")

    def connect(self):
        try:
            self.soc.connect((self.camserver_ip, self.camserver_port))
        except Exception as e:
            print(f"CAMserver connection error {e}")

    def send_command(self, command : str):
        try:
            command=command+"\n"
            self.soc.send(command.encode())
            # ? sendall

            # print server answer
            ans=self.soc.recv(1024).decode()
            print("Answer: "+ans)

        except Exception as e:
            print("Error sending command: "+command)

    # additional info in file headers, see param list
    def setMxSettings(self, data : str):
        self.send_command("MxSettings "+data)
        """
        Wavelength;
        Energy_range;
        Detector_distance;
        Detector_Voffset;
        Beam_xy;
        Beam_x;
        Beam_y;
        Flux;
        Filter_transmission;
        Start_angle;
        Angle_increment;
        Detector_2theta;
        Polarization;
        Alpha;
        Kappa;
        Phi;
        Phi_increment;
        Chi;
        Chi_increment;
        Omega;
        Omega_increment;
        Oscillation_axis;
        N_oscillations;
        Start_position;
        Position_increment;
        Shutter_time;
        CBF_template_file
        """

    def setNImages(self, n : int = 1):
        self.send_command("NImages "+str(n))

    # exposure time
    def setExpTime(self, t : float):
        self.send_command("ExpTime "+str(t))

    # period between exposures starts
    def setExpPeriod(self, t : float):
        self.send_command("ExpPeriod "+str(t))

    def set_imgpath(self, data : str):
        self.send_command("imgpath "+data)

    # prefer .CBF
    def start_Exposure(self, filename):
        self.send_command("Exposure "+filename)

    def socket_shutdown(self):
        try:
            self.soc.shutdown(socket.SHUT_RDWR)
        except Exception as e:
            print("Error shutdown socket")

    # use AFTER shutdown
    def close(self):
        try:
            self.soc.close()
        except Exception as e:
            print("Error closing socket")


#print("CAMserver ok")
#cam=DectrisCamserver()
#cam.connect()
#cam.send_command("test")
#cam.close()
