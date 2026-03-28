#import tango
#dev = tango.DeviceProxy("sys/tg_test/1")
# or using a network address format if not using the Tango database
# dev = tango.DeviceProxy("tango://hostname:port/sys/tg_test/1#dbase=no")

from sardana import State

from sardana.pool.controller import MotorController

class ArduinoMotorController(MotorController):

    motor_state = 1
    motor_position = 0

    def __init__(self, inst, props, *args, **kwargs):
        #super(SpringfieldMotorController, self).__init__(inst, props, *args, **kwargs)
        super().__init__()
        # initialize hardware communication
        #self.springfield = springfieldlib.SpringfieldMotorHW()
        # do some initialization
        #self._motors = {}
        self.motor_state = 1
        self.motor_position = 0

        self.AccelerationTime=0
        self.DecelerationTime=0
        self.MinVelocity=0
        self.MaxVelocity=1
        self.step_per_unit=1

    # TEST, use only 1 motor!

    def AddDevice(self, axis):
        # some action, no matter
        #self._motors[axis] = True
        # don't use axis number
        self.motor_state = 1
        self.motor_position = 0

    def DeleteDevice(self, axis):
        # some action, no matter
        #del self._motor[axis]
        # don't use axis number
        pass


    def ReadOne(self, axis):
        """Get the specified motor position"""
        #return self.springfield.getPosition(axis)
        # don't use axis number
        return self.motor_position

    def StateOne(self, axis):
        """Get the specified motor state"""
        #springfield = self.springfield
        #state = springfield.getState(axis)
        # don't use axis number
        if self.motor_state == 1:
            return State.On, "Motor is stopped"
        elif self.motor_state == 2:
            return State.Moving, "Motor is moving"
        elif self.motor_state == 3:
            return State.Fault, "Motor has an error"

    def StartOne(self, axis, position):
        """Move the specified motor to the specified position"""
        #self.springfield.move(axis, position)

        # don't use axis number
        #for test
        self.motor_state = 2
        self.motor_position = position
        self.motor_state = 1

    def StopOne(self, axis):
        """Stop the specified motor"""
        #self.springfield.stop(axis)
        # don't use axis number
        self.motor_state = 1

    def GetAxisPar(self, axis, name):
        # don't use axis number
        if name == "acceleration":
            v = self.AccelerationTime
        elif name == "deceleration":
            v = self.DecelerationTime
        elif name == "base_rate":
            v = self.MinVelocity
        elif name == "velocity":
            v = self.MaxVelocity
        elif name == "step_per_unit":
            v = self.step_per_unit
        return v

    def SetAxisPar(self, axis, name, value):
        # don't use axis number
        name = name.lower()
        if name == "acceleration":
            self.AccelerationTime=value
        elif name == "deceleration":
            self.DecelerationTime=value
        elif name == "base_rate":
            self.MinVelocity=value
        elif name == "velocity":
            self.MaxVelocity=value
        elif name == "step_per_unit":
            self.step_per_unit= value