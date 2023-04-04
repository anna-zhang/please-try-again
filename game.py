#!/usr/bin/env python

from flask import Flask, request, make_response, render_template

#-----------------------------------------------------------------------

app = Flask(__name__) # set up Flask server

#-----------------------------------------------------------------------

# Home
@app.route('/', methods=['GET'])
@app.route('/index', methods=['GET'])
def index():
    html = render_template('index.html')
    response = make_response(html)
    return response

# How to Play
@app.route('/instructions', methods=['GET'])
def instructions():
    slide_number = 1
    html = render_template('instructions.html', slide=slide_number)
    response = make_response(html)
    return response

# Play Game
@app.route('/play', methods=['GET'])
def play():
    html = render_template('game.html')
    response = make_response(html)
    return response