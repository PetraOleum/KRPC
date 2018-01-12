#! /bin/python3
# A script that flies a plane
import time
import krpc

# The IP of the KRPC server (if not same computer)
remote = '192.169.1.10'
conn = krpc.connect(name='Plane autopilot', address=remote)
vessel = conn.space_center.active_vessel
body = vessel.orbit.body
r_frame = body.reference_frame
print(vessel.name)
vessel.control.brakes = True

vessel.auto_pilot.target_pitch_and_heading(0, 90)
vessel.auto_pilot.engage()
#vessel.auto_pilot.sas = True
vessel.control.throttle = 1

print('Launching!')
vessel.control.activate_next_stage()
time.sleep(3)
vessel.control.brakes = False

surf_vel = conn.get_call(getattr, vessel.flight(r_frame), 'horizontal_speed')

expr = conn.krpc.Expression.greater_than(
    conn.krpc.Expression.call(surf_vel),
    conn.krpc.Expression.constant_double(60))
event = conn.krpc.add_event(expr)
with event.condition:
    event.wait()

print('Tilt up')
vessel.auto_pilot.target_pitch_and_heading(20, 90)

srf_altitude = conn.get_call(getattr, vessel.flight(), 'surface_altitude')

expr = conn.krpc.Expression.greater_than(
    conn.krpc.Expression.call(srf_altitude),
    conn.krpc.Expression.constant_double(40))
event = conn.krpc.add_event(expr)
with event.condition:
    event.wait()

print('Gear up')
vessel.control.gear = False

expr = conn.krpc.Expression.greater_than(
    conn.krpc.Expression.call(surf_vel),
    conn.krpc.Expression.constant_double(200))
event = conn.krpc.add_event(expr)
with event.condition:
    event.wait()

print('glide')
vessel.auto_pilot.target_pitch_and_heading(5, 90)
vessel.control.throttle = 0.20
time.sleep(35)

vessel.control.roll = 0.03
vessel.auto_pilot.target_pitch_and_heading(5, 120)
time.sleep(8)
vessel.auto_pilot.target_pitch_and_heading(5, 180)
time.sleep(8)
vessel.auto_pilot.target_pitch_and_heading(5, 210)
time.sleep(8)
vessel.auto_pilot.target_pitch_and_heading(2, 270)
time.sleep(8)
vessel.control.roll = 0.00
vessel.control.throttle = 0
vessel.auto_pilot.target_pitch_and_heading(-15, 270)

expr = conn.krpc.Expression.less_than(
    conn.krpc.Expression.call(srf_altitude),
    conn.krpc.Expression.constant_double(300))
event = conn.krpc.add_event(expr)
with event.condition:
    event.wait()

vessel.auto_pilot.target_pitch_and_heading(2, 270)
vessel.control.gear = True

expr = conn.krpc.Expression.less_than(
    conn.krpc.Expression.call(srf_altitude),
    conn.krpc.Expression.constant_double(30))
event = conn.krpc.add_event(expr)
with event.condition:
    event.wait()

vessel.auto_pilot.target_pitch_and_heading(14, 270)

time.sleep(5)

vert_vel = conn.get_call(getattr, vessel.flight(r_frame),
                         'vertical_speed')

expr = conn.krpc.Expression.less_than(
    conn.krpc.Expression.call(vert_vel),
    conn.krpc.Expression.constant_double(0))
event = conn.krpc.add_event(expr)
with event.condition:
    event.wait()

vessel.auto_pilot.target_pitch_and_heading(5, 270)

vessel.control.brakes = True


conn.close()
