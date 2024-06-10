#!/usr/bin/env python3
#import pdb;pdb.set_trace()
"""
::

  File:    main.py
  Authors: Michael Altfield <michael@buskill.in>
  Created: 2020-06-23
  Updated: 2024-02-25
  Version: 0.3

This is the main wrapper script for launching the BusKill app.

It has no functions and simply sets-up some essential requirements based on the platform, sets-up logging, and then either launches the CLI (``buskill_cli.py``) or the GUI (``buskill_gui.py``).

For more info, see: https://buskill.in/

"""

# this is needed for supporting Windows 10 with OpenGL < v2.0
# Example: VirtualBox w/ OpenGL v1.1
import platform, os
CURRENT_PLATFORM = platform.system().upper()
if CURRENT_PLATFORM.startswith( 'WIN' ):
    os.environ['KIVY_GL_BACKEND'] = 'angle_sdl2'

# grp is only available on *nix systems
if CURRENT_PLATFORM.startswith( 'LINUX' ) or CURRENT_PLATFORM.startswith( 'DARWIN' ):
	import grp

################################################################################
#                                   IMPORTS                                    #
################################################################################

import argparse, logging, sys, multiprocessing, tempfile
import packages.buskill

################################################################################
#                                  SETTINGS                                    #
################################################################################

#BUSKILL_VERSION = '0.1'
from buskill_version import BUSKILL_VERSION

################################################################################
#                                  MAIN BODY                                   #
################################################################################

if __name__ == '__main__':

	#################
	# SETUP LOGGING #
	#################

	# TODO: disable logging by default; enable it with an argument
	# TODO: be able to override the path to the log file with an env var or argument value; make these just the defaults
	log_file_path = os.path.join( tempfile.gettempdir(), 'buskill.log' )

	logging.basicConfig(
	 filename = log_file_path,
	 filemode = 'a',
	 format = '%(asctime)s,%(msecs)d %(name)s %(levelname)s %(message)s',
	 datefmt = '%H:%M:%S',
	 level = logging.DEBUG
	)
	msg = "==============================================================================="
	print( msg ); logging.info( msg )
	msg = "INFO: Writing to log file '" +str(log_file_path)+ "'"
	print( msg ); logging.info( msg )

	logging.debug( 'BUSKILL_VERSION|' +str(BUSKILL_VERSION)+ '|' )
	logging.debug( 'os.environ|' +str(os.environ)+ '|' )
	logging.debug( 'user|' +str(os.getlogin())+ '|' )
	logging.debug( 'uid|' +str(os.getuid())+ '|' )
	if grp:
		logging.debug( 'group|' +str(grp.getgrgid( os.getgid() ))+ '|' )
	logging.debug( 'gid|' +str(os.getgid())+ '|' )
	logging.debug( 'sys.argv|' +str(sys.argv)+ '|' )
	logging.debug( 'sys.builtin_modules_names|' +str(sys.builtin_module_names)+ '|' )
	logging.debug( 'sys.executable|' +str(sys.executable)+ '|' )
	logging.debug( 'sys.path|' +str(sys.path)+ '|' )
	logging.debug( 'sys.prefix|' +str(sys.prefix)+ '|' )
	logging.debug( 'sys.version|' +str(sys.version)+ '|' )
	logging.debug( 'sys.api_version|' +str(sys.api_version)+ '|' )
	logging.debug( 'sys.version_info|' +str(sys.version_info)+ '|' )
	logging.debug( '__name__|' +str(__name__)+ '|' )

	# platform info
	logging.debug( 'sys.platform|' +str(sys.platform)+ '|' )
	logging.debug( 'platform.platform()|' +str(platform.platform())+ '|' )
	logging.debug( 'platform.system()|' +str(platform.system())+ '|' )
	logging.debug( 'platform.release()|' +str(platform.release())+ '|' )
	logging.debug( 'platform.version()|' +str(platform.version())+ '|' )
	logging.debug( 'platform.machine()|' +str(platform.machine())+ '|' )

	# what platform are they running?
	CURRENT_PLATFORM = platform.system().upper()
	if CURRENT_PLATFORM.startswith( 'LINUX' ):
		# they're running linux; what distro and version of linux?
		try:
			with open( "/etc/os-release" ) as f:
				logging.debug( str(f.read()) )
		except Exception:
			pass

	if CURRENT_PLATFORM.startswith( 'WIN' ):
		# they're running windows; what version of windows?
		try:
			logging.debug( 'sys.getwindowsversion()|' +str(sys.getwindowsversion())+ '|' )
		except Exception:
			pass
	
	if CURRENT_PLATFORM.startswith( 'DARWIN' ):
		# they're running mac; what version of macos?
		try:
			logging.debug( 'platform.uname()|' +str(platform.uname())+ '|' )
			logging.debug( 'platform.mac_ver()|' +str(platform.mac_ver())+ '|' )
		except Exception:
			pass

	###########
	# PREREQS #
	###########

	# fix windows "error: unrecognized arguments: --multiprocessing-fork"
	# * kttps://stackoverflow.com/questions/46335842/python-multiprocessing-throws-error-with-argparse-and-pyinstaller
	multiprocessing.freeze_support()

	# fix macos error "The process has forked and you cannot use this CoreFoundation functionality safely. You MUST exec()."
	if CURRENT_PLATFORM.startswith( 'DARWIN' ):
		multiprocessing.set_start_method('spawn')

	msg = "buskill version " +str(BUSKILL_VERSION)
	print( msg ); logging.info( msg )

	# instantiate the buskill object
	global bk
	bk = packages.buskill.BusKill()

	#############
	# LAUNCH UI #
	#############

	# did we get any command-line arguments?
	if len(sys.argv) < 2:
		# we were given 0 command line arguments; just launch the GUI

		print( "No command-line arguments detected. Launching GUI" )
		print( "Hint: execute `buskill --help` for command-line usage" )

		# tell kivy to store its data in our buskill DATA_DIR
		os.environ['KIVY_HOME'] = bk.DATA_DIR

		from buskill_gui import BusKillApp
		BusKillApp( bk ).run()

	else:
		# the user passed-in arguments; give 'em the cli

		from buskill_cli import *
		ret = BusKillCLI( bk )

		sys.exit( ret )

