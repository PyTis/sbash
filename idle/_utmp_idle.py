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

import os		# for stat (to get idle times)
if os.name != 'posix':
	raise ImportError("This modules requires a posix compatible system.")
import time		# for the idle time math
import getpass		# for getuser()
import stat		# for stat constants
import errno		# for errno constants
import utmp		# for reading the utmp file (unix only)
import UTMPCONST	# for utmp constants
from pprint import pprint
import sys  # added by jlee XXX:TODO remove this when done debugging

__all__ = ['_idle']	# don't clutter the namespace

def _idle(update_ttys=True):
	"""returns the min idle time of the current user. you can optionally
	update the idle times of the other tty's to prevent any sudden jumps
	in values from this function, should a recent terminal be closed."""

	idle = None
	user = getpass.getuser()
	print(user)
	u = utmp.UtmpRecord()	# iterator
	tty = {}		# dictionary of stats

# USER EXAMPLE
# : root :
# utmp.UtmpEntry( ut_type=2, ut_pid=0, ut_line='~', ut_id='~~',
# ut_user='reboot', ut_host='3.13.0-45-generic', ut_exit=(0, 0), ut_session=0,
# ut_tv=(1546498580, 227865), ut_addr_v6=(0, 0, 0, 0) )
#
# available variables
# 'ut_addr_v6', 'ut_exit', 'ut_host', 'ut_id', 'ut_line', 'ut_pid',
# 'ut_session', 'ut_tv', 'ut_type', 'ut_user'
#
# USER EXAMPLE
# : jlee :
# utmp.UtmpEntry( ut_type=2, ut_pid=0, ut_line='~', ut_id='~~',
# ut_user='reboot', ut_host='3.13.0-45-generic', ut_exit=(0, 0), ut_session=0,
# ut_tv=(1546498580, 227865), ut_addr_v6=(0, 0, 0, 0) )

	for x in u:
		if x.ut_type == UTMPCONST.USER_PROCESS \
		and x.ut_user == user:
			# try/except in case /dev/* doesn't work/exist
			try:
				'''
				tty['ut_addr_v6'] = x.ut_addr_v6
				tty['ut_exit'] = x.ut_exit
				tty['ut_host'] = x.ut_host
				tty['ut_id'] = x.ut_id
				tty['ut_line'] = x.ut_line
				tty['ut_pid'] = x.ut_pid
				tty['ut_session'] = x.ut_session
				tty['ut_tv'] = x.ut_tv
				tty['ut_type'] = x.ut_type
				tty['ut_user'] = x.ut_user
				'''
				tty[x.ut_line] = os.stat('/dev/'+x.ut_line)
				z = time.time() - tty[x.ut_line][stat.ST_ATIME]
			except:
				z = None

			if z is not None:
				if idle is None: idle = z
				idle = min(idle, z)

		elif x.ut_type == UTMPCONST.USER_PROCESS \
		and x.ut_user == '':
			pprint(x)
			# trying this for root.
			try:
				'''
				tty['ut_addr_v6'] = x.ut_addr_v6
				tty['ut_exit'] = x.ut_exit
				tty['ut_host'] = x.ut_host
				tty['ut_id'] = x.ut_id
				tty['ut_line'] = x.ut_line
				tty['ut_pid'] = x.ut_pid
				tty['ut_session'] = x.ut_session
				tty['ut_tv'] = x.ut_tv
				tty['ut_type'] = x.ut_type
				tty['ut_user'] = x.ut_user
				'''
				tty[x.ut_line] = os.stat('/dev/'+x.ut_line)
				z = time.time() - tty[x.ut_line][stat.ST_ATIME]
			except:
				z = None

			if z is not None:
				if idle is None: idle = z
				idle = min(idle, z)

	# possible values from utmp, and formatting data:
	# '%-10s %-5s %10s %-10s %-25s %-15s %-10s %-10s %-10s %-10s %-10s'
	# (USER, TTY, PID, HOST, LOGIN, IDLE, TYPE, SESSION, ID, EXIT, IPV6')
	# (x.ut_user, x.ut_line, x.ut_pid, x.ut_host, time.ctime(x.ut_tv[0]), 
	# z, x.ut_type, x.ut_session, x.ut_id, x.ut_exit, x.ut_addr_v6)

	u.endutent()					# close the utmp file!
	pprint(tty)
	sys.exit(1)

	# if you `watch' the output of this function, the idle time value will
	# slowly increase as the time passes. if you then close the least idle
	# terminal, suddenly the idle time will jump to that of the next least
	# idle. the bad side effect is that a system which is being used alot,
	# can suddenly seem as if it's been idle for a very long time. to stop
	# this from happening, we can optionally `touch' all the /dev/'s using
	# python os.utime and change them to match the least idle tty. if this
	# is what you want, then you must choose so explicitly, and accept all
	# of the consequences. (whatever they may be!) only ATIME is modified.
	if update_ttys:
		if idle is None: add = 0
		else: add = idle
		for (key, value) in tty.items():
		# set the ATIME to now + however long the shortest /dev/ has
		# been idle for. this is similar to using unix `touch, minus
		# the extra idle offset we add on so as not to reset it all.
			try:
				os.utime('/dev/'+key,
				(time.time()+add, value[stat.ST_MTIME]))
			except OSError, e:
				if e.errno == errno.EPERM:
					pass
				else: raise e

	# if utmp is empty
	if idle is None: return None
	else: return int(idle*1000)


if __name__ == '__main__':
	print _idle()

