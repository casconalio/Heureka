import copy

class PathToGoal:
    def __init__(self, initial_facts):
        self.facts=initial_facts
        #self.cost=

    #def cost(self):

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


def read_kb(line):

    final_result=[]
    final_required=[]
    result, required = split_rule(line) #result is key, required is value in kb
    set=[]
    set2=[] #used for OR
    count = 0
    last_op = ""
    for word in result:
        if word == "and":
            if word != last_op:
                set=[]#makes it empty because it's a new set
                set.append(result[count-1]) #avoids repeats
            set.append(result[count+1])
            last_op=word

            #if the next operator is not the same or if is checking past the end of result
            #Have to check plus three in case there is a NOT in the next word
            if count+3>len(result) or result[count+3] != word or result[count+2] != word:
                final_result.append(set) #appends if no more AND chaining

        elif word == "or":
            set=[] #both sets should always be empty when dealing with or
            set2=[]
            if word != last_op:
                set.append(result[count-1]) #blocks repeats
            set2.append(result[count+1])
            final_result.append(set)
            final_result.append(set2)
            last_op=word

        elif word == "not":
            set.append("-"+str(result[count+1])) #appends "-"fact
            count =  count + 1
            continue
        elif len(result)<2:
            final_result.append([word])
        else:
            count = count + 1
            continue
        last_op = word
        count = count + 1


    set=[]
    set2=[] #used for OR
    count = 0
    last_op = ""
    for word in required:
        if word == "and":
            if word != last_op:
                set=[]#makes it empty because it's a new set
                set.append(required[count-1]) #avoids repeats
            set.append(required[count+1])
            last_op=word

            #if the next operator is not the same or if is checking past the end of result
            #Have to check plus three in case there is a NOT in the next word

            if count+3>len(required) or (required[count+3] != word and required[count+2] != word):
                final_required.append(set) #appends if no more AND chaining

        elif word == "or":
            set=[] #both sets should always be empty when dealing with or
            set2=[]
            if word != last_op:
                set.append(result[count-1]) #blocks repeats
            set2.append(result[count+1])
            final_required.append(set)
            final_required.append(set2)
            last_op=word

        elif word == "not":
            set.append("-"+str(result[count+1])) #appends "-"fact
            count =  count + 1
            continue
        elif len(required)<2:
            final_required.append([word])
        else:
            count = count + 1
            continue
        last_op = word
        count = count + 1
    return [final_result, final_required]

initial_kb=[]
initial_facts=[]
paths=[]
KB = []
f=open("/home/badcode/Desktop/AI/Inference_Engine/breakfast.txt", 'r')
for line in f:
    if not len(line):
        continue
    elif len(line.split())>1:
        initial_kb.append(line)
    else:
        initial_facts.append(line)

for line in initial_kb: #initalize clauses
    result, required = read_kb(line)
    init_clause = Clause(result, required)
    KB.append(init_clause)



new_path = PathToGoal(initial_facts)
paths.append(new_path)








