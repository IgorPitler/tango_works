import PyTango
import tango

##### YOU DON'T NEED THIS SCRIPT NOW!!!!

device_name="lab1/table1/dev3"

print("Setting up attributes polling...")
# setting up polling
device_proxy = tango.DeviceProxy(device_name)

# reinitialize ?
#device_proxy.command_inout('Init')

device_proxy.poll_attribute("demo_attribute", 300)
device_proxy.poll_attribute("State", 300)
device_proxy.poll_attribute("Status", 300)

print("Ready.")