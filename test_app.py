from unittest import TestCase
from flask import jsonify

from app import app, games

# Make Flask errors be real errors, not HTML pages with error info
app.config['TESTING'] = True

# This is a bit of hack, but don't use Flask DebugToolbar
app.config['DEBUG_TB_HOSTS'] = ['dont-show-debug-toolbar']


class BoggleAppTestCase(TestCase):
    """Test flask app of Boggle."""

    def setUp(self):
        """Stuff to do before every test."""

        app.config['TESTING'] = True

    def test_homepage(self):
        """Make sure information is in the session and HTML is displayed"""
        with app.test_client() as client:
            response = client.get('/')
            html = response.get_data(as_text=True)
            self.assertIn('<table class="board">', html)

    def test_api_new_game(self):
        """Test starting a new game."""

        with app.test_client() as client:
            resp = client.post(
                '/api/new-game'
            )
            json = resp.get_json()
            self.assertIsInstance(json['gameId'], str)
            self.assertIsInstance(json['board'], list)
            self.assertIn(json['gameId'], games)
            self.assertEqual({"gameId": json['gameId'], "board": json['board']}, json)
            # make a post request to /api/new-game
            # get the response body as json using .get_json()
            # test that the game_id is a string
            # test that the board is a list
            # test that the game_id is in the dictionary of games (imported from app.py above)

    def test_score_word(self):
        """Test if word is valid"""

        with app.test_client() as client:
            # make a post request to /api/new-game
            new_game_resp = client.post('/api/new-game')
            # get the response body as json using .get_json()
            new_game_json = new_game_resp.get_json()
            # find that game in the dictionary of games (imported from app.py above)
            game = games[new_game_json["gameId"]]

            # manually change the game board's rows so they are not random
            game.board = [['A', 'E', 'K', 'I', 'A'],
                          ['K', 'D', 'S', 'R', 'K'],
                          ['G', 'F', 'D', 'R', 'A'],
                          ['L', 'P', 'A', 'O', 'N'],
                          ['J', 'C', 'P', 'X', 'I']]

            # test to see that a valid word on the altered board returns {'result': 'ok'}
            valid_word_resp = client.post("/api/score-word", json={
                "gameId": new_game_json["gameId"],
                "word": "ADD"
            })
            valid_word_json = valid_word_resp.get_json()
            self.assertEqual({"result": "ok"}, valid_word_json)
            # test to see that a valid word not on the altered board returns {'result': 'not-on-board'}
            valid_word_resp = client.post("/api/score-word", json={
                "gameId": new_game_json["gameId"],
                "word": "SOAP"
            })
            valid_word_json = valid_word_resp.get_json()
            self.assertEqual({"result": "not-on-board"}, valid_word_json)
            # test to see that an invalid word returns {'result': 'not-word'}
            valid_word_resp = client.post("/api/score-word", json={
                "gameId": new_game_json["gameId"],
                "word": "AKGLJ"
            })
            valid_word_json = valid_word_resp.get_json()
            self.assertEqual({"result": "not-word"}, valid_word_json)
