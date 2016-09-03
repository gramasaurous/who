#!/usr/bin/env python

# Graham Greving
# grahamgreving@gmail.com
# 09/02/2016
# Simple Python interface for Hue lights

import logging
import requests

# who class defines a connection to a specific hue device and its lights
class Who:
	def __repr__(self):
		string = self.ip + "\n"
		for l in self.lights:
			string += "\t %s \n" % (l)
		return string

	def __init__(self, bridge_ip, api_token, logger=None):
		self.logger = logger or logging.getLogger(__name__)
		self.ip = bridge_ip
		self.api_token = api_token
		self.lights = []
		# get_lights() is where connection to bridge is attempted
		# and will throw an appropriate exception if something goes wrong
		# see get_lights() for documentation
		self.get_lights()

	def get_lights(self):
		try:
			url = "http://" + self.ip + "/api/" + self.api_token + "/lights"
			r = requests.get(url, timeout=2)
			r.raise_for_status()
			lights = r.json()
			if lights[0]['error']:
				self.logger.error("Bad API token")
				raise Exception, "Bad API token"
			for light in lights:
				self.lights.append(self.Light(self, light, lights[light]))
		except requests.exceptions.HTTPError:
			self.logger.error("Get Lights Request recieved error code: " + r.status_code)
			raise
		except requests.exceptions.Timeout:
			self.logger.exception("Connection to bridge timed out")
			raise
		except Exception:
			self.logger.exception("Get Lights Request Caught Exception")
			raise

	class Light:
		def __repr__(self):
			state = "on" if self.state["on"] else "off"
			string = "light id: %s (%s) - %s" % (self.id, self.name, state)
			# string = "light #" + self.id + " (" + self.name + ")" + 
			return string

		def __init__(self, bridge, id, attrs):
			try:
				self.bridge = bridge
				self.id = id
				self.name = attrs['name']
				self.swversion = attrs['swversion']
				self.manufacturename = attrs['manufacturername']
				self.state = attrs['state']
				self.uniqueid = attrs['uniqueid']
				self.modelid = attrs['modelid']
			except Exception:
				self.bridge.logger.error("Light init caught exception. probably bad json deref")
				raise
