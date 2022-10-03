from p5 import *
import numpy as np
from boid import Boid
from enum import Enum
import matplotlib.pyplot as plt
from model import model
from mpc import mpc
from simulator import simulator

class Stage(Enum):
    SPLIT = 1
    LATERAL = 2
    REFORM = 3
    FINISHED = 4


x_pos = []
y_pos = []
x_speed = []
y_speed = []
costs = []
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

acc_x = []
acc_y = []

stage = Stage.SPLIT
stage_i = 16

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

platoon_size = 2

model = model()
mpc = mpc(model)
simulator = simulator(model)

x0 = np.zeros(17).reshape(-1, 1)
u0 = np.zeros(4).reshape(-1, 1)

platoons = []

for i in range(2):
    platoons.append([])
    for j in range(2):
        x0[2 * (2 * i + j)][0] = lane_positions[platoon_lane + i]
        x0[2 * (2 * i + j) + 1][0] = platoon_start + vehicle_space * j

        x0[2 * (2 * i + j + 4)][0] = 0
        x0[2 * (2 * i + j + 4) + 1][0] = platoon_speed
        platoons[i].append(Boid(platoon_lane + i, platoon_start + vehicle_space * j, width, height, platoon_speed, lane_positions, True))

x0[16][0] = 1

ego_lane = 0
ego_reference = 0
target_lane = 2

ego_vehicle = platoons[ego_lane][ego_reference]
platoons[ego_lane].remove(ego_vehicle)


simulator.x0 = x0
mpc.x0 = x0

mpc.set_initial_guess()

simulator.reset_history()
simulator.x0 = x0
mpc.reset_history()


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

    global acc_x
    global acc_y

    global t 
    global times
    global stage
    global costs

    global ego_reference

    global x0
    global u0
    global mpc
    global simulator

    #this happens every time
    background(30, 30, 47)

    fill(100, 100, 100)
    stroke(0, 0, 0)

    # draw lanes
    for i in range(lanes):
        rect(lane_start_x + lane_size * i, 0, lane_size, 1000)

    cost = 0
    s = x0[stage_i][0]

    if s == 1:
        cost = cost + x0[5][0]
    else:
        cost = cost - x0[5][0]
    
    if s == 2:
        cost = cost - x0[8][0]
    else:
        cost = cost + x0[8][0]**2

    if s == 3:
        cost = cost + x0[3][0] + x0[7][0]
    else:
        cost = cost - x0[3][0] - x0[7][0]

    if s == 3 or s == 4:
        cost = cost - x0[1][0]
    else:
        cost = cost + x0[1][0]

    costs.append(cost)
    
    acc_x.append(u0[0][0])
    acc_y.append(u0[1][0])

    for i in range(len(platoons)):
        for j in range(len(platoons[i])):
            vehicle = platoons[i][j]

            vehicle.show()
            # vehicle.update()

            if i == 1 and j == 0:
                p1_x_pos.append(vehicle.position.x)
                p1_y_pos.append(vehicle.position.y)
                p1_x_speed.append(vehicle.velocity.x)
                p1_y_speed.append(vehicle.velocity.y)

            if i == 1 and j == 1:
                p2_x_pos.append(vehicle.position.x)
                p2_y_pos.append(vehicle.position.y)
                p2_x_speed.append(vehicle.velocity.x)
                p2_y_speed.append(vehicle.velocity.y)

    ego_vehicle.show()

    x_pos.append(ego_vehicle.position.x)
    y_pos.append(ego_vehicle.position.y)
    x_speed.append(ego_vehicle.velocity.x)
    y_speed.append(ego_vehicle.velocity.y)
    times.append(t)

    if ego_vehicle.position.y >= 800:
        fig, (ax0, ax1, ax2, ax4, ax3) = plt.subplots(5)
        fig.tight_layout(pad = 1.0)

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

        ax4.plot(times, acc_x, color = 'r', label='x acc')
        ax4.plot(times, acc_y, color = 'g', label='y acc')
        ax4.set_ylabel("Acceleration")
        ax4.set_xlabel("time")
        ax4.set_title("Control Input")
        ax4.legend(loc = "upper left")

        ax3.plot(times, costs)
        ax3.set_ylabel("Cost")
        ax3.set_xlabel("time")
        ax3.set_title("Cost Function")

        ax0.legend(ncol = 3)
        ax1.legend(loc = "upper left")
        ax2.legend(ncol = 3, loc = "upper left")

        plt.show()

    u0 = mpc.make_step(x0)
    x0 = simulator.make_step(u0)

    simulator.x0 = x0
    mpc.x0 = x0

    ego_vehicle.position = Vector(x0[0][0], x0[1][0])
    ego_vehicle.velocity = Vector(x0[8][0], x0[9][0])

    for i in range(0, len(platoons)):
        for j in range(0, len(platoons[i])):
            vehicle = platoons[i][j]

            vehicle.position = Vector(x0[2 * (i + j) + 2][0], x0[2 * (i + j) + 3][0])
            vehicle.velocity = Vector(x0[2 * (i + j) + 10][0], x0[2 * (i + j) + 11][0])


    if stage == Stage.SPLIT:
        for i in range(len(platoons)):
            if i != ego_lane:
                if platoons[i][ego_reference + 1].position.y - platoons[i][ego_reference].position.y >= vehicle_space * 2:

                    x0[stage_i][0] = 2
                    simulator.x0 = x0
                    mpc.x0 = x0
                    stage = Stage.LATERAL


    if stage == Stage.LATERAL:
        current_lane = ego_vehicle.lane

        if target_lane > current_lane:
            speed = 2
        else:
            speed = -2
        
        ego_vehicle.velocity = Vector(speed, vehicle.velocity.y)

        if ego_vehicle.position.x >= lane_positions[target_lane] - 30 and ego_vehicle.position.x <= lane_positions[target_lane] + 30:
            ego_vehicle.lane = target_lane
            ego_vehicle.platoon = False

            stage = Stage.REFORM
            x0[stage_i][0] = 3
            simulator.x0 = x0
            mpc.x0 = x0


    if stage == Stage.REFORM:
        for i in range(len(platoons)):
            missing_car = 0
            if i != ego_lane:

                if platoons[i][ego_reference - 1 + missing_car].position.y - platoons[i][ego_reference + missing_car].position.y <= vehicle_space:

                    stage = Stage.FINISHED
                    x0[stage_i][0] = 4
                    simulator.x0 = x0
                    mpc.x0 = x0

    t += 1


run()