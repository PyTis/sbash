sbash
=====

Okay, lets talk why.  Why is this needed?  Well, it may not be for you, or...
it may just be exactly what you are looking for.  I know I want it, that is
why I am writing it.  Because I think others may find it useful, is why I am
taking out the time to try to do it right.
So talking about me, I am a programmer, heavy into it.  Full APC rack at my
home, dual power sources, dual internet providers, full redundancy, 2U APC
Battery Backups with 2 PDU's, and 12 servers.  I'm balls deap into it.  I am
willing to bet there may be others out there like me.  Perhaps not as crazy as
I am, but I know for a fact, many programmers have their own servers.  And,
there have to be other groups of friends like me and mine, that have their own
private networks (I host part of our private encrypted mesh network).  Now, in
my development, many times I just develop within a user's directory, on a
client's server.  However, there are other times, where I find myself almost
always su'ed to root on a server (generally on servers that I am writting
daemons on).  I hate having to open another SSH shell or puTTy window because
of idle timeout.  I usually always have one open for each of my main servers
(the ones I intereact with the most).  

In puTTy's settings, I have Enable TCP keepalives (SO_KEEPALIVE option)
checked.  Outside of puTTY, I have:
	ServerAliveInterval 120

This will send a "null packet" every 120 seconds on your SSH connections to
keep them alive.  On the server side, I have: 
	ClientAliveInterval 120
	ClientAliveCountMax 720

This will make the server send the clients a “null packet” every 120 seconds
and not disconnect them until the client have been inactive for 720 intervals
(120 seconds * 720 = 86400 seconds = 24 hours).

View more on this at: https://bjornjohansen.no/ssh-timeout

Now, I also have ScreenSaver's turned off.  I work from home, and the chance of
someone (a coworker) messing with my computer is very low.  On the other hand,
with me haveing a 2 and 4 year old walking up to my keyboard when I am away,
and trying to mimic daddy, the chance of one of them pressing up arrow and the
Enter Key, are not impossible.  I just don't like leaving a root terminal
exposed.  I know the right thing to do is to log out, but this isn't really
convienent in full development mode.  Sometimes I am in the middle of
something, with dozens of files open in a single vim window via split screen,
and closing the window even disconnecting from screen or tmux isn't that
apparent, what if I forget to do this?  Why can't I just have the screen simply
"lock" after idle timeout, and ask for a password to unlock it, just like a
Winblows screen saver, or even cooler, have an actual text based screen saver
kick in.  I have pondered this idea for many years.  Finally, I am doing
something about it.

Guide to other files.
---------------------

README.rst
__________

(THIS FILE)

LICENSE
_______ 

  This will be updated, for now I am using my old PyTis License, but the *"GNU
Affero General Public License v3.0"* seems very intriguing.  The two things I
want to keep from my License is the "You must keep my logo file with the code
base," and the "You must credit the original author, and all subsequent
authors."  Which actually, that section itself may need updated, because I
believe it actually only states that you must credit the original author (me),
however my intent was, that anyone who does a fork of my project, add their
name to the Author's list, and if their project is then forked, the next
developer add their name, continuously appending to the list of authors, but
never removing an author's name.

TASKS.rst
_________

A roadmap for the current itteration, before the next major releases.

TODO
____

A roadmap and/or brain dump for ideas for future versions, after the next major
release.

NAME
----

sbash or msbash, Stands for Secure Bash or a More Secure Bash.

S. secure
B. bourne
A. again
SH.shell

SYNOPSIS
--------

sbash [optional - path to config/-V/-h/--help]

DESCRIPTION
-----------

MY STANDARDS ABOUT PROGRAM DESIGN
---------------------------------

One thing I do, when naming a program, I.E. one of the "programs" in this
module, is named pylock.  I created the file, pylock.py, and symbolically link
it, to pylock, chmoded with 0755 and a shebang line.  Simple enough right?  But
before I am "locked" in on the name, I usually always do two tasks.  First I
type "which {PROGRAM-NAME}" in this case, "which pylock" to make sure I have no
conflicts on my system.  Then I also always open aptitude, and search for the
name I've chosen.  After I searched for pylock, and found there were zero
results in aptitude, the name is confirmed.  Not before.  If I found any
projects, or software with the same name, even if they are written in some
other language, like Ruby or Go, and I don't have them installed, I would
change the name.  This way if someone else one day uses my program and does
have those things installed, they wouldn't have a naming conflict.  I just
consider this a good standard.

Additionally to this, I used to always have my main programs without
extensions, but I later found that when adding on to them, I couldn't easily
import functions from these files, as the were not valid python modules.
Therefore I've began creating all programs with .py extensions, and using
symbolic links, as described above, to create the program that is executed.


OPTIONS
-------


