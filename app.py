from boggle import Boggle
from flask import Flask, render_template, jsonify, session, request
app = Flask(__name__)

# Your routes and other app setup code go here

app = Flask(__name__)
app.config["SECRET_KEY"] = "i-have-no-idea"


boggle_game = Boggle()

@app.route('/')
def homepage():
    """display the boggle board"""

    board = boggle_game.make_board()
    # store the board in the session
    session['board'] = board 
    highscore = session.get("highscore", 0)
    nplays = session.get('nplays', 0)

    return render_template("index.html", board=board, highscore=highscore, nplays=nplays)

@app.route("/check-word")
def check_word():
    """Check whether or not word is in dictionary"""

    word = request.args["word"]
    board = session["board"]
    response = boggle_game.check_valid_word(board, word)

    return jsonify({'result': response})

@app.route('/post-score', methods=["POST"])
def post_score():
    """Receive score, update high score if appropiate, update nplays"""

    score = request.json["score"]
    highscore = session.get('highscore', 0)
    nplays = session.get('nplays', 0)

    session['nplays'] = nplays + 1
    session['highscore'] = max(score, highscore)

    return jsonify(brokeRecord=score > highscore)