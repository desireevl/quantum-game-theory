from flask import Flask
from flask_restful import Api, Resource, reqparse
from flask_cors import CORS

from quantum_game_theory.logic import Game


class QuantumApi(Resource):
    @classmethod
    def make_api(self, *args, **kwargs):
        return self

    @staticmethod
    def build_parser():
        parser = reqparse.RequestParser()
        parser.add_argument('protocol', type=str,
                            location='json', required=True)
        parser.add_argument('game', type=str, location='json', required=True)
        parser.add_argument('players', type=int,
                            location='json', required=True)
        parser.add_argument('payoff', type=list,
                            location='json', required=True)
        parser.add_argument('player1', type=list,
                            location='json', required=True)
        parser.add_argument('player2', type=list,
                            location='json', required=True)
        parser.add_argument('player3', type=list,
                            location='json', required=True)
        parser.add_argument('player4', type=list,
                            location='json', required=True)
        return parser

    def run_game(self, game, protocol, all_states):
        game = Game(game, protocol)
        results = game.play_game(all_states)
        return results

    def post(self):
        args = self.build_parser().parse_args()

        input_info = {}
        for key, item in args.items():
            input_info[key] = item

        all_states = [
            input_info['player1'],
            input_info['player2'],
            input_info['player3'],
            input_info['player4']
        ]

        results = self.run_game(
            input_info['game'],
            input_info['protocol'],
            all_states
        )

        # print(results)
        return results


app = Flask(__name__)
CORS(app)
api = Api(app)
api.add_resource(QuantumApi, '/')


if __name__ == '__main__':
    app.run(debug=True)
