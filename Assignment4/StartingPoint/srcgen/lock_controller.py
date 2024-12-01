"""Implementation of statechart lock_controller.
Generated by itemis CREATE code generator.
"""

import queue
import sys, os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../lib')))
from yakindu.rx import Observable

class LockController:
	"""Implementation of the state machine LockController.
	"""

	class State:
		""" State Enum
		"""
		(
			main_region_idk,
			main_region_idk_r1b,
			main_region_idk_r1a,
			main_region_idk_r1d,
			main_region_idk_r1e,
			main_region_idk_r1c,
			main_region_idk_r2low_water_level,
			main_region_idk_r2idk_initial,
			main_region_emergency_mode,
			main_region_request_in_sensor_break,
			null_state
		) = range(11)
	
	
	def __init__(self):
		""" Declares all necessary variables including list of states, histories etc. 
		"""
		
		self.LOW = 0
		self.HIGH = 1
		self.LOW_LVL = 500
		self.HIGH_LVL = 1500
		self.request_lvl_change = None
		self.water_lvl = None
		self.water_lvl_value = None
		self.resume = None
		self.door_obstructed = None
		self.set_request_pending = None
		self.set_request_pending_value = None
		self.set_request_pending_observable = Observable()
		self.set_sensor_broken = None
		self.set_sensor_broken_observable = Observable()
		self.open_flow = None
		self.open_flow_value = None
		self.open_flow_observable = Observable()
		self.close_flow = None
		self.close_flow_value = None
		self.close_flow_observable = Observable()
		self.open_doors = None
		self.open_doors_value = None
		self.open_doors_observable = Observable()
		self.close_doors = None
		self.close_doors_value = None
		self.close_doors_observable = Observable()
		self.green_light = None
		self.green_light_value = None
		self.green_light_observable = Observable()
		self.red_light = None
		self.red_light_value = None
		self.red_light_observable = Observable()
		
		self.__internal_event_queue = queue.Queue()
		self.in_event_queue = queue.Queue()
		self.__previous_water_lvl = None
		self.__working_side = None
		self.__opposite_side = None
		self.__temp = None
		self.water_lvl_reached = None
		
		# enumeration of all states:
		self.__State = LockController.State
		self.__state_conf_vector_changed = None
		self.__state_vector = [None] * 2
		for __state_index in range(2):
			self.__state_vector[__state_index] = self.State.null_state
		
		# for timed statechart:
		self.timer_service = None
		self.__time_events = [None] * 2
		
		# history vector:
		self.__history_vector = [None] * 2
		for __history_index in range(2):
			self.__history_vector[__history_index] = self.State.null_state
		
		# initializations:
		#Default init sequence for statechart LockController
		self.__previous_water_lvl = self.LOW_LVL
		self.__working_side = self.LOW
		self.__opposite_side = self.HIGH
		self.__temp = 0
		self.__is_executing = False
		self.__state_conf_vector_position = None
	
	def is_active(self):
		"""Checks if the state machine is active.
		"""
		return self.__state_vector[0] is not self.__State.null_state or self.__state_vector[1] is not self.__State.null_state
	
	def is_final(self):
		"""Checks if the statemachine is final.
		Always returns 'false' since this state machine can never become final.
		"""
		return False
			
	def is_state_active(self, state):
		"""Checks if the state is currently active.
		"""
		s = state
		if s == self.__State.main_region_idk:
			return (self.__state_vector[0] >= self.__State.main_region_idk)\
				and (self.__state_vector[0] <= self.__State.main_region_idk_r2idk_initial)
		if s == self.__State.main_region_idk_r1b:
			return self.__state_vector[0] == self.__State.main_region_idk_r1b
		if s == self.__State.main_region_idk_r1a:
			return self.__state_vector[0] == self.__State.main_region_idk_r1a
		if s == self.__State.main_region_idk_r1d:
			return self.__state_vector[0] == self.__State.main_region_idk_r1d
		if s == self.__State.main_region_idk_r1e:
			return self.__state_vector[0] == self.__State.main_region_idk_r1e
		if s == self.__State.main_region_idk_r1c:
			return self.__state_vector[0] == self.__State.main_region_idk_r1c
		if s == self.__State.main_region_idk_r2low_water_level:
			return self.__state_vector[1] == self.__State.main_region_idk_r2low_water_level
		if s == self.__State.main_region_idk_r2idk_initial:
			return self.__state_vector[1] == self.__State.main_region_idk_r2idk_initial
		if s == self.__State.main_region_emergency_mode:
			return self.__state_vector[0] == self.__State.main_region_emergency_mode
		if s == self.__State.main_region_request_in_sensor_break:
			return self.__state_vector[0] == self.__State.main_region_request_in_sensor_break
		return False
		
	def time_elapsed(self, event_id):
		"""Add time events to in event queue
		"""
		if event_id in range(2):
			self.in_event_queue.put(lambda: self.raise_time_event(event_id))
			self.run_cycle()
	
	def raise_time_event(self, event_id):
		"""Raise timed events using the event_id.
		"""
		self.__time_events[event_id] = True
	
	def __execute_queued_event(self, func):
		func()
	
	def __get_next_event(self):
		if not self.__internal_event_queue.empty():
			return self.__internal_event_queue.get()
		if not self.in_event_queue.empty():
			return self.in_event_queue.get()
		return None
	
	
	def raise_water_lvl_reached(self):
		"""Raise method for event water_lvl_reached.
		"""
		self.__internal_event_queue.put(self.__raise_water_lvl_reached_call)
	
	def __raise_water_lvl_reached_call(self):
		"""Raise callback for event water_lvl_reached.
		"""
		self.water_lvl_reached = True
	
	def raise_request_lvl_change(self):
		"""Raise method for event request_lvl_change.
		"""
		self.in_event_queue.put(self.__raise_request_lvl_change_call)
		self.run_cycle()
	
	def __raise_request_lvl_change_call(self):
		"""Raise callback for event request_lvl_change.
		"""
		self.request_lvl_change = True
	
	def raise_water_lvl(self, value):
		"""Raise method for event water_lvl.
		"""
		self.in_event_queue.put(lambda: self.__raise_water_lvl_call(value))
		self.run_cycle()
	
	def __raise_water_lvl_call(self, value):
		"""Raise callback for event water_lvl.
		"""
		self.water_lvl = True
		self.water_lvl_value = value
	
	def raise_resume(self):
		"""Raise method for event resume.
		"""
		self.in_event_queue.put(self.__raise_resume_call)
		self.run_cycle()
	
	def __raise_resume_call(self):
		"""Raise callback for event resume.
		"""
		self.resume = True
	
	def raise_door_obstructed(self):
		"""Raise method for event door_obstructed.
		"""
		self.in_event_queue.put(self.__raise_door_obstructed_call)
		self.run_cycle()
	
	def __raise_door_obstructed_call(self):
		"""Raise callback for event door_obstructed.
		"""
		self.door_obstructed = True
	
	def __entry_action_main_region_idk_r1_b(self):
		"""Entry action for state 'B'..
		"""
		#Entry action for state 'B'.
		self.timer_service.set_timer(self, 0, (2 * 1000), False)
		
	def __entry_action_main_region_idk_r1_a(self):
		"""Entry action for state 'A'..
		"""
		#Entry action for state 'A'.
		self.open_doors_observable.next(self.__working_side)
		self.green_light_observable.next(self.__working_side)
		
	def __entry_action_main_region_idk_r1_d(self):
		"""Entry action for state 'D'..
		"""
		#Entry action for state 'D'.
		self.timer_service.set_timer(self, 1, (1 * 1000), False)
		
	def __entry_action_main_region_idk_r1_e(self):
		"""Entry action for state 'E'..
		"""
		#Entry action for state 'E'.
		self.close_flow_observable.next(self.__working_side)
		self.set_request_pending_observable.next(False)
		self.open_doors_observable.next(self.__working_side)
		self.green_light_observable.next(self.__working_side)
		
	def __entry_action_main_region_idk_r1_c(self):
		"""Entry action for state 'C'..
		"""
		#Entry action for state 'C'.
		self.close_doors_observable.next(self.__working_side)
		self.open_flow_observable.next(self.__opposite_side)
		
	def __entry_action_main_region_idk_r2_low_water_level(self):
		"""Entry action for state 'Low water level'..
		"""
		#Entry action for state 'Low water level'.
		self.__previous_water_lvl = self.water_lvl_value
		
	def __entry_action_main_region_emergency_mode(self):
		"""Entry action for state 'EmergencyMode'..
		"""
		#Entry action for state 'EmergencyMode'.
		self.red_light_observable.next(self.HIGH)
		self.red_light_observable.next(self.LOW)
		self.close_doors_observable.next(self.HIGH)
		self.close_doors_observable.next(self.LOW)
		self.close_flow_observable.next(self.HIGH)
		self.close_flow_observable.next(self.LOW)
		self.set_sensor_broken_observable.next()
		
	def __exit_action_main_region_idk_r1_b(self):
		"""Exit action for state 'B'..
		"""
		#Exit action for state 'B'.
		self.timer_service.unset_timer(self, 0)
		
	def __exit_action_main_region_idk_r1_d(self):
		"""Exit action for state 'D'..
		"""
		#Exit action for state 'D'.
		self.timer_service.unset_timer(self, 1)
		
	def __enter_sequence_main_region_idk_default(self):
		"""'default' enter sequence for state idk.
		"""
		#'default' enter sequence for state idk
		self.__enter_sequence_main_region_idk_r1_default()
		self.__enter_sequence_main_region_idk_r2_default()
		
	def __enter_sequence_main_region_idk_r1_b_default(self):
		"""'default' enter sequence for state B.
		"""
		#'default' enter sequence for state B
		self.__entry_action_main_region_idk_r1_b()
		self.__state_vector[0] = self.State.main_region_idk_r1b
		self.__state_conf_vector_position = 0
		self.__state_conf_vector_changed = True
		self.__history_vector[0] = self.__state_vector[0]
		
	def __enter_sequence_main_region_idk_r1_a_default(self):
		"""'default' enter sequence for state A.
		"""
		#'default' enter sequence for state A
		self.__entry_action_main_region_idk_r1_a()
		self.__state_vector[0] = self.State.main_region_idk_r1a
		self.__state_conf_vector_position = 0
		self.__state_conf_vector_changed = True
		self.__history_vector[0] = self.__state_vector[0]
		
	def __enter_sequence_main_region_idk_r1_d_default(self):
		"""'default' enter sequence for state D.
		"""
		#'default' enter sequence for state D
		self.__entry_action_main_region_idk_r1_d()
		self.__state_vector[0] = self.State.main_region_idk_r1d
		self.__state_conf_vector_position = 0
		self.__state_conf_vector_changed = True
		self.__history_vector[0] = self.__state_vector[0]
		
	def __enter_sequence_main_region_idk_r1_e_default(self):
		"""'default' enter sequence for state E.
		"""
		#'default' enter sequence for state E
		self.__entry_action_main_region_idk_r1_e()
		self.__state_vector[0] = self.State.main_region_idk_r1e
		self.__state_conf_vector_position = 0
		self.__state_conf_vector_changed = True
		self.__history_vector[0] = self.__state_vector[0]
		
	def __enter_sequence_main_region_idk_r1_c_default(self):
		"""'default' enter sequence for state C.
		"""
		#'default' enter sequence for state C
		self.__entry_action_main_region_idk_r1_c()
		self.__state_vector[0] = self.State.main_region_idk_r1c
		self.__state_conf_vector_position = 0
		self.__state_conf_vector_changed = True
		self.__history_vector[0] = self.__state_vector[0]
		
	def __enter_sequence_main_region_idk_r2_low_water_level_default(self):
		"""'default' enter sequence for state Low water level.
		"""
		#'default' enter sequence for state Low water level
		self.__entry_action_main_region_idk_r2_low_water_level()
		self.__state_vector[1] = self.State.main_region_idk_r2low_water_level
		self.__state_conf_vector_position = 1
		self.__state_conf_vector_changed = True
		self.__history_vector[1] = self.__state_vector[1]
		
	def __enter_sequence_main_region_idk_r2_idk_initial_default(self):
		"""'default' enter sequence for state idk initial.
		"""
		#'default' enter sequence for state idk initial
		self.__state_vector[1] = self.State.main_region_idk_r2idk_initial
		self.__state_conf_vector_position = 1
		self.__state_conf_vector_changed = True
		self.__history_vector[1] = self.__state_vector[1]
		
	def __enter_sequence_main_region_emergency_mode_default(self):
		"""'default' enter sequence for state EmergencyMode.
		"""
		#'default' enter sequence for state EmergencyMode
		self.__entry_action_main_region_emergency_mode()
		self.__state_vector[0] = self.State.main_region_emergency_mode
		self.__state_conf_vector_position = 0
		self.__state_conf_vector_changed = True
		
	def __enter_sequence_main_region_request_in_sensor_break_default(self):
		"""'default' enter sequence for state request in sensor break.
		"""
		#'default' enter sequence for state request in sensor break
		self.__state_vector[0] = self.State.main_region_request_in_sensor_break
		self.__state_conf_vector_position = 0
		self.__state_conf_vector_changed = True
		
	def __enter_sequence_main_region_default(self):
		"""'default' enter sequence for region main region.
		"""
		#'default' enter sequence for region main region
		self.__react_main_region__entry_default()
		
	def __enter_sequence_main_region_idk_r1_default(self):
		"""'default' enter sequence for region r1.
		"""
		#'default' enter sequence for region r1
		self.__react_main_region_idk_r1__entry_default()
		
	def __shallow_enter_sequence_main_region_idk_r1(self):
		"""shallow enterSequence with history in child r1.
		"""
		#shallow enterSequence with history in child r1
		state = self.__history_vector[0]
		if state == self.State.main_region_idk_r1b:
			self.__enter_sequence_main_region_idk_r1_b_default()
		elif state == self.State.main_region_idk_r1a:
			self.__enter_sequence_main_region_idk_r1_a_default()
		elif state == self.State.main_region_idk_r1d:
			self.__enter_sequence_main_region_idk_r1_d_default()
		elif state == self.State.main_region_idk_r1e:
			self.__enter_sequence_main_region_idk_r1_e_default()
		elif state == self.State.main_region_idk_r1c:
			self.__enter_sequence_main_region_idk_r1_c_default()
		
	def __enter_sequence_main_region_idk_r2_default(self):
		"""'default' enter sequence for region r2.
		"""
		#'default' enter sequence for region r2
		self.__react_main_region_idk_r2__entry_default()
		
	def __shallow_enter_sequence_main_region_idk_r2(self):
		"""shallow enterSequence with history in child r2.
		"""
		#shallow enterSequence with history in child r2
		state = self.__history_vector[1]
		if state == self.State.main_region_idk_r2low_water_level:
			self.__enter_sequence_main_region_idk_r2_low_water_level_default()
		elif state == self.State.main_region_idk_r2idk_initial:
			self.__enter_sequence_main_region_idk_r2_idk_initial_default()
		
	def __exit_sequence_main_region_idk(self):
		"""Default exit sequence for state idk.
		"""
		#Default exit sequence for state idk
		self.__exit_sequence_main_region_idk_r1()
		self.__exit_sequence_main_region_idk_r2()
		self.__state_vector[0] = self.State.null_state
		self.__state_vector[1] = self.State.null_state
		self.__state_conf_vector_position = 1
		
	def __exit_sequence_main_region_idk_r1_b(self):
		"""Default exit sequence for state B.
		"""
		#Default exit sequence for state B
		self.__state_vector[0] = self.State.main_region_idk
		self.__state_conf_vector_position = 0
		self.__exit_action_main_region_idk_r1_b()
		
	def __exit_sequence_main_region_idk_r1_a(self):
		"""Default exit sequence for state A.
		"""
		#Default exit sequence for state A
		self.__state_vector[0] = self.State.main_region_idk
		self.__state_conf_vector_position = 0
		
	def __exit_sequence_main_region_idk_r1_d(self):
		"""Default exit sequence for state D.
		"""
		#Default exit sequence for state D
		self.__state_vector[0] = self.State.main_region_idk
		self.__state_conf_vector_position = 0
		self.__exit_action_main_region_idk_r1_d()
		
	def __exit_sequence_main_region_idk_r1_e(self):
		"""Default exit sequence for state E.
		"""
		#Default exit sequence for state E
		self.__state_vector[0] = self.State.main_region_idk
		self.__state_conf_vector_position = 0
		
	def __exit_sequence_main_region_idk_r1_c(self):
		"""Default exit sequence for state C.
		"""
		#Default exit sequence for state C
		self.__state_vector[0] = self.State.main_region_idk
		self.__state_conf_vector_position = 0
		
	def __exit_sequence_main_region_idk_r2_low_water_level(self):
		"""Default exit sequence for state Low water level.
		"""
		#Default exit sequence for state Low water level
		self.__state_vector[1] = self.State.main_region_idk
		self.__state_conf_vector_position = 1
		
	def __exit_sequence_main_region_idk_r2_idk_initial(self):
		"""Default exit sequence for state idk initial.
		"""
		#Default exit sequence for state idk initial
		self.__state_vector[1] = self.State.main_region_idk
		self.__state_conf_vector_position = 1
		
	def __exit_sequence_main_region_emergency_mode(self):
		"""Default exit sequence for state EmergencyMode.
		"""
		#Default exit sequence for state EmergencyMode
		self.__state_vector[0] = self.State.null_state
		self.__state_conf_vector_position = 0
		
	def __exit_sequence_main_region_request_in_sensor_break(self):
		"""Default exit sequence for state request in sensor break.
		"""
		#Default exit sequence for state request in sensor break
		self.__state_vector[0] = self.State.null_state
		self.__state_conf_vector_position = 0
		
	def __exit_sequence_main_region(self):
		"""Default exit sequence for region main region.
		"""
		#Default exit sequence for region main region
		state = self.__state_vector[0]
		if state == self.State.main_region_idk_r1b:
			self.__exit_sequence_main_region_idk_r1_b()
		elif state == self.State.main_region_idk_r1a:
			self.__exit_sequence_main_region_idk_r1_a()
		elif state == self.State.main_region_idk_r1d:
			self.__exit_sequence_main_region_idk_r1_d()
		elif state == self.State.main_region_idk_r1e:
			self.__exit_sequence_main_region_idk_r1_e()
		elif state == self.State.main_region_idk_r1c:
			self.__exit_sequence_main_region_idk_r1_c()
		elif state == self.State.main_region_emergency_mode:
			self.__exit_sequence_main_region_emergency_mode()
		elif state == self.State.main_region_request_in_sensor_break:
			self.__exit_sequence_main_region_request_in_sensor_break()
		state = self.__state_vector[1]
		if state == self.State.main_region_idk_r2low_water_level:
			self.__exit_sequence_main_region_idk_r2_low_water_level()
		elif state == self.State.main_region_idk_r2idk_initial:
			self.__exit_sequence_main_region_idk_r2_idk_initial()
		
	def __exit_sequence_main_region_idk_r1(self):
		"""Default exit sequence for region r1.
		"""
		#Default exit sequence for region r1
		state = self.__state_vector[0]
		if state == self.State.main_region_idk_r1b:
			self.__exit_sequence_main_region_idk_r1_b()
		elif state == self.State.main_region_idk_r1a:
			self.__exit_sequence_main_region_idk_r1_a()
		elif state == self.State.main_region_idk_r1d:
			self.__exit_sequence_main_region_idk_r1_d()
		elif state == self.State.main_region_idk_r1e:
			self.__exit_sequence_main_region_idk_r1_e()
		elif state == self.State.main_region_idk_r1c:
			self.__exit_sequence_main_region_idk_r1_c()
		
	def __exit_sequence_main_region_idk_r2(self):
		"""Default exit sequence for region r2.
		"""
		#Default exit sequence for region r2
		state = self.__state_vector[1]
		if state == self.State.main_region_idk_r2low_water_level:
			self.__exit_sequence_main_region_idk_r2_low_water_level()
		elif state == self.State.main_region_idk_r2idk_initial:
			self.__exit_sequence_main_region_idk_r2_idk_initial()
		
	def __react_main_region_idk_r2__choice_0(self):
		"""The reactions of state null..
		"""
		#The reactions of state null.
		if (((self.water_lvl_value - self.__previous_water_lvl)) if ((self.water_lvl_value - self.__previous_water_lvl)) >= 0 else -(((self.water_lvl_value - self.__previous_water_lvl)))) > 1000:
			self.__exit_sequence_main_region_idk()
			self.__enter_sequence_main_region_emergency_mode_default()
		elif self.water_lvl_value > (self.HIGH_LVL - 30) if (self.__working_side == self.LOW) else self.water_lvl_value < (self.LOW_LVL + 30):
			self.raise_water_lvl_reached()
			self.__enter_sequence_main_region_idk_r2_low_water_level_default()
		else:
			self.__enter_sequence_main_region_idk_r2_low_water_level_default()
		
	def __react_main_region_idk_r1__entry_default(self):
		"""Default react sequence for shallow history entry .
		"""
		#Default react sequence for shallow history entry 
		#Enter the region with shallow history
		if self.__history_vector[0] is not self.State.null_state:
			self.__shallow_enter_sequence_main_region_idk_r1()
		else:
			self.__enter_sequence_main_region_idk_r1_a_default()
		
	def __react_main_region_idk_r2__entry_default(self):
		"""Default react sequence for shallow history entry .
		"""
		#Default react sequence for shallow history entry 
		#Enter the region with shallow history
		if self.__history_vector[1] is not self.State.null_state:
			self.__shallow_enter_sequence_main_region_idk_r2()
		else:
			self.__enter_sequence_main_region_idk_r2_idk_initial_default()
		
	def __react_main_region__entry_default(self):
		"""Default react sequence for initial entry .
		"""
		#Default react sequence for initial entry 
		self.__enter_sequence_main_region_idk_default()
		
	def __react(self, transitioned_before):
		"""Implementation of __react function.
		"""
		#State machine reactions.
		return transitioned_before
	
	
	def __main_region_idk_react(self, transitioned_before):
		"""Implementation of __main_region_idk_react function.
		"""
		#The reactions of state idk.
		return self.__react(transitioned_before)
	
	
	def __main_region_idk_r1_b_react(self, transitioned_before):
		"""Implementation of __main_region_idk_r1_b_react function.
		"""
		#The reactions of state B.
		transitioned_after = self.__main_region_idk_react(transitioned_before)
		if transitioned_after < 0:
			if self.__time_events[0]:
				self.__exit_sequence_main_region_idk_r1_b()
				self.__time_events[0] = False
				self.__enter_sequence_main_region_idk_r1_c_default()
				transitioned_after = 0
			elif self.door_obstructed:
				self.__exit_sequence_main_region_idk_r1_b()
				self.__enter_sequence_main_region_idk_r1_b_default()
				transitioned_after = 0
		return transitioned_after
	
	
	def __main_region_idk_r1_a_react(self, transitioned_before):
		"""Implementation of __main_region_idk_r1_a_react function.
		"""
		#The reactions of state A.
		transitioned_after = self.__main_region_idk_react(transitioned_before)
		if transitioned_after < 0:
			if self.request_lvl_change:
				self.__exit_sequence_main_region_idk_r1_a()
				self.red_light_observable.next(self.__working_side)
				self.set_request_pending_observable.next(True)
				self.__enter_sequence_main_region_idk_r1_b_default()
				transitioned_after = 0
		return transitioned_after
	
	
	def __main_region_idk_r1_d_react(self, transitioned_before):
		"""Implementation of __main_region_idk_r1_d_react function.
		"""
		#The reactions of state D.
		transitioned_after = self.__main_region_idk_react(transitioned_before)
		if transitioned_after < 0:
			if self.__time_events[1]:
				self.__exit_sequence_main_region_idk_r1_d()
				self.__temp = self.__working_side
				self.__working_side = self.__opposite_side
				self.__opposite_side = self.__temp
				self.__time_events[1] = False
				self.__enter_sequence_main_region_idk_r1_e_default()
				transitioned_after = 0
		return transitioned_after
	
	
	def __main_region_idk_r1_e_react(self, transitioned_before):
		"""Implementation of __main_region_idk_r1_e_react function.
		"""
		#The reactions of state E.
		transitioned_after = self.__main_region_idk_react(transitioned_before)
		if transitioned_after < 0:
			if self.request_lvl_change:
				self.__exit_sequence_main_region_idk_r1_e()
				self.red_light_observable.next(self.__working_side)
				self.set_request_pending_observable.next(True)
				self.__enter_sequence_main_region_idk_r1_b_default()
				transitioned_after = 0
		return transitioned_after
	
	
	def __main_region_idk_r1_c_react(self, transitioned_before):
		"""Implementation of __main_region_idk_r1_c_react function.
		"""
		#The reactions of state C.
		transitioned_after = self.__main_region_idk_react(transitioned_before)
		if transitioned_after < 0:
			if self.water_lvl_reached:
				self.__exit_sequence_main_region_idk_r1_c()
				self.__enter_sequence_main_region_idk_r1_d_default()
				transitioned_after = 0
		return transitioned_after
	
	
	def __main_region_idk_r2_low_water_level_react(self, transitioned_before):
		"""Implementation of __main_region_idk_r2_low_water_level_react function.
		"""
		#The reactions of state Low water level.
		transitioned_after = transitioned_before
		if transitioned_after < 1:
			if self.water_lvl:
				self.__exit_sequence_main_region_idk_r2_low_water_level()
				self.__react_main_region_idk_r2__choice_0()
				transitioned_after = 1
		return transitioned_after
	
	
	def __main_region_idk_r2_idk_initial_react(self, transitioned_before):
		"""Implementation of __main_region_idk_r2_idk_initial_react function.
		"""
		#The reactions of state idk initial.
		transitioned_after = transitioned_before
		if transitioned_after < 1:
			if self.water_lvl:
				self.__exit_sequence_main_region_idk_r2_idk_initial()
				self.__react_main_region_idk_r2__choice_0()
				transitioned_after = 1
		return transitioned_after
	
	
	def __main_region_emergency_mode_react(self, transitioned_before):
		"""Implementation of __main_region_emergency_mode_react function.
		"""
		#The reactions of state EmergencyMode.
		transitioned_after = self.__react(transitioned_before)
		if transitioned_after < 0:
			if self.resume:
				self.__exit_sequence_main_region_emergency_mode()
				self.__enter_sequence_main_region_idk_default()
				transitioned_after = 0
			elif self.request_lvl_change:
				self.__exit_sequence_main_region_emergency_mode()
				self.set_request_pending_observable.next(True)
				self.__enter_sequence_main_region_request_in_sensor_break_default()
				transitioned_after = 0
		return transitioned_after
	
	
	def __main_region_request_in_sensor_break_react(self, transitioned_before):
		"""Implementation of __main_region_request_in_sensor_break_react function.
		"""
		#The reactions of state request in sensor break.
		transitioned_after = self.__react(transitioned_before)
		if transitioned_after < 0:
			if self.resume:
				self.__exit_sequence_main_region_request_in_sensor_break()
				self.red_light_observable.next(self.__working_side)
				self.raise_request_lvl_change()
				self.__enter_sequence_main_region_idk_default()
				transitioned_after = 0
		return transitioned_after
	
	
	def __clear_in_events(self):
		"""Implementation of __clear_in_events function.
		"""
		self.request_lvl_change = False
		self.water_lvl = False
		self.resume = False
		self.door_obstructed = False
		self.__time_events[0] = False
		self.__time_events[1] = False
	
	
	def __clear_internal_events(self):
		"""Implementation of __clear_internal_events function.
		"""
		self.water_lvl_reached = False
	
	
	def __micro_step(self):
		"""Implementation of __micro_step function.
		"""
		transitioned = -1
		self.__state_conf_vector_position = 0
		state = self.__state_vector[0]
		if state == self.State.main_region_idk_r1b:
			transitioned = self.__main_region_idk_r1_b_react(transitioned)
		elif state == self.State.main_region_idk_r1a:
			transitioned = self.__main_region_idk_r1_a_react(transitioned)
		elif state == self.State.main_region_idk_r1d:
			transitioned = self.__main_region_idk_r1_d_react(transitioned)
		elif state == self.State.main_region_idk_r1e:
			transitioned = self.__main_region_idk_r1_e_react(transitioned)
		elif state == self.State.main_region_idk_r1c:
			transitioned = self.__main_region_idk_r1_c_react(transitioned)
		elif state == self.State.main_region_emergency_mode:
			transitioned = self.__main_region_emergency_mode_react(transitioned)
		elif state == self.State.main_region_request_in_sensor_break:
			transitioned = self.__main_region_request_in_sensor_break_react(transitioned)
		if self.__state_conf_vector_position < 1:
			state = self.__state_vector[1]
			if state == self.State.main_region_idk_r2low_water_level:
				self.__main_region_idk_r2_low_water_level_react(transitioned)
			elif state == self.State.main_region_idk_r2idk_initial:
				self.__main_region_idk_r2_idk_initial_react(transitioned)
	
	
	def run_cycle(self):
		"""Implementation of run_cycle function.
		"""
		#Performs a 'run to completion' step.
		if self.timer_service is None:
			raise ValueError('Timer service must be set.')
		
		if self.__is_executing:
			return
		self.__is_executing = True
		next_event = self.__get_next_event()
		if next_event is not None:
			self.__execute_queued_event(next_event)
		condition_0 = True
		while condition_0:
			self.__micro_step()
			self.__clear_in_events()
			self.__clear_internal_events()
			condition_0 = False
			next_event = self.__get_next_event()
			if next_event is not None:
				self.__execute_queued_event(next_event)
				condition_0 = True
		self.__is_executing = False
	
	
	def enter(self):
		"""Implementation of enter function.
		"""
		#Activates the state machine.
		if self.timer_service is None:
			raise ValueError('Timer service must be set.')
		
		if self.__is_executing:
			return
		self.__is_executing = True
		#Default enter sequence for statechart LockController
		self.__enter_sequence_main_region_default()
		self.__is_executing = False
	
	
	def exit(self):
		"""Implementation of exit function.
		"""
		#Deactivates the state machine.
		if self.__is_executing:
			return
		self.__is_executing = True
		#Default exit sequence for statechart LockController
		self.__exit_sequence_main_region()
		self.__state_vector[0] = self.State.null_state
		self.__state_vector[1] = self.State.null_state
		self.__state_conf_vector_position = 1
		self.__is_executing = False
	
	
	def trigger_without_event(self):
		"""Implementation of triggerWithoutEvent function.
		"""
		self.run_cycle()
	
