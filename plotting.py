import matplotlib.pyplot as plt
import numpy as np

from map import Map

class Plotting:
    def __init__(self,map,start,end):
        self.map = map
        self.start = start
        self.end = end
    
    def plot_grid(self,name):
        plt.figure(figsize=(self.map.width, self.map.height))
        plt.xlim(-1, self.map.width)
        plt.ylim(-1, self.map.height)

        obs_x = [x[0] for x in self.map.obs]
        obs_y = [x[1] for x in self.map.obs]

        plt.plot(self.start[0], self.start[1], "bs", markersize=1)
        plt.plot(self.end[0], self.end[1], "gs", markersize=1)
        plt.plot(obs_x, obs_y, "sk")
        plt.title(name)
        plt.axis("equal")
    
    def animation(self, path, visited, name):
        self.plot_grid(name)
        #self.plot_visited(visited)
        self.plot_path(path)
        ax = plt.gca()                                 #获取到当前坐标轴信息
        ax.xaxis.set_ticks_position('top')   #将X坐标轴移到上面
        ax.invert_yaxis()   
        plt.savefig('result/updated.png')
        plt.show()
    
    def plot_visited(self, visited, cl='gray'):
        if self.start in visited:
            visited.remove(self.start)

        if self.end in visited:
            visited.remove(self.end)

        count = 0

        for x in visited:
            count += 1
            plt.plot(x[0], x[1], color=cl, marker='o')
            plt.gcf().canvas.mpl_connect('key_release_event',
                                         lambda event: [exit(0) if event.key == 'escape' else None])

            if count < len(visited) / 3:
                length = 20
            elif count < len(visited) * 2 / 3:
                length = 30
            else:
                length = 40
            #
            # length = 15

            if count % length == 0:
                plt.pause(0.01)

        plt.pause(0.01)
        
    def plot_path(self, path, cl='r', flag=False):
        path_x = [path[i][0] for i in range(len(path))]
        path_y = [path[i][1] for i in range(len(path))]

        if not flag:
            plt.plot(path_x, path_y, linewidth='1', color='r')
        else:
            plt.plot(path_x, path_y, linewidth='1', color=cl)

        plt.plot(self.start[0], self.start[1], "bs", markersize=1)
        plt.plot(self.end[0], self.end[1], "gs", markersize=1)

        plt.pause(0.01)