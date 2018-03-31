""" This app needs Flask to run. Use "pip install flask" to install. """

""" HOW TO RUN THIS APP
    Point your terminal to this folder, then execute this command (in Linux) :
        export FLASK_APP=main.py
        flask run
    Not sure how you would do that on Windows...
    For more information, visit their website : http://flask.pocoo.org
    """

from flask import Flask, render_template

app = Flask(__name__) # The web server

""" ROUTING RULES """
@app.route("/",methods=["GET"])
def SendMain():
    return render_template("index.html")

# Run the server
if (__name__) == '__main__':
    app.run()
