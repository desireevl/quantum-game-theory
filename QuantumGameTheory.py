import numpy as np
from utils import predefined_games, unitary_gates, Protocol
from enum import Enum
from qiskit import QuantumCircuit, Aer, execute, IBMQ
from qiskit.quantum_info import Operator
import numpy as np
import pandas as pd


class PayoffTable:
    # object that stores the data of a game theory game

    def __init__(self, n_players=2, n_choices=2, payoff=None):
        self.n_players = n_players
        self.n_choices = n_choices
        self.payoff = payoff

    def set_payoff(self, tuple, payoff):
        # sets the payoff value for a given tuple of player choices
        self.payoff[self._get_index(tuple), :] = payoff

    def get_payoffs(self, choices):
        # access the payoff tuple for a given tuple of choices
        return self.payoff[choices]

    def _get_index(self, choices):
        # gets the index from a given tuple of player choices
        bin_string = ''.join(str(i) for i in choices)
        return int(bin_string, self.n_choices)


class QuantumGame:
    def __init__(self, player_gates, protocol: Protocol = Protocol.EWL):
        self.protocol = protocol
        self.player_gates = player_gates
        self.num_players = len(player_gates)
        self.J, self.Jdg = self._make_J_operators()
        self.circ = self._make_circuit(player_gates)

    def _make_J_operators(self):
        I = np.identity(1 << self.num_players)
        X = np.matrix([[0, 1], [1, 0]])
        tensorX = X

        for i in range(self.num_players - 1):
            tensorX = np.kron(tensorX, X)

        J = Operator(1 / np.sqrt(2) * (I + 1j * tensorX))
        Jdg = Operator(1 / np.sqrt(2) * (I - 1j * tensorX))

        return J, Jdg

    def _make_circuit(self, player_gates):
        circ = QuantumCircuit(self.num_players, self.num_players)
        circ.append(self.J, range(self.num_players))
        circ.barrier()
        for i in range(self.num_players):
            circ = self._add_player_gates(circ, i, player_gates[i])
        circ.barrier()
        if self.protocol == Protocol.EWL:
            circ.append(self.Jdg, range(self.num_players))
            circ.barrier()
        circ.measure(range(self.num_players), range(self.num_players))
        return circ

    def _add_player_gates(self, circ, player_num, gates):
        for i in range(len(gates)):
            circ.append(gates[i], [player_num])
        return circ

    def draw_circuit(self, filepath):
        self.circ.draw(filename=filepath, output='mpl')

class Game:
    
    def __init__(self, game_name, protocol, payoff_table=None, group = 'open', backend = "qasm_simulator"):
        self._game_name = game_name
        self._n_players, self._n_choices, self._payoff_table = self._generate_payoff_table(game_name, payoff_table)
        self._protocol = Protocol[protocol]
        self._quantum_game = None
        self._final_results = None
        self._backend = self._set_backend(group, backend)
    
    def set_protocol(self, protocol):
        self._protocol = Protocol[protocol]
    
    def _set_backend(self, group, backend):
        if self._protocol == Protocol.Classical:
            return "Classical"
        if backend == "qasm_simulator":
            return Aer.get_backend("qasm_simulator")
        else:
            IBMQ.load_account()
            provider = IBMQ.get_provider(group=group)
            return provider.get_backend(backend)
    
    def _generate_payoff_table(self, game_name, payoff_table):
        if payoff_table == None:
            payoff_table = predefined_games[game_name]
        n_players = len(list(payoff_table.keys())[0])
        n_choices = int(len(payoff_table)**(1/n_players))
        payoff_table = PayoffTable(n_players, n_choices, payoff_table)
        return n_players, n_choices, payoff_table
    
    def display_payoffs(self):
        print('Game: ' + self._game_name)
        print('Payoffs: ')
        choices=list(self._payoff_table.payoff.keys())
        payoffs=list(self._payoff_table.payoff.values())
        payoff_table = pd.DataFrame({'outcome': choices, 'payoffs': payoffs})
        payoff_table = payoff_table.sort_values(by=['outcome'])
        return payoff_table
    
    def format_choices(self, player_choices):
        formatted_player_choices = []
        for choice in player_choices:
            if isinstance(choice, list):
                formatted_player_choices.append(choice)
            else:
                formatted_player_choices.append([choice])
        return formatted_player_choices
    
    def _generate_quantum_circuit(self, player_gates):
        self._protocol
        if self._protocol == Protocol.Classical:
            return None
        player_gate_objects = []
        for i in range(len(player_gates)):
            player_gate_objects.append([])
            for j in player_gates[i]:
                player_gate_objects[i].append(unitary_gates[j])        
        self._quantum_game = QuantumGame(player_gate_objects, self._protocol)
        self._quantum_game.circ.draw()
        return self._quantum_game.circ
    
    def _generate_final_choices(self, player_choices, n_times):
        if self._protocol == Protocol.Classical:
            player_choices_str=''
            for player_choice in player_choices:
                for choice in player_choice:
                    player_choices_str += str(choice)
            return {player_choices_str: n_times}
        else:
            job_sim = execute(self._quantum_game.circ, self._backend, shots=n_times)
            res_sim = job_sim.result()
            return res_sim.get_counts(self._quantum_game.circ)
    
    def _get_payoffs(self, choices):
        return self._payoff_table.get_payoffs(choices)
    
    def _get_winners(self,payoffs):
        argmaxes = np.argwhere(payoffs==np.max(payoffs)).flatten()
        if len(argmaxes)==len(payoffs):
            return 'no winners'
        winners = ''
        for i in argmaxes:
            winners += 'P' + str(i+1) + ' '
        return winners
    
    def _generate_final_results(self, final_choices):
        choices = []
        num_times = []
        payoffs = []
        winners = []
        for curr_choices, curr_num_times in final_choices.items():
            choices.append(curr_choices)
            num_times.append(curr_num_times)
            curr_payoffs = self._get_payoffs(curr_choices)
            payoffs.append(curr_payoffs)
            winners.append(self._get_winners(curr_payoffs))
        return pd.DataFrame({'outcome':choices, 'payoffs':payoffs, 'winners': winners, 'num_times':num_times, 'backend':str(self._backend)})
         
    
    def play_game(self, player_choices, n_times=1):
        player_choices = self.format_choices(player_choices)
        final_payoffs = []
        self.quantum_circuit = self._generate_quantum_circuit(player_choices)
        final_choices = self._generate_final_choices(player_choices, n_times)
        self._final_results = self._generate_final_results(final_choices)
        return final_choices, self._final_results
        