import heapq
from collections import deque

class Boxes:
    def __init__(self, box, east, north, west, south, isStart, isTrap, isGoal):
        self.box = box
        self.west = west
        self.north = north
        self.east = east
        self.south = south
        self.isStart = isStart
        self.isTrap = isTrap
        self.isGoal = isGoal
        self.cost = 1
        self.heuristic =0
    def __str__(self):
        return f"{self.box}"

# labels for boxes (for 8x8, change here for different map dimensions)
labels = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h']
num_row_boxes = 8

# storing boxes
boxes_list = []

for label in labels:
    row = []
    for i in range(1, num_row_boxes + 1):
        box = Boxes(f"{label}{i}", "null", "null", "null", "null", False, False, False)
        row.append(box)
    boxes_list.append(row)

for row in boxes_list:
    for box in row:
        print(box, end=" ")
    print()

#Read input
def read_input_data(file_path):
    with open(file_path, 'r') as file:
        lines = file.readlines()

    start_node = lines[0].split(":")[1].strip()
    goal_nodes = lines[1].split(":")[1].strip().split()
    trap_nodes = lines[2].split(":")[1].strip().split()
    walls = lines[3].split(":")[1].strip().split()

    return start_node, goal_nodes, trap_nodes, walls

# Read input data from the file
file_path = 'input_data.txt'
start_node, goal_Nodes, trap_Nodes, walls = read_input_data(file_path)

# print(len(walls))
for row in boxes_list:    
    for i in range(len(row)-1):
        isWall = row[i].box + "-" + row[i+1].box
        
        row[i].east = row[i+1].box
        row[i+1].west = row[i].box        
        if isWall in walls:
            row[i].east = "null"
            row[i+1].west = "null" 

for i in range(len(boxes_list) -1):
    for j in range(num_row_boxes):
        isCWall = boxes_list[i][j].box + "-" + boxes_list[i+1][j].box
        
        boxes_list[i][j].south = boxes_list[i+1][j].box
        boxes_list[i+1][j].north = boxes_list[i][j].box
        if isCWall in walls:
            boxes_list[i][j].south = "null"
            boxes_list[i+1][j].north = "null"

found_start = False

for i, row in enumerate(boxes_list):
    for j, box in enumerate(row):
        if box.box == start_node:
            box.isStart = True
            box.cost=0
            print(f"Found start node '{start_node}' at row: {i}, column: {j}")
            found_start = True
            break
    if found_start:
        break

# find trap nodes and goal nodes:
for row in boxes_list:
    for box in row:
        if box.box in trap_Nodes:
            box.isTrap = True
            box.cost = 7
        if box.box in goal_Nodes:
            box.isGoal = True

def is_valid_move(curr_box, next_box):
    return curr_box.south == next_box.box or curr_box.north == next_box.box or \
           curr_box.east == next_box.box or curr_box.west == next_box.box

def depth_first_search(start_node, goal_nodes, boxes_list):
    stack = [(start_node, [])]  # Initialize the stack with the start node and an empty path

    visited = set()

    while stack:
        current_node, path = stack.pop()

        if current_node in visited:
            continue

        visited.add(current_node)

        if current_node in goal_nodes:
            print(f"Goal node '{current_node}' reached!")
            print("Visited nodes:", visited)
            total_cost = sum(boxes_list[ord(node[0]) - ord('a')][int(node[1]) - 1].cost for node in path)
            print("Path is:",path)
            print("total cost =", total_cost)
            return path + [current_node]

        # Expand the current node's neighbors
        current_row = int(current_node[1]) - 1
        current_col = ord(current_node[0]) - ord('a')

        neighbors = []

        if current_row >= 0 and boxes_list[current_col][current_row].south != "null":
            neighbors.append(boxes_list[current_col][current_row].south)

        if current_row < len(boxes_list) - 1 and boxes_list[current_col][current_row].north != "null":
            neighbors.append(boxes_list[current_col][current_row].north)

        if current_col >= 0 and boxes_list[current_col][current_row].east != "null":
            neighbors.append(boxes_list[current_col][current_row].east)

        if current_col < len(boxes_list[0]) - 1 and boxes_list[current_col][current_row].west != "null":
            neighbors.append(boxes_list[current_col][current_row].west)

        for neighbor in neighbors:
            if neighbor not in visited:
                stack.append((neighbor, path + [current_node]))

def find_closest_goal(start_node, goal_nodes):
    closest_goal = goal_nodes[0]
    min_distance = manhattan_distance(start_node, closest_goal)

    for goal_node in goal_nodes[1:]:
        distance = manhattan_distance(start_node, goal_node)
        if distance < min_distance:
            min_distance = distance
            closest_goal = goal_node

    return closest_goal

def find_box_indexes(boxes_list, target_box):
    for i, row in enumerate(boxes_list):
        for j, box in enumerate(row):
            if box.box == target_box:
                return i, j
    return None  

    
def manhattan_distance(node, goal_node):
    # Extract x and y coordinates from node and goal_node
    node_x, node_y = int(node[1]), ord(node[0]) - ord('a') + 1
    goal_x, goal_y = int(goal_node[1]), ord(goal_node[0]) - ord('a') + 1

    # Calculate Manhattan distance
    distance = abs(node_x - goal_x) + abs(node_y - goal_y)
    return distance

def greedy_best_first_search(start_node, goal_nodes, boxes_list):
    priority_queue = []  # Priority queue to store nodes based on heuristic values

    # Calculate the initial heuristic value for the start node
    start_heuristic = manhattan_distance(start_node, goal_nodes[0])
    
    heapq.heappush(priority_queue, (start_heuristic, start_node, [start_node]))

    visited = set()  # Set to keep track of visited nodes

    while priority_queue:
        current_heuristic, current_node, path = heapq.heappop(priority_queue)
       

        # Check if the current node is a goal node
        if current_node in goal_nodes:
            print(f"Goal node '{current_node}' reached!")
            print("Visited nodes:", visited)
            total_cost = sum(boxes_list[ord(node[0]) - ord('a')][int(node[1]) - 1].cost for node in path)
            print("Path is:",path)
            print("total cost =", total_cost)
            return path  # Return the path taken to reach the goal

        # Expand the current node's neighbors
        current_row = int(current_node[1]) - 1
        current_col = ord(current_node[0]) - ord('a')

        neighbors = []

        if current_row >= 0 and boxes_list[current_col][current_row].south != "null":
            neighbors.append(boxes_list[current_col][current_row].south)

        if current_row < len(boxes_list) - 1 and boxes_list[current_col][current_row].north != "null":
            neighbors.append(boxes_list[current_col][current_row].north)

        if current_col >= 0 and boxes_list[current_col][current_row].east != "null":
            neighbors.append(boxes_list[current_col][current_row].east)

        if current_col < len(boxes_list[0]) - 1 and boxes_list[current_col][current_row].west != "null":
            neighbors.append(boxes_list[current_col][current_row].west)

        # Calculate the heuristic value for each neighbor and enqueue into the priority queue
        for neighbor in neighbors:
            if neighbor not in visited:
                heuristic = min(manhattan_distance(neighbor, goal) for goal in goal_nodes)
                heapq.heappush(priority_queue, (heuristic, neighbor,path + [neighbor]))
                visited.add(neighbor)

    print("Goal node not reachable!")
    print("Visited nodes:", visited)
def a_star_search(start_node, goal_nodes, boxes_list):
    priority_queue = []  # Priority queue to store nodes based on A* priority values

    # Calculate the initial heuristic value for the start node
    start_heuristic = manhattan_distance(start_node, goal_nodes[0])
    start_cost = 0  # Initial cost is 0
    heapq.heappush(priority_queue, (start_heuristic + start_cost, start_node,[start_node]))

    visited = set()  # Set to keep track of visited nodes
    while priority_queue:
        current_priority, current_node, path = heapq.heappop(priority_queue)

        # Check if the current node is a goal node
        if current_node in goal_nodes:
            print(f"Goal node '{current_node}' reached!")
            print("Visited nodes:", visited)
            total_cost = sum(boxes_list[ord(node[0]) - ord('a')][int(node[1]) - 1].cost for node in path)
            print("Path is:",path)
            print("total cost =", total_cost)
            
            return path  # Return the path taken to reach the goal

        # Expand the current node's neighbors
        current_row = int(current_node[1]) - 1
        current_col = ord(current_node[0]) - ord('a')

        neighbors = []

        if current_row >= 0 and boxes_list[current_col][current_row].south != "null":
            neighbors.append(boxes_list[current_col][current_row].south)

        if current_row < len(boxes_list) - 1 and boxes_list[current_col][current_row].north != "null":
            neighbors.append(boxes_list[current_col][current_row].north)

        if current_col >= 0 and boxes_list[current_col][current_row].east != "null":
            neighbors.append(boxes_list[current_col][current_row].east)

        if current_col < len(boxes_list[0]) - 1 and boxes_list[current_col][current_row].west != "null":
            neighbors.append(boxes_list[current_col][current_row].west)

        # Calculate the A* priority value for each neighbor and enqueue into the priority queue
        for neighbor in neighbors:
            if neighbor not in visited:
                path_cost = sum(boxes_list[ord(node[0]) - ord('a')][int(node[1]) - 1].cost for node in path)
                heuristic = min(manhattan_distance(neighbor, goal) for goal in goal_nodes)
                priority = heuristic + path_cost
                heapq.heappush(priority_queue, (priority, neighbor, path + [neighbor]))
                visited.add(neighbor)

    print("Goal node not reachable!")
    print("Visited nodes:", visited)

def uniform_cost_search(start_node, goal_nodes, boxes_list):
    priority_queue = []  # Priority queue to store nodes based on total cost (path cost)
    
    # Enqueue the start node with a cost of 0 and an empty path
    heapq.heappush(priority_queue, (0, start_node, [start_node]))

    visited = set()  # Set to keep track of visited nodes

    while priority_queue:
        current_cost, current_node, path = heapq.heappop(priority_queue)

        # Check if the current node is a goal node
        if current_node in goal_nodes:
            print(f"Goal node '{current_node}' reached!")
            print("Visited nodes:", visited)
            total_cost = sum(boxes_list[ord(node[0]) - ord('a')][int(node[1]) - 1].cost for node in path)
            print("Path is:",path)
            print("total cost =", total_cost)
            return path  # Return the path taken to reach the goal

        # Expand the current node's neighbors
        current_row = int(current_node[1]) - 1
        current_col = ord(current_node[0]) - ord('a')

        neighbors = []

        if current_row >= 0 and boxes_list[current_col][current_row].south != "null":
            neighbors.append(boxes_list[current_col][current_row].south)

        if current_row < len(boxes_list) - 1 and boxes_list[current_col][current_row].north != "null":
            neighbors.append(boxes_list[current_col][current_row].north)

        if current_col >= 0 and boxes_list[current_col][current_row].east != "null":
            neighbors.append(boxes_list[current_col][current_row].east)

        if current_col < len(boxes_list[0]) - 1 and boxes_list[current_col][current_row].west != "null":
            neighbors.append(boxes_list[current_col][current_row].west)

        for neighbor in neighbors:
            if neighbor not in visited:
                # Calculate the path cost from the start node to the neighbor
                new_cost = current_cost + boxes_list[current_col][current_row].cost
                heapq.heappush(priority_queue, (new_cost, neighbor, path + [neighbor]))
                visited.add(neighbor)

    print("Goal node not reachable!")
    print("Visited nodes:", visited)

def iterative_deepening_search(start_node, goal_nodes, boxes_list, max_depth):
    for depth_limit in range(1, max_depth + 1):
        print(f"\nSearching with depth limit: {depth_limit}")
        visited = set()
        start_box = find_box(boxes_list, start_node)
        result = dfs_with_depth_limit(start_box, goal_nodes, boxes_list, depth_limit, visited)
        if result is not None:
            print("Goal reached!")
            # print(f"Goal node '{result[result.__len__-1]}' reached!")
            total_cost = sum(boxes_list[ord(node[0]) - ord('a')][int(node[1]) - 1].cost for node in result)
            print("Path is:",result)
            print("total cost =", total_cost)
            return result
    print("Goal not reachable within the depth limit.")
    return None

def find_box(boxes_list, target_box):
    for row in boxes_list:
        for box in row:
            if box.box == target_box:
                return box
    return None

def dfs_with_depth_limit(current_node, goal_nodes, boxes_list, depth_limit, visited):
    
    visited.add(current_node.box)
    # for node in visited:
    #     print(node, end=" ")
    neighbors = []

    if current_node.box in goal_nodes:
        print(f"Goal node '{current_node}' reached!")
        print("Visited nodes:", visited)
        return [current_node.box]

    if depth_limit == 0:
        return None

    for neighbor_label in [current_node.north, current_node.east, current_node.south, current_node.west]:
        if neighbor_label != "null":
            neighbor = find_box(boxes_list, neighbor_label)
            neighbors.append(neighbor)
            if neighbor.box not in visited and is_valid_move(current_node, neighbor):
                result = dfs_with_depth_limit(neighbor, goal_nodes, boxes_list, depth_limit - 1, visited)
                if result is not None:
                    return [current_node.box] + result

    return None

def breadth_first_search(start_node, goal_nodes, boxes_list):
    queue = deque([(start_node, [])])  # Initialize the queue with the start node and an empty path

    visited = set()

    while queue:
        current_node, path = queue.popleft()

        if current_node in visited:
            continue

        visited.add(current_node)
        print(f"Visiting: {current_node}")

        if current_node in goal_nodes:
            print(f"Goal node '{current_node}' reached!")
            print("Visited nodes:", visited)
            total_cost = sum(boxes_list[ord(node[0]) - ord('a')][int(node[1]) - 1].cost for node in path)
            print("total cost =", total_cost)
            return path + [current_node]

        # Expand the current node's neighbors
        current_row = int(current_node[1]) - 1
        current_col = ord(current_node[0]) - ord('a')

        neighbors = []

        if current_row >= 0 and boxes_list[current_col][current_row].south != "null":
            neighbors.append(boxes_list[current_col][current_row].south)

        if current_row < len(boxes_list) - 1 and boxes_list[current_col][current_row].north != "null":
            neighbors.append(boxes_list[current_col][current_row].north)

        if current_col >= 0 and boxes_list[current_col][current_row].east != "null":
            neighbors.append(boxes_list[current_col][current_row].east)

        if current_col < len(boxes_list[0]) - 1 and boxes_list[current_col][current_row].west != "null":
            neighbors.append(boxes_list[current_col][current_row].west)

        for neighbor in neighbors:
            if neighbor not in visited:
                queue.append((neighbor, path + [current_node]))

    print("Goal node not reachable!")
    print("Visited nodes:", visited)
    return None

def menu():
    print("Choose a search algorithm:")
    print("1. Depth-First Search (DFS)")
    print("2. Greedy Best-First Search")
    print("3. A* Search")
    print("4. Uniform Cost Search")
    print("5. Iterative Deepening Search")
    print("6. Breadth first search")
    print("0. Exit")

    choice = input("Enter your choice (0-6): ")
    return choice

def main():
    # ... (your existing code)

    while True:
        choice = menu()

        if choice == '1':
            print("Running Depth-First Search:")
            dfs_result = depth_first_search(start_node, goal_Nodes, boxes_list)

        elif choice == '2':
            print("Running Greedy Best-First Search:")
            greedy_result = greedy_best_first_search(start_node, goal_Nodes, boxes_list)

        elif choice == '3':
            print("Running A* Search:")
            a_star_result = a_star_search(start_node, goal_Nodes, boxes_list)

        elif choice == '4':
            print("Running Uniform Cost Search:")
            uniform_cost_result = uniform_cost_search(start_node, goal_Nodes, boxes_list)

        elif choice == '5':
            max_depth = int(input("Enter the maximum depth for Iterative Deepening Search: "))
            print(f"Running Iterative Deepening Search with max depth {max_depth}:")
            iterative_deepening_result = iterative_deepening_search(start_node, goal_Nodes, boxes_list, max_depth)
        
        elif choice == '6':
            print("Running Breadth-First Search:")
            bfs_result = breadth_first_search(start_node, goal_Nodes, boxes_list)

        elif choice == '0':
            print("Exiting program.")
            break

        else:
            print("Invalid choice. Please enter a number between 0 and 5.")

if __name__ == "__main__":
    main()





