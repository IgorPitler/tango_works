#v1
from random import randint
from typing import Any

from sardana.pool.controller import ZeroDController

from sardana import State

class SampleZeroDController(ZeroDController):

    # sample random values 1 - 10
    counter_value = 0

    def __init__(self, inst, props, *args, **kwargs):
        super(ZeroDController, self).__init__(inst, props, *args, **kwargs)

        # some init action
        self.counter_value= randint(0, 10)

    def AddDevice(self, axis: int):
        pass

    def DeleteDevice(self, axis: int):
        pass

    # in Spock read: zerod1.CurrentValue
    def ReadOne(self, axis: int) -> Any:
        self.counter_value=randint(0, 10)
        return self.counter_value

    def StateOne(self, axis: int):
        return State.On, "Counter is stopped"