#v1
from random import randint
from typing import Any

from sardana.pool.controller import CounterTimerController

from sardana import State

class SampleCounterController(CounterTimerController):

    # sample random values 1 - 10
    counter_value = 0

    def __init__(self, inst, props, *args, **kwargs):
        super(CounterTimerController, self).__init__(inst, props, *args, **kwargs)

        # some init action
        self.counter_value= randint(0, 10)

    def AddDevice(self, axis: int):
        pass

    def DeleteDevice(self, axis: int):
        pass

    def ReadOne(self, axis: int) -> Any:
        self.counter_value=randint(0, 10)
        return self.counter_value

    def StateOne(self, axis: int):
        return State.On, "Counter is stopped"

    def LoadOne(self, axis: int, value: float, repetitions: int, latency: float):
        pass

    def StartOne(self, axis: int, value: float):
        pass

    def StopOne(self, axis: int):
        pass