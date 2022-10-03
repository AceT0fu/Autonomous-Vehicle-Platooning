from p5 import *
import numpy as np
from sqlalchemy import true
from boid import Boid
import matplotlib.pyplot as plt

width = 1000
height = 1000

perception = 60

lanes = 2
lane_size = 100
lane_start_x = (width / 2) - (lane_size * lanes / 2)
vehicle_start_x = lane_start_x + lane_size / 2

lane_positions = []

for i in range(lanes):
    lane_positions.append(lane_start_x + lane_size / 2 + lane_size * i)

# flock = [Boid(*np.random.rand(2)*1000, width, height) for _ in range(30)]

platoon = []
platoon.append(Boid(0, 0, width, height, 4, lane_positions, True))
platoon.append(Boid(0, 150, width, height, 2, lane_positions, False))
platoon.append(Boid(1, 300, width, height, 2, lane_positions, False))

x_pos = []
y_pos = []
x_speed = []
y_speed = []
t = 0
times = []

def setup():
    #this happens just once
    size(width, height) #instead of create_canvas


def draw():
    global x_pos
    global y_pos
    global x_speed
    global y_speed
    global t 
    global times

    #this happens every time
    background(30, 30, 47)

    fill(100, 100, 100)
    stroke(0, 0, 0)

    # draw lanes
    for i in range(lanes):
        rect(lane_start_x + lane_size * i, 0, lane_size, 1000)

    for vehicle in platoon:
        vehicle.show()
        apply_behaviour(vehicle, platoon)
        vehicle.update()

        # graph generation
        ##################################

        if vehicle.ego:
            
            x_pos.append(vehicle.position.x)
            y_pos.append(vehicle.position.y)
            x_speed.append(vehicle.velocity.x)
            y_speed.append(vehicle.velocity.y)
            times.append(t)

            if vehicle.position.y == 1000:
                fig, (ax0, ax1, ax2) = plt.subplots(3)
                fig.tight_layout(pad = 2.0)

                ax0.plot(x_pos, y_pos)
                ax0.set_ylabel("y position")
                ax0.set_xlabel("x position")
                ax0.set_title("Vehicle Position")

                ax1.plot(times, x_speed)
                ax1.set_ylabel("x speed")
                ax1.set_xlabel("time")
                ax1.set_title("Lateral Velocity")

                ax2.plot(times, y_speed)
                ax2.set_ylabel("y speed")
                ax2.set_xlabel("time")
                ax2.set_title("Longitudinal Velocity")

                plt.show()

    t += 1

    ########################


def check_crash(vehicle, platoon):
    for target in platoon:
        difference = target.position.y - vehicle.position.y
        if vehicle.lane == target.lane and difference < perception and difference > 0 and target.velocity.y <= vehicle.velocity.y:
            return target

    return None


def change_lane(vehicle, platoon):
    current_lane = vehicle.lane
    target_lane = (current_lane + 1) % lanes

    if target_lane > current_lane:
        speed = 2
    else:
        speed = -2
    
    vehicle.velocity = Vector(speed, vehicle.velocity.y)


def apply_behaviour(vehicle, platoon):
    for i in range(len(lane_positions)):
        if vehicle.position.x == lane_positions[i]:
            vehicle.lane = i

    target_vehicle = check_crash(vehicle, platoon)

    if target_vehicle:
        vehicle.velocity = target_vehicle.velocity
        change_lane(vehicle, platoon)
    else: 
        vehicle.velocity = Vector(0, vehicle.max_speed)

run()