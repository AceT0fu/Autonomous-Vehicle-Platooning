from p5 import *
import numpy as np
from boid import Boid
from model import model
from mpc import mpc
from simulator import simulator
import do_mpc
import matplotlib.pyplot as plt
import matplotlib as mpl
import numpy as np
from enum import Enum


class Stage(Enum):
    CRUISE = 1
    CHANGE = 2

stage = Stage.CRUISE

width = 1000
height = 1000
t = 0

perception = 60

lanes = 2
lane_size = 100
lane_start_x = (width / 2) - (lane_size * lanes / 2)
vehicle_start_x = lane_start_x + lane_size / 2

lane_positions = []

for i in range(lanes):
    lane_positions.append(lane_start_x + lane_size / 2 + lane_size * i)


ego_speed = 4
platoon_speed = 2

stopping_distance = 0


platoon = []

# Set the initial state of simulator:
model = model()
mpc = mpc(model)
simulator = simulator(model)

x0 = np.array([lane_positions[0], 0, lane_positions[0], 150, lane_positions[1], 300, 0, 0, 0, platoon_speed, 0, platoon_speed, 1]).reshape(-1,1) 
u0 = np.array([0, 0]).reshape(-1,1) 

platoon.append(Boid(0, width, height, ego_speed, lane_positions, x0, False))
platoon.append(Boid(0, width, height, platoon_speed, lane_positions, x0, True))
platoon.append(Boid(1, width, height, platoon_speed, lane_positions, x0, True))

simulator.x0 = x0
mpc.x0 = x0

mpc.set_initial_guess()

simulator.reset_history()
simulator.x0 = x0
mpc.reset_history()

p_x = []
p_y = []
v_x = []
v_y = []
acc_x = []
acc_y = []
costs = []
times = []

def setup():
    #this happens just once
    size(width, height) #instead of create_canvas

def draw():
    global t
    global times

    global x0
    global u0

    global acc_x
    global acc_y

    global stage

    #this happens every time
    background(30, 30, 47)

    fill(100, 100, 100)
    stroke(0, 0, 0)


    cost = 0

    if x0[12][0] == 1:
        cost = cost + x0[6][0]**2 - x0[1][0]**2
    else:
        cost = cost + x0[1][0]
        if x0[12][0] == 2:
            cost = cost - x0[6][0] ** 2
        else:
            cost = cost + x0[6][0] ** 2

    # draw lanes
    for i in range(lanes):
        rect(lane_start_x + lane_size * i, 0, lane_size, 1000)

    u0 = mpc.make_step(x0)
    x0 = simulator.make_step(u0)

    simulator.x0 = x0
    mpc.x0 = x0

    for i in range(0, len(platoon)):
        vehicle = platoon[i]

        target_vehicle = check_crash(vehicle, platoon)

        if target_vehicle:
            target_lane = (vehicle.lane + 1) % lanes

            if target_lane > vehicle.lane:
                x0[12][0] = 2
            else:
                x0[12][0] = 3


        vehicle.position = Vector(x0[2 * i][0], x0[2 * i + 1][0])
        vehicle.velocity = Vector(x0[2 * i + 6][0], x0[2 * i + 7][0])


        for j in range(len(lane_positions)):
            if vehicle.position.x >= lane_positions[j] - 33 and vehicle.position.x <= lane_positions[j] + 33:
                if j != vehicle.lane:
                    vehicle.lane = j
                    x0[12][0] = 1

        vehicle.show()


    p_x.append(x0[0][0])
    p_y.append(x0[1][0])
    v_x.append(x0[6][0])
    v_y.append(x0[7][0])

    acc_x.append(u0[0][0])
    acc_y.append(u0[1][0])

    costs.append(cost)
    times.append(t)

    t += 1

    if x0[1][0] >= 900 or x0[0][0] >= 900:
        fig, (ax0, ax1, ax2, ax3, ax4) = plt.subplots(5)
        fig.tight_layout(pad = 1.0)

        ax0.plot(p_x, p_y)
        ax0.set_ylabel("y position")
        ax0.set_xlabel("x position")
        ax0.set_title("Vehicle Position")

        ax1.plot(times, v_x)
        ax1.set_ylabel("x speed")
        ax1.set_xlabel("time")
        ax1.set_title("Lateral Velocity")

        ax2.plot(times, v_y)
        ax2.set_ylabel("y speed")
        ax2.set_xlabel("time")
        ax2.set_title("Longitudinal Velocity")

        ax3.plot(times, acc_x, color = 'r', label='x acc')
        ax3.plot(times, acc_y, color = 'g', label='y acc')
        ax3.set_ylabel("Acceleration")
        ax3.set_xlabel("time")
        ax3.set_title("Control Input")

        ax4.plot(times, costs)
        ax4.set_ylabel("Cost")
        ax4.set_xlabel("time")
        ax4.set_title("Cost Function")

        ax3.legend(loc = 'upper right')

        plt.show()
        exit()


def check_bounds(x0):
    lower_bounds = [0, 0, 0, 0]
    upper_bounds = [1000, 1000, 10, 10]

    new_states = np.zeros(4).reshape(-1, 1)

    for i in range(4):
        if x0[i] < lower_bounds[i]:
            new_states[i] = lower_bounds[i]
        elif x0[i] > upper_bounds[i]:
            new_states[i] = upper_bounds[i]
        else:
            new_states[i] = x0[i]

    return new_states


def check_crash(vehicle, platoon):
    for target in platoon:
        difference = target.position.y - vehicle.position.y
        if vehicle.lane == target.lane and difference < perception and difference > 0 and target.velocity.y <= vehicle.velocity.y:
            return target

    return None


run()