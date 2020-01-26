import base64
import numpy as np
import pandas as pd

from flask import Flask
from flask_restful import Api, Resource, reqparse
from qiskit import Aer, execute, IBMQ, QuantumCircuit
from qiskit.quantum_info import Operator
from qiskit.visualization import plot_histogram
from io import BytesIO

from quantum_game_theory.utils import predefined_games, Protocol, unitary_gates


class PayoffTable:
    """
    Stores the data of the game
    """

    def __init__(self, n_players=2, n_choices=2, payoff=None):
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
        self.num_players = len(player_gates)
        self.J, self.Jdg = self._make_J_operators()
        self.circ = self._make_circuit(player_gates)

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

    def _make_circuit(self, player_gates):
        """ Generates the base circuit """
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
        """ Adds the gates chosen by player to the cirucit """
        for i in range(len(gates)):
            circ.append(gates[i], [player_num])
        return circ

    def draw_circuit(self):
        """ Saves the circuit image to specified filepath """
        self.circ.draw(output='mpl')


class Game:
    """
    Handles all the game logic and execution of the quantum game and final output of the results.
    """

    def __init__(self, game_name, protocol, payoff_table=None, group='open', backend='qasm_simulator'):
        """
        Args:
            game_name (str): name of game to be played
            protocol (str): name of the protocol to be used
            payoff_table (dict): custom payoff table, otherwise uses default 
            group (str): IBMQ group type
            backend (str): backend name to execute circuit
        """
        self._game_name = game_name
        self._n_players, self._n_choices, self._payoff_table = self._generate_payoff_table(
            game_name, payoff_table)
        self._protocol = Protocol[protocol]
        self._quantum_game = None
        self._final_results = None
        self._backend = self._set_backend(group, backend)

    def set_protocol(self, protocol, group='open', backend='qasm_simulator'):
        self._protocol = Protocol[protocol]
        self._backend = self._set_backend(group, backend)

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
        """ Creates the payoff table object used to store choices """
        if payoff_table == None:
            payoff_table = predefined_games[game_name]

        n_players = len(list(payoff_table.keys())[0])
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
        self._protocol
        if self._protocol == Protocol.Classical:
            return None
        player_gate_objects = []
        for i in range(len(player_gates)):
            player_gate_objects.append([])
            for j in player_gates[i]:
                player_gate_objects[i].append(unitary_gates[j])
        self._quantum_game = QuantumGame(player_gate_objects, self._protocol)
        circ_img = self._quantum_game.circ.draw(output='mpl')
        buffered = BytesIO()
        circ_img.savefig(buffered, format="png")
        circ_str = base64.b64encode(buffered.getvalue())
        circ_str = circ_str.decode("utf-8") 
        return self._quantum_game.circ, circ_str

    def _generate_final_choices(self, player_choices, n_times):
        """ Executes the either the classical game or the quantum circuit on the simulator """
        if self._protocol == Protocol.Classical:
            player_choices_str = ''
            for player_choice in player_choices:
                for choice in player_choice:
                    player_choices_str += str(choice)
            final_choices = {player_choices_str: n_times}
            img = plot_histogram(final_choices)
            buf = BytesIO()
            img.savefig(buf, format="png")
            graph_str = base64.b64encode(buf.getvalue())
            graph_str = graph_str.decode("utf-8") 
            return final_choices, graph_str
        else:
            # runs the circuit on an IBMQ device or simulator
            job_sim = execute(self._quantum_game.circ,
                              self._backend, shots=n_times)
            res_sim = job_sim.result()
            counts = res_sim.get_counts(self._quantum_game.circ)
            # now we need to invert the order of the counts because our convention is [P1,P2]
            counts_inverted = {}
            for key, value in counts.items():
                counts_inverted[key[::-1]] = value
            img = plot_histogram(counts_inverted)
            buf = BytesIO()
            img.savefig(buf, format="png")
            graph_str = base64.b64encode(buf.getvalue())
            graph_str = graph_str.decode("utf-8") 
            return counts_inverted, graph_str

    def _get_payoffs(self, choices):
        return self._payoff_table.get_payoffs(choices)

    def _get_winners(self, payoffs):
        """ Finds the winner from the payoff """
        argmaxes = np.argwhere(payoffs == np.max(payoffs)).flatten()
        if len(argmaxes) == len(payoffs):  # if all 0, then all are max, returns n_player arr
            return 'no winners'
        winners = ''
        for i in argmaxes:
            winners += 'P' + str(i+1)
        return winners

    def _generate_final_results(self, results, circ_str, graph_str):
        """ Returns DataFrame of outcome and number of times, payoff, winner and backend used """
        outcome = []
        num_times = []
        payoffs = []
        winners = []
        for curr_choices, curr_num_times in results.items():
            outcome.append(curr_choices)
            num_times.append(curr_num_times)
            curr_payoffs = self._get_payoffs(curr_choices)
            payoffs.append(curr_payoffs)
            winners.append(self._get_winners(curr_payoffs))
        return {'outcome': outcome, 'payoffs': payoffs, 'winners': winners, 'num_times': num_times, 'backend': str(self._backend), 'full_circ_str': circ_str, 'graph_str': graph_str}

    def play_game(self, player_choices, n_times=1):
        """ Main game function that puts together all the components"""
        player_choices = self.format_choices(player_choices)
        self.quantum_circuit, circ_str = self._generate_quantum_circuit(player_choices)
        final_choices, graph_str = self._generate_final_choices(player_choices, n_times)
        self._final_results = self._generate_final_results(final_choices, circ_str, graph_str)
        return self._final_results, final_choices
