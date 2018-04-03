""" This app needs Flask to run. Use "pip install flask" to install.
    For more information, visit their website : http://flask.pocoo.org """

from flask import Flask, render_template, request
import math
import json
import copy

app = Flask(__name__) # The web server
adj_matrix = []
nodes = []
heur_matrix = []
start = 0
end = 0

# "Euclidean Distance" using Haversine formula, because inputs are latitudes-longitudes
def Distance(lat1, lng1, lat2, lng2):
    # Converts degrees to radians
    lng1, lat1, lng2, lat2 = map(math.radians, [lng1, lat1, lng2, lat2])
    # The real Haversine formula
    a = math.sin((lat2 - lat1)/2)**2 + math.cos(lat1) * math.cos(lat2) * math.sin((lng2 - lng1)/2)**2
    c = 2 * math.asin(math.sqrt(a))
    return (6371000 * c) # 6371000 = radius of Earth in metres

# Fill heur_matrix with "Euclidean distance" between nodes
def GenHeur():
    global heur_matrix
    for s_node in nodes:
        heur_matrix.append([])
        for t_node in nodes:
            dist = Distance(s_node["lat"],s_node["lng"],t_node["lat"],t_node["lng"])
            heur_matrix[len(heur_matrix) - 1].append(copy.copy(dist))

# Returns live node cost to solution
def NodeCost(a_live_node):
    return (a_live_node[1] + a_live_node[2])

# A* Algorithm
def AStar():
    global adj_matrix, nodes, heur_matrix, start, end
    GenHeur() # Generate heuristic data
    live_nodes = [] # Store live nodes here
    results = [] # Store results here

    # Generating, for the first time, live nodes from the starting point
    i = 1
    for dist in adj_matrix[start-1]:
        if (dist != -1):
            live_nodes.append([[i,start], dist, heur_matrix[i-1][end-1], []])
            # Last part of each element is a list of visited nodes. Now, we must initialize it.
            for j in range(len(nodes)):
                live_nodes[len(live_nodes)-1][3].append(False)
            # Marks starting node and node i (in map) as visited
            live_nodes[len(live_nodes)-1][3][start-1] = True
            live_nodes[len(live_nodes)-1][3][i-1] = True
        i = i + 1
    # Searching for the best (minimum) cost between those live nodes
    best_live_node = live_nodes[0]
    for i in range(1,len(live_nodes)):
        if (NodeCost(best_live_node) > NodeCost(live_nodes[i])):
            best_live_node = live_nodes[i]
    print(best_live_node[0])

    # Loop until the best live node reaches the solution
    while(best_live_node[0][0] != end):
        # Generates new live nodes
        i = 1
        for dist in adj_matrix[best_live_node[0][0] - 1]:
            if ((dist != -1) and not best_live_node[3][i-1]):
                live_nodes.append([[i] + best_live_node[0],best_live_node[1] + dist,heur_matrix[i-1][end-1], copy.copy(best_live_node[3])])
                live_nodes[len(live_nodes)-1][3][i-1] = True # Marks this node (in map) as visited
            i = i + 1
        # Deletes parent node from live_nodes
        live_nodes.remove(best_live_node)
        # Determining which live node is the best
        best_live_node = live_nodes[0]
        for i in range(1,len(live_nodes)):
            if (NodeCost(best_live_node) > NodeCost(live_nodes[i])):
                best_live_node = live_nodes[i]
        print(best_live_node[0])

    print("FOUND : " + str(best_live_node[0]) + " with dist. : " + str(NodeCost(best_live_node)))
    # Moves best_live_node to results
    results.append(copy.copy(best_live_node))
    # Deletes best_live_node from live_nodes
    live_nodes.remove(best_live_node)
    # Checks whether there's a node that still has lower cost than this best_live_node
    # Note that this RARELY happens
    print("Checking for more...")
    ExistShorter = False
    for node in live_nodes:
        if (NodeCost(results[0]) >= NodeCost(node)):
            ExistShorter = True
            best_live_node = node

    while (ExistShorter):
        # If it exists, expand that node
        while((best_live_node[0][0] != end) and ExistShorter):
            # Generates new live nodes
            i = 1
            for dist in adj_matrix[best_live_node[0][0] - 1]:
                if ((dist != -1) and not best_live_node[3][i-1]):
                    live_nodes.append([[i] + best_live_node[0],best_live_node[1] + dist,heur_matrix[i-1][end-1], copy.copy(best_live_node[3])])
                    live_nodes[len(live_nodes)-1][3][i-1] = True # Marks this node (in map) as visited
                i = i + 1
            # Deletes parent node from live_nodes
            live_nodes.remove(best_live_node)
            # Determining which live node is the best
            best_live_node = live_nodes[0]
            for i in range(1,len(live_nodes)):
                if (NodeCost(best_live_node) > NodeCost(live_nodes[i])):
                    best_live_node = live_nodes[i]
            print(best_live_node[0])

            # Checks if the best_live_node is still shorter than the current result
            for curRes in results:
                if (NodeCost(curRes) < NodeCost(best_live_node)):
                        ExistShorter = False

        # Checks if the best_live_node reaches end node and it is shorter than current results
        if ((best_live_node[0][0] == end) and ExistShorter):
            print("FOUND : " + str(best_live_node[0]) + " with dist. : " + str(NodeCost(best_live_node)))
            results.append(copy.copy(best_live_node))
            live_nodes.remove(best_live_node)

        # Checks whether there's still more nodes to expand
        print("Checking for more...")
        ExistShorter = False
        for node in live_nodes:
            for curRes in results:
                if (NodeCost(curRes) > NodeCost(best_live_node)):
                        ExistShorter = True

    print("Done.")
    print("Result : ")
    for res in results:
        print("FOUND : " + str(res[0]) + " with dist. : " + str(NodeCost(res)))
    return results


""" ROUTING RULES """
# Main page
@app.route("/",methods=["GET"])
def SendMain():
    return render_template("index.html")

# Send input to this address to be processed
@app.route("/ProcInput",methods=["POST"])
def ProcessInput():
    global adj_matrix, nodes, start, end, heur_matrix
    # Clears internal data struct
    heur_matrix = []
    status = 0
    path = []
    try:
        # Reading received data and putting it into internal data struct
        inp = json.JSONDecoder().decode(request.form["input"])
        nodes = copy.deepcopy(inp["node_list"])
        print("Received " + str(len(nodes)) + " nodes.")
        adj_matrix = copy.deepcopy(inp["matrix"])
        start = int(inp["start"])
        end = int(inp["end"])
        if (start < 0):
            status = 2
        elif (end > (len(nodes)+1)):
            status = 3
        else:
            # Run A* algo
            path = AStar()
    except(ValueError):
        # That means that start/end node is not entered
        status = 1
    except(KeyError):
        # That means no data received/data corrupt
        status = -999

    # Format out as JSON string
    out = json.JSONEncoder().encode({"status" : status, "path" : path})
    return out

# Run the server
if (__name__) == '__main__':
    app.run()
