#!/usr/bin/env python

# Graham Greving
# grahamgreving@gmail.com
# 09/02/2016
# Simple Python interface for Hue lights

# import logging
import urequests as requests
import json

# who class defines a connection to a specific hue device and its lights
class Who:
	def __repr__(self):
		string = self.ip + "\n"
		for l in self.lights:
			string += "\t %s \n" % (l)
		return string

	def __init__(self, bridge_ip, api_token, logger=None):
		# self.logger = logger or logging.getLogger(__name__)
		self.ip = bridge_ip
		self.api_token = api_token
		self.lights = []
		# get_lights() is where connection to bridge is attempted
		# and will throw an appropriate exception if something goes wrong
		# see get_lights() for documentation
		self.get_lights()

	# search lights by name
	# raises a KeyError exception if not found
	# names are unique, so returns first found
	def find_light(self, name):
		found = False
		for l in self.lights:
			if l.name == name:
				found = True
				return l
		if not found:
			# self.logger.warn("Light not found %s" % (name))
			raise KeyError

	# establishes a connection to the bridge and retrieves list of connected
	# lights.
	def get_lights(self):
		try:
			url = "http://" + self.ip + "/api/" + self.api_token + "/lights"
			r = requests.get(url)
			#r.raise_for_status()
			if r.status_code != 200:
				raise Exception
			lights = r.json()
			# on error r.json() returns a list containing a dict
			# on success, r.json() just returns a dict
			if type(lights) == list and lights[0]['error']:
				# self.logger.error("Bad API token")
				# raise Exception, "Bad API token"
				raise Exception
			for light_id in lights:
				self.lights.append(self.Light(self, light_id, lights[light_id]))
		#except requests.exceptions.HTTPError:
			# self.logger.error("Get Lights Request recieved error code: " + r.status_code)
		#	raise
		#except requests.exceptions.Timeout:
			# self.logger.exception("Connection to bridge timed out")
		#	raise
		except Exception:
			# self.logger.exception("Get Lights Request Caught Exception")
			raise

	# on/off/toggle work by light_id (ing) or by name (string)
	def on(self, light):
		try:
			self.lights[light].change_state("on")
		except TypeError:
			self.find_light(light).change_state("on")
		except IndexError:
			# self.logger.exception("Bad light id")
			raise

	def off(self, light):
		try:
			self.lights[light].change_state("off")
		except TypeError:
			self.find_light(light).change_state("off")
		except IndexError:
			# self.logger.exception("Bad light id")
			raise

	def toggle(self, light):
		try:
			self.lights[light].change_state("toggle")
		except TypeError:
			self.find_light(light).change_state("toggle")
		except IndexError:
			# self.logger.exception("Bad light id")
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
				self.payload = {'on': self.state['on']}
				self.url = "http://%s/api/%s/lights/%s/state" % (self.bridge.ip, self.bridge.api_token, self.id)
				self.data = json.dumps(self.payload)
				self.res = requests.Response()
			except Exception:
				# self.bridge.logger.error("Light init caught exception. probably bad json deref")
				raise

		# need to make this callback proof 
		# - no memory allocation
		# short and simple might want to create a separate callback
		def change_state(self, state='toggle'):
			if state == 'toggle':
				self.payload['on'] = not self.state['on']
			elif state == 'on':
				self.payload['on'] = True
			elif state == 'off':
				self.payload['on'] = False
			else:
				# raise Exception, "Invalid state."
				raise Exception
			# payload = {'on': new_state}
			try:
				# url = "http://%s/api/%s/lights/%d/state" % (self.bridge.ip, self.api_token, self.id)
				# url = "http://" + self.bridge.ip + "/api/" + self.bridge.api_token + "/lights/" + self.id + "/state"
				self.res = requests.put(self.url, self.data)
				#r.raise_for_status()
				if self.res.status_code != 200:
					raise Exception
				# ret = r.json()[0]
				if not self.res.json()[0]['success']:
					# self.bridge.logger.error("Update state failed.")
					# raise Exception, "Update state failed."
					raise Exception
				else:
					self.state['on'] = self.payload['on']
			except Exception:
				# self.bridge.logger.exception("Change State Request Caught exception. %(url)s %(payload)s")
				raise
