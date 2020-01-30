from QuantumGameTheory import Game
import base64
from qiskit.visualization import plot_histogram
from io import BytesIO

GAME = '4-minority'
PROTOCOL = 'EWL'

game = Game(GAME, PROTOCOL)

print(f'Running game: {GAME}')
print('-'*25)
print('Options: X, Y, S, Z, H, T, W, Rz1, X, Ry1, Rz2')
print('Please type as a list, eg. W, Rz1, Z')
print('-'*25)
print('Input player 1 gates:')
state_1_input = input()
state_1 = [x.strip() for x in state_1_input.split(',')]

print('Input player 2 gates:')
state_2_input = input()
state_2 = [x.strip() for x in state_2_input.split(',')]

print('Input player 3 gates:')
state_3_input = input()
state_3 = [x.strip() for x in state_3_input.split(',')]

print('Input player 4 gates:')
state_4_input = input()
state_4 = [x.strip() for x in state_4_input.split(',')]

all_states = [state_1, state_2, state_3, state_4]

results = game.play_game(all_states)
print('Game: ' + GAME)
print('Results:')
print(results)


img = plot_histogram(results)
bufbufbuf = BytesIO()
img.savefig(bufbufbuf, format="JPEG")

print(base64.b64encode(bufbufbuf.getvalue()))
