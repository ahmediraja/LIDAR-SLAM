import math
import pygame

class buildEnvironment:
    def __init__(self, MapDimensions):
        pygame.init()
        self.pointCloud = []
        self.externalMap = pygame.image.load('map2.png') # change the map source file
        self.mapWidth, self.mapHeight = MapDimensions
        self.mapWindowName = 'Lidar Sensing Sim for SLAM'
        pygame.display.set_caption(self.mapWindowName)
        self.map = pygame.display.set_mode((self.mapWidth, self.mapHeight))
        self.map.blit(self.externalMap,(0,0))

        # colours definitions
        self.black = (0,0,0)
        self.grey = (80,80,80)
        self.red = (255,0,0)
        self.green = (0,255,0)
        self.blue = (0,0,255)
        self.white = (255,255,255)

    # convert sensor data to cartisian coords using geometery
    def rawData2Cartisian(self, distance, angle, robotPosition):
        x = distance * math.cos(angle) + robotPosition[0]
        y = -distance * math.sin(angle) + robotPosition[1]
        return (int(x), int(y))

    def dataStorage(self, data):
        print(len(self.pointCloud))
        for element in data:
            point = self.rawData2Cartisian(element[0], element[1], element[2])
            if point not in self.pointCloud: # avoid duplicates
                self.pointCloud.append(point)

    def showSensorData(self):
        self.infoMap = self.map.copy()
        for point in self.pointCloud:
            self.infoMap.set_at((int(point[0]), int(point[1])), (255, 0, 0))

