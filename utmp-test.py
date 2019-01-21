#!/usr/bin/env python
# -*- coding: utf-8 -*-

from utmp import UtmpFile
import time

for utmp in UtmpFile():
    # utmp is a Utmp object
    if utmp.ut_user_process:
        print '%s logged in at %s on tty %s' % (utmp.ut_user, time.ctime(utmp.ut_time), utmp.ut_line)

