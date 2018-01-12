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
button = panel.add_button("Stop monitor")
button.rect_transform.position = (0, 0)

# Set up a stream to monitor the throttle button
button_clicked = conn.add_stream(getattr, button, 'clicked')
f = open(datafile, 'w')
f.write('timepoint, current_altitude, v_speed, h_speed, mass, fuel, available_thrust\n')
timepoint = 0

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
    f.write('{0}, {1}, {2}, {3}, {4}, {5}, {6}\n'.format(timepoint,
                                                         current_altitude,
                                                         v_speed, h_speed, vm, vm - dry_mass, at))
    timepoint = timepoint + 1
    time.sleep(0.1)

f.close()
button.remove()
panel.remove()
conn.close()
