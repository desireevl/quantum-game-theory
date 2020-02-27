import base64
import json
import numpy as np
import operator
import pandas as pd

from flask import Flask
from flask_restful import Api, Resource, reqparse
from qiskit import Aer, execute, IBMQ, QuantumCircuit
from qiskit.providers.ibmq import least_busy
from qiskit.quantum_info import Operator
from qiskit.visualization import plot_histogram
from io import BytesIO

# if you need to use "from utils import ..." please don't push that and keep this line the same
from quantum_game_theory.utils import gen_predefined_payoffs, Protocol, unitary_gates


class PayoffTable:
    """
    For if you want to create a custom payoff table. This is not in use and not implemented 
    """

    def __init__(self, n_players, n_choices, payoff=None):
        """
        Args:
            n_players (int): number of players
            n_choices (int): number of choices
            payoff (dict): custom payoff, otherwise uses default
        """
        self.n_players = n_players
        self.n_choices = n_choices
        self.payoff = payoff

    def set_payoff(self, tuple, payoff):
        """ Sets the payoff value for a given tuple of player choices """
        self.payoff[self._get_index(tuple), :] = payoff

    def get_payoffs(self, choices):
        """ Access the payoff tuple for a given tuple of choices """
        return self.payoff[choices]

    def _get_index(self, choices):
        """ Gets the index from a given tuple of player choices """
        bin_string = ''.join(str(i) for i in choices)
        return int(bin_string, self.n_choices)

    def get_payoff_table(self):
        return self.payoff


class QuantumGame:
    """
    Handles the quantum side of the game including creating the custom gates
    and defining the circuit.
    """

    def __init__(self, player_gates, protocol: Protocol = Protocol.EWL):
        """
        Args:
            player_gates (list): gates chosen by the player
            protocol (enum):
        """
        self.protocol = protocol
        self.player_gates = player_gates
        self.num_players = self._get_num_players()
        self.J, self.Jdg = self._make_J_operators()
        self.circ = self._make_circuit(player_gates)

    def _get_num_players(self):
        counter = 0
        for gates in self.player_gates:
            if len(gates) > 0:
                counter += 1
        return counter

    def _make_J_operators(self):
        """ Creates the J unitary and its adjoint """
        I = np.identity(1 << self.num_players)
        X = np.matrix([[0, 1], [1, 0]])
        tensorX = X

        for i in range(self.num_players - 1):
            tensorX = np.kron(tensorX, X)

        J = Operator(1 / np.sqrt(2) * (I + 1j * tensorX))
        Jdg = Operator(1 / np.sqrt(2) * (I - 1j * tensorX))

        return J, Jdg
    
    def _make_decomposed_J_operators(self) -> QuantumCircuit:
        circ = QuantumCircuit(self.num_players + 1)
        circ.cx(0, self.num_players)
        circ.h(0)
        for i in range(1,self.num_players):
            circ.cx(0,i)
        circ.x(self.num_players)
        for i in range(1,self.num_players):
            circ.ccx(0,self.num_players,i)
        circ.x(self.num_players)
        circ.x(0)
        for i in range(1,self.num_players):
            circ.ccx(0,self.num_players,i)
        circ.x(0)
        circ.s(0)
        return circ

    def _make_circuit(self, player_gates):
        """ Generates the base circuit """
        if self.num_players == 2:
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

        else: 
            circ = QuantumCircuit(self.num_players+1, self.num_players+1)
            circ += self._make_decomposed_J_operators()
            circ.barrier()

            for i in range(self.num_players):
                circ = self._add_player_gates(circ, i, player_gates[i])
            circ.barrier()

            if self.protocol == Protocol.EWL:
                circ += self._make_decomposed_J_operators().inverse()
                circ.barrier()
            circ.measure(range(self.num_players+1), range(self.num_players+1))
            return circ

    def _add_player_gates(self, circ, player_num, gates):
        """ Adds the gates chosen by player to the cirucit """
        for i in range(len(gates)):
            circ.append(gates[i], [player_num])
        return circ

    def draw_circuit(self):
        """ Saves the circuit image to specified filepath """
        return self.circ.draw(output='mpl')


class Game:
    """
    Handles all the game logic and execution of the quantum game and final output of the results.
    """

    def __init__(self, game_name, protocol, num_players, payoff_table=None, group='open', backend='simulator'):
        """
        Args:
            game_name (str): name of game to be played
            protocol (str): name of the protocol to be used
            payoff_table (dict): custom payoff table, otherwise uses default 
            group (str): IBMQ group type
            backend (str): backend name to execute circuit
        """
        self._game_name = game_name
        self._num_players = num_players
        self._n_players, self._n_choices, self._payoff_table = self._generate_payoff_table(
            self._game_name, self._num_players, payoff_table)
        self._protocol = Protocol[protocol]
        self._quantum_game = None
        self._final_results = None
        self._backend = self._set_backend(group, backend)

    def set_protocol(self, protocol, backend, group='open'):
        self._protocol = Protocol[protocol]
        self._backend = self._set_backend(group, backend)

    def _set_backend(self, group, backend):
        if self._protocol == Protocol.Classical:
            return "Classical"
        if backend == "simulator":
            return Aer.get_backend("qasm_simulator")
        else:
            print('Loading IBM Q account ... ')
            IBMQ.load_account()
            print('Getting least busy device ...')
            provider = IBMQ.get_provider(hub='ibm-q')
            small_devices = provider.backends(filters=lambda x: x.configuration().n_qubits == 5
                                   and not x.configuration().simulator)
            least_busy_device = least_busy(small_devices)
            print(f'Least busy device: {least_busy_device}')

            return least_busy_device

    def _generate_payoff_table(self, game_name, num_players, payoff_input):
        """ Creates the payoff table object used to store choices """
        payoff_table = gen_predefined_payoffs(game_name, num_players, payoff_input)
        n_players = num_players
        n_choices = int(len(payoff_table)**(1/n_players))
        payoff_table = PayoffTable(n_players, n_choices, payoff_table)
        return n_players, n_choices, payoff_table

    def display_payoffs(self):
        """ Way to display a table of payoffs"""
        print('Game: ' + self._game_name)
        print('Payoffs: ')
        choices = list(self._payoff_table.payoff.keys())
        payoffs = list(self._payoff_table.payoff.values())
        payoff_table = pd.DataFrame({'outcome': choices, 'payoffs': payoffs})
        payoff_table = payoff_table.sort_values(by=['outcome'])
        return payoff_table

    def format_choices(self, player_choices):
        """ Ensures that different ways of inputting single choices (e.g. [['H'], ['H']] and ['H', 'H']) are all treated the same"""
        formatted_player_choices = []
        for choice in player_choices:
            if isinstance(choice, list):
                formatted_player_choices.append(choice)
            else:
                formatted_player_choices.append([choice])
        return formatted_player_choices

    def _generate_quantum_circuit(self, player_gates):
        """generates the quantum circuit for the game in qiskit (or returns None if it is a classical game)"""
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
        """ Executes the either the classical game or the quantum circuit on the simulator """
        if self._protocol == Protocol.Classical:
            player_choices_str = ''
            for player_choice in player_choices:
                for choice in player_choice:
                    player_choices_str += str(choice)
            return {player_choices_str: n_times}
        else:
            # runs the circuit on an IBMQ device or simulator
            print('Executing circuit ....')
            job_sim = execute(self._quantum_game.circ,
                              self._backend, shots=n_times)
            print('Circuit running ...')
            res_sim = job_sim.result()
            print('Circuit finished running, getting counts ...')
            # final_unitary = res_sim.get_unitary
            counts = res_sim.get_counts(self._quantum_game.circ)
            # now we need to invert the order of the counts because our convention is [P1,P2]
            counts_inverted={}
            for key, value in counts.items():
                if self._num_players == 2:
                    counts_inverted[key[::-1]]=value
                else:
                    counts_inverted[key[:0:-1]]=value
            return counts_inverted

    def _get_payoffs(self, choices):
        return self._payoff_table.get_payoffs(choices)

    def _get_winners(self, payoff):
        """ Finds the winner from the payoff """
        argmaxes = np.argwhere(payoff == np.max(payoff)).flatten()
        if len(argmaxes) == 1:
            return 'P' + str(argmaxes[0] + 1)
        else:
            return 'no winners'


    def _generate_final_results(self, results):
        """ Returns DataFrame of outcome and number of times, payoff, winner and backend used """
        outcome = []
        num_times = []
        payoffs = []
        winners = []

        highest_prob = max(results.items(), key=operator.itemgetter(1))[0]
        curr_payoffs = self._get_payoffs(highest_prob)
        payoffs.append(curr_payoffs)
        winners.append(self._get_winners(curr_payoffs))

        for curr_choices, curr_num_times in results.items():
            outcome.append(curr_choices)
            num_times.append(curr_num_times)
        payoff_json = json.dumps(self._payoff_table.get_payoff_table())
        return {'outcome': outcome, 'payoffs': payoffs, 'players': self._num_players, 'game': self._game_name, 'payoff_matrix': payoff_json, 'winners': winners, 'num_times': num_times, 'backend': str(self._backend)}

    def base64_figure(self, fig):
        buf = BytesIO()
        fig.savefig(buf, format="png")
        fig_str = base64.b64encode(buf.getvalue())
        fig_str = fig_str.decode("utf-8")

        return fig_str

    def play_game(self, player_choices, n_times=50):
        """ Main game function that puts together all the components"""
        player_choices = self.format_choices(player_choices)
        self.quantum_circuit = self._generate_quantum_circuit(player_choices)
        final_choices = self._generate_final_choices(player_choices, n_times)
        print('player', player_choices)
        print('final', final_choices)
        self._final_results = self._generate_final_results(final_choices)

        # Generate graph(s)
        if self._protocol != Protocol.Classical:
            circuit_fig = self.quantum_circuit.draw(output='mpl')
            circuit_fig.suptitle("Full Circuit for Players", fontsize=25)

            probability_graph_img = plot_histogram(final_choices)
            probability_graph_img.suptitle("Probability Graph", fontsize=25)
            axes = probability_graph_img.get_axes()
            for t in axes[0].get_xticklabels():
                t.set_rotation(0)

            self._final_results['full_circ_str'] = self.base64_figure(circuit_fig)
            self._final_results['graph_str'] = self.base64_figure(probability_graph_img)

        return final_choices, self._final_results
