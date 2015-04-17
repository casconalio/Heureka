import math


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



roads = roads_array()
loc_x = 10
loc_y = 70
final_x = 80
final_y = 70
"""
print("x:"+str(loc_x) + " y:" +str(loc_y))
print("x:"+str(roads[0].x_start) + " y:" +str(roads[0].y_start))
print(type(loc_x))
print(type(roads[0].x_start))

if loc_x == roads[0].x_start and loc_y == roads[0].y_start:
    print("yay")
"""
while loc_x != final_x or loc_y != final_y:
    for road in roads:
        if ((loc_x == road.x_start and loc_y == road.y_start)
        or (loc_x == road.x_finish and loc_y == road.y_finish)):
            possible_xloc = road.x_start
            possible_yloc = road.y_start

            #makes sure next point is not same as current point
            if possible_xloc == loc_x and possible_yloc == loc_y:
                possible_xloc = road.x_finish
                possible_yloc = road.y_finish


            #consider changing to less than or equal to
            dist1 = distance(loc_x, loc_y, final_x, final_y)
            dist2 = distance(possible_xloc, possible_yloc, final_x, final_y)
            print("dist1:" + str(dist1) + " dist2:" + str(dist2))
            if dist1 < dist2:
                continue


            loc_x=possible_xloc
            loc_y=possible_yloc
            print("changed road")
            print("x:"+str(loc_x) + " y:" +str(loc_y))
            if(loc_x == final_x and loc_y== final_y):
                break





print("success")