#v1
import tango
from tango._tango import DbDevInfo

print("Creating Tango device...")

tangodb=tango.Database()

device_class_name="TangoDemodev1"
device_name="lab1/table1/dev3"
instance_name="instance1"

logging_level="DEBUG"
logging_target="device::lab1/table1/dev2"

new_device_info=DbDevInfo()
new_device_info._class=device_class_name
new_device_info.server=device_class_name+"/"+instance_name
new_device_info.name=device_name
tangodb.add_device(new_device_info)

# setting properties...
print("Setting up device properties...")
device_properties= {
    "demo_property": ["demo_property_value"],
    "logging_level": logging_level,
    "logging_target": logging_target
}
tangodb.put_device_property(device_name, device_properties)

# polling is setting up in main device class (see init_device()) !!!

#print("Finished. Now run your device, and after that run setup script to continue setup!")
print("Finished. Now run your device!")
