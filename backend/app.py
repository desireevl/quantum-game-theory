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
        parser.add_argument('player1', type=list,
                            location='json', required=True)
        parser.add_argument('player2', type=list,
                            location='json', required=True)
        parser.add_argument('player3', type=list,
                            location='json', required=True)
        parser.add_argument('player4', type=list,
                            location='json', required=True)
        parser.add_argument('device', type=str,
                            location='json', required=True)
        parser.add_argument('payoff', type=dict,
                            location='json', required=True)
        return parser

    def run_game(self, game, protocol, all_states, player_num, payoff, device):
        print('HEREEEE1')
        game = Game(game, protocol, player_num, payoff_table=payoff, backend=device)
        print('HEREEE2')
        results = game.play_game(all_states)
        return results

    def post(self):
        args = self.build_parser().parse_args()
        print('YOOOOO')
        print(args['game'])
        print(args['device'])

        all_states = [
            args['player1'],
            args['player2'],
            args['player3'],
            args['player4']
        ]

        outcomes, results = self.run_game(
            args['game'],
            args['protocol'],
            all_states,
            args['players'],
            args['payoff'],
            args['device']
        )
        
        return results


app = Flask(__name__)
CORS(app)
api = Api(app)
api.add_resource(QuantumApi, '/')


if __name__ == '__main__':
    app.run(debug=True)
