#v1
import tango
from tango.server import Device
from tango.server import attribute, command
from tango.server import device_property
from tango import  DevState

class log_consumer(Device):

    log_file_name = device_property(dtype=str)
    log_recording_is_active=True # by default

    def init_device(self):
        super().init_device()  # call first
        print("Starting log consumer device...")

    @command(dtype_in=tango.DevVarStringArray)
    def log(self, details):
        #details[0]: the timestamp in millisecond
        #details[1]: the log level
        #details[2]: the log source(i.e.device name)
        #details[3]: the log message
        #details[4]: the log NDC(contextual info) - Not used but reserved
        #details[5]: the thread identifier(i.e.the thread from which the
        # log request comes from)
        if self.log_recording_is_active:
            #do some recording
            #test output
            print("Log message:")
            print(details[2]) # source
            print(details[3]) # details

    @command()
    def start_recording(self):
        self.log_recording_is_active=True
        self.set_status("Status: log recording is ON")
        self.set_state(DevState.ON)
        print("Starting recording logs")

    @command()
    def stop_recording(self):
        self.log_recording_is_active=False
        self.set_status("Status: log recording is OFF")
        self.set_state(DevState.OFF)
        print("Stopping recording logs")

    def delete_device(self):
        print("Deleting logger device...")
        super().delete_device()  # call last

if __name__ == "__main__":
    log_consumer.run_server()