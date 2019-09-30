import collections

class Queue:
    def __init__(self):
        self.elements = collections.deque()

    def empty(self):
        return len(self.elements) == 0

    def put(self, x):
        self.elements.append(x)

    def get(self):
        return self.elements.popleft()

def BFS(graph, start, goal=3):
    frontier = Queue()
    frontier.put(start)
    came_from = {}
    came_from[start] = None

    while not frontier.empty():
        current = frontier.get()

        if graph[current] == goal:
            return came_from, current, True

        neighbours = []
        for n in range(current[1] - 1, current[1] + 2):
            for m in range(current[0] - 1, current[0] + 2):
                if not (n == current[1] and m == current[0]) and n > -1 and m > -1 and n < graph.shape[0] and m < graph.shape[1] and graph[current] != 2:
                    neighbours.append((m,n))

        for neighbour in neighbours:
            if neighbour not in came_from:
                frontier.put(neighbour)
                came_from[neighbour]=current

    return came_from,current, False

class Stack:
    def __init__(self):
        self.elements=collections.deque()

    def empty(self):
        return len(self.elements) == 0

    def put(self, x):
        self.elements.appendleft(x)

    def get(self):
        return self.elements.popleft()

def DFS(graph, start, goal=3):
    frontier = Stack()
    frontier.put(start)
    came_from = {}
    came_from[start] = None

    while not frontier.empty():
        current = frontier.get()

        if graph[current] == goal:
            return came_from, current, True

        neighbours = []
        for n in range(current[1] - 1, current[1] + 2):
            for m in range(current[0] - 1, current[0] + 2):
                if not (n == current[1] and m == current[0]) and n > -1 and m > -1 and n < graph.shape[0] and m < graph.shape[1] and graph[current] != 2:
                    neighbours.append((m,n))

        neighbours.reverse()
        for neighbour in neighbours:
            if neighbour not in came_from:
                frontier.put(neighbour)
                came_from[neighbour]=current

    return came_from,current, False

class PriorityQueue:
    def __init__(self):
        self.elements = {}

    def empty(self):
        return len(self.elements) == 0

    def put(self, x, priority):
        self.elements[x] = priority

    def get(self):
        best_item = None
        best_priority = None
        for item, priority in self.elements.items():
            if best_priority is None or priority < best_priority:
                best_item = item
                best_priority = priority

        del self.elements[best_item]

        return best_item

def Dijkstra(graph, priorities, start, goal = 3):

    frontier = PriorityQueue()

    frontier.put(start,0)

    came_from = {}
    came_from[start] = None

    cost_so_far = {}
    cost_so_far[start] = 0

    while not frontier.empty():

        current = frontier.get()

        if graph[current] == goal:
                return came_from, current, True

        neighbours = []
        for n in range(current[1]-1, current[1]+2):
            for m in range(current[0]-1, current[0]+2):
                if not (n==current[1] and m==current[0]) and n > -1 and m >-1 and n < graph.shape[1] and m < graph.shape[0] and graph[current] != 2:
                    neighbours.append((m,n))

        for neighbour in neighbours:
            new_cost = cost_so_far[current]+priorities[neighbour]
            if neighbour not in cost_so_far or new_cost < cost_so_far[neighbour]:
                cost_so_far[neighbour] = new_cost
                frontier.put(neighbour,new_cost)
                came_from[neighbour] = current

    return came_from, current, False

def heuristic(a,b):
    (x1, y1) = a
    (x2, y2) = b
    return abs(x1 - x2) + abs(y1 - y2)

def a_star(graph, priorities, start, end, goal=3):
    frontier = PriorityQueue()
    frontier.put(start,0)

    came_from = {}
    came_from[start] = None

    cost_so_far = {}
    cost_so_far[start] = 0

    while not frontier.empty():

        current = frontier.get()

        if graph[current] == goal:
            return came_from, current, True

        neighbours = []
        for n in range(current[1]-1,current[1]+2):
            for m in range(current[0]-1,current[0]+2):
                if not (n==current[1] and m==current[0]) and n > -1 and m > -1 and n < graph.shape[0] and m < graph.shape[1] and graph[current] != 2:
                    neighbours.append((m,n))

        for neighbour in neighbours:
            new_cost = cost_so_far[current] + priorities[neighbour] + heuristic(neighbour, end)
            if neighbour not in cost_so_far or new_cost< cost_so_far[neighbour]:
                cost_so_far[neighbour] = new_cost
                frontier.put(neighbour,new_cost)
                came_from[neighbour] = current

        print (cost_so_far)

    return came_from, current, False

def reconstruct_path(came_from, start, goal):
    current = goal
    path = []
    while current != start:
        path.append(current)
        current = came_from[current]
    path.append(start)
    path.reverse()
    return path