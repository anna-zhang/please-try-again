#!/usr/bin/env python

from flask import Flask, request, make_response, render_template, session, redirect, url_for
from cards_list import Card, cards, all_card_indices, remaining_card_indices
import os
from werkzeug.utils import secure_filename
import random


#-----------------------------------------------------------------------

UPLOAD_FOLDER = os.path.join('static', 'uploads') # static folder is the default Flask folder for static files

#-----------------------------------------------------------------------

app = Flask(__name__) # set up Flask server
app.secret_key = "a secret key for testing" # need to set a secret key in order to use session cookies
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER # configure the file upload folder

#-----------------------------------------------------------------------

# Get a random card, returns the index of that card in cards list
def get_random_card():
    global remaining_card_indices
    global all_card_indices

    if len(remaining_card_indices) == 0: # restart
        random_card = -1 # no more cards left
        remaining_card_indices = all_card_indices.copy() # reset card options to all possible cards
    else:
        random_index = random.randrange(len(remaining_card_indices))
        random_card = remaining_card_indices[random_index] # get the card index at that random index of the remaining_card_indices list
        remaining_card_indices.pop(random_index) # remove the card index at that random index of the remaining_card_indices list 
        
        # Print the remaining list of card indices
        print("List after removal of random card : " + str(remaining_card_indices))
    return random_card
    

#-----------------------------------------------------------------------

# Home
@app.route('/', methods=['GET'])
@app.route('/index', methods=['GET'])
def index():
    global remaining_card_indices
    global all_card_indices
    print("ALL CARD INDICES: " + str(all_card_indices))
    html = render_template('index.html', title="Please Try Again")
    response = make_response(html)
    session['player1'] = '' # player 1 name
    session['player2'] = '' # player 2 name
    session['moderator'] = None # which player is in this role right now, either 'player1' or 'player2'
    session['provider'] = None # which player is in this role right now, either 'player1' or 'player2'
    session['round_number'] = 0 # remember which round the pair of players is currently on
    session['card_index'] = 0 # remember which card the pair of players is currently on
    session['turn'] = None # remember which role is currently up, either 'provider' or 'moderator'
    return response

# How to Play
@app.route('/instructions', methods=['GET'])
def instructions():
    slide_number = 1
    html = render_template('instructions.html', slide=slide_number, title="How to Play")
    response = make_response(html)
    return response

# Set Up Game: get names of players
@app.route('/setup', methods=['GET'])
def setup():
    html = render_template('setup.html', title="Set Up")
    response = make_response(html)
    return response

# Set Up Game: save names of players in session cookies and redirect to start game
@app.route('/setup_game', methods=['POST'])
def setup_game():
    global remaining_card_indices
    global all_card_indices
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
    # session['card_index'] = 26 # set the card number for the round; TODO: change this for testing
    remaining_card_indices = all_card_indices.copy() # restart with all possible card options
    print("Reset cards")
    print("remaining_card_indices: " + str(remaining_card_indices))
    print("all_card_indices: " + str(all_card_indices))
    session['card_index'] = get_random_card()
    session['attempt_number'] = 1 # set which attempt number the provider is on for this card
    
    return response

# Play Game
@app.route('/play', methods=['GET'])
def play():
    html = render_template('game.html', title="Game") # TODO: check usage
    response = make_response(html)
    return response


# Role Call
@app.route('/role_call', methods=['GET'])
def role_call():
    round_num = session['round_number'] # which round the players are on
    attempt_num = session['attempt_number'] # get current attempt number
    curr_role = session['turn'] # 'moderator' or 'provider'
    curr_player_num = session[curr_role] # 'player1' or 'player2'
    curr_player_name = session[curr_player_num] # player 1's name or player 2's name

    if not curr_player_name:
        return render_template('error.html', title="Error")

    return render_template('role_call.html', curr_role=curr_role, curr_player_name=curr_player_name, round_num=round_num, attempt_num=attempt_num, title="Role Call")

# Content submission page
@app.route('/input_content', methods=['GET'])
def input_content():
    card_index = session['card_index'] # get the index of the card in the cards list for the round
    curr_card = cards[card_index] # get current Card, which holds all info (prompt, rule, input types, options)
    card_number = curr_card.id # get unique identifier of card
    print(curr_card)
    prompt = curr_card.prompt # String with prompt
    input_types = curr_card.input_types # list of input types
    options = curr_card.options # list of options, applicable only if checkbox or radio input types, None otherwise
    round_num = session['round_number'] # which round the players are on
    attempt_num = session['attempt_number'] # get current attempt number
    html = render_template('input_content.html', card_number=card_number, round_num=round_num, prompt=prompt, input_types=input_types, options=options, attempt_num=attempt_num, title="Input Content")
    response = make_response(html)
    return response

# Process submitted content from content submission page
@app.route('/submit_content', methods=['POST'])
def submit_content():
    card_index = session['card_index'] # get the index of the card in the cards list for the round
    curr_card = cards[card_index] # get current Card, which holds all info (prompt, rule, input types, options)
    card_number = curr_card.id # get unique identifier of card
    print(curr_card)
    input_types = curr_card.input_types # list of input types

    session["submitted_content"] = {} # clear previous cookie

    for input in input_types:
        if input == "image":
            img = request.files['image-input']
            # get filename of the uploaded image
            img_filename = secure_filename(img.filename)
            # save the file locally
            img.save(os.path.join(app.config['UPLOAD_FOLDER'], img_filename))
            # remember the uploaded image
            session["submitted_content"]["image"] = os.path.join(app.config['UPLOAD_FOLDER'], img_filename)
            # session['uploaded_img_file_path'] = os.path.join(app.config['UPLOAD_FOLDER'], img_filename)
        else:
            input_field = input + "-input"
            # for checkboxes
            if input == "checkbox": 
                session["submitted_content"][input] = request.form.getlist(input_field)
            else:
                session["submitted_content"][input] = request.form.get(input_field)
        print("SUBMITTED CONTENT: " + str(session["submitted_content"])) # FOR DEBUGGING
    
    # Switch roles
    session['turn'] = 'moderator'
    return redirect(url_for('role_call'))

# Get rule card instruction
@app.route('/rule_card', methods=['GET'])
def rule_card():
    card_index = session['card_index'] # get the index of the card in the cards list for the round
    curr_card = cards[card_index] # get current Card, which holds all info (prompt, rule, input types, options)
    card_number = curr_card.id # get unique identifier of card
    round_num = session['round_number'] # which round the players are on
    attempt_num = session['attempt_number'] # get current attempt number
    html = render_template('rule_card.html', card_number=card_number, round_num=round_num, attempt_num=attempt_num, title="Rule Card")
    response = make_response(html)
    return response


@app.route('/review_content', methods=['GET'])
def review_content():
    card_index = session['card_index'] # get the index of the card in the cards list for the round
    curr_card = cards[card_index] # get current Card, which holds all info (prompt, rule, input types, options)
    card_number = curr_card.id # get unique identifier of card
    print(curr_card)

    prompt = curr_card.prompt # String with prompt
    input_types = curr_card.input_types # list of input types
    options = curr_card.options # list of options, applicable only if checkbox or radio input types, None otherwise
    submitted_content = session["submitted_content"]
    
    round_num = session['round_number'] # which round the players are on
    attempt_num = session['attempt_number'] # get current attempt number
    html = render_template('review_content.html', card_number=card_number, round_num=round_num, prompt=prompt, input_types=input_types, options=options, submitted_content=submitted_content, attempt_num=attempt_num, title="Review Content")
    response = make_response(html)
    return response

@app.route('/accept_content', methods=['GET'])
def accepted_content():
    round_num = session['round_number'] # which round the players are on
    attempt_num = session['attempt_number'] # get current attempt number
    html = render_template('accepted_content.html', round_num=round_num, attempt_num=attempt_num, title="Accepted Content")
    response = make_response(html)
    return response

@app.route('/reject_content', methods=['GET'])
def rejected_content():
    session['turn'] = 'provider' # back to provider's turn
    curr_role = session['turn'] # 'moderator' or 'provider'
    curr_player_num = session[curr_role] # 'player1' or 'player2'
    curr_player_name = session[curr_player_num] # player 1's name or player 2's name
    round_num = session['round_number'] # which round the players are on
    attempt_num = session['attempt_number'] # get current attempt number
    html = render_template('rejected_content.html', round_num=round_num, curr_player_name=curr_player_name, attempt_num=attempt_num, title="Rejected Content")
    response = make_response(html)
    return response

# Redirect to the content input page to try again
@app.route('/try_again', methods=['GET'])
def try_again():
    curr_attempt_num = session['attempt_number'] # get current attempt number
    session['attempt_number'] = curr_attempt_num + 1
    response = redirect(url_for('input_content'))
    return response

# Give option to skip this round or exit game entirely 
@app.route('/exit_game', methods=['GET'])
def exit_game():
    html = render_template('exit_game.html', title="Exit Game")
    response = make_response(html)
    return response

# Give option to skip this round or exit game entirely 
@app.route('/game_over', methods=['GET'])
def game_over():
    html = render_template('game_over.html', title="Game Over")
    response = make_response(html)
    return response

# Give option to skip this round or exit game entirely 
@app.route('/next_round', methods=['GET'])
def next_round():
    # Change roles
    session['moderator'] = session['provider']
    if session['moderator'] == 'player2':
        session['provider'] = 'player1'
    else:
        session['provider'] = 'player2'
    session['turn'] = 'provider' # back to provider starting
    session['round_number'] = session['round_number'] + 1 # increment round number
    selected_card = get_random_card() # get the index of a random card in the cards array
    if selected_card != -1: # game is not over yet
        session['card_index'] = selected_card  # set the new card, if there is still one that exists
        session['attempt_number'] = 1 # set which attempt number the provider is on for this card
        response = redirect(url_for('role_call'))
    else:
        response = redirect(url_for('game_over'))
    return response
    
    
    