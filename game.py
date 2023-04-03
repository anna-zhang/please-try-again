#!/usr/bin/env python

from flask import Flask, request, make_response, render_template

#-----------------------------------------------------------------------

app = Flask(__name__) # set up Flask server

#-----------------------------------------------------------------------

# For each Flask function, can provide multiple paths
@app.route('/', methods=['GET'])
@app.route('/index', methods=['GET'])
def index():
    html = render_template('index.html')
    response = make_response(html)
    return response