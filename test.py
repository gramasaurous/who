#!/usr/binpython
import sys
import who

# Simple test cases to outline how the interface should work
# and to test the individual methods
def test_harness(bridge_ip, api_token):
	# Initialize a who instance
	# first arg is the IP of the hue bridge
	# second arg is the api token generated (in the future, if this is blank,
	# the interface can generate one)
	mywho = Who(bridge_ip, api_token)

	# Toggle all of the lights belonging to mywho
	for light in mywho.lights:
		light.toggle()
	# or alternatively:
	mywho.all_toggle()
	# on
	mywho.all_on()
	# off
	mywho.all_off()

	# Toggle a single light by name
	mywho.toggle("bob")

	# Toggle a single light by id
	mywho.toggle(1)

	# Turn on/off a single light
	mywho.on("bob")
	mywho.on(1)
	mywho.off("bob")
	mywho.off(1)

	# force an update of the bridge state
	mywho.update() 
	# force an update of all the lights state
	mywho.all_update()

if __name__ == '__main__':
	if len(sys.argv) != 3:
		print("Error. Useage: test.py bridge_ip api_token")
		sys.exit(-1)
	bridge_ip = sys.argv[1]
	api_token = sys.argv[2]
	test_harness(bridge_ip, api_token)
