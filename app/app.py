# Github link: https://github.com/StephanieChiang/3-Brain-Cells


class Node:
    def __init__(self, state="", depth=0, action="0"):
        self.state = state
        self.isVisited = False
        self.depth = depth
        self.action = action


def print_board(size, values_string):
    values = list(values_string)
    counter = 0
    for value in values:
        counter += 1
        print(value, end=" ")
        if counter == size:
            counter = 0
            print()


def string_to_array(size, state_string):
    new_list = []
    split_string = []

    for i in range(0, len(state_string), size):
        split_string.append(state_string[i:i + size])

    for i in split_string:
        row = list(i)
        new_list.append(row)

    return new_list


def array_to_string(size, state_array):
    state_string = ""

    for i in state_array:
        state_string += ''.join(i)

    return state_string


def flip(value):
    if value == "1":
        return "0"
    else:
        return "1"


def get_position(row, col):
    position = ""
    letter = chr(ord(str(row)) + 17)
    number = col + 1
    position += letter + str(number)

    return position


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

            new_states.append(Node(array_to_string(size, new_board), depth, position))

    return new_states


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


def dfs(size, max_depth, values):
    start_node = Node(values, 1, "0")
    open_list = [start_node]
    closed_list = []
    solution = []
    search_path = []
    found = False

    while open_list:
        current_state = open_list.pop(0)
        search_path.append(current_state)

        if len(solution) != 0:
            last = solution[-1]

            if current_state.depth < last.depth:
                new_solution = []
                for i in solution:
                    if i.depth < current_state.depth:
                        new_solution.append(i)

                solution = new_solution

        solution.append(current_state)

        if all(s == "0" for s in current_state.state):
            found = True
            break
        else:

            if current_state.depth < max_depth:
                new_boards = generate_options(size, current_state)

                closed_list.append(current_state)

                unique_boards = unique_states(new_boards, open_list, closed_list)

                unique_boards.sort(key=lambda x: x.state)

                open_list = unique_boards + open_list

    if all(s == "0" for s in current_state.state):
        print("Search complete")

        print("final board")

        print_board(size, current_state.state)
    else:
        print("No solution found")
        solution = ["no solution"]

    answer = (found, [solution, search_path])

    return answer


def start():
    f = open("input.txt", "r")
    counter = 0

    for x in f:
        commands = x.split()
        size = int(commands[0])
        max_depth = int(commands[1])
        max_search = int(commands[2])
        values = commands[3]

        results = dfs(size, max_depth, values)
        file_name = str(counter) + "_dfs_solution.txt"

        f = open(file_name, "w")

        if results[0]:
            for i in results[1][0]:
                f.write(i.action + " " + i.state + "\n")

            f.close()
        else:
            f.write("no solution")

        file_name = str(counter) + "_dfs_search.txt"

        f = open(file_name, "w")

        for i in results[1][1]:
            f.write("0 0 0 " + i.state + "\n")

        f.close()

        counter += 1


# ------------------ Start code here ------------------

start()
