import math
from enum import Enum, unique
from typing import List, Optional, Tuple


@unique
class Direction(Enum):
    North = 0
    East = 1
    South = 2
    West = 3


def distance(x_pos_start, y_pos_start, x_pos_target, y_pos_target):
    dist = math.sqrt((x_pos_start - x_pos_target) * (x_pos_start - x_pos_target) +
                     (y_pos_start - y_pos_target) * (y_pos_start - y_pos_target))
    return dist

class Planet:

    def __init__(self):
        self.nodes = []
        self.paths = []
        self.nodes_in_planet = []
        self.updated_nodes = []
        pass

    def choose_drive_direction(self, node):
        for direction in Direction:
            print("Richtung: {}".format(direction))
            if node[direction] is True:
                print("suche in dieser Richtung...")
                path_known = False
                for path in self.paths:
                    print("Vergleiche Pfad {} mit Node {}".format(path, node))
                    if path["x_position_start"] == node["x_position"] and path["y_position_start"] == node["y_position"] \
                            and path["direction_start"] == direction:
                        print("Pfad bereits bekannt")
                        path_known = True
                        break
                    if path["x_position_target"] == node["x_position"] and path["y_position_target"] == node["y_position"] \
                            and path["direction_target"] == direction:
                        print("Pfad bereits bekannt")
                        path_known = True
                        break
                if path_known is False:
                    print("Fahre in Richtung {}".format(direction))
                    return direction
        if node[Direction.North] is True:
            return Direction.North
        if node[Direction.East] is True:
            return Direction.East
        if node[Direction.South] is True:
            return Direction.South
        return Direction.West

    def add_node(self, x_pos, y_pos, line_direction):
        for nod in self.nodes:
            if nod["x_position"] == x_pos and nod["y_position"] == y_pos:
                return
        self.nodes.append({"x_position": x_pos, "y_position": y_pos, Direction.North: line_direction[Direction.North],
                                Direction.East: line_direction[Direction.East],
                                Direction.South: line_direction[Direction.South], Direction.West: line_direction[Direction.West]})
        self.print_nodes()
        pass

    # example: add_path((0, 3, Direction.North), (0, 3, Direction.West))
    def add_path(self, start: Tuple[int, int, Direction], target: Tuple[int, int, Direction]):
        self.paths.append({"x_position_start": start[0], "y_position_start": start[1], "direction_start": start[2],
                  "x_position_target": target[0], "y_position_target": target[1], "direction_target": target[2]})
        pass

    def initialize(self, start):
        node_dis_pre = []
        for node in self.nodes:
            if node["x_position"] == start["x_position"] and node["y_position"] == start["y_position"]:
                node_dis_pre.append([node, 0, None])
            else:
                node_dis_pre.append([node, math.inf, None])
        return node_dis_pre

    def node_smallest_distance(self):
        is_smallest = math.inf
        i = 0
        index = 0
        for node in self.nodes_in_planet:
            may_smallest = node[1]
            if is_smallest > may_smallest:
                is_smallest = may_smallest
                index = i
            i += 1
        return index

    def neighbours_u(self, u):
        list_of_neighbours = []
        for path in self.paths:
            if (u[0]["x_position"] == path["x_position_start"] and u[0]["y_position"] == path["y_position_start"]) \
                    or (u[0]["x_position"] ==  path["x_position_target"] and u[0]["y_position"] == path["y_postiion_start"]):
                list_of_neighbours.append(path)
        return list_of_neighbours

    def distance_update(self, u, neighbour):
        alternative = u[1] + distance(u[0]["x_position"], u[0]["y_position"], neighbour[0]["x_position"], neighbour[0]["y_position"])
        if alternative < neighbour[1]:
            neighbour[1] = alternative
            neighbour[2] = direction_to_u(u, neighbour)

    def direction_to_u(self, u, neighbour):
        for path in self.paths:
            if u[0]["x_position"] == path["x_position_start"] and u[0]["y_position"] == path["y_position_start"] and neighbour[0]["x_position"] == path["x_position_target"] and neighbour[0]["y_position"] == path["y_position_target"]:
                return path["direction_target"]
            if u[0]["x_position"] == path["x_position_target"] and u[0]["y_position"] == path["y_position_target"] and neighbour[0]["x_position"] == path["x_position_start"] and neighbour[0]["y_position"] == path["y_position_start"]:
                return path["direction_start"]



    def dijkstra(self, start):
        self.nodes_in_planet = initialize(start)
        while self.nodes_in_planet is True:
            index = node_smallest_distance()
            u = self.nodes_in_planet.pop(index)
            self.updated_nodes.append(u)
            list_of_neighbours = neighbours_u(u)
            for neighbour in list_of_neighbours:
                for node in self.nodes_in_planet:
                    if neighbour["x_position"] == node[0]["x_position"] and neighbour["y_position"] == node[0]["y_position"]:
                        distance_update(u, node)

    # example: shortest_path((0,0), (2,2)) returns: [(0, 0, Direction.East), (1, 0, Direction.North)]
    # example: shortest_path((0,0), (1,2)) returns: None
    def shortest_path(self, start: Tuple[int, int], target: Tuple[int, int]) -> Optional[List[Tuple[int, int, Direction]]]:
        """return a shortest path between two crossings"""
        shortest_path = []
        dijkstra(start)
        for node in self.updated_nodes:
            if target[0] == node[0]["x_position"] and target[1] == node[0]["y_position"]:
                shortest_path.append([node[0]["x_position"], node[0]["y_position"], node[2]])
        for node in shortest_path:
            if node[2] is None:
                return shortest_path
            for path in self.paths:
                if node[0] == path["x_position_start"] and node[1] == path["y_position_start"] and node[2] == path["direction_start"]:
                    shortest_path.append([path["x_position_target"], path["y_position_target"], path["direction_target"]])
                if node[0] == path["x_position_target"] and node[1] == path["y_position_target"] and node[2] == path["direction_target"]:
                    shortest_path.append([path["x_position_start"], path["y_position_start"], path["direction_start"]])
        return shortest_path





        pass


    def print_nodes(self):
        for node in self.nodes:
            print("X: {}, Y: {}, Verbindungen: N:{}, E:{}, S:{}, W:{}".format(node["x_position"], node["y_position"], node[Direction.North], node[Direction.East], node[Direction.South], node[Direction.West]))
