print "Start simulator (SITL)"
import dronekit_sitl, math
sitl = dronekit_sitl.start_default()
connection_string = sitl.connection_string()
from dronekit import connect, VehicleMode,mavutil
import time
# Connect to the Vehicle.
print("Connecting to vehicle on: %s" % (connection_string,))
vehicle = connect(connection_string, wait_ready=True)

def arm_and_takeoff(aTargetAltitude):
	"""
	Arms vehicle and fly to aTargetAltitude.
	"""

	print "Basic pre-arm checks"
	# Don't try to arm until autopilot is ready
	while not vehicle.is_armable:
		print " Waiting for vehicle to initialise..."
		time.sleep(1)

	print "Arming motors"
	# Copter should arm in GUIDED mode
	vehicle.mode    = VehicleMode("GUIDED")
	vehicle.armed   = True

	# Confirm vehicle armed before attempting to take off
	while not vehicle.armed:
		print " Waiting for arming..."
		time.sleep(1)

	print "Taking off!"
	vehicle.simple_takeoff(aTargetAltitude) # Take off to target altitude

	# Wait until the vehicle reaches a safe height before processing the goto (otherwise the command
	#  after Vehicle.simple_takeoff will execute immediately).
	while True:
		print " Altitude: ", vehicle.location.global_relative_frame
		#Break and return from function just below target altitude.
		if vehicle.location.global_relative_frame.alt>=aTargetAltitude*0.95:
			print "Reached target altitude"
			break
		time.sleep(1)

def send_ned_velocity(velocity_x, velocity_y, velocity_z, duration):
	"""
	Move vehicle in direction based on specified velocity vectors.
	"""
	msg = vehicle.message_factory.set_position_target_local_ned_encode(
		0,       # time_boot_ms (not used)
		0, 0,    # target system, target component
		mavutil.mavlink.MAV_FRAME_LOCAL_NED, # frame
		0b0000111111000111, # type_mask (only speeds enabled)
		0, 0, 0, # x, y, z positions (not used)
		velocity_x, velocity_y, velocity_z, # x, y, z velocity in m/s
		0, 0, 0, # x, y, z acceleration (not supported yet, ignored in GCS_Mavlink)
		0, 0)    # yaw, yaw_rate (not supported yet, ignored in GCS_Mavlink)


	# send command to vehicle on 1 Hz cycle
	for x in range(0,duration):
		vehicle.send_mavlink(msg)
		time.sleep(1)
		print " Location: ", vehicle.location.global_relative_frame

def get_distance_metres(aLocation1, aLocation2):
	"""
	Returns the ground distance in metres between two `LocationGlobal` or `LocationGlobalRelative` objects.

	This method is an approximation, and will not be accurate over large distances and close to the
	earth's poles. It comes from the ArduPilot test code:
	https://github.com/diydrones/ardupilot/blob/master/Tools/autotest/common.py
	"""
	dlat = aLocation2.lat - aLocation1.lat
	dlong = aLocation2.lon - aLocation1.lon
	return math.sqrt((dlat*dlat) + (dlong*dlong)) * 1.113195e5

def detect_image():
	return False

arm_and_takeoff(3)
# Get Vehicle Home location - will be `None` until first set by autopilot
while not vehicle.location.global_relative_frame:
	print " Waiting for home location ..."
# We have a home location, so print it!        
print "\n Home location: %s" % vehicle.location.global_relative_frame
homeLocation = vehicle.location.global_relative_frame

print " Location: ", vehicle.location.global_relative_frame
time.sleep(2)

while (not detect_image()) and get_distance_metres(homeLocation, vehicle.location.global_relative_frame)<10:
	print "Searching: %s" % vehicle.location.global_relative_frame
	send_ned_velocity(0.5,0,0,1)

#send the location to remote pc

time.sleep(1)
vehicle.airspeed=3
vehicle.simple_goto(homeLocation)

while(get_distance_metres(homeLocation, vehicle.location.global_relative_frame)>1):
	#continue to fly until reach home location
	vehicle.simple_goto(homeLocation)
	time.sleep(3)
	print "Coming back! Location: ", vehicle.location.global_relative_frame
	continue

print "Setting LAND mode..."
print "Landing..."
vehicle.mode = VehicleMode("LAND")
time.sleep(5)
print "Landing Location: ", vehicle.location.global_relative_frame
#Close vehicle object before exiting script
print "Close vehicle object"
vehicle.close()

# Shut down simulator if it was started.
if sitl is not None:
	sitl.stop()