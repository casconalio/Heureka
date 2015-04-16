
class Road:
    def __init__(self, line):
        words = []
        for word in line.split():
            words.append(word)

        if isinstance(words[0], int):
            self.x_start=words[0]
            self.y_start=words[1]
            self.name=words[2]
            self.x_finish=words[3]
            self.y_finish=words[4]
        else:#the very first value is the starting location
            self.x_start=words[1]
            self.y_start=words[2]
            self.name=words[0]



#returns array of all road objects
def roads_array():
    roads=[] #all road objects in array
    f=open("/home/badcode/Desktop/AI/copenhagen_data_fixed.txt", 'r')
    for line in f:
        if len(line)>2: #for some reason last line is just 1 character of white space so this dodges that
            new_road=Road(line)
            roads.append(new_road)
    return roads

roads=roads_array()
start_loc=roads[0]
roads=roads[1:]

