from p5 import *
import numpy as np
from boid import Boid
from enum import Enum
import matplotlib.pyplot as plt

class Stage(Enum):
    SPLIT = 1
    LATERAL = 2
    REFORM = 3
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

stage = Stage.SPLIT

width = 1000
height = 1000

perception = 0

lanes = 3
lane_size = 100
lane_start_x = (width / 2) - (lane_size * lanes / 2)

lane_positions = []

for i in range(lanes):
    lane_positions.append(lane_start_x + lane_size / 2 + lane_size * i)

platoon_speed = 2
ego_speed = 4

vehicle_space = 50  # space taken up by each vehicle in the platoon
platoon_start = 100 # y coordinate of platoon start
platoon_lane = 0

platoons = []

for i in range(2):
    platoons.append([])
    for j in range(2):
        platoons[i].append(Boid(platoon_lane + i, platoon_start + vehicle_space * j, width, height, platoon_speed, lane_positions, True))

ego_lane = 0
ego_reference = 0
target_lane = 2

ego_vehicle = platoons[ego_lane][ego_reference]
platoons[ego_lane].remove(ego_vehicle)


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

    for i in range(len(platoons)):
        for j in range(len(platoons[i])):
            vehicle = platoons[i][j]

            vehicle.show()
            vehicle.update()

            # graph generation
            ##################################

            if i == 1 and j == 2:
                p1_x_pos.append(vehicle.position.x)
                p1_y_pos.append(vehicle.position.y)
                p1_x_speed.append(vehicle.velocity.x)
                p1_y_speed.append(vehicle.velocity.y)

            if i == 1 and j == 3:
                p2_x_pos.append(vehicle.position.x)
                p2_y_pos.append(vehicle.position.y)
                p2_x_speed.append(vehicle.velocity.x)
                p2_y_speed.append(vehicle.velocity.y)

    ego_vehicle.show()
    ego_vehicle.update()

    x_pos.append(ego_vehicle.position.x)
    y_pos.append(ego_vehicle.position.y)
    x_speed.append(ego_vehicle.velocity.x)
    y_speed.append(ego_vehicle.velocity.y)
    times.append(t)

    if ego_vehicle.position.y >= 800:
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

    ######################################

    if stage == Stage.SPLIT:
        for i in range(len(platoons)):
            if i != ego_lane:
                # vehicles behind ego slow down
                for j in range(ego_reference + 1):
                    platoons[i][j].velocity = Vector(0, platoon_speed / 2)

                # check gap created
                if platoons[i][ego_reference + 1].position.y - platoons[i][ego_reference].position.y == vehicle_space * 2:
                    for j in range(ego_reference + 1):
                        # resume platoon speed
                        platoons[i][j].velocity = Vector(0, platoon_speed)

                    stage = Stage.LATERAL


    if stage == Stage.LATERAL:
        # lane change
        current_lane = ego_vehicle.lane

        if target_lane > current_lane:
            speed = 2
        else:
            speed = -2
        
        ego_vehicle.velocity = Vector(speed, vehicle.velocity.y)

        if ego_vehicle.position.x == lane_positions[target_lane]:
            ego_vehicle.velocity = Vector(0, ego_speed)
            ego_vehicle.lane = target_lane
            ego_vehicle.platoon = False

            stage = Stage.REFORM


    if stage == Stage.REFORM:
        for i in range(len(platoons)):
            missing_car = 0
            if i != ego_lane:
                missing_car = 1
            for j in range(ego_reference + missing_car, len(platoons[i])):
                # slow down for merge
                platoons[i][j].velocity = Vector(0, platoon_speed / 2)

            if platoons[i][ego_reference + missing_car].position.y - platoons[i][ego_reference - 1 + missing_car].position.y == vehicle_space:
                for x in range(len(platoons)):
                    for j in range(0, len(platoons[x])):
                        # resume platoon speed
                        platoons[x][j].velocity = Vector(0, platoon_speed)

                    stage = stage.FINISHED

    t += 1

run()