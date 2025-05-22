import math
from map import Map
#from gridtile import GridTile
import numpy as np

class Graph:
    def __init__(self, map, agent_size):
        self.map = map
        self.agent_size = agent_size
        self.graph_width = math.ceil(self.map.width / self.agent_size)
        self.graph_height = math.ceil(self.map.height / self.agent_size)
    
    def createMapRepresentation(self):
        new_map = Map()
        new_map.width = self.map.width
        new_map.height = self.map.height
        #new_map.map_tiles = np.zeros((self.map.width,self.map.height),dtype=GridTile)
        for i in range(self.graph_width):
            for j in range(self.graph_height):
                boundary_min_x = i*self.agent_size
                boundary_min_y = j*self.agent_size
                boundary_max_x = boundary_min_x + self.agent_size-1
                boundary_max_y = boundary_min_y + self.agent_size-1
                obtacle = False

                #self.new_map.map_tiles[i,j] = GridTile(i,j)
                for x in range(boundary_min_x, boundary_max_x+1):
                    for y in range(boundary_min_y, boundary_max_y+1):
                        if (x,y) in self.map.obs:
                            obtacle = True
                if obtacle:
                    for x in range(boundary_min_x, boundary_max_x+1):
                        for y in range(boundary_min_y, boundary_max_y+1):
                            new_map.obs.add((x,y))
        return new_map