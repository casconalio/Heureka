import math
import numpy as np
import copy


class Road:
    def __init__(self, line):
        words = []
        for word in line.split():
            words.append(word)


        #cast to integers
        self.x_start=int(words[0])
        self.y_start=int(words[1])
        self.name=words[2]
        self.x_finish=int(words[3])
        self.y_finish=int(words[4])

class Route:
    def __init__(self, loc, final):
        self.path = []
        self.path=[loc] #path taken
        self.cost = distance(loc[0], loc[1], final[0], final[1])

def calc_cost(loc1, loc2, destination):
    h=distance(loc2[0], loc2[1], destination[0], destination[1]) #distance to loc from next pos
    g=distance(loc1[0], loc1[1], loc2[0], loc2[1]) #estimated distance from next node to goal
    old_dist= distance(loc1[0], loc1[1], destination[0], destination[1])
    f= h + g - old_dist #subtract old dist because we would have every nodes distance to final in calculation
    return f

#returns array of all road objects
def roads_array():
    roads=[] #all road objects in array
    f=open("/home/badcode/Desktop/AI/copenhagen_data_fixed.txt", 'r')
    for line in f:
        if len(line)>2: #for some reason last line is just 1 character of white space so this dodges that
            new_road=Road(line)
            roads.append(new_road)
    return roads

#distance between two points
def distance(x1, y1, x2, y2):
    dist=math.sqrt((x2-x1)**2+(y2-y1)**2) # ** is exponent in python
    return dist

def possible_nodes(roads, current, final):
    to_explore=np.zeros((1,2)) #list of points to explore
    loc = current.path[-1]
    for road in roads:

        if loc[0] == road.x_start and loc[1] == road.y_start: #make sure the road has starting point at current location

            possible_xloc = road.x_finish
            possible_yloc = road.y_finish

            possible = [possible_xloc, possible_yloc]
            if possible in current.path: #if the next point has already been explored in current path don't visit
                continue
            previous_row = list(to_explore[-1, :]) #casts to list so no conflicting data types
            if possible == previous_row: #avoids duplicates
                continue

            to_explore = np.vstack((to_explore, possible)) #appends to matrix of all possible points to explore
    to_explore = np.delete(to_explore, (0), axis=0) #removes first row because is full of zeros
    return to_explore

def path_finder(roads, loc, final):

    routes_traveled = []
    new_route = Route(loc, final)

    routes_traveled.append(new_route)
    while loc[0] != final[0] or loc[1] != final[1]: #while not at final pos

        to_explore = possible_nodes(roads, routes_traveled[0], final) #points to explore

        while not len(to_explore): #if no possible places to explore enter this loop
            routes_traveled.pop() #if not possible from current route delete route
            if not len(routes_traveled):
                return "not possible to reach destination"
            loc = routes_traveled[0].path[-1] #return last location in the next best route
            to_explore = possible_nodes(roads, current, final)

        #THIS UPDATES ROUTES TRAVELS WITHOUT ADDING NEW ROW
        current = copy.deepcopy(routes_traveled[0]) #current is always front because is sorted
        cost = calc_cost(loc, list(to_explore[0, :]), final) + current.cost
        routes_traveled[0].path.append(list(to_explore[0, :])) #MAKE SURE THIS WORKS!!
        routes_traveled[0].cost = cost

        to_explore = np.delete(to_explore, (0), axis=0) #removes first row
        #THIS ADDS A NEW ROW
        if len(to_explore) > 0:

            for possible_point in to_explore: #possible nodes to check
                new_route = copy.deepcopy(current) #changes location in memory to not be the same
                cost = calc_cost(loc, possible_point, final) + current.cost
                new_route.cost = cost
                new_route.path = current.path
                new_route.path.append(list(possible_point))

                routes_traveled.append(new_route)


        routes_traveled = sorted(routes_traveled, key=lambda route: route.cost) #sorts based on lowest cost

        loc = routes_traveled[0].path[-1] #DOUBLE CHECK THIS



    print("number of routes explored:" + str(len(routes_traveled)))
    for route in routes_traveled:
        print(route.path)
        print(route.cost)
    return "success"

roads = roads_array()
loc = [10, 70]
final = [80, 70]

print(path_finder(roads, loc, final))





