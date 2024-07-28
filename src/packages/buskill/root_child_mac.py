#!/usr/bin/env python3
"""
::

  File:    packages/buskill/root_child_mac.py
  Authors: Michael Altfield <michael@buskill.in>
  Created: 2022-10-15
  Updated: 2024-07-27
  Version: 0.2

This is a very small python script that is intended to be run with root privileges on MacOS platforms. It should be as small and paranoid as possible, and only contain logic that cannot run as the normal user due to insufficient permissions (eg shutting down the machine)

For more info, see: https://buskill.in/
"""

################################################################################
#                                   IMPORTS                                    #
################################################################################

import logging, re, sys, subprocess, os

################################################################################
#                                  SETTINGS                                    #
################################################################################

################################################################################
#                                  FUNCTIONS                                   #
################################################################################

# this function will gently shutdown a MacOS machine
def trigger_softshutdown_mac():
	msg = "BusKill soft-shutdown trigger executing now"
	logging.debug( msg )

	# first we try to shutdown with `shutdown`
	trigger_softshutdown_mac_shutdown()

# shutdown the computer with the `shutdown` command
def trigger_softshutdown_mac_shutdown():

	try:
		# first try to shutdown with the `shutdown` command
		msg = "Attempting to execute `shutdown -h now`"
		logging.info(msg)

		# TODO: swap 'reboot' for actual 'shutdown' command
		result = subprocess.run(
		 #[ 'reboot' ],
		 [ 'shutdown', '-h', 'now' ],
		 capture_output=True,
		 text=True
		)

		msg = "subprocess returncode|" +str(result.returncode)+ "|"
		logging.debug(msg)

		msg = "subprocess stdout|" +str(result.stdout)+ "|"
		logging.debug(msg)

		msg = "subprocess stderr|" +str(result.stderr)+ "|"
		logging.debug(msg)

		if result.returncode != 0:
			# that didn't work; log it and try fallback
			msg = "Failed to execute `shutdown -h now`!"
			logging.warning(msg)

		trigger_softshutdown_mac_halt()

	except Exception as e:
		# that didn't work; log it and try fallback
		msg = "Failed to execute `shutdown -h now`!"
		logging.warning(msg)

		trigger_softshutdown_mac_halt()

# shutdown the computer with the `halt` command
def trigger_softshutdown_mac_halt():

	try:
		# try to shutdown with the `halt` command
		msg = "Attempting to execute `halt"
		logging.info(msg)

		result = subprocess.run(
		 #[ 'reboot' ],
		 [ 'halt' ],
		 capture_output=True,
		 text=True
		)

		msg = "subprocess returncode|" +str(result.returncode)+ "|"
		logging.debug(msg)

		msg = "subprocess stdout|" +str(result.stdout)+ "|"
		logging.debug(msg)

		msg = "subprocess stderr|" +str(result.stderr)+ "|"
		logging.debug(msg)

		if result.returncode != 0:
			# that didn't work; log it and give up :(
			msg = "Failed to execute `halt`! "
			logging.error(msg)

	except Exception as e:
		# that didn't work; log it and give up :(
		msg = "Failed to execute `halt`! " +str(e)
		logging.error(msg)

################################################################################
#                                  MAIN BODY                                   #
################################################################################

####################
# HANDLE ARGUMENTS #
####################

# the first argument is the file path to where we write logs
log_file_path = sys.argv[1]

# check sanity of input. Be very suspicious
if not re.match( "^[A-Za-z0-9\-\_\./\ ]+$", log_file_path ):
	print( "First positional argument (log file path) is invalid. Exiting" )
	sys.exit(1)

#################
# SETUP LOGGING #
#################

logging.basicConfig(
 filename = log_file_path,
 filemode = 'a',
 format = '%(asctime)s,%(msecs)d root_child %(levelname)s %(message)s',
 datefmt = '%H:%M:%S',
 level = logging.DEBUG
)

msg = "==============================================================================="
logging.info(msg)
msg = "root_child_mac is writing to log file '" +str(log_file_path)+ "'"
logging.info(msg)

#############
# HARDENING #
#############

# SECURITY NOTE:
# 
#  Whenever you execute something as root, it's very important that you know
#  _what_ you're executing. For example, never execute a script as root that is
#  world-writeable. In general, assuming the script is named 'root_child.py':
#
#  1. Make sure root_child.py has permissions root:root 0500 (and therefore only
#     writeable and executable by root)
#  2. Make sure I specify the absolute path to root_child.py, and that path
#     cannot be maliciously manipulated
#  3. Make sure that root_child.py isn't actually a (sym)link
#
# The parent process that spawned us is able to check #2 and #3, but
# unfortunately we can't package a .dmg with a file owned by root, so on
# first run, we harden ourselves by changing the owner of this root_child file
# to be owned by root:root
# 
# See also:
#  * https://github.com/BusKill/buskill-app/issues/14#issuecomment-1272449172
#  * https://github.com/BusKill/buskill-app/issues/14#issuecomment-1279975783
#  * https://github.com/BusKill/buskill-app/issues/77#issuecomment-2254299923

our_filepath = os.path.abspath(__file__)

msg = "Attempting to harden ourselves " +str(our_filepath)
logging.info(msg)

try:
	# set owner of <this> binary to root:root
	os.chown( our_filepath, 0, 0 )
except Exception as e:
	msg = "Failed to harden"
	logging.warning(msg)

#############
# MAIN LOOP #
#############

# loop and listen for commands from the parent process
while True:

	msg = "Waiting for command"
	logging.info(msg)

	# block until we receive a command (ending with a newline) from stdin
	command = sys.stdin.buffer.readline().strip().decode('ascii')
	msg = "Command received"
	logging.info(msg)

	# check sanity of received command. Be very suspicious
	if not re.match( "^[A-Za-z_-]+$", command ):
		msg = "Bad Command Ignored\n"

		logging.error(msg)
		sys.stdout.buffer.write( msg.encode(encoding='ascii') )
		sys.stdout.flush()
		continue

	# what was the command they sent us?
	if command == "soft-shutdown":
		# they want us to shutdown the machine; do it!
		msg = "Command is 'soft-shutdown'"
		logging.debug(msg)

		try:
			msg = "Attempting to call trigger_softshutdown_mac()"
			logging.debug(msg)

			trigger_softshutdown_mac()
			msg = "Finished executing 'soft-shutdown'\n"
			logging.info(msg)

		except Exception as e:
			msg = "Failed to execute trigger_softshutdown_mac()\n" +str(e)
			logging.error(msg)

	elif command == "ping":
		# they just want to check to see if we're still alive; respond with pong
		msg = "Command is 'ping'"
		logging.debug(msg)

		msg = "pong\n"
		logging.info(msg)

	else:   
		# I have no idea what they want; tell them we ignored the request
		msg = "Unknown Command Ignored\n"
		logging.warning(msg)

	sys.stdout.buffer.write( msg.encode(encoding='ascii') )
	sys.stdout.flush()
