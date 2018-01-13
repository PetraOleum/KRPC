#! /bin/python3

# Modified from the script at
# http://krpc.github.io/krpc/tutorials/user-interface.html

datafile = 'flight.csv'
remote = '192.168.1.10'

import time
import krpc

conn = krpc.connect(name='Flight monitor', address=remote)
canvas = conn.ui.stock_canvas

# Get the size of the game window in pixels
screen_size = canvas.rect_transform.size

# Add a panel to contain the UI elements
panel = canvas.add_panel()

# Position the panel on the left of the screen
rect = panel.rect_transform
rect.size = (200, 50)
rect.position = (110-(screen_size[0]/2), screen_size[1]/2-75)

# Add a button to set the throttle to maximum
button = panel.add_button("Start monitor")
button.rect_transform.position = (0, 0)

# Set up a stream to monitor the throttle button
button_clicked = conn.add_stream(getattr, button, 'clicked')

# Wait for button
while button_clicked() == False:
    time.sleep(0.1)

button.remove()

# replace button
button = panel.add_button("Stop monitor")
button.rect_transform.position = (0, 0)
button_clicked = conn.add_stream(getattr, button, 'clicked')

f = open(datafile, 'w')
f.write('mission_time, current_altitude, v_speed, h_speed, mass, electric_charge, liquid_fuel, oxidizer, available_thrust, current_thrust, g_force, apoapsis, periapsis, orbital_radius, orbit_speed, orbit_period\n')

vessel = conn.space_center.active_vessel
body = vessel.orbit.body
r_frame = body.reference_frame

while button_clicked() == False:
    dry_mass = vessel.dry_mass
    vm = vessel.mass
    at = vessel.available_thrust
    current_altitude = vessel.flight(r_frame).surface_altitude
    v_speed = vessel.flight(r_frame).vertical_speed
    h_speed = vessel.flight(r_frame).horizontal_speed
    c_thrust = vessel.thrust
    e_charge = vessel.resources.amount('ElectricCharge')
    lf = vessel.resources.amount('LiquidFuel')
    ox = vessel.resources.amount('Oxidizer')
    g_force = vessel.flight(r_frame).g_force
    timept = vessel.met
    vo = vessel.orbit
    ap = vo.apoapsis_altitude
    pa = vo.periapsis_altitude
    orad = vo.radius
    os = vo.speed
    op = vo.period
    f.write('{0}, {1}, {2}, {3}, {4}, {5}, {6}, {7}, {8}, {9}, {10}, {11}, {12}, {13}, {14}, {15}\n'.format(timept, current_altitude, v_speed, h_speed, vm, e_charge, lf, ox, at, c_thrust, g_force, ap, pa, orad, os, op)) 
    time.sleep(0.1)

f.close()
button.remove()
panel.remove()
conn.close()
