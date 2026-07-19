#v1
import tango

print("Removing Tango device demodev1...")

device_class_name="TangoDemodev1"
instance_name="instance1"
device_name="lab1/table1/dev3"

tangodb=tango.Database()

tangodb.delete_device(device_name)
tangodb.delete_server(device_class_name+"/"+instance_name)

print("Device removed.")