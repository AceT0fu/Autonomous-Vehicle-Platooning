from p5 import *
import numpy as np
from boid import Boid
from enum import Enum
import matplotlib.pyplot as plt
from model import model
from mpc import mpc
from simulator import simulator

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

acc_x_1 = []
acc_y_1 = []


costs = []

stage_i = 12
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
platoon_size = 2

model = model()
mpc = mpc(model)
simulator = simulator(model)

x0 = np.zeros(13).reshape(-1, 1)
u0 = np.zeros(6).reshape(-1,1) 

x0[0][0] = lane_positions[0] # ego pos x
x0[1][0] = 0 # ego pos y

x0[6][0] = 0 # ego speed x
x0[7][0] = 0 # ego speed y

ego_vehicles = []
ego_vehicles.append(Boid(0, 0, width, height, ego_speed, lane_positions, False))

ego_references = [1]

platoon = []

for i in range(platoon_size):
    x0[2 * (i + 1)][0] = lane_positions[platoon_lane]
    x0[2 * (i + 1) + 1][0] = platoon_start + vehicle_space * i

    x0[2 * (i + 4)][0] = 0
    x0[2 * (i + 4) + 1][0] = platoon_speed

    platoon.append(Boid(platoon_lane, platoon_start + vehicle_space * i, width, height, platoon_speed, lane_positions, True))

x0[stage_i][0] = 1

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

    global acc_x_1
    global acc_x_2
    global acc_x_3

    global acc_y_1
    global acc_y_2
    global acc_y_3

    global t 
    global times
    global stage

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

    cost = - x0[5][0] **2

    s = x0[stage_i][0]

    if s == 1:
        cost = cost - x0[1][0]**2
    else:
        cost = cost + x0[1][0]**2

    if s == 2:
        cost = cost + x0[3][0]**2
    else:
        cost = cost - x0[3][0]**2

    if s == 3:
        cost = cost - x0[6][0]**2
    else:
        cost = cost + x0[6][0]**2
    
    costs.append(cost)

    acc_x_1.append(u0[0][0])
    acc_y_1.append(u0[1][0])

    for i in range(len(platoon)):
        vehicle = platoon[i]

        platoon_start = platoon[0].position.y

        if i == 0:
            p1_x_pos.append(vehicle.position.x)
            p1_y_pos.append(vehicle.position.y)
            p1_x_speed.append(vehicle.velocity.x)
            p1_y_speed.append(vehicle.velocity.y)

        if i == 1:
            p2_x_pos.append(vehicle.position.x)
            p2_y_pos.append(vehicle.position.y)
            p2_x_speed.append(vehicle.velocity.x)
            p2_y_speed.append(vehicle.velocity.y)

    for vehicle in ego_vehicles:

        x_pos.append(vehicle.position.x)
        y_pos.append(vehicle.position.y)
        x_speed.append(vehicle.velocity.x)
        y_speed.append(vehicle.velocity.y)
        times.append(t)

        if vehicle.position.y >= 500:
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

            ax4.plot(times, acc_x_1, color='r', label='x acc')
            ax4.plot(times, acc_y_1, color='g', label='y acc')
            ax4.set_ylabel("Acceleration")
            ax4.set_xlabel("time")
            ax4.set_title("Control Input")
            ax4.legend()

            ax3.plot(times, costs)
            ax3.set_ylabel("Cost")
            ax3.set_xlabel("time")
            ax3.set_title("Cost Function")

            ax0.legend(ncol = 3)
            ax1.legend(loc = "upper left")
            ax2.legend(ncol = 3)

            plt.show()


    ego_vehicle = ego_vehicles[0]
    ego_reference = ego_references[0]

    u0 = mpc.make_step(x0)
    x0 = simulator.make_step(u0)

    simulator.x0 = x0
    mpc.x0 = x0

    ego_vehicle.position = Vector(x0[0][0], x0[1][0])
    ego_vehicle.velocity = Vector(x0[6][0], x0[7][0])

    ego_vehicle.show()

    for i in range(0, len(platoon)):
        vehicle = platoon[i]

        vehicle.position = Vector(x0[2 * (i + 1)][0], x0[2 * (i + 1) + 1][0])
        vehicle.velocity = Vector(x0[2 * (i + 4)][0], x0[2 * (i + 4) + 1][0])

        vehicle.show()


    if stage == Stage.LONGITUDINAL:

        if ego_reference == len(platoon):
            # if vehicle wants to merge to front of platoon, would be more efficient to take an extra step forward
            reference = platoon_start + ego_reference  * vehicle_space
        else:
            reference = platoon_start + (ego_reference - 1) * vehicle_space - 10

        if ego_vehicle.position.y >= reference:
            
            stage = Stage.SPLIT
            x0[stage_i][0] = 2
            simulator.x0 = x0
            mpc.x0 = x0

    if stage == Stage.SPLIT:
        if platoon[ego_reference].position.y - platoon[ego_reference - 1].position.y >= vehicle_space * 2:

            stage = Stage.LATERAL
            x0[stage_i][0] = 3
            simulator.x0 = x0
            mpc.x0 = x0


    if stage == Stage.LATERAL:

        if ego_vehicle.position.x >= lane_positions[platoon_lane] - 35 and ego_vehicle.position.x <= lane_positions[platoon_lane] + 35:

            #merge successful
            ego_vehicle.lane = platoon_lane
            ego_vehicle.platoon = True

            stage = Stage.FINISHED
            x0[stage_i][0] = 4
            simulator.x0 = x0
            mpc.x0 = x0



    t += 1

run()