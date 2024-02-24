from flask import Flask, request, render_template, jsonify
from uuid import uuid4

from boggle import BoggleGame

app = Flask(__name__)
app.config["SECRET_KEY"] = "this-is-secret"

# The boggle games created, keyed by game id
games = {}


@app.get("/")
def homepage():
    """Show board."""

    return render_template("index.html")


@app.post("/api/new-game")
def new_game():
    """Start new game and return JSON about game.

    Returns: JSON of {
       gameId: "...uuid-of-game...",
       board: [ [ 'A', 'B', ... ], ... ]
    }
    """

    # get a unique string id for the board we're creating
    game_id = str(uuid4())
    game = BoggleGame()
    games[game_id] = game

    return jsonify({'gameId': game_id, 'board': game.board})

@app.post('/api/score-word')
def check_valid_word():
    """Expects gameId and word. Checks validity of word and returns result as JSON."""
    gameId = request.json['gameId']
    word = request.json['word'].upper()
    game = games[gameId]
    if (not game.is_word_in_word_list(word)):
        return jsonify({"result": "not-word"})
    elif (not game.check_word_on_board(word)):
        return jsonify({"result": "not-on-board"})
    else:
        return jsonify({"result": "ok"})
