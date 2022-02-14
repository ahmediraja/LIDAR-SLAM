
import math
import pygame
import numpy as np

def uncertainty_add(distance, angle, sigma):
    mean = np.array([distance, angle])
    covariance = np.diag(sigma**2)
    distance, angle = np.random.multivariate_normal(mean, covariance)
    distance = max(distance, 0) # cant be negative, correct to 0 if needed
    angle = max(angle, 0) # cant be negative, correct to 0 if needed
    return [distance, angle]




class LaserSensor:
    def __init__(self, range, map, uncertainty):
        self.range = range
        self.speed = 5 # samples per second
        self.sigma = np.array([uncertainty[0], uncertainty[1]])
        self.position = (0, 0) # top-right of screen
        self.map = map
        self.w, self.h = pygame.display.get_surface().get_size()
        self.sensedObstacles = []
    
    # distance calc using pythagorean theorem
    def distance(self, obstaclePosition):
        px=(obstaclePosition[0]-self.position[0])**2
        py=(obstaclePosition[1]-self.position[1])**2
        return math.sqrt(px+py)

    def sense_obstacles(self):
        data = []
        x1, y1 = self.position[0], self.position[1]
        numSamples = 60 # number of samples in a full circle rotation
        for angle in np.linspace(0, 2*math.pi, 60, False):
            x2, y2 = (x1 + self.range * math.cos(angle), y1 - self.range * math.sin(angle))
            for i in range(0,100):
                u = i / 100
                x = int(x2*u + x1*(1-u))
                y = int(y2*u + y1*(1-u))
                if (0<x<self.w and 0<y<self.h):
                    color = self.map.get_at((x,y))
                    if (color[0], color[1], color[2]) == (0,0,0): # if obstacle detected
                        distance = self.distance((x,y))
                        output = uncertainty_add(distance, angle, self.sigma) # making it more realistic with errors
                        output.append(self.position)
                        data.append(output) # store the measurements
                        break # no need to continue with this laser since obstacle was detected

        if len(data) > 0:
            return data
        else:
            return False
