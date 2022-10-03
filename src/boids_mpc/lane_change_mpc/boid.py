from p5 import *
import numpy as np

class Boid():

    def __init__(self, lane, width, height, velocity, lane_positions, x0, platoon):
        self.lane = lane
        self.position = Vector(lane_positions[lane], x0[1][0])
        self.width = width
        self.height = height

        self.max_speed = velocity

        self.velocity = Vector(0, velocity)
        self.acceleration = Vector(0, 0)

        self.changing = False

        self.platoon = platoon

    

    def show(self):
        if self.platoon:
            stroke(255)
            fill(255)
        else:
            stroke(255, 0, 0)
            fill(255, 0, 0)
        circle((self.position.x, self.position.y), 35)


    def update(self):
        self.position += self.velocity
        self.velocity += self.acceleration

        if self.position.x > self.width:
            self.position.x = 0
        elif self.position.x < 0:
            self.position.x = self.width

        if self.position.y > self.height:
            self.position.y = 0
        elif self.position.y < 0:
            self.position.y = self.height
            

    def setSpeed(self, velocity):
        if velocity.y > self.max_speed:
            self.velocity = Vector(0, self.max_speed)
        else:
            self.velocity = velocity


        print("SPEED IS " + str(velocity.y))
