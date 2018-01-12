import krpc
conn = krpc.connect(name='Hello World')
vessel = conn.space_center.active_vessel
print(vessel.name)

vessel.auto_pilot.target_pitch_and_heading(90, 90)
vessel.auto_pilot.engage()
vessel.auto_pilot.sas = True
vessel.control.throttle = 1

print('Launching!')
vessel.control.activate_next_stage()

mean_altitude = conn.get_call(getattr, vessel.flight(), 'mean_altitude')
expr = conn.krpc.Expression.greater_than(
    conn.krpc.Expression.call(mean_altitude),
    conn.krpc.Expression.constant_double(1000))
event = conn.krpc.add_event(expr)
with event.condition:
    event.wait()

print('Gravity turn')
vessel.auto_pilot.target_pitch_and_heading(60, 90)

fuel_amount = conn.get_call(vessel.resources.amount, 'SolidFuel')
expr = conn.krpc.Expression.equal(
    conn.krpc.Expression.call(fuel_amount),
    conn.krpc.Expression.constant_float(0.0))
event = conn.krpc.add_event(expr)
with event.condition:
    event.wait()

print('Detatching upper stage')
vessel.control.activate_next_stage()
vessel.auto_pilot.disengage()
vessel.auto_pilot.sas = False

srf_altitude = conn.get_call(getattr, vessel.flight(), 'surface_altitude')
expr = conn.krpc.Expression.less_than(
    conn.krpc.Expression.call(srf_altitude),
    conn.krpc.Expression.constant_double(1000))
event = conn.krpc.add_event(expr)
with event.condition:
    event.wait()

print('Deploying chute')
vessel.control.activate_next_stage()
