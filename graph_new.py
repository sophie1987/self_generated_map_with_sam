import math
from map import Map
#from gridtile import GridTile
import numpy as np

class Graph_New:
    def __init__(self, map, agent_size):
        self.map = map
        self.agent_size = agent_size

    def createMapRepresentation(self):
        new_obs = set()
        for x in range(self.map.width):
            for y in range(self.map.height):
                if self._isPassable(x, y, self.agent_size):
                    continue
                new_obs.add((x, y))
        new_map = Map()
        new_map.width = self.map.width
        new_map.height = self.map.height
        new_map.obs = new_obs
        return new_map

    def _isPassable(self, x, y, size):
        left = math.floor((size-1)/2)
        right = math.ceil((size-1)/2)
        for i in range(x-left, x+right+1):
            for j in range(y-left, y+right+1):
                if i<=0 or i>=self.map.width or j<=0 or j>=self.map.height or (i, j) in self.map.obs:
                    return False
        return True