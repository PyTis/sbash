#!/usr/bin/python
"""
    Evanescent machine idle detection and shutdown tool.
    Copyright (C) 2008  James Shubin, McGill University
    Written for McGill University by James Shubin <purpleidea@gmail.com>

    This program is free software: you can redistribute it and/or modify
    it under the terms of the GNU Affero General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.

    This program is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU Affero General Public License for more details.

    You should have received a copy of the GNU Affero General Public License
    along with this program.  If not, see <http://www.gnu.org/licenses/>.
"""

__all__ = ['idle', 'is_idle', 'timeleft']

import time
from _utmp_idle import _idle as _idle


def idle():
	"""Returns the number of milliseconds that the machine has been idle.
	This should work on X11 (including the DPMS bug workaround) and on
	Windows. With this function, moving the mouse resets the counter.
	This also looks at each readable tty. (using utmp on posix)"""
	return _idle()


def is_idle(threshold):
	"""is the current user idle (eg: past-threshold) or not?
	threshold is specified in seconds for logical usage."""
	assert type(threshold) is int
	return idle() > int(threshold*1000)


def timeleft(threshold):
	"""return the approximate number of seconds left before the user would
	be expected to go idle, assuming no more input activity is seen."""
	assert type(threshold) is int
	return int((int(threshold*1000) - idle()) / 1000)

def event_on_idle(frequency=10, repeat=False, event_callback, *args, **kwargs):
	""" 
	int: frequency - seconds, how often to check to see if idle.
	bool: repeat - call the callback once idle, and then continue looping, or
		break
	function: event_callback - self explanitory
	*args, and **kwargs are passed to event_callback


always, or once,
	while True: if idle(): event_callback()
	
	I really wish it could be this simple, however, it needs to be threaded, so
	you can "'set-it' and 'forget-it'", with it running in the background.

	a "WHEN" conditional, repeat=True, 
	a "ONCE" conditional, repeat=False
	

Timer(*args, **kwargs)
    Factory function to create a Timer object.

    Timers call a function after a specified number of seconds:

        t = Timer(30.0, f, args=[], kwargs={})
        t.start()
        t.cancel()     # stop the timer's action if it's still waiting
(END)

	"""
	def call_the_callback():
	
		t = threading.Timer(frequency, idle_screen)

	while True:
		if idle(): 
			event_callback(*args, **kwargs)
			if not repeat:
				break
		
		# now here is my conundrum, has it really been test_time since the last
		# run? or does the idle() function take some of that time?  I.E. Let's say
		# that you rant to test for idle every single second, however, idle() takes
		# 0.5 seconds to run (hypothetically), then you really only need to sleep
		# for 0.5 seconds, to ensure this is running every 1 second, or what ever
		# you wish the testing time to be.  I am going to make this a little
		# smarter than normal, or at least try to.  I am going to make this self
		# adjusting.  
		else:
			time.sleep(frequency)

class Timer (object):
	pass

class StopWatch (object):
	running = False
	_elapsed = 0.0
	start_time = 0.0
	last_elapsed = 0.0
	last_time = 0.0

	def set_elapsed(self,elapsed_time):
		self._elapsed=elapsed_time
	def get_elapsed(self):
		if self.running: return self._elapsed + float(time.time()-self.start_time)
		return self._elapsed
	time=elapsed = property(get_elapsed, set_elapsed) # setting an Alias
		
	def __init__(self):
		self.running = False
		self.start_time = float(0.0)
		self.elapsed = float(0.0)

	def Start(self):
		self.start_time = time.time()
		self.running = True
	# setting an Alias
	start=Start

	def Stop(self):
		self.elapsed = float(time.time()-self.start_time) + float(self.elapsed)
		self.start_time = time.time()
		self.running = False
	# setting an Alias
	stop=pause=Stop

	def Reset(self):
		self.last_time=self.last_elapsed=self.time
		self.running = False
		self.start_time = float(0.0)
		self.elapsed = float(0.0)
	# setting an Alias
	reset=Reset


if __name__ == '__main__':
	print idle()

