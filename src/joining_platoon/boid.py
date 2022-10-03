from p5 import *
import numpy as np

class Boid():

    def __init__(self, lane, y, width, height, velocity, lane_positions, platoon):
        self.lane = lane
        self.position = Vector(lane_positions[lane], y)
        self.width = width
        self.height = height

        self.max_speed = velocity
        self.max_force = 1

        self.platoon = platoon

        # velocity = (np.random.rand(2) - 0.5) * 10
        # acceleration = (np.random.rand(2) - 0.5) / 2
        # self.acceleration = Vector(*acceleration)

        self.velocity = Vector(0, velocity)
        self.acceleration = Vector(0, 0)


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

        # if np.linalg.norm(self.velocity) > self.max_speed:
        #     self.velocity = self.velocity / np.linalg.norm(self.velocity) * self.max_speed

        #     self.acceleration = Vector(*np.zeros(2))

        if self.position.x > self.width:
            self.position.x = 0
        elif self.position.x < 0:
            self.position.x = self.width

        if self.position.y > self.height:
            self.position.y = 0
        elif self.position.y < 0:
            self.position.y = self.height
    
    # def align(self, boids):
    #     steering = Vector(*np.zeros(2))
    #     total = 0
    #     avg_vec = Vector(*np.zeros(2))

    #     for boid in boids:
    #         if np.linalg.norm(boid.position - self.position) < self.perception:
    #             avg_vec += boid.velocity
    #             total += 1

    #     if total > 0:
    #         avg_vec /= total
    #         avg_vec = Vector(*avg_vec)
    #         avg_vec = (avg_vec /np.linalg.norm(avg_vec)) * self.max_speed
    #         steering = avg_vec - self.velocity

    #     return steering


    # def separation(self, boids):
    #     steering = Vector(*np.zeros(2))
    #     total = 0
    #     avg_vector = Vector(*np.zeros(2))

    #     for boid in boids:
    #         distance = np.linalg.norm(boid.position - self.position)
    #         if self.position != boid.position and distance < self.perception:
    #             diff = self.position - boid.position
    #             diff /= distance
    #             avg_vector += diff
    #             total += 1

    #     if total > 0:
    #         avg_vector /= total
    #         avg_vector = Vector(*avg_vector)

    #         if np.linalg.norm(steering) > 0:
    #             avg_vector = (avg_vector / np.linalg.norm(steering)) * self.max_speed
    #         steering = avg_vector - self.velocity

    #         if np.linalg.norm(steering)> self.max_force:
    #             steering = (steering /np.linalg.norm(steering)) * self.max_force

    #     return steering