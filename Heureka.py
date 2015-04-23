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
    def __init__(self, start_point, final_point):
        self.path=[] #roads taken
        self.cost = distance(start_point[0], start_point[1], final_point[0], final_point[1])

def calc_cost(loc1, loc2, destination):
    h=distance(loc2[0], loc2[1], destination[0], destination[1]) #distance to loc from next pos
    g=distance(loc1[0], loc1[1], loc2[0], loc2[1]) #estimated distance from next node to goal
    old_dist= distance(loc1[0], loc1[1], destination[0], destination[1])
    f= h + g - old_dist #subtract old dist because we would have every nodes distance to final in calculation
    return f

#finds point based on intersection names
def find_point(road1_name, road2_name):
    road1_possibility=[]
    road2_possibility=[]
    if road1_name == road2_name:
        print("Please specify two different road names")
        return
    for road in roads:
        if road.name == road1_name:
            road1_possibility.append(road)
            continue #prevents to objects from being assigned the same
        if road.name == road2_name:
            road2_possibility.append(road)
    for road1 in road1_possibility:
        for road2 in road2_possibility:
            #checks all possible combinations start finish to find correct intersection
            if road_start(road1) == road_start(road2):
                return road_start(road1)
            elif road_start(road1) == road_end(road2):
                return road_start(road1)
            elif road_end(road1) == road_start(road2):
                return road_end(road1)
            elif road_end(road1) == road_end(road2):
                return road_end(road1)
            else:
                return "roads do not intersect"

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

def road_start(road):
    x=road.x_start
    y=road.y_start
    start=[x,y]
    return start

def road_end(road):
    x=road.x_finish
    y=road.y_finish
    finish=[x,y]
    return finish



def roads_to_explore(roads, routes_traveled, start):
    current = routes_traveled[0]
    possible_roads = []
    if not len(current.path): #ONLY ENTERS ON FIRST TIME BECAUSE IT COULD BE ONE OF FOUR ROAD OBJECTS
        loc = start
    else:
        loc = [current.path[-1].x_finish, current.path[-1].y_finish]
    for road in roads:
        if loc[0] == road.x_start and loc[1] == road.y_start: #make sure the road has starting point at current location

            possible = [road.x_finish, road.y_finish]

            skip_iter=0 #values are added if trying to add previously visited point
            #if the next point has already been explored in current path don't visit
            for routes in routes_traveled:
                for explored_roads in routes.path:
                    explore_start = road_start(explored_roads)
                    explore_end = road_end(explored_roads)
                    if road_end(explored_roads) == possible or (start == possible and len(current.path)): #start coordinate is not in explored
                        print("already explored")
                        skip_iter= skip_iter+1
                        #break #skips rest of iters because point should not be appended
            if skip_iter: #skip iter so road not appended
                    continue
            possible_roads.append(road)
    return possible_roads

def path_finder(roads, start, final):

    routes_traveled = []
    new_route = Route(start, final) #this route has no road to start just a cost
    routes_traveled.append(new_route)
    loc = start
    while loc != final: #while not at final pos

        to_explore = roads_to_explore(roads, routes_traveled, start) #points to explore

        while not len(to_explore): #if no possible places to explore enter this loop
            routes_traveled.pop() #if not possible from current route delete route
            if not len(routes_traveled):
                return "not possible to reach destination"
            loc = [routes_traveled[0].path[-1].x_finish, routes_traveled[0].path[-1].y_finish] #return last location in the next best route
            to_explore = roads_to_explore(roads, routes_traveled, start)

        #THIS UPDATES ROUTES TRAVELS WITHOUT ADDING NEW ROW
        current = copy.deepcopy(routes_traveled[0]) #current is always front because is sorted
        road_finish = [to_explore[0].x_finish, to_explore[0].y_finish] #next possible road start
        cost = calc_cost(loc, road_finish, final) + current.cost
        routes_traveled[0].path.append(to_explore[0]) #MAKE SURE THIS WORKS!!
        routes_traveled[0].cost = cost

        #to_explore = np.delete(to_explore, (0), axis=0) #removes first row
        to_explore.pop(0)
        #THIS ADDS A NEW ROW
        if len(to_explore) > 0:

            for possible_road in to_explore: #possible nodes to check
                possible_point = [possible_road.x_finish, possible_road.y_finish]
                new_route = copy.deepcopy(current) #changes location in memory to not be the same
                cost = calc_cost(loc, possible_point, final) + current.cost
                new_route.cost = cost
                new_route.path.append(possible_road)

                routes_traveled.append(new_route)


        routes_traveled = sorted(routes_traveled, key=lambda route: route.cost) #sorts based on lowest cost
        loc = [routes_traveled[0].path[-1].x_finish, routes_traveled[0].path[-1].y_finish] #DOUBLE CHECK THIS




    print("number of routes explored:" + str(len(routes_traveled)))
    for route in routes_traveled:
        print(route.cost)
        print([route.path[0].x_start, route.path[0].y_start])
        for road in route.path:
            print([road.x_finish, road.y_finish, road.name])

    return "success"

roads = roads_array()

#ROADS MUST INTERSECT
start_1 = roads[0].name
start_2 = roads[7].name

finish_1 = roads[10].name
finish_2 = roads[15].name

start = find_point(start_1, start_2)
finish = find_point(finish_1, finish_2)
print("start loc:" +str(start))
print("end loc:" + str(finish))
print(path_finder(roads, start, finish))





