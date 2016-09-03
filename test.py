#!/usr/binpython
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
	except "Bad API Token":
		print("bad api token %s" % (api_token))
	except requests.exceptions.Timeout:
		print("probably bad connection to the bridge")

	# # Toggle all of the lights belonging to mywho
	# for light in mywho.lights:
	# 	light.toggle()
	# # or alternatively:
	# mywho.all_toggle()
	# # on
	# mywho.all_on()
	# # off
	# mywho.all_off()

	name = "bob"
	light_id = 1
	print("on by name: %s" % (name))
	mywho.on("bob")
	time.sleep(2)
	print("off by name: %s" % (name))
	mywho.off("bob")
	time.sleep(2)
	print("toggle by name: %s" % (name))
	mywho.toggle("bob")
	time.sleep(2)

	print("off by id: %d" % (light_id))
	mywho.off(light_id)
	time.sleep(2)

	print("on by id: %d" % (light_id))
	mywho.on(light_id)
	time.sleep(2)

	print("toggle by id: %d" % (light_id))
	mywho.toggle(light_id)
	time.sleep(2)
	bad name or ID
	try:
		mywho.on("bab")
		mywho.on(5)
	except:
		print("bad name")
		raise

	# mywho.off("bob")
	# mywho.off(1)

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
