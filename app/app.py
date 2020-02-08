class Node:
    def __init__(self, state="", depth=0, action="0"):
        self.state = state
        self.isVisited = False
        self.depth = depth
        self.action = action