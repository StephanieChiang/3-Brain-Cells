# Github link: https://github.com/StephanieChiang/3-Brain-Cells
# Reference: COMP 472 State Space Search Lecture Slides


# Node class which contains board's current state and its information
class Node:
    def __init__(self, state="", depth=0, action="0", path=[], f=0, g=0, h=0):
        self.state = state
        self.isVisited = False
        self.depth = depth
        self.action = action
        self.path = path
        self.f = f
        self.g = g
        self.h = h


# Prints board in easy to read format
def print_board(size, values_string):
    values = list(values_string)
    counter = 0
    for value in values:
        counter += 1
        print(value, end=" ")
        if counter == size:
            counter = 0
            print()


# Converts board state in string format to array format
def string_to_array(size, state_string):
    new_list = []
    split_string = []

    for i in range(0, len(state_string), size):
        split_string.append(state_string[i:i + size])

    for i in split_string:
        row = list(i)
        new_list.append(row)

    return new_list


# Converts board state in array format to string format
def array_to_string(size, state_array):
    state_string = ""

    for i in state_array:
        state_string += ''.join(i)

    return state_string


# Returns opposite value of a token
def flip(value):
    if value == "1":
        return "0"
    else:
        return "1"


# Returns board position of a token based on its array index
def get_position(row, col):
    position = ""
    letter = chr(ord(str(row)) + 17)
    number = col + 1
    position += letter + str(number)

    return position


# Calculate heuristic for each board from a bfs search
def heuristic_bfs(boards):
    for i in boards:
        split_string = list(i.state)
        h = split_string.count("1")
        i.h = h
        i.f = h

    return boards


# Calculate heuristic for each board from a A* search
def heuristic_a_star(boards):
    for i in boards:
        split_string = list(i.state)
        h = split_string.count("1")
        i.h = h
        i.g = i.depth - 1
        i.f = h + i.depth - 1

    return boards


# Generate possible child nodes given a current state of a board
def generate_options(size, current_state):
    new_states = []
    depth = current_state.depth + 1

    for i in range(size):
        for j in range(size):
            new_board = string_to_array(size, current_state.state)

            # flip selected position
            # row:i col:j
            new_board[i][j] = flip(new_board[i][j])
            position = get_position(i, j)

            # flip top
            row = i - 1
            if row >= 0:
                new_board[row][j] = flip(new_board[row][j])

            # flip bottom
            row = i + 1
            if row < size:
                new_board[row][j] = flip(new_board[row][j])

            # flip left
            col = j - 1
            if col >= 0:
                new_board[i][col] = flip(new_board[i][col])

            # flip right
            col = j + 1
            if col < size:
                new_board[i][col] = flip(new_board[i][col])

            new_state = array_to_string(size, new_board)
            new_node = Node(new_state, depth, position, current_state.path + [position + " " + new_state])
            new_states.append(new_node)

    return new_states


# Return only boards that have not been used in either the open list or closed list
def unique_states(children, open_list, closed_list):
    joined_list = open_list + closed_list
    filtered_states = []

    for i in children:
        duplicate = False
        for j in joined_list:
            if j.state == i.state:
                duplicate = True

        if not duplicate:
            filtered_states.append(i)

    return filtered_states


# Dfs function
def dfs(size, max_depth, values):
    # Create starting node and its open and closed list
    start_node = Node(values, 1, "0", ["0 " + values])
    open_list = [start_node]
    closed_list = []
    search_path = []

    while open_list:
        # Use the first item on open list, and append this node to search path since this node will be evaluated
        current_state = open_list.pop(0)
        search_path.append(current_state)

        # If goal state is achieved, break out of loop
        if all(s == "0" for s in current_state.state):
            break
        else:

            # If depth limit is not reached, generate more boards
            if current_state.depth < max_depth:
                new_boards = generate_options(size, current_state)

                closed_list.append(current_state)

                unique_boards = unique_states(new_boards, open_list, closed_list)

                # Sort generated boards based on position of first white token
                unique_boards.sort(key=lambda x: x.state)

                open_list = unique_boards + open_list

    # Check is goal state is achieved or not
    if all(s == "0" for s in current_state.state):
        print("Search complete")
        print("final board")
        solution = current_state.path
        print_board(size, current_state.state)
    else:
        print("No solution found")
        solution = ["no solution"]

    # Returns solution path and search path as a tuple
    answer = (solution, search_path)

    return answer


# Bfs and A* function. The algorithm is chosen based on the boolean value of a_star that is used as parameter
def search_informed(size, max_search, values, a_star):
    start_node = Node(values, 1, "0", ["0 " + values])

    # Calculate heuristic for start node
    split_string = list(start_node.state)
    h = split_string.count("1")

    # Check whether to use bfs or A* algorithm to calculate appropriate heuristic
    if a_star:
        start_node.h = h
        start_node.g = start_node.depth - 1
        start_node.f = h + start_node.depth - 1
    else:
        start_node.h = h
        start_node.f = h

    open_list = [start_node]
    closed_list = []
    search_path = []

    while open_list:
        # Use the first item on open list, and append this node to search path since this node will be evaluated
        current_state = open_list.pop(0)
        search_path.append(current_state)

        # If goal state is achieved, break out of loop
        if all(s == "0" for s in current_state.state):
            break
        else:
            # If search limit is reached, break out of loop
            if len(search_path) < max_search:
                new_boards = generate_options(size, current_state)

                closed_list.append(current_state)

                unique_boards = unique_states(new_boards, open_list, closed_list)

                # Check whether to use bfs or A* algorithm to calculate appropriate heuristic
                boards_heuristic = heuristic_a_star(unique_boards) if a_star else heuristic_bfs(unique_boards)

                open_list = boards_heuristic + open_list

                # Sort boards based on heuristic value and then by position of first white token
                open_list.sort(key=lambda x: (x.f, x.state))
            else:
                break

    # Check is goal state is achieved or not
    if all(s == "0" for s in current_state.state):
        print("Search complete")
        print("final board")
        solution = current_state.path
        print_board(size, current_state.state)
    else:
        print("No solution found")
        solution = ["no solution"]

    # Returns solution path and search path as a tuple
    answer = (solution, search_path)

    return answer


# Function to write solution path to file
def write_solution(file_name, results):
    f = open(file_name, "w")

    for i in results:
        f.write(i + "\n")

    f.close()


# Function to write search path to file
def write_search(file_name, results):
    f = open(file_name, "w")

    for i in results:
        f.write("{} {} {} {} \n".format(i.f, i.g, i.h, i.state))

    f.close()


# Function used to start code
def start():
    f = open("input.txt", "r")
    counter = 0

    for x in f:
        commands = x.split()
        size = int(commands[0])
        max_depth = int(commands[1])
        max_search = int(commands[2])
        values = commands[3]

        results_dfs = dfs(size, max_depth, values)
        file_name = str(counter) + "_dfs_solution.txt"
        write_solution(file_name, results_dfs[0])
        file_name = str(counter) + "_dfs_search.txt"
        write_search(file_name, results_dfs[1])

        results_bfs = search_informed(size, max_search, values, False)
        file_name = str(counter) + "_bfs_solution.txt"
        write_solution(file_name, results_bfs[0])
        file_name = str(counter) + "_bfs_search.txt"
        write_search(file_name, results_bfs[1])

        results_astar = search_informed(size, max_search, values, True)
        file_name = str(counter) + "_astar_solution.txt"
        write_solution(file_name, results_astar[0])
        file_name = str(counter) + "_astar_search.txt"
        write_search(file_name, results_astar[1])

        counter += 1


# ------------------ Start code here ------------------

start()
