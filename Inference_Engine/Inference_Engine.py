import copy


"""
First clauses should go into remain. From there each one is expanded. As soon as it is expanded it
should be removed from remain and added to used_clauses. Once remain is the empty set we have solved
our goal
"""
class PathToGoal:
    def __init__(self, initial_facts):
        self.facts = initial_facts #totally useless
        self.used_clauses = [] #clauses that have been traveled
        self.remain = [] #clauses that have to be proven can continue
        self.cost = 0

class Clause:
    def __init__(self, result, required):
        self.result=result
        self.required=required

#below functions are used for initialization
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
#above functions are used for initialization

def calc_cost(path):
    shortest_dist = 0 #initialize
    for clause in path.remain: #calculates path to shortest proof for each of remaining proofs
        #so if hotdrink and food were in remain it would calculate egg and tea
        if isinstance(clause, str): #if this is an item just add 1
            shortest_dist += 1
        else: #if this is actually a clause
            shortest_dist += len(clause.required)

    traveled = len(path.used_clauses) #path traveled
    if len(path.used_clauses)>1:
        old_est = len(path.used_clauses[-1].required) #old shortest est
    else:
        old_est = 0 #old shortest est
    cost = shortest_dist + traveled - old_est
    return cost

def possible_clause(current, kb, goal, req_item=''):
    possible_nodes = []
    for clause in kb:
        for result in clause.result:
            if not len(current.used_clauses) and not len(current.remain): #when there is no starting point enter
                if goal in result:
                    possible_nodes.append(clause)

            elif req_item in result and clause not in current.used_clauses:
                possible_nodes.append(clause)

    possible_nodes = sorted(possible_nodes, key=lambda clause: clause.required) #sorts based on least required
    return possible_nodes

#PROBLEM IS IN HERE SOMEWHERE
def append_path(to_explore, paths, is_start = 0): #adds new row to paths
    original = copy.deepcopy(paths[0]) #preserve original
    for count, clause in enumerate(to_explore): #add new possible paths to explore
        new_path = copy.deepcopy(original)
        if not count: #appends for first iteration and adds rows for the rest
            paths[0].remain.extend(clause)
            if not is_start:
                paths[0].used_clauses.append(paths[0].remain[0])
                paths[0].remain.pop(0) #remove previous clause. So when breakfast is expanded remove and replace
            #it with a clause that points to all of it's items
            paths[0].cost = calc_cost(paths[0])
            continue
        new_path.remain.extend(clause)
        if not is_start: #enters if it's not the first iter
            new_path.used_clauses.append(new_path.remain[0]) #adds clause to used before popped
            new_path.remain.pop(0) #removes clause be this clause was replaced with a new set of clauses
        new_path.cost = calc_cost(new_path)
        paths.append(new_path)
    return paths

def comb_to_explore(new_clauses):#returns all possible unique combinations of to explore
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
    return to_explore

#updates to explore
def update_to_explore(current, kb, goal):
    new_clauses=[] #list of clauses for each required item
    to_explore = []
    #Generates next nodes
    if len(current.remain): #checks to make sure not the first iteration
        for item in current.remain[0].required: #expands first node in remaining nodes to explore
            to_explore = possible_clause(paths[0], kb, goal, item)
            if not len(to_explore):
                to_explore.append(item) #if item is requirement make sure to keep it as something to explore
            new_clauses.append(to_explore)
    else: #enters on first iteration
        for clause in possible_clause(paths[0], kb, goal): #appends clauses with identical results as seperate lists
            to_explore.append([clause])
    if len(new_clauses)>1:#is there an "AND" in requirement
        to_explore = comb_to_explore(new_clauses)
    return to_explore

def prove_goal(kb, paths, goal):
    to_explore = []
    for clause in possible_clause(paths[0], kb, goal): #appends clauses with identical results as seperate lists
        to_explore.append([clause])
    if len(to_explore) > 0: #adds row
        paths = append_path(to_explore, paths, 1)

    while len(paths[0].remain): #exit with empty clause
        current = copy.deepcopy(paths[0]) #set head 0th is thought to be best

        if isinstance(current.remain[0], str):
            if current.remain[0] in current.facts:
                paths[0].used_clauses.append(current.remain[0])
                paths[0].remain.pop(0)
                continue
            else:
                paths.pop(0)
                current = copy.deepcopy(paths[0])

        to_explore = update_to_explore(current, kb, goal)

        while not len(to_explore): #if no possible places to explore enter this loop
            paths.pop(0) #if not possible from current path delete path
            print("route removed no possible place to go")
            if not len(paths):
                return "not possible to reach destination"
            current = copy.deepcopy(paths[0]) #return last location in the next best route
            to_explore = update_to_explore(current, kb, goal)

        if len(to_explore) > 0: #adds row
            paths = append_path(to_explore, paths)

#if the front element in remains is a string('juice') and is not in facts. Then remove this entire path
#as it will never be possible
        if isinstance(paths[0].remain[0], str):
            if paths[0].remain[0] in paths[0].facts:
                paths[0].used_clauses.append(paths[0].remain[0])
                paths[0].remain.pop(0)
            else:
                paths.pop(0)
        else:
            if set(paths[0].remain[0].required).issubset(paths[0].facts): #if the the requirements of the
                #first clause in remain is a subset of facts then pop it from remain because it can be proven
                paths[0].used_clauses.append(paths[0].remain[0])
                paths[0].remain.pop(0)

        paths = sorted(paths, key=lambda clause: clause.cost) #sorts based on lowest cost
    return "sucess!"


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
print(prove_goal(KB, paths, goal))










