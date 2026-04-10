#v1
from random import randint
from typing import Any

import time

from sardana.pool.controller import CounterTimerController

from sardana import State

class SampleCounterController(CounterTimerController):

    # sample random values 1 - 10
    counter_value = 0

    current_state = State.On

    default_timer = 1

    def __init__(self, inst, props, *args, **kwargs):
        super(CounterTimerController, self).__init__(inst, props, *args, **kwargs)

        # some init action
        self.counter_value= randint(0, 10)

    def AddDevice(self, axis: int):
        pass

    def DeleteDevice(self, axis: int):
        pass

    # in Spock read: counter1.Value
    def ReadOne(self, axis: int) -> Any:
        self.counter_value=randint(0, 10)
        return self.counter_value

    def StateOne(self, axis: int):
        if self.current_state == State.On:
            return State.On, "Counter is stopped"
        elif self.current_state == State.Moving:
            return State.Moving, "Counter is acquiring"
        elif self.current_state == State.Fault:
            return State.Fault, "Counter has an error"

    def LoadOne(self, axis: int, value: float, repetitions: int, latency: float):
        # ?
        self.current_state= State.On


    def StartOne(self, axis: int, value: float):
        self.counter_value = randint(0, 10)
        self.current_state= State.Moving

        #test!
        time.sleep(value)

        self.current_state= State.On

    def StopOne(self, axis: int):
        self.current_state= State.On