#!/usr/bin/env python

from flask import Flask, request, make_response, render_template, session, redirect, url_for

#-----------------------------------------------------------------------

app = Flask(__name__) # set up Flask server
app.secret_key = "a secret key for testing" # need to set a secret key in order to use session cookies

#-----------------------------------------------------------------------

# Home
@app.route('/', methods=['GET'])
@app.route('/index', methods=['GET'])
def index():
    html = render_template('index.html')
    response = make_response(html)
    session['player1'] = '' # player 1 name
    session['player2'] = '' # player 2 name
    session['moderator'] = None # which player is in this role right now, either 'player1' or 'player2'
    session['provider'] = None # which player is in this role right now, either 'player1' or 'player2'
    session['round_number'] = 0 # remember which round the pair of players is currently on
    session['card_number'] = 0 # remember which card the pair of players is currently on
    session['turn'] = None # remember which role is currently up, either 'provider' or 'moderator'
    return response

# How to Play
@app.route('/instructions', methods=['GET'])
def instructions():
    slide_number = 1
    html = render_template('instructions.html', slide=slide_number)
    response = make_response(html)
    return response

# Set Up Game: get names of players
@app.route('/setup', methods=['GET'])
def setup():
    html = render_template('setup.html')
    response = make_response(html)
    return response

# Set Up Game: save names of players in session cookies and redirect to start game
@app.route('/setup_game', methods=['POST'])
def setup_game():
    player1_name = request.form.get('moderator')
    player2_name = request.form.get('content-provider')
    response = redirect(url_for('role_call'))
    # Remember player names
    session['player1'] = player1_name
    session['player2'] = player2_name
    # Remember which player is fulfilling which role
    session['moderator'] = 'player1'
    session['provider'] = 'player2'
    session['turn'] = 'provider' # set which role is starting
    session['round_number'] = 1 # set which round number the pair of players is on
    session['card_number'] = 1 # set the card number for the round
    return response

# Play Game
@app.route('/play', methods=['GET'])
def play():
    html = render_template('game.html')
    response = make_response(html)
    return response


# Role Call
@app.route('/role_call', methods=['GET'])
def role_call():
    round_num = session['round_number'] # which round the players are on
    curr_role = session['turn'] # 'moderator' or 'provider'
    curr_player_num = session[curr_role] # 'player1' or 'player2'
    curr_player_name = session[curr_player_num] # player 1's name or player 2's name

    if not curr_player_name:
        return render_template('error.html')

    return render_template('role_call.html', curr_role=curr_role, curr_player_name=curr_player_name, round_num=round_num)
