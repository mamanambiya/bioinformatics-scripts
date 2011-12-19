#!/usr/bin/env python
#
# A Python script to retrieve the PID of the Papers or Papers2 app and kill it
# This can be added to crontab in order to kill Papers at a given time

# import required modules
import psutil
import os, signal

# define constant array with the name of the processes
# you required to be closed
PROC_NAMES = ["Papers", "Papers2"]

# iterate through all processes
for proc in psutil.process_iter():
	# check if process name is in the PROC_NAMES list
	if proc.name in PROC_NAMES:
		# send a SIGTERM signal to the process
		# should should call a graceful exit of
		# the program (as opposed to SIGKILL)
		os.kill(proc.pid, signal.SIGTERM)
