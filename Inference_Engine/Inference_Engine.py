import copy


class PathToGoal:
    def __init__(self, initial_facts):
        self.facts = initial_facts
        self.used_clauses = []
        self.cost = 0

class Clause:
    def __init__(self, result, required):
        self.result=result
        self.required=required

def split_rule(line):
    result = []
    required = []
    line=line.split() #splits line into list of only it's words

    line_required = copy.deepcopy(line) #need to be able to pop already visited words
    for word in line:
        if word == "if":
            line_required.pop(0)
            break
        result.append(word)
        line_required.pop(0)
    for word in line_required:
        required.append(word)
    return [result, required]

def read_kb_section(section): #section is either result or required string
    list_vals = [] #either required or result
    count = 0
    for word in section:
        if word == "not":
            list_vals.append("-"+str(section[count+1])) #appends "-"fact
            count+=2
        else:
            list_vals.append(word)
            count+=1
    return list_vals


def read_kb(line): #initialize knowledge base
    result, required = split_rule(line) #result is key, required is value in kb
    result = read_kb_section(result)
    required = read_kb_section(required)
    return [result, required]

def new_facts(current, facts):
    for clause in current.used_clauses: #go through clause objects
        set_required = set(clause.required)
        set_results = set(clause.result)
        set_facts = set(facts)
        if set_required.issubset(set_facts) and not set_results.issubset(set_facts):
            for item in set_results:
                print(str(set_required) + " => " + str(set_results))
                facts.append(item)
    return facts


def calc_cost(kb, clauses):
    shortest_dist = len(clauses[-1].required)
    traveled = len(clauses)
    if len(clauses)>1:
        old_est = len(clauses[-2].required)
    else:
        old_est = 0
    cost = shortest_dist + traveled - old_est
    return cost

def possible_clause(current, kb, goal, req_item=''):
    if len(current.used_clauses):
        head = current.used_clauses[-1] #last clause explored
    possible_nodes = []
    for clause in kb:
        for result in clause.result:
            if not len(current.used_clauses): #when there is no starting point enter
                if goal in result:
                    possible_nodes.append(clause)
                #continue
            elif req_item in result and clause not in current.used_clauses:
                possible_nodes.append(clause)

    possible_nodes = sorted(possible_nodes, key=lambda clause: clause.required) #sorts based on least required
    return possible_nodes

def prove_goal(kb, paths, goal):
    while goal not in paths[0].facts: #make sure goal is not in head path
        current = copy.deepcopy(paths[0]) #set head 0th is thought to be best
        new_clauses=[] #list of clauses for each required item
        if len(current.used_clauses):
            for item in current.used_clauses[-1].required:
                to_explore = possible_clause(paths[0], kb, goal, item)
                new_clauses.append(to_explore)
        else:
            to_explore = possible_clause(paths[0], kb, goal) #only enters for starting pos

        if len(new_clauses)>1:#is there an "AND" in requirement
            to_explore = []

            for clause in new_clauses:
                if to_explore:
                    new_l = []
                    for i in clause:
                        for j in to_explore:
                            new_l.append([i])
                            new_l[-1].extend(j)
                    to_explore = new_l
                else:
                    for i in clause:
                        to_explore.append([i])


##############################BELOW HAS NOT BEEN CHANGED TO FIT CODE YET #####################

        while not len(to_explore): #if no possible places to explore enter this loop
            paths.pop(0) #if not possible from current path delete path
            print("route removed no possible place to go")
            if not len(paths):
                return "not possible to reach destination"
            current = copy.deepcopy(paths[0]) #return last location in the next best route
            for item in current.used_clauses[-1].required:
                to_explore = possible_clause(paths[0], kb, goal, item)
                new_clauses.append(to_explore)

        #THIS UPDATES ROUTES TRAVELS WITHOUT ADDING NEW ROW
        paths[0].used_clauses.append(to_explore[0])
        paths[0].cost = calc_cost(kb, paths[0].used_clauses) #first object

        to_explore.pop(0) #remove first possible clause as it is already added

        if len(to_explore) > 0: #adds row
            for clause in to_explore: #add new possible paths to explore
                new_path = copy.deepcopy(current)
                new_path.used_clauses.append(clause)
                new_path.cost = calc_cost(kb, new_path.used_clauses)
                paths.append(new_path)
        current = copy.deepcopy(paths[0])
        paths[0].facts = new_facts(current, current.facts)
        paths = sorted(paths, key=lambda clause: clause.cost) #sorts based on lowest cost


initial_kb = []
initial_facts = []
paths = []
KB = []

f=open("/home/badcode/Desktop/AI/Inference_Engine/breakfast.txt", 'r')
for line in f:
    if not len(line):
        continue
    elif len(line.split())>1:
        line = line.strip() #removes \n
        initial_kb.append(line)
    else:
        line = line.strip() #removes \n
        initial_facts.append(line)

for line in initial_kb: #initalize clauses
    result, required = read_kb(line)
    init_clause = Clause(result, required)
    KB.append(init_clause)


goal = KB[0].result[0]
new_path = PathToGoal(initial_facts)
paths.append(new_path)
prove_goal(KB, paths, goal)










