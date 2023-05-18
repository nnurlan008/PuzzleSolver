# this file contains utility function implementations
# in order to solve the problem
# first define the initial state: input from the user mostly
# goal state

import time
import copy
import matplotlib.pyplot as plt
import sys

#goal state:
goalState = [[1, 2, 3], [4, 5, 6], [7, 8, 0]]

#lets create Node class which will save input node
# with the following properties:
class Node:
    def __init__(self, node_state, node_depth=0, expanded=False):
        self.parent_nodes = []
        self.node_state = node_state # state of the node
        self.node_depth = node_depth # depth from depth 0; parent node depth + 1
        self.heuristic = 0 # heuristic cost of the node
        self.expanded = expanded # is this node expanded before?

    def get_state(self):
        return self.node_state

class Problem:
    def __init__(self, initial_state, goal_state, node=Node, length=3):
        self.initial_state = initial_state
        self.goal_state = goal_state
        self.node = node
        self.puzzle_length = length

    #def initial_state(self):
    #    return self.initial_state
    
    def goal_state(self):
        return self.goal_state
    
    def set_init_state(self, state):
        self.initial_state = state


def print_state(current_state):
    for i in current_state:
        print( "-------")
        string = "|"
        for k in i:
            string += str(k) + "|"
        print(string)
    print( "-------")
    
def move(current_state, action=0):
    # action = 0: move blank cell up
    # action = 1: move blank cell down
    # action = 2: move blank cell left
    # action = 3: move blank cell right
    
    for i in current_state:
        for k in i:
            if k == 0:
                index = (current_state.index(i), i.index(k))
    
    # up movement
    if action == 0:
        if index[0] != 0:
            current_state[index[0]][index[1]] = current_state[index[0] - 1][index[1]]
            current_state[index[0] - 1][index[1]] = 0
            return current_state
        else: 
            return None
        
    # down movement
    if action == 1:
        if index[0] != len(current_state)-1:
            current_state[index[0]][index[1]] = current_state[index[0] + 1][index[1]]
            current_state[index[0] + 1][index[1]] = 0
            return current_state
        else: 
            return None
        
    # left movement
    if action == 2:
        if index[1] != 0:
            current_state[index[0]][index[1]] = current_state[index[0]][index[1] - 1]
            current_state[index[0]][index[1] - 1] = 0
            return current_state
        else: 
            return None
        
    # right movement
    if action == 3:
        if index[1] != len(current_state)-1:
            current_state[index[0]][index[1]] = current_state[index[0]][index[1] + 1]
            current_state[index[0]][index[1] + 1] = 0
            return current_state
        else: 
            return None


# a function to create all possible nodes 
def possible_states(state_matrix):
    expansions_matrix = []

    up = copy.deepcopy(state_matrix)
    down = copy.deepcopy(state_matrix)
    left = copy.deepcopy(state_matrix)
    right = copy.deepcopy(state_matrix)

    expansions_matrix.append(move(up, 0))
    expansions_matrix.append(move(down, 1))
    expansions_matrix.append(move(left, 2))
    expansions_matrix.append(move(right, 3))

    return expansions_matrix




# check if there is blank in the input matrix
def is_state_valid(matrix, row):
    for i in range(row):
        for k in range(row):
            if matrix[i][k] == 0:
                return True
    return False

def get_algo():
    print("Now, you need to select the algorithm: ")
    print("1: Uniform Cost Search.")
    print("2: A* with the Misplaced Tile heuristic.")
    print("3: A* with the Manhattan Distance heuristic.")
    algo = input("Your choice: ")
    try:
        algo = int(algo)
    except ValueError:
        print("Invalid Input: " + algo)
    if algo < 1 or algo > 3:
        print("Enter 1, 2, or 3!")
    
    return algo

# function shown in the project pdf
def general_search(problem=Problem, function=1):
        
    time_started = time.time()

    my_queue = []
    visited_states = []
    n_visited = 0
    queue_size = 0
    max_queue_size = 0
    goal_state = problem.goal_state

    if function == 1:
        heuristic = 0 # heuristic is zero for ucs
    elif function == 2:
        heuristic = heuristic_misplaced(problem.initial_state, goal_state)
    elif function == 3:
        heuristic = heuristic_manhattan(problem.initial_state, goal_state)

    node = Node(problem.initial_state, 0, False)
    node.heuristic = heuristic
    
    my_queue.append(node)
    visited_states.append(node.node_state)
    queue_size += 1
    max_queue_size += 1

    while True:
        
        if function != 1:
            my_queue = sorted(my_queue, key=lambda x: (x.node_depth + x.heuristic, x.node_depth))

        if len(my_queue) == 0:
            print("Failure! No solution found within an hour!")
            return None, None, None
        
        next_node = my_queue.pop(0)
        queue_size -= 1

        if next_node.expanded == False:
            n_visited += 1
            next_node.expanded = True
        
        if n_visited != 1:
            print("Best node chosen to expand with g(n) = " + str(next_node.node_depth) + \
                   " and h(n) = " + str(next_node.heuristic) + ":")
            print_state(next_node.get_state())
        else:
            print("Expanding node: ")
            print_state(next_node.get_state())

        if next_node.get_state() == goal_state:
            
            print("Success:)")
            print("The total of "+str(n_visited-1)+" nodes have been expanded\
                  \nThe max number of nodes/states in the queue in one time instance is "\
                  + str(max_queue_size) + "\nTime taken is " + \
                    str((time.time()-time_started)*1000) + " seconds")
            print_state(next_node.get_state()) 
            return n_visited-1, max_queue_size, (time.time()-time_started)*1000 #, child_node.parent_nodes

        expansion = possible_states(next_node.get_state())
     
        for child_state in expansion:
            if is_state_visited(child_state, visited_states):
                #print_state(child_state)
                child_node = Node(child_state)
                if function == 1:
                    child_node.node_depth = next_node.node_depth + 1
                    child_node.heuristic = 0
                elif function == 2:
                    child_node.node_depth = next_node.node_depth + 1
                    child_node.heuristic = heuristic_misplaced(child_node.get_state(), goal_state)
                elif function == 3:
                    child_node.node_depth = next_node.node_depth + 1
                    child_node.heuristic = heuristic_manhattan(child_node.get_state(), goal_state)
                
                
                my_queue.append(child_node)
                visited_states.append(child_node.get_state())
                queue_size += 1
        
        if queue_size > max_queue_size:
            max_queue_size = queue_size

        if time.time() - time_started > 1*60*60*1000:
            print("An hour passed but no solution has been found. Exit!!!")

def is_state_visited(state, array):
    if state is None:
        return False
    
    for i in range(len(array)):
        if state == array[i]:
            return False
        
    return True


def heuristic_misplaced(current_state, goal_state):
    #goal_state = problem.goal_state()
    #current_state = problem.initial_state()
    h = 0
    length = len(current_state)

    for i in range(length):
        for j in range(length):
            if int(current_state[i][j]) != goal_state[i][j] and int(current_state[i][j]) != 0:
                h += 1
    return h

def heuristic_manhattan(current_state, goal_state):
    #goal_state = problem.goal_state()
    #current_state = problem.initial_state()
    h = 0
    length = len(current_state)
    gr, gc, r, c = 0, 0, 0, 0

    for l in range(1, length*length):
        for i in range(length):
            for j in range(length):
                if int(current_state[i][j]) == l:
                    r = i
                    c = j
                if goal_state[i][j] == l:
                    gr = i
                    gc = j
        h += abs(gr-r) + abs(gc-c)

    return h 


# a function to create a custom input and goal state
def create_states():
    print("Enter number of rows (=columns) in input or press Enter for 8-puzzle:")
    try:
        row_number = input() or int(3)
        row_number = int(row_number)
        if row_number <= 0:
            print("Invalid number for rows")
            raise ValueError
        
    except ValueError:
        print("Error: input a valid number for the number of rows in input")
        exit()

    print("The selected number of rows is:" + str(row_number))
    print("Now, let's create the input matrix or state")

    initial_state = []
    for i in range(row_number):
        print("Enter the " + str(i + 1) + 
              "-th row with space in between numbers and 0 for blank:")
        
        input_row = input()
        try:
            input_row = [int(a) for a in input_row.split()]
        except ValueError:
            print("Invalid input!")
            exit()

        initial_state.append(input_row)

    if not is_state_valid(initial_state, row_number):
        print("There is no blank symbol; 0 in the state matrix")
        return None, None
    
    print("initial state is as below:")
    print_state(initial_state)
        #print("There is an error in initial state. Check ")
    
    #let's create the default goal states:
    goal_state = [[(k+1) + (row_number*m) for k in range(row_number)] for m in range(row_number)]
    goal_state[row_number-1][row_number-1] = 0 # blank symbol
    
    #global goalState
    #goalState = goal_state

    print("Do you want to have default goal states: y/n, press Enter for y")
    print("Default goal state looks like:")
    print_state(goal_state)

    mode = input() or "y"
    if mode != "y":
        for i in range(row_number):
            print("Enter the " + str(i + 1) + 
              "-th row with space in between numbers and 0 for blank:")
        
        input_row = input()
        try:
            input_row = [int(a) for a in input_row.split()]
        except ValueError:
            print("Invalid input!")
            exit()

        goal_state.append(input_row)

    if not is_state_valid(initial_state, row_number):
        print("There is no blank symbol; 0 in the state matrix")
        return None, None
    
    return initial_state, goal_state

def check_solvability(state):
    length = len(state)
    total_inversion = 0
    for row in range(length):
        for column in range(length):
            total_inversion += find_inversion(state, row, column)
        
    if total_inversion % 2 == 1:
        return False
    return True 
    
def find_inversion(state, row, column):
    length = len(state)
    inversion = 0
    for i in range(length):
        for k in range(length):
            if i >= row and k >= column:
                if state[row][column] > state[i][k] and state[i][k] != 0:
                    inversion += 1
    return inversion

def plot():
    depth0 = [[1, 2, 3], [4, 5, 6], [7, 8, 0]]
    depth2 = [[1, 2, 3], [4, 5, 6], [0, 7, 8]]
    depth4 = [[1, 2, 3], [5, 0, 6], [4, 7, 8]]
    depth8 = [[1, 3, 6], [5, 0, 2], [4, 7, 8]]
    depth12 = [[1, 3, 6], [5, 0, 7], [4, 8, 2]]
    depth16 = [[1, 6, 7], [5, 0, 3], [4, 8, 2]]
    depth20 = [[7, 1, 2], [4, 8, 5], [6, 3, 0]]
    depth24 = [[0, 7, 2], [4, 6, 1], [3, 5, 8]]
    depth = [[[1, 2, 3], [4, 5, 6], [7, 8, 0]],
             [[1, 2, 3], [4, 5, 6], [0, 7, 8]],
             [[1, 2, 3], [5, 0, 6], [4, 7, 8]],
             [[1, 3, 6], [5, 0, 2], [4, 7, 8]],
             [[1, 3, 6], [5, 0, 7], [4, 8, 2]],
             [[1, 6, 7], [5, 0, 3], [4, 8, 2]],
             [[7, 1, 2], [4, 8, 5], [6, 3, 0]],
             [[0, 7, 2], [4, 6, 1], [3, 5, 8]]]
    depth_array = [0, 2, 4, 8, 12, 16, 20, 24]
    nodes_array1 = [] #contains #ofnodes expanded for each input for algo 1
    max_qs_array1 = [] #contains max queue size for each input for algo 1
    time1 = []
    nodes_array2 = [] #contains #ofnodes expanded for each input for algo 2
    max_qs_array2 = [] #contains max queue size for each input for algo 2
    time2 = []
    nodes_array3 = [] #contains #ofnodes expanded for each input for algo 3
    max_qs_array3 = [] #contains max queue size for each input for algo 3
    time3 = []
    problem = Problem(depth0, goalState, len(goalState))
    print_state(problem.goal_state)
    
    for i in range(len(depth_array)-1):
        problem.set_init_state(depth[i])
        number_nodes_expanded, max_queue_size, time = general_search(problem, 1)
        
        nodes_array1.append(number_nodes_expanded)
        max_qs_array1.append(max_queue_size)
        time1.append(time)

    for i in range(len(depth_array)):
        problem.set_init_state(depth[i])
        number_nodes_expanded, max_queue_size, time = general_search(problem, 2)
        
        nodes_array2.append(number_nodes_expanded)
        max_qs_array2.append(max_queue_size)
        time2.append(time)

    for i in range(len(depth_array)):
        problem.set_init_state(depth[i])
        number_nodes_expanded, max_queue_size, time = general_search(problem, 3)
        
        nodes_array3.append(number_nodes_expanded)
        max_qs_array3.append(max_queue_size)
        time3.append(time)
    
    print("nodes array1:")
    print(nodes_array1)
    
    print("max_queue array1")
    print(max_qs_array1)

    print("nodes array2:")
    print(nodes_array2)
    
    print("max_queue array2")
    print(max_qs_array2)

    print("nodes array3:")
    print(nodes_array3)
    
    print("max_queue array3")
    print(max_qs_array3)
    
    print("time3")
    print(time3)

    plt.plot(depth_array[0:-1], time1, marker='p', label='Uniform Cost Search')
    plt.plot(depth_array, time2, marker='p', label='Misplaced')
    plt.plot(depth_array, time3, marker='p', label='Manhattan')
    plt.xlabel("Solution Depth g(n)")
    #plt.ylabel("Expanded Nodes")
    #plt.title("Expanded Nodes vs Solution depth")
    
    #plt.ylabel("Maximum Queue Size")
    #plt.title("Maximum Queue Size vs Solution depth")

    plt.ylabel("Time in seconds")
    plt.title("Time vs Solution depth")
    plt.legend(loc="upper left")
    plt.grid()
    plt.margins(x=0, y=0)
    plt.xticks(depth_array)
    plt.yticks([*range(0, 180000, 10000)])
    plt.rc('xtick', labelsize=20) 
    plt.rc('ytick', labelsize=20) 

    plt.show()  





def main():
    initial_state, goal_state = create_states()
    if len(initial_state) <= 4:
        if goal_state == goalState:
            if check_solvability(initial_state):
                print("The puzzle is solvable.")
            else: 
                print("The puzzle is unsolvable.")
                sys.exit()
        else: print("Since the goal state is different" 
                    "the solvability check is not done. \n" 
                    "If the puzzle is unsolvable, the system will exit after some 1 hour:)")
    else: print("Solvability check cannot be done for this puzzle")

    algo = get_algo()
    #print_state(initial_state)
    #print_state(goal_state)
    problem = Problem(initial_state, goal_state, len(initial_state))

    print("Search Started")
    number_nodes_expanded, max_queue_size, time = general_search(problem, algo)
    #backtrace = input("Do you want to print the states in the solution path: y/[n]") or "n"

    #if backtrace == 'y':
    #    for i in parent_nodes:
    #        print_state(i.get_state())



if __name__ == "__main__":
    main()
