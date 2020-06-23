#!/usr/bin/env python3.7
################################################################################
# File:    buskill_gui.py
# Purpose: This is the code to launch the BusKill GUI app
#          For more info, see: https://buskill.in/
# Authors: Michael Altfield <michael@buskill.in>
# Created: 2020-06-23
# Updated: 2020-06-23
# Version: 0.1
################################################################################

import buskill
import webbrowser

import kivy
#kivy.require('1.0.6') # replace with your current kivy version !

from kivy.app import App
from kivy.uix.widget import Widget
from kivy.uix.label import Label
from kivy.uix.gridlayout import GridLayout
from kivy.properties import ObjectProperty

from kivy.core.window import Window
Window.size = ( 480, 800 )

class MainWindow(GridLayout):

	toggle_btn = ObjectProperty(None)
	status = ObjectProperty(None)

	def toggleBusKill(self):
		buskill.toggle()
		if buskill.isArmed():
			self.toggle_btn.text = 'Arm'
			self.status.text = 'BusKill is currently disarmed.'
			self.toggle_btn.background_color = [1,1,1,1]
			buskill.buskill_is_armed = False
		else:
			self.toggle_btn.text = 'Disarm'
			self.status.text = 'BusKill is currently armed.'
			self.toggle_btn.background_color = [1,0,0,1]
			buskill.buskill_is_armed = True

class CriticalError(GridLayout):

	msg = ObjectProperty(None)

	def showError( self, msg ):
		self.msg.text = msg

	def fileBugReport( self ):
		# TODO: make this a redirect on buskill.in so old versions aren't tied
		#       to github.com
		webbrowser.open( 'https://github.com/BusKill/buskill-app/issues' )

class BusKill(App):

	buskill.init()
	print( buskill.ERR_PLATFORM_NOT_SUPPORTED )

	def build(self):

		buskill.init()

		# is the OS that we're running on supported?
		if buskill.isPlatformSupported():

			# yes, this platform is supported; show the main window
			return MainWindow()

		else:
			# the current platform isn't supported; show critical error window

			crit = CriticalError()
			crit.showError( buskill.ERR_PLATFORM_NOT_SUPPORTED )
			return crit
