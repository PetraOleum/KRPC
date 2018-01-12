#! /bin/python3
# Hover vessel
import time
import krpc

# Target altitude in meters
target_altitude = 1000

# The IP of the KRPC server (if not same computer)
remote = '192.168.1.10'
# Make connection
conn = krpc.connect(name='Hover', address=remote)

# Important objects
vessel = conn.space_center.active_vessel
body = vessel.orbit.body
r_frame = body.reference_frame
print(vessel.name)

vessel.control.throttle = 0.0
vessel.control.activate_next_stage()

grav = body.surface_gravity
at = vessel.available_thrust
dry_mass = vessel.dry_mass

vessel.control.legs = False
vessel.auto_pilot.target_pitch_and_heading(90, 90)
vessel.auto_pilot.engage()
timepoint = 0

while at > 0:
    vm = vessel.mass
    minviable = (vm * grav) / at
    current_altitude = vessel.flight(r_frame).surface_altitude
    v_speed = vessel.flight(r_frame).vertical_speed
    if current_altitude > target_altitude:
        if v_speed < 0:
            vessel.control.throttle = minviable * 0.6
        else:
            vessel.control.throttle = 0
    else:
        if v_speed > 0:
            vessel.control.throttle = (2 - ((current_altitude + 20) /
                                            (target_altitude + 20))) * minviable
        else:
            vessel.control.throttle = (3 - (current_altitude / target_altitude)) * minviable
    time.sleep(0.1)
    at = vessel.available_thrust
    timepoint = timepoint + 1

conn.close()
