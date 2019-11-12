from backend import Backend

GAME = 'minority'
PROTOCOL = 'MW'

backend_game = Backend(GAME)

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


counts, raw_game_results = backend_game.play(all_states, PROTOCOL)

print('Counts')
print(counts)
print('Results')
print(raw_game_results)