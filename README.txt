Daemon that receives the path to the file/folder as the command line argument, archives this folder/file on system signal SIGUSR1
and extracts it on a signal SIGUSR2.
Path to the folder here backups are stored is hard-coded :) change the constant in my_daemon.py