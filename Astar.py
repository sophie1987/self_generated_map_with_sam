import math
import heapq
import random
from map import Map
#import plotting
#from time_consume import *
#from graph_new import Graph
from graph_new import Graph_New
from generate_passible_pic import generate_all_result
import plotting

class AStar:
    """AStar set the cost + heuristics as the priority
    """
    def __init__(self, heuristic_type):
        self.heuristic_type = heuristic_type
        self.map = Map() # class Env
        self.u_set = None
        self.obs = None

    def set_map(self, map):
        self.map = map
        self.u_set = self.map.motions  # feasible input set
        self.obs = self.map.obs  # position of obstacles

    def set_goal(self, s_start, s_goal):
        self.s_start = s_start
        self.s_goal = s_goal

    #@get_time
    def searching(self):
        """
        A_star Searching.
        :return: path, visited order
        """
        self.OPEN = []  # priority queue / OPEN set
        self.CLOSED = []  # CLOSED set / VISITED order
        self.PARENT = dict()  # recorded parent
        self.g = dict()  # cost to come
        #if self.s_start in self.obs or self.s_goal in self.obs:
        #    print("Start or Goal is in obstacle!")
        #    return [], []
        if self.s_start in self.obs:
            print("Start is in obstacle!")
            return [], []
        if self.s_goal in self.obs:
            print("Goal is in obstacle!")
            return [], []
        self.PARENT[self.s_start] = self.s_start
        self.g[self.s_start] = 0
        self.g[self.s_goal] = math.inf
        heapq.heappush(self.OPEN,
                       (self.f_value(self.s_start), self.s_start))

        while self.OPEN:
            _, s = heapq.heappop(self.OPEN)
            self.CLOSED.append(s)

            if s == self.s_goal:  # stop condition
                break

            for s_n in self.get_neighbor(s):
                new_cost = self.g[s] + self.cost(s, s_n)

                if s_n not in self.g:
                    self.g[s_n] = math.inf

                if new_cost < self.g[s_n]:  # conditions for updating Cost
                    self.g[s_n] = new_cost
                    self.PARENT[s_n] = s
                    heapq.heappush(self.OPEN, (self.f_value(s_n), s_n))

        return self.extract_path(self.PARENT), self.CLOSED
    def get_neighbor(self, s):
        return [(s[0] + u[0], s[1] + u[1]) for u in self.u_set]

    def cost(self, s_start, s_goal):
        if self.is_collision(s_start, s_goal):
            return math.inf
        
        return math.hypot(s_goal[0] - s_start[0], s_goal[1] - s_start[1])
        #return math.hypot(s_goal[0] - s_start[0], s_goal[1] - s_start[1])+self.weight[s_goal]

    def is_collision(self, s_start, s_end):
        if s_start in self.obs or s_end in self.obs:
            return True

        if s_start[0] != s_end[0] and s_start[1] != s_end[1]:
            if s_end[0] - s_start[0] == s_start[1] - s_end[1]:
                s1 = (min(s_start[0], s_end[0]), min(s_start[1], s_end[1]))
                s2 = (max(s_start[0], s_end[0]), max(s_start[1], s_end[1]))
            else:
                s1 = (min(s_start[0], s_end[0]), max(s_start[1], s_end[1]))
                s2 = (max(s_start[0], s_end[0]), min(s_start[1], s_end[1]))

            if s1 in self.obs or s2 in self.obs:
                return True

        return False

    def f_value(self, s):
        return self.g[s] + self.heuristic(s)

    def extract_path(self, PARENT):
        path = [self.s_goal]
        s = self.s_goal

        while True:
            s = PARENT[s]
            path.append(s)

            if s == self.s_start:
                break

        return list(path)

    def heuristic(self, s):
        heuristic_type = self.heuristic_type  # heuristic type
        goal = self.s_goal  # goal node

        if heuristic_type == "manhattan":
            return abs(goal[0] - s[0]) + abs(goal[1] - s[1])
        else:
            return math.hypot(goal[0] - s[0], goal[1] - s[1])


def loadTestCase(test_case_filename):
    test_case_list = []
    with open(test_case_filename, "r") as f:
        lines = f.readlines()
        for line in lines:
            line_list = line.strip().split(" ")
            start_x = int(line_list[0])
            start_y = int(line_list[1])
            goal_x = int(line_list[2])
            goal_y = int(line_list[3])
            test_case_list.append([(start_x, start_y), (goal_x, goal_y)])
    return test_case_list

def main():
    #result_filename = 'result/passible.txt'
    result_filename = 'mixed_result.txt'
    #generate_all_result(RESULAT_PASSIBLE=result_filename)
    agent_size = 5

    origin_map = Map()
    origin_map.readMap(result_filename)
    astar = AStar("euclidean")
    graph = Graph_New(origin_map, agent_size)
    new_map = graph.createMapRepresentation()
    astar.set_map(new_map)

    print(f"original obstacles: {len(origin_map.obs)}")
    print(f"updated obstacles: {len(new_map.obs)}")
    s_goal = (77,5)
    s_start = (68,300)
    astar.set_goal(s_start, s_goal)
    path,visit = astar.searching()
    plot = plotting.Plotting(new_map, s_start, s_goal)
    plot.animation(path, visit, "A*")  # animation
    print(f"path length: {len(path)}")

if __name__ == '__main__':
    main()
