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
			main_region_o,
			main_region_or1a,
			main_region_or1b,
			main_region_or2c,
			main_region_or2d,
			main_region_or2e,
			main_region_or2f,
			main_region_or3g,
			main_region_or3h,
			null_state
		) = range(10)
	
	
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
		
		self.in_event_queue = queue.Queue()
		
		# enumeration of all states:
		self.__State = LockController.State
		self.__state_conf_vector_changed = None
		self.__state_vector = [None] * 3
		for __state_index in range(3):
			self.__state_vector[__state_index] = self.State.null_state
		
		# for timed statechart:
		self.timer_service = None
		self.__time_events = [None] * 8
		
		# initializations:
		self.__is_executing = False
		self.__state_conf_vector_position = None
	
	def is_active(self):
		"""Checks if the state machine is active.
		"""
		return self.__state_vector[0] is not self.__State.null_state or self.__state_vector[1] is not self.__State.null_state or self.__state_vector[2] is not self.__State.null_state
	
	def is_final(self):
		"""Checks if the statemachine is final.
		Always returns 'false' since this state machine can never become final.
		"""
		return False
			
	def is_state_active(self, state):
		"""Checks if the state is currently active.
		"""
		s = state
		if s == self.__State.main_region_o:
			return (self.__state_vector[0] >= self.__State.main_region_o)\
				and (self.__state_vector[0] <= self.__State.main_region_or3h)
		if s == self.__State.main_region_or1a:
			return self.__state_vector[0] == self.__State.main_region_or1a
		if s == self.__State.main_region_or1b:
			return self.__state_vector[0] == self.__State.main_region_or1b
		if s == self.__State.main_region_or2c:
			return self.__state_vector[1] == self.__State.main_region_or2c
		if s == self.__State.main_region_or2d:
			return self.__state_vector[1] == self.__State.main_region_or2d
		if s == self.__State.main_region_or2e:
			return self.__state_vector[1] == self.__State.main_region_or2e
		if s == self.__State.main_region_or2f:
			return self.__state_vector[1] == self.__State.main_region_or2f
		if s == self.__State.main_region_or3g:
			return self.__state_vector[2] == self.__State.main_region_or3g
		if s == self.__State.main_region_or3h:
			return self.__state_vector[2] == self.__State.main_region_or3h
		return False
		
	def time_elapsed(self, event_id):
		"""Add time events to in event queue
		"""
		if event_id in range(8):
			self.in_event_queue.put(lambda: self.raise_time_event(event_id))
			self.run_cycle()
	
	def raise_time_event(self, event_id):
		"""Raise timed events using the event_id.
		"""
		self.__time_events[event_id] = True
	
	def __execute_queued_event(self, func):
		func()
	
	def __get_next_event(self):
		if not self.in_event_queue.empty():
			return self.in_event_queue.get()
		return None
	
	
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
	
	def __entry_action_main_region_o_r1_a(self):
		"""Entry action for state 'A'..
		"""
		#Entry action for state 'A'.
		self.timer_service.set_timer(self, 0, (1 * 1000), False)
		self.open_flow_observable.next(self.HIGH)
		
	def __entry_action_main_region_o_r1_b(self):
		"""Entry action for state 'B'..
		"""
		#Entry action for state 'B'.
		self.timer_service.set_timer(self, 1, (1 * 1000), False)
		self.open_flow_observable.next(self.LOW)
		
	def __entry_action_main_region_o_r2_c(self):
		"""Entry action for state 'C'..
		"""
		#Entry action for state 'C'.
		self.timer_service.set_timer(self, 2, 500, False)
		self.green_light_observable.next(self.LOW)
		
	def __entry_action_main_region_o_r2_d(self):
		"""Entry action for state 'D'..
		"""
		#Entry action for state 'D'.
		self.timer_service.set_timer(self, 3, 500, False)
		self.green_light_observable.next(self.HIGH)
		
	def __entry_action_main_region_o_r2_e(self):
		"""Entry action for state 'E'..
		"""
		#Entry action for state 'E'.
		self.timer_service.set_timer(self, 4, 500, False)
		self.red_light_observable.next(self.LOW)
		
	def __entry_action_main_region_o_r2_f(self):
		"""Entry action for state 'F'..
		"""
		#Entry action for state 'F'.
		self.timer_service.set_timer(self, 5, 500, False)
		self.red_light_observable.next(self.HIGH)
		
	def __entry_action_main_region_o_r3_g(self):
		"""Entry action for state 'G'..
		"""
		#Entry action for state 'G'.
		self.timer_service.set_timer(self, 6, 250, False)
		
	def __entry_action_main_region_o_r3_h(self):
		"""Entry action for state 'H'..
		"""
		#Entry action for state 'H'.
		self.timer_service.set_timer(self, 7, 250, False)
		
	def __exit_action_main_region_o_r1_a(self):
		"""Exit action for state 'A'..
		"""
		#Exit action for state 'A'.
		self.timer_service.unset_timer(self, 0)
		self.close_flow_observable.next(self.HIGH)
		
	def __exit_action_main_region_o_r1_b(self):
		"""Exit action for state 'B'..
		"""
		#Exit action for state 'B'.
		self.timer_service.unset_timer(self, 1)
		self.close_flow_observable.next(self.LOW)
		
	def __exit_action_main_region_o_r2_c(self):
		"""Exit action for state 'C'..
		"""
		#Exit action for state 'C'.
		self.timer_service.unset_timer(self, 2)
		
	def __exit_action_main_region_o_r2_d(self):
		"""Exit action for state 'D'..
		"""
		#Exit action for state 'D'.
		self.timer_service.unset_timer(self, 3)
		
	def __exit_action_main_region_o_r2_e(self):
		"""Exit action for state 'E'..
		"""
		#Exit action for state 'E'.
		self.timer_service.unset_timer(self, 4)
		
	def __exit_action_main_region_o_r2_f(self):
		"""Exit action for state 'F'..
		"""
		#Exit action for state 'F'.
		self.timer_service.unset_timer(self, 5)
		
	def __exit_action_main_region_o_r3_g(self):
		"""Exit action for state 'G'..
		"""
		#Exit action for state 'G'.
		self.timer_service.unset_timer(self, 6)
		
	def __exit_action_main_region_o_r3_h(self):
		"""Exit action for state 'H'..
		"""
		#Exit action for state 'H'.
		self.timer_service.unset_timer(self, 7)
		
	def __enter_sequence_main_region_o_default(self):
		"""'default' enter sequence for state O.
		"""
		#'default' enter sequence for state O
		self.__enter_sequence_main_region_o_r1_default()
		self.__enter_sequence_main_region_o_r2_default()
		self.__enter_sequence_main_region_o_r3_default()
		
	def __enter_sequence_main_region_o_r1_a_default(self):
		"""'default' enter sequence for state A.
		"""
		#'default' enter sequence for state A
		self.__entry_action_main_region_o_r1_a()
		self.__state_vector[0] = self.State.main_region_or1a
		self.__state_conf_vector_position = 0
		self.__state_conf_vector_changed = True
		
	def __enter_sequence_main_region_o_r1_b_default(self):
		"""'default' enter sequence for state B.
		"""
		#'default' enter sequence for state B
		self.__entry_action_main_region_o_r1_b()
		self.__state_vector[0] = self.State.main_region_or1b
		self.__state_conf_vector_position = 0
		self.__state_conf_vector_changed = True
		
	def __enter_sequence_main_region_o_r2_c_default(self):
		"""'default' enter sequence for state C.
		"""
		#'default' enter sequence for state C
		self.__entry_action_main_region_o_r2_c()
		self.__state_vector[1] = self.State.main_region_or2c
		self.__state_conf_vector_position = 1
		self.__state_conf_vector_changed = True
		
	def __enter_sequence_main_region_o_r2_d_default(self):
		"""'default' enter sequence for state D.
		"""
		#'default' enter sequence for state D
		self.__entry_action_main_region_o_r2_d()
		self.__state_vector[1] = self.State.main_region_or2d
		self.__state_conf_vector_position = 1
		self.__state_conf_vector_changed = True
		
	def __enter_sequence_main_region_o_r2_e_default(self):
		"""'default' enter sequence for state E.
		"""
		#'default' enter sequence for state E
		self.__entry_action_main_region_o_r2_e()
		self.__state_vector[1] = self.State.main_region_or2e
		self.__state_conf_vector_position = 1
		self.__state_conf_vector_changed = True
		
	def __enter_sequence_main_region_o_r2_f_default(self):
		"""'default' enter sequence for state F.
		"""
		#'default' enter sequence for state F
		self.__entry_action_main_region_o_r2_f()
		self.__state_vector[1] = self.State.main_region_or2f
		self.__state_conf_vector_position = 1
		self.__state_conf_vector_changed = True
		
	def __enter_sequence_main_region_o_r3_g_default(self):
		"""'default' enter sequence for state G.
		"""
		#'default' enter sequence for state G
		self.__entry_action_main_region_o_r3_g()
		self.__state_vector[2] = self.State.main_region_or3g
		self.__state_conf_vector_position = 2
		self.__state_conf_vector_changed = True
		
	def __enter_sequence_main_region_o_r3_h_default(self):
		"""'default' enter sequence for state H.
		"""
		#'default' enter sequence for state H
		self.__entry_action_main_region_o_r3_h()
		self.__state_vector[2] = self.State.main_region_or3h
		self.__state_conf_vector_position = 2
		self.__state_conf_vector_changed = True
		
	def __enter_sequence_main_region_default(self):
		"""'default' enter sequence for region main region.
		"""
		#'default' enter sequence for region main region
		self.__react_main_region__entry_default()
		
	def __enter_sequence_main_region_o_r1_default(self):
		"""'default' enter sequence for region r1.
		"""
		#'default' enter sequence for region r1
		self.__react_main_region_o_r1__entry_default()
		
	def __enter_sequence_main_region_o_r2_default(self):
		"""'default' enter sequence for region r2.
		"""
		#'default' enter sequence for region r2
		self.__react_main_region_o_r2__entry_default()
		
	def __enter_sequence_main_region_o_r3_default(self):
		"""'default' enter sequence for region r3.
		"""
		#'default' enter sequence for region r3
		self.__react_main_region_o_r3__entry_default()
		
	def __exit_sequence_main_region_o_r1_a(self):
		"""Default exit sequence for state A.
		"""
		#Default exit sequence for state A
		self.__state_vector[0] = self.State.main_region_o
		self.__state_conf_vector_position = 0
		self.__exit_action_main_region_o_r1_a()
		
	def __exit_sequence_main_region_o_r1_b(self):
		"""Default exit sequence for state B.
		"""
		#Default exit sequence for state B
		self.__state_vector[0] = self.State.main_region_o
		self.__state_conf_vector_position = 0
		self.__exit_action_main_region_o_r1_b()
		
	def __exit_sequence_main_region_o_r2_c(self):
		"""Default exit sequence for state C.
		"""
		#Default exit sequence for state C
		self.__state_vector[1] = self.State.main_region_o
		self.__state_conf_vector_position = 1
		self.__exit_action_main_region_o_r2_c()
		
	def __exit_sequence_main_region_o_r2_d(self):
		"""Default exit sequence for state D.
		"""
		#Default exit sequence for state D
		self.__state_vector[1] = self.State.main_region_o
		self.__state_conf_vector_position = 1
		self.__exit_action_main_region_o_r2_d()
		
	def __exit_sequence_main_region_o_r2_e(self):
		"""Default exit sequence for state E.
		"""
		#Default exit sequence for state E
		self.__state_vector[1] = self.State.main_region_o
		self.__state_conf_vector_position = 1
		self.__exit_action_main_region_o_r2_e()
		
	def __exit_sequence_main_region_o_r2_f(self):
		"""Default exit sequence for state F.
		"""
		#Default exit sequence for state F
		self.__state_vector[1] = self.State.main_region_o
		self.__state_conf_vector_position = 1
		self.__exit_action_main_region_o_r2_f()
		
	def __exit_sequence_main_region_o_r3_g(self):
		"""Default exit sequence for state G.
		"""
		#Default exit sequence for state G
		self.__state_vector[2] = self.State.main_region_o
		self.__state_conf_vector_position = 2
		self.__exit_action_main_region_o_r3_g()
		
	def __exit_sequence_main_region_o_r3_h(self):
		"""Default exit sequence for state H.
		"""
		#Default exit sequence for state H
		self.__state_vector[2] = self.State.main_region_o
		self.__state_conf_vector_position = 2
		self.__exit_action_main_region_o_r3_h()
		
	def __exit_sequence_main_region(self):
		"""Default exit sequence for region main region.
		"""
		#Default exit sequence for region main region
		state = self.__state_vector[0]
		if state == self.State.main_region_or1a:
			self.__exit_sequence_main_region_o_r1_a()
		elif state == self.State.main_region_or1b:
			self.__exit_sequence_main_region_o_r1_b()
		state = self.__state_vector[1]
		if state == self.State.main_region_or2c:
			self.__exit_sequence_main_region_o_r2_c()
		elif state == self.State.main_region_or2d:
			self.__exit_sequence_main_region_o_r2_d()
		elif state == self.State.main_region_or2e:
			self.__exit_sequence_main_region_o_r2_e()
		elif state == self.State.main_region_or2f:
			self.__exit_sequence_main_region_o_r2_f()
		state = self.__state_vector[2]
		if state == self.State.main_region_or3g:
			self.__exit_sequence_main_region_o_r3_g()
		elif state == self.State.main_region_or3h:
			self.__exit_sequence_main_region_o_r3_h()
		
	def __react_main_region_o_r1__entry_default(self):
		"""Default react sequence for initial entry .
		"""
		#Default react sequence for initial entry 
		self.__enter_sequence_main_region_o_r1_a_default()
		
	def __react_main_region_o_r2__entry_default(self):
		"""Default react sequence for initial entry .
		"""
		#Default react sequence for initial entry 
		self.__enter_sequence_main_region_o_r2_c_default()
		
	def __react_main_region_o_r3__entry_default(self):
		"""Default react sequence for initial entry .
		"""
		#Default react sequence for initial entry 
		self.__enter_sequence_main_region_o_r3_g_default()
		
	def __react_main_region__entry_default(self):
		"""Default react sequence for initial entry .
		"""
		#Default react sequence for initial entry 
		self.__enter_sequence_main_region_o_default()
		
	def __react(self, transitioned_before):
		"""Implementation of __react function.
		"""
		#State machine reactions.
		return transitioned_before
	
	
	def __main_region_o_react(self, transitioned_before):
		"""Implementation of __main_region_o_react function.
		"""
		#The reactions of state O.
		return self.__react(transitioned_before)
	
	
	def __main_region_o_r1_a_react(self, transitioned_before):
		"""Implementation of __main_region_o_r1_a_react function.
		"""
		#The reactions of state A.
		transitioned_after = self.__main_region_o_react(transitioned_before)
		if transitioned_after < 0:
			if self.__time_events[0]:
				self.__exit_sequence_main_region_o_r1_a()
				self.__time_events[0] = False
				self.__enter_sequence_main_region_o_r1_b_default()
				transitioned_after = 0
		return transitioned_after
	
	
	def __main_region_o_r1_b_react(self, transitioned_before):
		"""Implementation of __main_region_o_r1_b_react function.
		"""
		#The reactions of state B.
		transitioned_after = self.__main_region_o_react(transitioned_before)
		if transitioned_after < 0:
			if self.__time_events[1]:
				self.__exit_sequence_main_region_o_r1_b()
				self.__time_events[1] = False
				self.__enter_sequence_main_region_o_r1_a_default()
				transitioned_after = 0
		return transitioned_after
	
	
	def __main_region_o_r2_c_react(self, transitioned_before):
		"""Implementation of __main_region_o_r2_c_react function.
		"""
		#The reactions of state C.
		transitioned_after = transitioned_before
		if transitioned_after < 1:
			if self.__time_events[2]:
				self.__exit_sequence_main_region_o_r2_c()
				self.__time_events[2] = False
				self.__enter_sequence_main_region_o_r2_d_default()
				transitioned_after = 1
		return transitioned_after
	
	
	def __main_region_o_r2_d_react(self, transitioned_before):
		"""Implementation of __main_region_o_r2_d_react function.
		"""
		#The reactions of state D.
		transitioned_after = transitioned_before
		if transitioned_after < 1:
			if self.__time_events[3]:
				self.__exit_sequence_main_region_o_r2_d()
				self.__time_events[3] = False
				self.__enter_sequence_main_region_o_r2_e_default()
				transitioned_after = 1
		return transitioned_after
	
	
	def __main_region_o_r2_e_react(self, transitioned_before):
		"""Implementation of __main_region_o_r2_e_react function.
		"""
		#The reactions of state E.
		transitioned_after = transitioned_before
		if transitioned_after < 1:
			if self.__time_events[4]:
				self.__exit_sequence_main_region_o_r2_e()
				self.__time_events[4] = False
				self.__enter_sequence_main_region_o_r2_f_default()
				transitioned_after = 1
		return transitioned_after
	
	
	def __main_region_o_r2_f_react(self, transitioned_before):
		"""Implementation of __main_region_o_r2_f_react function.
		"""
		#The reactions of state F.
		transitioned_after = transitioned_before
		if transitioned_after < 1:
			if self.__time_events[5]:
				self.__exit_sequence_main_region_o_r2_f()
				self.__time_events[5] = False
				self.__enter_sequence_main_region_o_r2_c_default()
				transitioned_after = 1
		return transitioned_after
	
	
	def __main_region_o_r3_g_react(self, transitioned_before):
		"""Implementation of __main_region_o_r3_g_react function.
		"""
		#The reactions of state G.
		transitioned_after = transitioned_before
		if transitioned_after < 2:
			if self.__time_events[6]:
				self.__exit_sequence_main_region_o_r3_g()
				self.set_request_pending_observable.next(False)
				self.__time_events[6] = False
				self.__enter_sequence_main_region_o_r3_h_default()
				transitioned_after = 2
		return transitioned_after
	
	
	def __main_region_o_r3_h_react(self, transitioned_before):
		"""Implementation of __main_region_o_r3_h_react function.
		"""
		#The reactions of state H.
		transitioned_after = transitioned_before
		if transitioned_after < 2:
			if self.__time_events[7]:
				self.__exit_sequence_main_region_o_r3_h()
				self.set_request_pending_observable.next(True)
				self.__time_events[7] = False
				self.__enter_sequence_main_region_o_r3_g_default()
				transitioned_after = 2
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
		self.__time_events[2] = False
		self.__time_events[3] = False
		self.__time_events[4] = False
		self.__time_events[5] = False
		self.__time_events[6] = False
		self.__time_events[7] = False
	
	
	def __micro_step(self):
		"""Implementation of __micro_step function.
		"""
		transitioned = -1
		self.__state_conf_vector_position = 0
		state = self.__state_vector[0]
		if state == self.State.main_region_or1a:
			transitioned = self.__main_region_o_r1_a_react(transitioned)
		elif state == self.State.main_region_or1b:
			transitioned = self.__main_region_o_r1_b_react(transitioned)
		if self.__state_conf_vector_position < 1:
			state = self.__state_vector[1]
			if state == self.State.main_region_or2c:
				transitioned = self.__main_region_o_r2_c_react(transitioned)
			elif state == self.State.main_region_or2d:
				transitioned = self.__main_region_o_r2_d_react(transitioned)
			elif state == self.State.main_region_or2e:
				transitioned = self.__main_region_o_r2_e_react(transitioned)
			elif state == self.State.main_region_or2f:
				transitioned = self.__main_region_o_r2_f_react(transitioned)
		if self.__state_conf_vector_position < 2:
			state = self.__state_vector[2]
			if state == self.State.main_region_or3g:
				self.__main_region_o_r3_g_react(transitioned)
			elif state == self.State.main_region_or3h:
				self.__main_region_o_r3_h_react(transitioned)
	
	
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
		self.__state_vector[2] = self.State.null_state
		self.__state_conf_vector_position = 2
		self.__is_executing = False
	
	
	def trigger_without_event(self):
		"""Implementation of triggerWithoutEvent function.
		"""
		self.run_cycle()
	
