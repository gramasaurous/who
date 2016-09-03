#!/usr/bin/env python
import sys
import requests
import who
import time

# Simple test cases to outline how the interface should work
# and to test the individual methods
def test_harness(bridge_ip, api_token):
	# Initialize a who instance
	# first arg is the IP of the hue bridge
	# second arg is the api token generated (in the future, if this is blank,
	# the interface can generate one)
	try:
		mywho = who.Who(bridge_ip, api_token)
		print(mywho)
	except requests.exceptions.Timeout:
		print("probably bad connection to the bridge")
	except Exception:
		print("bad api token %s" % (api_token))
		raise

	# # Toggle all of the lights belonging to mywho
	# for light in mywho.lights:
	# 	light.toggle()
	# # or alternatively:
	# mywho.all_toggle()
	# # on
	# mywho.all_on()
	# # off
	# mywho.all_off()

	delay = 1
	name = "bob"
	light_id = 1
	print("on by name: %s" % (name))
	mywho.on("bob")
	time.sleep(delay)
	print("off by name: %s" % (name))
	mywho.off("bob")
	time.sleep(delay)
	print("toggle by name: %s" % (name))
	mywho.toggle("bob")
	time.sleep(delay)

	print("off by id: %d" % (light_id))
	mywho.off(light_id)
	time.sleep(delay)

	print("on by id: %d" % (light_id))
	mywho.on(light_id)
	time.sleep(delay)

	print("toggle by id: %d" % (light_id))
	mywho.toggle(light_id)
	time.sleep(delay)
	#bad name or ID
	try:
		mywho.on("bab")
	except KeyError:
		print("on: bad name")
	try:
		mywho.on(5)
	except IndexError:
		print("on: bad id")
	try:
		mywho.off("bab")
	except KeyError:
		print("off: bad name")
	try:
		mywho.off(5)
	except IndexError:
		print("off: bad id")
	try:
		mywho.toggle("bab")
	except KeyError:
		print("toggle: bad name")
	try:
		mywho.toggle(5)
	except IndexError:
		print("toggle: bad id")
	# # force an update of the bridge state
	# mywho.update() 
	# # force an update of all the lights state
	# mywho.all_update()

if __name__ == '__main__':
	if len(sys.argv) != 3:
		print("Error. Useage: test.py bridge_ip api_token")
		sys.exit(-1)
	bridge_ip = sys.argv[1]
	api_token = sys.argv[2]
	test_harness(bridge_ip, api_token)
