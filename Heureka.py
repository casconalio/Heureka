import math
import numpy as np


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

def possible_nodes(roads, loc, final):
    to_explore=np.zeros((1,2)) #list of points to explore

    for road in roads:

        if ((loc[0] == road.x_start and loc[1] == road.y_start) #checks for possible points
        or (loc[0] == road.x_finish and loc[1] == road.y_finish)):

            possible_xloc = road.x_start
            possible_yloc = road.y_start


            #makes sure next point is not same as current point
            if possible_xloc == loc[0] and possible_yloc == loc[1]:
                possible_xloc = road.x_finish
                possible_yloc = road.y_finish

            possible = [possible_xloc, possible_yloc]
            #consider changing to less than or equal to
            #BE CAREFUL THIS IS WHERE COULD GET STUCK AT BOTTOM OF HILL
            dist1 = distance(loc[0], loc[1], final[0], final[1])
            dist2 = distance(possible[0], possible[1], final[0], final[1])
            #print("dist1:" + str(dist1) + " dist2:" + str(dist2))
            if dist1 < dist2:
                continue

            to_explore = np.vstack((to_explore, possible)) #appends to matrix of all possible points to explore

    return to_explore

def path_finder(roads, loc, final):

    routes_traveled = []
    new_route = Route(loc, final)

    #new_route.path.append(loc) #initializes starting position
    routes_traveled.append(new_route)
    while loc[0] != final[0] or loc[1] != final[1]: #while not at final pos

        to_explore = possible_nodes(roads, loc, final) #points to explore

        #THIS UPDATES ROUTES TRAVELS WITHOUT ADDING NEW ROW
        current = routes_traveled[0] #current is always front because is sorted
        cost = calc_cost(loc, to_explore[0, :], final) + current.cost
        routes_traveled[0].path.append(to_explore[0, :]) #MAKE SURE THIS WORKS!!
        routes_traveled[0].cost = cost

        to_explore = np.delete(to_explore, (0), axis=0) #removes first row

        #THIS ADDS A NEW ROW
        for possible_point in to_explore: #possible nodes to check

            cost = calc_cost(loc, possible_point, final) + current.cost

            new_route.cost = cost
            new_route.path = current.path.append(possible_point)

            routes_traveled.append(new_route)


        routes_traveled = sorted(routes_traveled, key=lambda route: route.cost) #sorts based on lowest cost

        loc = routes_traveled[0].path[-1] #DOUBLE CHECK THIS
        print("changed road")
        print("x:"+str(loc[0]) + " y:" +str(loc[1]))
        if(loc[0] == final[0] and loc[1]== final[1]):
            break

    print(len(routes_traveled))
    for route in routes_traveled:
        print(route.path)
        print(route.cost)

roads = roads_array()
loc = [10, 70]
final = [80, 70]

path_finder(roads, loc, final)

print("success")



