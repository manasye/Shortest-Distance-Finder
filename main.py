""" This app needs Flask to run. Use "pip install flask" to install. """

""" HOW TO RUN THIS APP
    Point your terminal to this folder, then execute this command (in Linux) :
        export FLASK_APP=main.py
        flask run
    Not sure how you would do that on Windows...
    For more information, visit their website : http://flask.pocoo.org
    """

from flask import Flask, render_template, request
import math
import json
import copy

app = Flask(__name__) # The web server
<<<<<<< HEAD
adj_matrix = []
=======
adj_matrix = [];
nodes = [];
heur_matrix = [];
start = "";
end = "";
>>>>>>> 5f9360781e0dd1c858f7c4c155e07f0ae5f3cfdd

# Euclidean Distance using Haversine formula, because inputs are latitudes-longitudes
def Distance(lat1, lng1, lat2, lng2):
    # Converts degrees to radians
    lng1, lat1, lng2, lat2 = map(math.radians, [lng1, lat1, lng2, lat2])
    # The real Haversine formula
    a = math.sin((lat2 - lat1)/2)**2 + math.cos(lat1) * math.cos(lat2) * math.sin((lng2 - lng1)/2)**2
    c = 2 * math.asin(math.sqrt(a))
    return (6371000 * c) # 6371000 = radius of Earth in metres

# Fill heur_matrix with Euclidean distance between nodes
def GenHeur():
    global heur_matrix
    i = 0
    for s_node in nodes:
        heur_matrix.append([]);
        for t_node in nodes:
            dist = Distance(s_node["lat"],s_node["lng"],t_node["lat"],t_node["lng"])
            heur_matrix[i].append(copy.copy(dist))
        i = i + 1
    print(heur_matrix)

# A* Algorithm
def AStar():
    GenHeur();
    path = []
    # Process adj_matrix here

    return path

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
    status = ''
    path = []
    try:
        # Reading received data and putting it into internal data struct
        inp = json.JSONDecoder().decode(request.form["input"])
        print("Accessing node_list...")
        nodes = copy.deepcopy(inp["node_list"])
        print("Accessing matrix...")
        adj_matrix = copy.deepcopy(inp["matrix"])
        print("Accessing starting point...")
        start = inp["start"]
        print("Accessing end point...")
        end = inp["end"]
        status = 0
        # Run A* algo
        path = AStar();
    except(KeyError):
        # That means no data received/data corrupt
        status = -999

    # Format out as JSON string
    out = json.JSONEncoder().encode({"status" : status, "path" : path})
    return out

# Run the server
if (__name__) == '__main__':
    app.run()
