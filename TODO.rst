TODO
====

Future Versions
---------------

K.I.S.S.: Keep it Simple Stupid.

I need to remember, I need to hold most of the features I've dremt up for
future versions.



 With a simple directive in tmux.conf, "new-session -s default", or similar, one can simply run on login "tmux attach", and it will either attach to a new session named default, or attach to an existing running session previously started.

server - runs and ensures no one is on tty without pts/1
like, not ssh'ed in, without being in a tmux session

client, that starts when each client starts to monitor their idle time, if
idle, then background's tmux, or screen, then starts the screen saver ( / locks
screen in version < 1), then asks for password to unlock screen, and return to
tmux or screen, not sure yet.


