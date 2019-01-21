TASKS
=====

Concept
_______

	Okay, first lets describe the problem.  A user logs into a Unix/Linux server,
with or without an SSH key (let us hope with) from a Microsuck Windows machine,
likely using putty, or similar GUI-less program.  Now they are facing a
text-only interface (Bash/sh/etc.), what happens when they walk away, without
closing the terminal?  Now there are a few settings that a user can tweak in
PuTTy or pageant, that will try to keep the connection alive as long as
possible, better yet, most of us programmers run our own servers, or at the
very least, have root access to the servers we work on.  I myself have been
known to tweak the sshd config so that the connections wouldn't timeout as
fast.  Instead of 30 minutes, I've changed them to 30 days.  Why?  Because if I
forget to open a "Screen" session, then when the connection is cut, I could
loose any unsaved work.  I know dozens of programmers who don't even know about
that (Screen, and it's ability to restore sessions after a disconnect), and who
shell in, only to open Vim next.  If 30 minutes goes by (the default amount of
time) without a key being pressed, the session is closed.  Oops, sorry guy,
your vim file is corrupted.  I know I myself had this happen on more than one
occasion.

	Why is this?  Why are session times cut at all?  It is for security.  What if
a user assumes the role of root (sudo su -), and then walks away from his/her
computer?  Anyone can walk over, and type anything, from HALT, or reboot, to
the infamous, "rm -rf \*".

	Wouldn't it be nice if we could lock the screen?  OR better yet, if we forgot
to, it would do it for us?  Much like Winblows turns a Screensaver on, then
requires a password to unlock the screen, this could/should happen on Linux.

	Imagine if you opened a PuTTy terminal, and after 3 minutes a text-based
screen-saver opened up, only to next, require a password to return to your
work.  This is my idea, at the heart of it, this is what I hope to accomplish.

	Now, to plan out a few steps, hopefully obvious ones, to accomplish this.


ROADMAP
-------

	I've already created a signal-test.py file (testing CTRL+C, and CTRL+Z) I
could catch and control SIGTERM SIGNALS to ensure a user could not circumvent
the screen-saver simply by pressing CTRL+C or CTRL+Break exiting the program,
or CTRL+z, back-grounding it.

	Now, how will this be designed?  
	How will it work?

	I believe, right off the bat, that it will require threading.  However, it
should be simple, and only really utilize two, separate threads.


	And now, sitting here, pondering and planning, I've just come to a
realization, I don't need the first version to have a screen saver.  The first
version, simply needs to "blank" the screen, to hide any proprietary, or
protected data, and "lock" the screen (requiring a password to return).  This
will simply require threading, as mentioned before.  


*Now, let's start with the design -*

	A "Master" primary program, to control the child threads.  Be it in Python or
in Bash.  This parent program, will be like a server to clients, we will dub
thee the "Controller" program.  This Controller program, will create a Bash
shell, and only really watch for a SigtermKill (exit) to know it itself should
exit.  It will pass all input, all keys depressed to the Bash program, while
MONITORIng idle time.  If idle time is greater than T, T being the set idle
time permitted, then it will hide, almost like minimizing in Winblows, the Bash
shell. Next it will use the SS Controller (Screen-Saver Controller), which at
first, will be just a blank screen.  This will be written to eventually be
able to read a settings file, to know which SS to load, but for now, will just
show a blank screen.  When the user presses ANY key, it will then know to
prompt the user for his/her password.  Only a successful password entry will
tell the SS Controller to close, and re-show the Bash program.  This is the
main concept.  Now, I foresee this being used, in the future by server admins,
who may wish to "force" this a security measure, on all system users,
therefore, it will likely run as root, perhaps when being installed, moving
"/bin/bash" (!which bash) to "/bin/bash.old" and then symbolically linking this
program, "/bin/sbash" to "/bin/bash."  The system administrator will likely set
the permitted idle-time, as well as the default screen saver.  


  Now, I've envisioned the SysAdmin to be able to permit, or disallow user
overrides.  Much like when configuring Apache for websites, when hosting
multiple sites in different /home/USER}/public_html directories, server admins
can allow, or disallow for .htaccess overrides.  I foresee some SysAdmins
having there config files for this program set so that no overrides are
permitted, and yet others allowing for some overrides, perhaps setting a strict
idle time, but allowing the screen saver that runs to be selected by the user,
and set in a user's .ssaver-config file located in /home/{USER}/.ssaver-config
file.  This would of course require some sort of interactive listing feature,
that would list possible, installed screen savers to the user, to try and chose
from.


Syncronis
Asyncronis
must run asynchronous so it can run returns immediately and we can continue in
the main thread.


Shell=True
	VS
shell=False

