import numpy as np
import matplotlib.pyplot as plt
import heapq

class Map():
    def __init__(self):
        self.width = 0
        self.height = 0
        self.motions = [(-1, 0), (-1, 1), (0, 1), (1, 1),
                        (1, 0), (1, -1), (0, -1), (-1, -1)]
        self.obs = set()
        self.map_weight = None
    
    def readMap(self, filename):
        self.map_weight = np.loadtxt(filename)
        self.height = self.map_weight.shape[0]
        self.width = self.map_weight.shape[1]
        for i in range(self.height):
            for j in range(self.width):
                point = (j, i)
                if self.map_weight[i, j] == 0:
                    self.obs.add(point)
    
    def heuristic(self, a, b):
        return abs(a[0] - b[0]) + abs(a[1] - b[1])
    
    def a_star_search(self, start, goal):
        open_set = []
        heapq.heappush(open_set, (0, start))
        came_from = {}
        g_score = {start: 0}
        f_score = {start: self.heuristic(start, goal)}
        
        while open_set:
            _, current = heapq.heappop(open_set)
            
            if current == goal:
                path = []
                while current in came_from:
                    path.append(current)
                    current = came_from[current]
                path.append(start)
                path.reverse()
                return path
            
            for dx, dy in self.motions:
                neighbor = (current[0] + dx, current[1] + dy)
                if 0 <= neighbor[0] < self.width and 0 <= neighbor[1] < self.height and neighbor not in self.obs:
                    tentative_g_score = g_score[current] + (1 - self.map_weight[neighbor[1], neighbor[0]])
                    if neighbor not in g_score or tentative_g_score < g_score[neighbor]:
                        came_from[neighbor] = current
                        g_score[neighbor] = tentative_g_score
                        f_score[neighbor] = tentative_g_score + self.heuristic(neighbor, goal)
                        heapq.heappush(open_set, (f_score[neighbor], neighbor))
        
        return None
    
    def draw_path(self, start, goal, path, path_length):
        array = self.map_weight.copy()
        array_uint8 = (array * 255).astype(np.uint8)
        
        plt.imshow(array_uint8, cmap='gray')
        plt.axis('off')  # 关闭坐标轴
        
        # Draw start and goal as red circles
        plt.scatter(start[0], start[1], color='red', s=30, zorder=5)  # Start point in red
        plt.scatter(goal[0], goal[1], color='red', s=30, zorder=5)    # Goal point in red
        
        # Annotate start and goal points
        #plt.annotate('Start', (start[0], start[1]), color='red', fontsize=6, ha='left', va='center', zorder=6)
        #plt.annotate('Goal', (goal[0], goal[1]), color='red', fontsize=6, ha='left', va='center', zorder=6)
        
        # Draw path as a red line
        if path:
            path_x, path_y = zip(*path)
            plt.plot(path_x, path_y, color='red', linewidth=2, zorder=5)
            
            # Annotate path length
            #mid_point = path[len(path) // 2]
            #plt.annotate(f'Path Length: {path_length:.2f}', (mid_point[0], mid_point[1]), color='red', fontsize=6, ha='center', va='center', zorder=6)
        
        plt.savefig('path_result.png')
        plt.show()

# 创建地图对象并读取数据
map_obj = Map()
map_obj.readMap('result/result.txt')

# 定义起始点和终点
start = (77,5)  # 起始点
goal = (68,300)  # 终点

# 计算最短路径
path = map_obj.a_star_search(start, goal)

# 输出路径长度（所有点的可通行值得和）
if path:
    path_length = sum(map_obj.map_weight[y, x] for x, y in path)
    print(f"Path length: {path_length}")
else:
    print("No path found")

# 绘制路径
map_obj.draw_path(start, goal, path,path_length)