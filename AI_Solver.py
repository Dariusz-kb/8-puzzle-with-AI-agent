from heapq import heappush, heappop

#The Manhattan Distance is calculating the total number of moves each tile is away from its start to goal position,
# assuming it can move directly to the goal position without any obstacles.
def manhattan_distance(state, goal_state):
    distance = 0
    #get size of puzzle board
    size = int(len(state) ** 0.5)
    #start loop to go through each tile in a state 
    for i in range(len(state)):
        if state[i] == 0: # ignore empty tile
            continue
        #get coordinates for row, col for current tile using divmod function
        current_row, current_col = divmod(i, size)
        #get the coordinates where the current tile should be
        goal_row, goal_col = divmod(goal_state.index(state[i]), size)
        #calculate distance
        distance += abs(current_row - goal_row) + abs(current_col - goal_col)
    return distance

def get_neighbors(state):
    # get size of puzzle board
    size = int(len(state) ** 0.5)
    # get position of empty tile
    zero_index = state.index(0)
    
    # initialise empty neighbors list
    neighbors = []
    # list with all possible moves up, down, left, right contains tuples with coordinates
    moves = [(-1, 0), (1, 0), (0, -1), (0, 1)]
    #get coordinates of for zero index 
    x, y = divmod(zero_index, size)
    
    # start for loop to go through the list of moves
    for dx, dy in moves:
        # get new coordinates for empty tile after move
        nx, ny = x + dx, y + dy
        # if statement to check if move in direction is allowed
        if 0 <= nx < size and 0 <= ny < size:
            # calculate new index for empty tile after move in direction
            new_index = nx * size + ny
            # create a copy of entire state list
            new_state = state[:]
            #swap places of empty tile and and a neighbor tile
            new_state[zero_index], new_state[new_index] = new_state[new_index], new_state[zero_index]
            # add new state into neighbor states array
            neighbors.append(new_state)
    # return array with the neighbor states
    return neighbors

#Function reconstruct_path is designed to trace back the path from a final 
#state to starting state of the puzzle after A* algorithm has found a solution.
#Function takes 2 arguments came_from and current which are the previous and current states
def reconstruct_path(came_from, current):
    #add current state, which is final state of the puzzles to the total path
    total_path = [current]
    # start while loop, get every state from came_from list and assigns that to current
    while current in came_from:
        current = came_from[current]
        #add the state to total path
        total_path.append(current)
    #Return total path with all the states in reversed order
    return total_path[::-1]

# A* algorithm takes 2 arguments start state and goal state
def a_star(start, goal):
    #create empty heap open_set into which the new elements will be added
    # It acts as a priority queue where the element with the lowest value is always at the front.
    open_set = []
    # heappush provides an implementation of the heap queue algorithm (priority queue algorithm)
    #by adding elements as tuples that include the Manhattan distance as a heuristic followed by the actual cost and the state itself,
    # the heapq automatically sorts the heap so that the element with the lowest heuristic cost is always the first to be popped.
    # This ensures that the A* algorithm explores the most promising nodes first, according to the heuristic.
    heappush(open_set, (manhattan_distance(start, goal), 0, start))
    #create empty dictionary came_from which will be used to keep track of the path
    # from the start state to each state visited by the algorithm.
    # This will allow for the reconstruction of the shortest path once the goal is reached
    came_from = {}
    # initialize a dictionary g_score for tracking of path costs with a single entry where the key is the starting state
    # (converted to a tuple for immutability), and the value is 0 because the cost from
    # the start state to itself its always 0.
    g_score = {tuple(start): 0}
    global states_checked
    
    # Initialize the state counter to track total number of states checked by algorithm
    states_checked = 0

    # start of while loop
    while open_set:
        #Multiple assignment statement, ignores the first value returned by heapq.heappop(open_set)
        _, current_cost, current = heappop(open_set)
        #convert current state into immutable tuple
        current_tuple = tuple(current)
        # Increment the state counter
        states_checked += 1
        #Check if current state is a goal state, if it is reconstruct the path 
        if current == goal:
            return reconstruct_path(came_from, current_tuple), states_checked
        #loop through the neighbor list for a current state and for each neighbor estimate g score
        for neighbor in get_neighbors(current):
            #estimated g score is equal to g score of current tuple +1
            estimated_g_score = g_score[current_tuple] + 1
            #convert neighbor state into tuple
            neighbor_tuple = tuple(neighbor)
            #Check if neighbor state not in dictionary g score or 
            # estimated g score is less than g score of neighbor already in dictionary 
            if neighbor_tuple not in g_score or estimated_g_score < g_score[neighbor_tuple]:
                #update came_from dictionary with the key neighbor state by the value of current state
                came_from[neighbor_tuple] = current_tuple
                #update dictionary g score for the key neighbor by the value of estimated g score
                g_score[neighbor_tuple] = estimated_g_score
                # calculate f score for A* algorithm ( f(x)= g(x)+h(x) )
                f_score = estimated_g_score + manhattan_distance(neighbor, goal)
                #push neighbor state along with f score and current cost into open set heap
                heappush(open_set, (f_score, current_cost + 1, neighbor))

    return None  # No solution


