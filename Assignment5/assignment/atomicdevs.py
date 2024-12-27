from copy import deepcopy

### EDIT THIS FILE ###

from pypdevs.DEVS import AtomicDEVS
from environment import *
import random
import dataclasses

@dataclasses.dataclass
class QueueState:
    queues: dict
    remaining_time: float
    outgoing_ship: Ship|None
    def __init__(self, ship_sizes):
        self.queues = {}
        for size in ship_sizes:
            self.queues[size] = []
        self.remaining_time = float("inf")
        self.priority = None
        self.outgoing_ship = None

class Queue(AtomicDEVS):
    def __init__(self, ship_sizes):
        super().__init__("Queue")
        self.state = QueueState(ship_sizes)
        self.in_ship = self.addInPort("in_ship")
        self.in_get_ship = self.addInPort("in_get_ship")
        self.out_ship = self.addOutPort("out_ship")

    def extTransition(self, inputs):
        if self.in_ship in inputs:
            self.state.queues[inputs[self.in_ship].size].insert(0, inputs[self.in_ship])
            self.state.remaining_time = 0
        if self.in_get_ship in inputs:
            self.state.outgoing_ship = None #LoadBalancer asks for new ship and thus current ship is moved to lock
            self.state.priority = inputs[self.in_get_ship]
            self.state.remaining_time = 0

        priority = self.state.priority
        priority_size = 1
        priority_size_next = 2
        if priority == PRIORITIZE_BIGGER_SHIPS:
            priority_size = 2
            priority_size_next = 1

        if priority_size in self.state.queues and len(self.state.queues[priority_size]) > 0 and self.state.outgoing_ship is None:
            self.state.outgoing_ship = self.state.queues[priority_size].pop()
        elif priority_size_next in self.state.queues and self.state.queues[priority_size_next] and self.state.outgoing_ship is None:
            self.state.outgoing_ship = self.state.queues[priority_size_next].pop()

        return self.state
    
    def timeAdvance(self):
        return self.state.remaining_time
    
    def outputFnc(self):
        if self.state.outgoing_ship is not None:
            return {self.out_ship: self.state.outgoing_ship}
        return {}
    
    def intTransition(self):
        #only called on out event
        self.state.remaining_time = float("inf")
        return self.state

@dataclasses.dataclass
class LoadBalancerState:
    remaining_time: float
    lock_capacities: list
    lock_available_space: list
    next_ship: Ship|None
    priority: int
    lock_open_list: list
    current_serving_lock: 0
    def __init__(self, lock_capacities, priority):
        self.lock_capacities = lock_capacities
        self.lock_available_space = deepcopy(lock_capacities)
        self.remaining_time = float("inf")
        self.next_ship = None
        self.priority = priority
        self.lock_open_list = [True] * len(lock_capacities)
        self.current_serving_lock = 0

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
        self.out_get_ship = self.addOutPort("out_get_ship")  # ask for ship given a priority

        self.out_ship_list = []
        self.in_ship_ack_list = []
        self.in_lock_opened_list = []
        for i in range(len(lock_capacities)):
            self.out_ship_list.append(self.addOutPort(f"out_ship_{i}"))
            self.in_ship_ack_list.append(self.addInPort(f"in_ship_ack_{i}")) #ack the out_ship

            self.in_lock_opened_list.append(self.addInPort(f"in_lock_open_{i}"))

        self.state.remaining_time = 0


    def extTransition(self, inputs):
        for i in range(len(self.state.lock_capacities)):
            if self.in_ship_ack_list[i] in inputs and self.state.next_ship is not None: #ship was successfully moved to lock
                self.state.lock_available_space[i] -= self.state.next_ship.size
                assert self.state.lock_available_space[i] >= 0, f"Negative lock space {self.state.lock_available_space}"
                self.state.next_ship = None
                self.state.remaining_time = 0 #ask for new ship immediately
                return self.state

        if self.in_ship in inputs and inputs[self.in_ship] is not None: #when ships comes in and there is not currently another ship
            self.state.next_ship = inputs[self.in_ship]

        for i in range(len(self.state.lock_capacities)):
            if self.in_lock_opened_list[i] in inputs:
                if inputs[self.in_lock_opened_list[i]] == True and self.state.lock_open_list[i] == False:  # when state changes back to open reset available cap to original cap
                    self.state.lock_available_space[i] = self.state.lock_capacities[i]
                self.state.lock_open_list[i] = inputs[self.in_lock_opened_list[i]]

            if self.state.lock_open_list[i] and self.state.next_ship is not None: #when lock is open move ship through to lock
                self.state.remaining_time = 0
                break
            elif not self.state.lock_open_list[i]: #when lock is closed don't move any ships
                self.state.remaining_time = float("inf")

        return self.state
    
    def timeAdvance(self):
        return self.state.remaining_time
    
    def outputFnc(self):
        output = {}
        if self.state.next_ship is None:
            ship_priority = self.state.priority
            if ship_priority == PRIORITIZE_BIGGER_SHIPS and self.state.lock_available_space[self.state.current_serving_lock] == 1:
                ship_priority = 1 #get a small ship
            output[self.out_get_ship] = ship_priority #ask new ship because next_ship is empty
        elif self.state.next_ship is not None:
            output[self.out_ship_list[self.state.current_serving_lock]] = self.state.next_ship #pass ship to lock

        return output
    
    def intTransition(self):
        if self.state.next_ship is not None:
            self.state.current_serving_lock = (self.state.current_serving_lock + 1) % len(self.state.lock_capacities)

        self.state.remaining_time = float("inf")
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
    max_wait_duration: float
    ships: list
    available_capacity: int
    closed: bool
    ack_ship: bool
    total_ships_passed: int
    max_ships_passed_at_once: int
    current_time: int
    time_until_max_wait_duration: float
    closing: bool
    def __init__(self, capacity, max_wait_duration, passthrough_duration):
        self.max_wait_duration = max_wait_duration
        self.remaining_time = float('inf')
        self.passthrough_duration = passthrough_duration
        self.ships = []
        self.available_capacity = capacity
        self.closed = False
        self.ack_ship = False
        self.total_ships_passed = 0
        self.max_ships_passed_at_once = 0
        self.current_time = 0
        self.time_until_max_wait_duration = 0
        self.closing = False

class Lock(AtomicDEVS):
    def __init__(self,
        capacity=2, # lock capacity (2 means: 2 ships of size 1 will fit, or 1 ship of size 2)
        max_wait_duration=60.0, 
        passthrough_duration=60.0*15.0, # how long does it take for the lock to let a ship pass through it
    ):
        super().__init__("Lock")
        self.state = LockState(capacity, max_wait_duration, passthrough_duration)
        self.state.remaining_time = float('inf')
        self.in_ship = self.addInPort("in_ship")
        self.out_ship_ack = self.addOutPort("out_ship_ack")  # ack the in ship

        self.out_ships = self.addOutPort("out_ships")
        self.out_lock_opened = self.addOutPort("out_lock_opened")


    def extTransition(self, inputs):
        self.state.current_time += self.elapsed
        if self.in_ship in inputs:
            if inputs[self.in_ship] is None:
                pass
            elif self.state.closed:
                self.state.ack_ship = False
                pass
            elif sum(ship.size for ship in self.state.ships) + inputs[self.in_ship].size <= self.state.available_capacity:
                self.state.ack_ship = True
                self.state.remaining_time = 0 #sendout ship ack immediately
                self.state.ships.append(inputs[self.in_ship])
            else:
                #lock is full, allow to pass through
                self.state.ack_ship = False
                self.state.closed = True
                self.state.remaining_time = 0
        return self.state
    
    def timeAdvance(self):
        return self.state.remaining_time
    
    def outputFnc(self):
        if self.state.ack_ship:
            return {self.out_ship_ack: self.state.ack_ship, self.out_lock_opened: not self.state.closed}
        elif len(self.state.ships) > 0 and not self.state.closing:
            return {self.out_ships: self.state.ships, self.out_lock_opened: True} #when comes here boats leave and thus lock opens
        return {self.out_lock_opened: not self.state.closed}
    
    def intTransition(self):
        self.state.current_time += self.state.remaining_time
        max_waiting_exceeded = self.state.time_until_max_wait_duration <=  self.state.current_time and len(self.state.ships) > 0
        self.state.remaining_time = float("inf")
        if self.state.closed and not self.state.closing:
            #reopen lock and set empty
            self.state.closed = False
            self.state.remaining_time = self.state.max_wait_duration
            self.state.time_until_max_wait_duration = self.state.current_time + self.state.max_wait_duration
            if sum(ship.size for ship in self.state.ships) >= self.state.max_ships_passed_at_once:
                self.state.max_ships_passed_at_once = sum(ship.size for ship in self.state.ships)
            self.state.ships = []
            self.state.total_ships_passed += 1
        elif self.state.closing:
            #close lock and wait until processed
            self.state.remaining_time = self.state.passthrough_duration
            self.state.closed = True
            self.state.closing = False
        elif not self.state.closed and (sum(ship.size for ship in self.state.ships) >= self.state.available_capacity or max_waiting_exceeded):
            #Close lock by sending signal to RoundRobinLoadBalancer
            self.state.remaining_time = 0
            self.state.closing = True
            self.state.closed = True
        elif len(self.state.ships) == 0 and self.state.closed:
            self.state.remaining_time = 0
            self.state.closed = False
        elif len(self.state.ships) == 0 and not self.state.closed:
            self.state.remaining_time = float("inf")
        if self.state.ack_ship:
            self.state.remaining_time = self.state.max_wait_duration
            self.state.ack_ship = False

        return self.state

### EDIT THIS FILE ###
