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