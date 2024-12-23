
### EDIT THIS FILE ###

from pypdevs.DEVS import AtomicDEVS
from environment import *
import random
import dataclasses

@dataclasses.dataclass
class QueueState:
    queues: dict
    remaining_time: float
    next_job: None
    def __init__(self, ship_sizes):
        self.queues = {}
        for size in ship_sizes:
            self.queues[size] = []
        self.remaining_time = float("inf")
        self.outgoing_ship = None

class Queue(AtomicDEVS):
    def __init__(self, ship_sizes):
        super().__init__("Queue")
        self.state = QueueState(ship_sizes)
        self.in_ship = self.addInPort("in_ship")
        self.in_get_ship = self.addInPort("in_get_ship")
        self.out_ship = self.addOutPort("out_ship")

    def extTransition(self, inputs):
        #TODO 2 events in input???
        if self.in_ship in inputs:
            self.state.queues[inputs[self.in_ship].size].insert(0, inputs[self.in_ship])
        if self.in_get_ship in inputs:
            priority = inputs[self.in_get_ship]
            if priority in self.state.queues and len(self.state.queues[priority]) > 0:
                self.state.outgoing_ship = self.state.queues[priority].pop()
                self.state.remaining_time = 0
            elif not priority in self.state.queues and self.state.queues[not priority]:
                self.state.outgoing_ship = self.state.queues[not priority].pop()
                self.state.remaining_time = 0
        return self.state
    
    def timeAdvance(self):
        return self.state.remaining_time
    
    def outputFnc(self):
        #output the next ship
        return {self.out_ship: self.state.outgoing_ship}
    
    def intTransition(self):
        #only called on out event
        self.state.remaining_time = float("inf")
        return self.state

@dataclasses.dataclass
class LoadBalancerState:
    remaining_time: float
    next_job: None
    def __init__(self, lock_capacities, priority):
        self.lock_capacities = lock_capacities
        self.lock_available_space = lock_capacities
        self.remaining_time = float("inf")
        self.next_ship = None
        self.priority = priority

PRIORITIZE_BIGGER_SHIPS = 0
PRIORITIZE_SMALLER_SHIPS = 1

class RoundRobinLoadBalancer(AtomicDEVS):
    def __init__(self,
        lock_capacities=[3,2], # two locks of capacities 3 and 2.
        priority=PRIORITIZE_BIGGER_SHIPS,
    ):
        super().__init__("RoundRobinLoadBalancer")
        self.state = LoadBalancerState(lock_capacities, priority)
        self.in_ship = self.addInPort("in_ship")
        self.in_lock_open = self.addInPort("in_lock_open")
        self.out_ship = self.addOutPort("out_ship")
        self.out_get_ship = self.addOutPort("out_get_ship")


    def extTransition(self, inputs):
        if self.in_ship in inputs and inputs[self.in_ship] is not None:
            self.state.next_ship = inputs[self.in_ship]
            self.state.remaining_time = 0 #move ship immediately to lock
        elif self.in_lock_open in inputs:
            self.state.remaining_time = 0
        else:
            self.state.remaining_time = float("inf")

        return self.state
    
    def timeAdvance(self):
        return self.state.remaining_time
    
    def outputFnc(self):
        return {self.out_ship: self.state.next_ship, self.out_get_ship: self.state.priority}
    
    def intTransition(self):
        self.state.remaining_time = float("inf")
        self.state.next_ship = None
        return self.state

class FillErUpLoadBalancer(AtomicDEVS):
    def __init__(self,
        lock_capacities=[3,2], # two locks of capacities 3 and 2.
        priority=PRIORITIZE_BIGGER_SHIPS,
    ):
        super().__init__("FillErUpLoadBalancer")
        # self.state = LoadBalancerState(...)

    # def extTransition(self, inputs):
    #     pass
    
    # def timeAdvance(self):
    #     pass
    
    # def outputFnc(self):
    #     pass
    
    # def intTransition(self):
    #     pass

@dataclasses.dataclass
class LockState:
    remaining_time: float
    ships: list
    available_capacity: int
    closed: bool
    def __init__(self, capacity, max_wait_duration, passthrough_duration):
        self.max_wait_duration = max_wait_duration
        self.remaining_time = self.max_wait_duration
        self.passthrough_duration = passthrough_duration
        self.ships = []
        self.available_capacity = capacity
        self.closed = False

class Lock(AtomicDEVS):
    def __init__(self,
        capacity=2, # lock capacity (2 means: 2 ships of size 1 will fit, or 1 ship of size 2)
        max_wait_duration=60.0, 
        passthrough_duration=60.0*15.0, # how long does it take for the lock to let a ship pass through it
    ):
        super().__init__("Lock")
        self.state = LockState(capacity, max_wait_duration, passthrough_duration)
        self.in_ship = self.addInPort("in_event")
        self.out_ships = self.addOutPort("out_event")
        self.out_lock_opened = self.addOutPort("out_lock_opened")


    def extTransition(self, inputs):
        if self.in_ship in inputs:
            if self.state.closed:
                pass
            elif len(self.state.ships) <= self.state.available_capacity:
                self.state.ships.append(inputs[self.in_ship])
            else:
                #lock is full, allow to pass through
                self.state.remaining_time = self.state.passthrough_duration
                self.state.closed = True
        return self.state
    
    def timeAdvance(self):
        return self.state.remaining_time
    
    def outputFnc(self):
        return {self.out_ships: self.state.ships, self.out_lock_opened: self.state.closed}
    
    def intTransition(self):
        if self.state.closed:
            #reopen lock and set empty
            self.state.closed = True
            self.state.remaining_time = self.state.max_wait_duration
            self.state.ships = []
        elif not self.state.closed:
            #close lock and wait to process
            self.state.remaining_time = self.state.passthrough_duration
            self.state.closed = True
        return self.state

### EDIT THIS FILE ###
