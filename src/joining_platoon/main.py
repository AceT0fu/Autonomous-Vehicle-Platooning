from p5 import *
import numpy as np
from boid import Boid
from enum import Enum
import matplotlib.pyplot as plt

class Stage(Enum):
    LONGITUDINAL = 1
    SPLIT = 2
    LATERAL = 3
    FINISHED = 4

x_pos = []
y_pos = []
x_speed = []
y_speed = []
t = 0
times = []

p1_x_pos = []
p1_y_pos = []
p1_x_speed = []
p1_y_speed = []

p2_x_pos = []
p2_y_pos = []
p2_x_speed = []
p2_y_speed = []


stage = Stage.LONGITUDINAL

width = 1000
height = 1000

perception = 0

lanes = 2
lane_size = 100
lane_start_x = (width / 2) - (lane_size * lanes / 2)

lane_positions = []

for i in range(lanes):
    lane_positions.append(lane_start_x + lane_size / 2 + lane_size * i)

platoon_speed = 2
ego_speed = 4

vehicle_space = 50  # space taken up by each vehicle in the platoon
platoon_start = 100 # y coordinate of platoon start
platoon_lane = 1

platoon = []

for i in range(2):
    platoon.append(Boid(platoon_lane, platoon_start + vehicle_space * i, width, height, platoon_speed, lane_positions, True))

ego_vehicles = []
ego_vehicles.append(Boid(0, 0, width, height, ego_speed, lane_positions, False))

ego_references = [1]


def setup():
    #this happens just once
    size(width, height) #instead of create_canvas


def draw():
    global x_pos
    global y_pos
    global x_speed
    global y_speed

    global p1_x_pos
    global p1_y_pos
    global p1_x_speed
    global p1_y_speed

    global p2_x_pos
    global p2_y_pos
    global p2_x_speed
    global p2_y_speed

    global t 
    global times
    global stage

    #this happens every time
    background(30, 30, 47)

    fill(100, 100, 100)
    stroke(0, 0, 0)

    # draw lanes
    for i in range(lanes):
        rect(lane_start_x + lane_size * i, 0, lane_size, 1000)

    # graph generation
    ############################################
    for i in range(len(platoon)):
        vehicle = platoon[i]

        vehicle.show()
        vehicle.update()

        platoon_start = platoon[0].position.y

        if i == 2:
            p1_x_pos.append(vehicle.position.x)
            p1_y_pos.append(vehicle.position.y)
            p1_x_speed.append(vehicle.velocity.x)
            p1_y_speed.append(vehicle.velocity.y)

        if i == 3:
            p2_x_pos.append(vehicle.position.x)
            p2_y_pos.append(vehicle.position.y)
            p2_x_speed.append(vehicle.velocity.x)
            p2_y_speed.append(vehicle.velocity.y)

    for vehicle in ego_vehicles:
        vehicle.show()
        vehicle.update()

        x_pos.append(vehicle.position.x)
        y_pos.append(vehicle.position.y)
        x_speed.append(vehicle.velocity.x)
        y_speed.append(vehicle.velocity.y)
        times.append(t)

        if vehicle.position.y == 500:
            fig, (ax0, ax1, ax2) = plt.subplots(3)
            fig.tight_layout(pad = 2.0)

            ax0.plot(x_pos, y_pos, color='r', label='ego')
            ax0.plot(p1_x_pos, p1_y_pos, '--', label='behind')
            ax0.plot(p2_x_pos, p2_y_pos, '--', color='g', label='infront')
            ax0.set_ylabel("y position")
            ax0.set_xlabel("x position")
            ax0.set_title("Vehicle Position")

            ax1.plot(times, x_speed, color='r', label='ego')
            ax1.plot(times, p1_x_speed, '--', label='behind')
            ax1.plot(times, p2_x_speed, '--', color='g', label='infront')
            ax1.set_ylabel("x speed")
            ax1.set_xlabel("time")
            ax1.set_title("Lateral Velocity")

            ax2.plot(times, y_speed, color='r', label='ego')
            ax2.plot(times, p1_y_speed, '--', label='behind')
            ax2.plot(times, p2_y_speed, '--', color='g', label='infront')
            ax2.set_ylabel("y speed")
            ax2.set_xlabel("time")
            ax2.set_title("Longitudinal Velocity")

            ax0.legend(ncol = 3)
            ax1.legend(loc = "lower left")
            ax2.legend(ncol = 3)

            plt.show()

    ############################################

    # find reference

    ego_vehicle = ego_vehicles[0]
    ego_reference = ego_references[0]

    if stage == Stage.LONGITUDINAL:
        if ego_reference == len(platoon):
            # if vehicle wants to merge to front of platoon, would be more efficient to take an extra step forward
            reference = platoon_start + ego_reference * vehicle_space
        else:
            reference = platoon_start + (ego_reference - 1) * vehicle_space

        if ego_vehicle.position.y == reference:
            ego_vehicle.velocity = Vector(0, platoon_speed) # slow down to speed of platoon
            if ego_reference == 0 or ego_reference == len(platoon):
                stage = Stage.LATERAL # don't need to split if merging to the front or back
            else:
                stage = Stage.SPLIT

    if stage == Stage.SPLIT:
        for i in range(ego_reference):
            platoon[i].velocity = Vector(0, platoon_speed / 2) # cars behind reference slow down to split
        
        if platoon[ego_reference].position.y - platoon[ego_reference - 1].position.y == vehicle_space * 2:
            for i in range(ego_reference):
                platoon[i].velocity = Vector(0, platoon_speed) # space is created so cars return to platoon speed

            stage = Stage.LATERAL

    if stage == Stage.LATERAL:
        current_lane = ego_vehicle.lane

        # lane change
        if platoon_lane > current_lane:
            speed = 2
        else:
            speed = -2
        
        ego_vehicle.velocity = Vector(speed, vehicle.velocity.y)

        if ego_vehicle.position.x == lane_positions[platoon_lane]:
            #merge successful
            ego_vehicle.velocity = Vector(0, platoon_speed)
            ego_vehicle.lane = platoon_lane
            ego_vehicle.platoon = True

    t += 1

run()