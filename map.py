import numpy as np

class Map():
    def __init__(self):
        self.width = 0
        self.height = 0
        self.motions = [(-1, 0), (-1, 1), (0, 1), (1, 1),
                        (1, 0), (1, -1), (0, -1), (-1, -1)]
        self.obs = set()
    
    def readMap(self, filename):
        '''with open(filename) as f:
            self.height = int(f.readline().strip().split()[1])
            self.width = int(f.readline().strip().split()[1])
            print(f"map size: {self.height} x {self.width}")

            for i in range(self.height):
                line = f.readline().strip()
                for j in range(self.width):
                    point = (j,i)
                    #self.map_tiles[j,self.height-i-1] = GridTile(j,self.height-i-1,line[j])
                    if line[j] in ['F','W','A','I']: # 森林，湿地，水体，不透水层，不能通行
                        self.obs.add(point)'''
        
        self.map_weight = np.loadtxt('converted_height.txt')
        self.height = self.map.shape[1]
        self.width = self.map.shape[0]
        for i in range(self.height):
            for j in range(self.width):
                point = (j,i)
                if self.map_weight[j,i] == 0:
                    self.obs.add(point)