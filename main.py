""" This app needs Flask to run. Use "pip install flask" to install. """

""" HOW TO RUN THIS APP
    Point your terminal to this folder, then execute this command (in Linux) :
        export FLASK_APP=main.py
        flask run
    Not sure how you would do that on Windows...
    For more information, visit their website : http://flask.pocoo.org
    """

from flask import Flask, render_template
from flask import request

app = Flask(__name__) # The web server
adj_matrix = []

""" A* Algorithm """
def AStar():
    path = []
    # Process adj_matrix here
    print("nanti ya, wkwk")
    return path

""" ROUTING RULES """
# Main page
@app.route("/",methods=["GET"])
def SendMain():
    return render_template("index.html")

# Send input to this address to be processed
@app.route("/ProcInput",methods=["POST"])
def ProcessInput():
    try:
        out = "HAHAHAHAHA\nYou send this : " + request.form["test"] + "."
    except(KeyError):
        out = "HAHAHAHAHA\nYou didn't send a thing."
    # Put input into adj_matrix
    # out = AStar();
    # Format out as JSON string
    return out

# Run the server
if (__name__) == '__main__':
    app.run()
