import math
import pyxel
from enum import Enum
from functools import partial
from backend import Backend

import matplotlib.pyplot as plt
import matplotlib.image as mpimg



class GameState(Enum):
    INTRO = 0
    PLAYER1 = 1
    PLAYER2 = 2
    PLAYER3 = 3
    PLAYER4 = 4
    CIRCUIT = 5
    RESULTS = 6


class GameTheoryApp:
    def __init__(self, width=160, height=120):
        self.backend = Backend('minority')
        
        self.game_state = GameState.INTRO

        self._width = width
        self._height = height
        self.state_1 = []
        self.state_2 = []
        self.state_3 = []
        self.state_4 = []
        
        self.all_states = []
        
        self.circuit_img_str = ''
        self.RawGameResults = []

        pyxel.init(160, 120, caption="Quantum Game Theory")

        pyxel.mouse(True)
        pyxel.run(self.update, self.draw)

    def update(self):
        if pyxel.btnp(pyxel.KEY_Q):
            pyxel.quit()

        if self.game_state == GameState.INTRO:
            self.handle_intro_events()

        elif self.game_state == GameState.PLAYER1:
            self.handle_player1()
        elif self.game_state == GameState.PLAYER2:
            self.handle_player2()
        elif self.game_state == GameState.PLAYER3:
            self.handle_player3()
        elif self.game_state == GameState.PLAYER4:
            self.handle_player4()
        elif self.game_state == GameState.CIRCUIT:
            self.handle_circuit()
        elif self.game_state == GameState.RESULTS:
            self.handle_results()


    def draw(self):
        pyxel.cls(0)

        if self.game_state == GameState.INTRO:
            self.draw_introscreen()
        elif self.game_state == GameState.PLAYER1:
            self.draw_player1()
        elif self.game_state == GameState.PLAYER2:
            self.draw_player2()
        elif self.game_state == GameState.PLAYER3:
            self.draw_player3()
        elif self.game_state == GameState.PLAYER4:
            self.draw_player4()
        elif self.game_state == GameState.CIRCUIT:
            self.draw_circuit()
        elif self.game_state == GameState.RESULTS:
            self.draw_results()


    ### Pyxel screens ###
    def draw_introscreen(self):
        pyxel.cls(0)
        pyxel.text(40, 40, "Quantum Game Maker", pyxel.frame_count % 16)
        x = 40
        y = 60
        w = 70
        h = 20
        pyxel.rectb(x, y, w, h, 7)
        pyxel.text(47, 67, "Click to Start", 7)

    def draw_player1(self):
        pyxel.text(40, 45, "Gates - Player 1", pyxel.frame_count % 16)

        pyxel.rectb(110, 110, 30, 10, 7)
        pyxel.text(115, 112, "Next", 7)

        gates_list = ['W', 'Rz1', 'X', 'Ry1', 'Rz2', 'Z', 'H', 'T']

        width_nomargin = self._width / 5
        gates_len = len(gates_list)
        y = 65

        gate_labels = []
        if len(gates_list) > 5:
            gate_labels = gates_list[:5]

        spacing = (self._width - (2 * width_nomargin)) / len(gate_labels)
        x_starting_pos = []
        new = width_nomargin

        for i in range(len(gates_list)):
            if len(x_starting_pos) == 0:
                x_starting_pos.append(new)
            else:
                x_starting_pos.append(new+spacing)
                new += spacing

        for x_pos, gate in zip(x_starting_pos, gates_list[:5]):
            self.pyxel_button(gate, x_pos, y, 12, 12, 13)

        if len(gates_list) > 5:
            gates_len = 5
            gate_labels = gates_list[5:]
            y += 16
            spacing = (self._width - (2 * width_nomargin)) / gates_len
            x_starting_pos = []
            new = width_nomargin

            for i in range(len(gates_list)):
                if len(x_starting_pos) == 0:
                    x_starting_pos.append(new)
                else:
                    x_starting_pos.append(new+spacing)
                    new += spacing

            for x_pos, gate in zip(x_starting_pos, gate_labels):
                self.pyxel_button(gate, x_pos, y, 12, 12, 13)

        # s = "Elapsed frame count is {}\n" "Current mouse position is ({},{})".format(
        #     pyxel.frame_count, pyxel.mouse_x, pyxel.mouse_y
        # )
        # pyxel.text(1, 1, s, 9)


    def draw_player2(self):
        pyxel.text(40, 45, "Gates - Player 2", pyxel.frame_count % 16)

        pyxel.rectb(110, 110, 30, 10, 7)
        pyxel.text(115, 112, "Next", 7)

        gates_list = ['W', 'Rz1', 'X', 'Ry1', 'Rz2', 'Z', 'H', 'T']

        width_nomargin = self._width / 5
        gates_len = len(gates_list)
        y = 65

        gate_labels = []
        if len(gates_list) > 5:
            gate_labels = gates_list[:5]

        spacing = (self._width - (2 * width_nomargin)) / len(gate_labels)
        x_starting_pos = []
        new = width_nomargin

        for i in range(len(gates_list)):
            if len(x_starting_pos) == 0:
                x_starting_pos.append(new)
            else:
                x_starting_pos.append(new+spacing)
                new += spacing

        for x_pos, gate in zip(x_starting_pos, gates_list[:5]):
            self.pyxel_button(gate, x_pos, y, 12, 12, 13)

        if len(gates_list) > 5:
            gates_len = 5
            gate_labels = gates_list[5:]
            y += 16
            spacing = (self._width - (2 * width_nomargin)) / gates_len
            x_starting_pos = []
            new = width_nomargin

            for i in range(len(gates_list)):
                if len(x_starting_pos) == 0:
                    x_starting_pos.append(new)
                else:
                    x_starting_pos.append(new+spacing)
                    new += spacing

            for x_pos, gate in zip(x_starting_pos, gate_labels):
                self.pyxel_button(gate, x_pos, y, 12, 12, 13)

        # s = "Elapsed frame count is {}\n" "Current mouse position is ({},{})".format(
        #     pyxel.frame_count, pyxel.mouse_x, pyxel.mouse_y
        # )
        # pyxel.text(1, 1, s, 9)

    
    def draw_player3(self):
        pyxel.text(40, 45, "Gates - Player 3", pyxel.frame_count % 16)

        pyxel.rectb(110, 110, 30, 10, 7)
        pyxel.text(115, 112, "Next", 7)

        gates_list = ['W', 'Rz1', 'X', 'Ry1', 'Rz2', 'Z', 'H', 'T']

        width_nomargin = self._width / 5
        gates_len = len(gates_list)
        y = 65

        gate_labels = []
        if len(gates_list) > 5:
            gate_labels = gates_list[:5]

        spacing = (self._width - (2 * width_nomargin)) / len(gate_labels)
        x_starting_pos = []
        new = width_nomargin

        for i in range(len(gates_list)):
            if len(x_starting_pos) == 0:
                x_starting_pos.append(new)
            else:
                x_starting_pos.append(new+spacing)
                new += spacing

        for x_pos, gate in zip(x_starting_pos, gates_list[:5]):
            self.pyxel_button(gate, x_pos, y, 12, 12, 13)

        if len(gates_list) > 5:
            gates_len = 5
            gate_labels = gates_list[5:]
            y += 16
            spacing = (self._width - (2 * width_nomargin)) / gates_len
            x_starting_pos = []
            new = width_nomargin

            for i in range(len(gates_list)):
                if len(x_starting_pos) == 0:
                    x_starting_pos.append(new)
                else:
                    x_starting_pos.append(new+spacing)
                    new += spacing

            for x_pos, gate in zip(x_starting_pos, gate_labels):
                self.pyxel_button(gate, x_pos, y, 12, 12, 13)

        # s = "Elapsed frame count is {}\n" "Current mouse position is ({},{})".format(
        #     pyxel.frame_count, pyxel.mouse_x, pyxel.mouse_y
        # )
        # pyxel.text(1, 1, s, 9)

    
    def draw_player4(self):
        pyxel.text(40, 45, "Gates - Player 4", pyxel.frame_count % 16)

        pyxel.rectb(110, 110, 30, 10, 7)
        pyxel.text(115, 112, "Next", 7)

        gates_list = ['W', 'Rz1', 'X', 'Ry1', 'Rz2', 'Z', 'H', 'T']

        width_nomargin = self._width / 5
        gates_len = len(gates_list)
        y = 65

        gate_labels = []
        if len(gates_list) > 5:
            gate_labels = gates_list[:5]

        spacing = (self._width - (2 * width_nomargin)) / len(gate_labels)
        x_starting_pos = []
        new = width_nomargin

        for i in range(len(gates_list)):
            if len(x_starting_pos) == 0:
                x_starting_pos.append(new)
            else:
                x_starting_pos.append(new+spacing)
                new += spacing

        for x_pos, gate in zip(x_starting_pos, gates_list[:5]):
            self.pyxel_button(gate, x_pos, y, 12, 12, 13)

        if len(gates_list) > 5:
            gates_len = 5
            gate_labels = gates_list[5:]
            y += 16
            spacing = (self._width - (2 * width_nomargin)) / gates_len
            x_starting_pos = []
            new = width_nomargin

            for i in range(len(gates_list)):
                if len(x_starting_pos) == 0:
                    x_starting_pos.append(new)
                else:
                    x_starting_pos.append(new+spacing)
                    new += spacing

            for x_pos, gate in zip(x_starting_pos, gate_labels):
                self.pyxel_button(gate, x_pos, y, 12, 12, 13)

        # s = "Elapsed frame count is {}\n" "Current mouse position is ({},{})".format(
        #     pyxel.frame_count, pyxel.mouse_x, pyxel.mouse_y
        # )
        # pyxel.text(1, 1, s, 9)

        # call quantum logic file, input self.all_states



################RUNQISKIT###############################

    def draw_circuit(self):
        # pyxel.rectb(110, 110, 30, 10, 7)
        # pyxel.text(115, 112, "Next", 7)
        # pyxel.blt(1, 1, 0, 0, 0, 200, 106)


        img=mpimg.imread(self.circuit_img_str)
        imgplot = plt.imshow(img)
        plt.show()


    def draw_results(self):
        self.quantum_results()

        pyxel.rectb(110, 110, 30, 10, 7)
        pyxel.text(115, 112, "Next", 7)

        state_1 = ''.join(self.state_1)
        state_2 = ''.join(self.state_2)
        state_3 = ''.join(self.state_3)
        state_4 = ''.join(self.state_4)

        game_result=[]

        for i in self.RawGameResults:
            game_result.append(str(i))

        P1_Result = game_result[0]
        P2_Result = game_result[1]
        P3_Result = game_result[2]
        P4_Result = game_result[3]

        victor=[]
        for i in range(len(self.RawGameResults)):
            if self.RawGameResults[i] == 0:
                victor.append('You Lose')
            elif self.RawGameResults[i] == 1:
                victor.append('You Win')

        P1_v = victor[0]
        P2_v = victor[1]
        P3_v = victor[2]
        P4_v = victor[3]

        the_variable = ''.join(self.state_1)
        pyxel.text(67, 15, "Results", pyxel.frame_count % 16)
        pyxel.line(40,30,40,110,7)
        pyxel.line(80,30,80,110,7)
        pyxel.line(115,37,115,110,7)
        pyxel.text(45,25,"Strategy",7)
        pyxel.text(95,25,"Game Results",7)
        pyxel.text(5,40,"Player 1", 7)
        pyxel.text(45,40,state_1, 7)
        pyxel.text(90,40,P1_Result,7)
        pyxel.text(120,40,P1_v,7)
        pyxel.text(5,60,"Player 2", 7)
        pyxel.text(45,60,state_2, 7)
        pyxel.text(90,60,P2_Result,7)
        pyxel.text(120,60,P2_v,7)
        pyxel.text(5,80,"Player 3", 7)
        pyxel.text(45,80,state_3, 7)
        pyxel.text(90,80,P3_Result,7)
        pyxel.text(120,80,P3_v,7)
        pyxel.text(5,100,"Player 4", 7)
        pyxel.text(45,100,state_4, 7)
        pyxel.text(90,100,P4_Result,7)
        pyxel.text(120,100,P4_v,7)


    ### Event handlers ###

    def handle_intro_events(self):
        if pyxel.btnp(pyxel.MOUSE_LEFT_BUTTON):
            self.game_state = GameState.PLAYER1  
    

    def handle_player1(self):
        if pyxel.btnp(pyxel.MOUSE_LEFT_BUTTON) and pyxel.mouse_x > 32 and pyxel.mouse_x < 43 and pyxel.mouse_y < 76 and pyxel.mouse_y > 64:
            print("w")
            self.state_1.append('W')
        elif pyxel.btnp(pyxel.MOUSE_LEFT_BUTTON) and pyxel.mouse_x > 51 and pyxel.mouse_x < 62 and pyxel.mouse_y < 76 and pyxel.mouse_y > 64:
            print('i')
            self.state_1.append('Rz1')
        elif pyxel.btnp(pyxel.MOUSE_LEFT_BUTTON) and pyxel.mouse_x > 69 and pyxel.mouse_x < 81 and pyxel.mouse_y < 76 and pyxel.mouse_y > 64:
            print('x')
            self.state_1.append('X')
        elif pyxel.btnp(pyxel.MOUSE_LEFT_BUTTON) and pyxel.mouse_x > 89 and pyxel.mouse_x < 100 and pyxel.mouse_y < 76 and pyxel.mouse_y > 64:
            print('y')
            self.state_1.append('Ry1')
        elif pyxel.btnp(pyxel.MOUSE_LEFT_BUTTON) and pyxel.mouse_x > 107 and pyxel.mouse_x < 119 and pyxel.mouse_y < 76 and pyxel.mouse_y > 64:
            print('s')
            self.state_1.append('Rz2')
        elif pyxel.btnp(pyxel.MOUSE_LEFT_BUTTON) and pyxel.mouse_x > 32 and pyxel.mouse_x < 43 and pyxel.mouse_y < 91 and pyxel.mouse_y > 81:
            print('z')
            self.state_1.append('Z')
        elif pyxel.btnp(pyxel.MOUSE_LEFT_BUTTON) and pyxel.mouse_x > 51 and pyxel.mouse_x < 61 and pyxel.mouse_y < 91 and pyxel.mouse_y > 81:
            print('h')
            self.state_1.append('H')
        elif pyxel.btnp(pyxel.MOUSE_LEFT_BUTTON) and pyxel.mouse_x > 70 and pyxel.mouse_x < 81 and pyxel.mouse_y < 91 and pyxel.mouse_y > 81:
            print('t')
            self.state_1.append('T')
        elif pyxel.btnp(pyxel.MOUSE_LEFT_BUTTON) and pyxel.mouse_x > 119 and pyxel.mouse_x < 139 and pyxel.mouse_y < 119 and pyxel.mouse_y > 110:
            self.game_state = GameState.PLAYER2

    def handle_player2(self):
        if pyxel.btnp(pyxel.MOUSE_LEFT_BUTTON) and pyxel.mouse_x > 32 and pyxel.mouse_x < 43 and pyxel.mouse_y < 76 and pyxel.mouse_y > 64:
            print("w")
            self.state_2.append('W')
        elif pyxel.btnp(pyxel.MOUSE_LEFT_BUTTON) and pyxel.mouse_x > 51 and pyxel.mouse_x < 62 and pyxel.mouse_y < 76 and pyxel.mouse_y > 64:
            print('i')
            self.state_2.append('Rz1')
        elif pyxel.btnp(pyxel.MOUSE_LEFT_BUTTON) and pyxel.mouse_x > 69 and pyxel.mouse_x < 81 and pyxel.mouse_y < 76 and pyxel.mouse_y > 64:
            print('x')
            self.state_2.append('X')
        elif pyxel.btnp(pyxel.MOUSE_LEFT_BUTTON) and pyxel.mouse_x > 89 and pyxel.mouse_x < 100 and pyxel.mouse_y < 76 and pyxel.mouse_y > 64:
            print('y')
            self.state_2.append('Ry1')
        elif pyxel.btnp(pyxel.MOUSE_LEFT_BUTTON) and pyxel.mouse_x > 107 and pyxel.mouse_x < 119 and pyxel.mouse_y < 76 and pyxel.mouse_y > 64:
            print('s')
            self.state_2.append('Rz2')
        elif pyxel.btnp(pyxel.MOUSE_LEFT_BUTTON) and pyxel.mouse_x > 32 and pyxel.mouse_x < 43 and pyxel.mouse_y < 91 and pyxel.mouse_y > 81:
            print('z')
            self.state_2.append('Z')
        elif pyxel.btnp(pyxel.MOUSE_LEFT_BUTTON) and pyxel.mouse_x > 51 and pyxel.mouse_x < 61 and pyxel.mouse_y < 91 and pyxel.mouse_y > 81:
            print('h')
            self.state_2.append('H')
        elif pyxel.btnp(pyxel.MOUSE_LEFT_BUTTON) and pyxel.mouse_x > 70 and pyxel.mouse_x < 81 and pyxel.mouse_y < 91 and pyxel.mouse_y > 81:
            print('t')
            self.state_2.append('T')
        elif pyxel.btnp(pyxel.MOUSE_LEFT_BUTTON) and pyxel.mouse_x > 119 and pyxel.mouse_x < 139 and pyxel.mouse_y < 119 and pyxel.mouse_y > 110:
            self.game_state = GameState.PLAYER3

    def handle_player3(self):
        if pyxel.btnp(pyxel.MOUSE_LEFT_BUTTON) and pyxel.mouse_x > 32 and pyxel.mouse_x < 43 and pyxel.mouse_y < 76 and pyxel.mouse_y > 64:
            print("w")
            self.state_3.append('W')
        elif pyxel.btnp(pyxel.MOUSE_LEFT_BUTTON) and pyxel.mouse_x > 51 and pyxel.mouse_x < 62 and pyxel.mouse_y < 76 and pyxel.mouse_y > 64:
            print('i')
            self.state_3.append('Rz1')
        elif pyxel.btnp(pyxel.MOUSE_LEFT_BUTTON) and pyxel.mouse_x > 69 and pyxel.mouse_x < 81 and pyxel.mouse_y < 76 and pyxel.mouse_y > 64:
            print('x')
            self.state_3.append('X')
        elif pyxel.btnp(pyxel.MOUSE_LEFT_BUTTON) and pyxel.mouse_x > 89 and pyxel.mouse_x < 100 and pyxel.mouse_y < 76 and pyxel.mouse_y > 64:
            print('y')
            self.state_3.append('Ry1')
        elif pyxel.btnp(pyxel.MOUSE_LEFT_BUTTON) and pyxel.mouse_x > 107 and pyxel.mouse_x < 119 and pyxel.mouse_y < 76 and pyxel.mouse_y > 64:
            print('s')
            self.state_3.append('Rz2')
        elif pyxel.btnp(pyxel.MOUSE_LEFT_BUTTON) and pyxel.mouse_x > 32 and pyxel.mouse_x < 43 and pyxel.mouse_y < 91 and pyxel.mouse_y > 81:
            print('z')
            self.state_3.append('Z')
        elif pyxel.btnp(pyxel.MOUSE_LEFT_BUTTON) and pyxel.mouse_x > 51 and pyxel.mouse_x < 61 and pyxel.mouse_y < 91 and pyxel.mouse_y > 81:
            print('h')
            self.state_3.append('H')
        elif pyxel.btnp(pyxel.MOUSE_LEFT_BUTTON) and pyxel.mouse_x > 70 and pyxel.mouse_x < 81 and pyxel.mouse_y < 91 and pyxel.mouse_y > 81:
            print('t')
            self.state_3.append('T')
        elif pyxel.btnp(pyxel.MOUSE_LEFT_BUTTON) and pyxel.mouse_x > 119 and pyxel.mouse_x < 139 and pyxel.mouse_y < 119 and pyxel.mouse_y > 110:
            self.game_state = GameState.PLAYER4
    
    def handle_player4(self):
        if pyxel.btnp(pyxel.MOUSE_LEFT_BUTTON) and pyxel.mouse_x > 32 and pyxel.mouse_x < 43 and pyxel.mouse_y < 76 and pyxel.mouse_y > 64:
            print("w")
            self.state_4.append('W')
        elif pyxel.btnp(pyxel.MOUSE_LEFT_BUTTON) and pyxel.mouse_x > 51 and pyxel.mouse_x < 62 and pyxel.mouse_y < 76 and pyxel.mouse_y > 64:
            print('i')
            self.state_4.append('Rz1')
        elif pyxel.btnp(pyxel.MOUSE_LEFT_BUTTON) and pyxel.mouse_x > 69 and pyxel.mouse_x < 81 and pyxel.mouse_y < 76 and pyxel.mouse_y > 64:
            print('x')
            self.state_4.append('X')
        elif pyxel.btnp(pyxel.MOUSE_LEFT_BUTTON) and pyxel.mouse_x > 89 and pyxel.mouse_x < 100 and pyxel.mouse_y < 76 and pyxel.mouse_y > 64:
            print('y')
            self.state_4.append('Ry1')
        elif pyxel.btnp(pyxel.MOUSE_LEFT_BUTTON) and pyxel.mouse_x > 107 and pyxel.mouse_x < 119 and pyxel.mouse_y < 76 and pyxel.mouse_y > 64:
            print('s')
            self.state_4.append('Rz2')
        elif pyxel.btnp(pyxel.MOUSE_LEFT_BUTTON) and pyxel.mouse_x > 32 and pyxel.mouse_x < 43 and pyxel.mouse_y < 91 and pyxel.mouse_y > 81:
            print('z')
            self.state_4.append('Z')
        elif pyxel.btnp(pyxel.MOUSE_LEFT_BUTTON) and pyxel.mouse_x > 51 and pyxel.mouse_x < 61 and pyxel.mouse_y < 91 and pyxel.mouse_y > 81:
            print('h')
            self.state_4.append('H')
        elif pyxel.btnp(pyxel.MOUSE_LEFT_BUTTON) and pyxel.mouse_x > 70 and pyxel.mouse_x < 81 and pyxel.mouse_y < 91 and pyxel.mouse_y > 81:
            print('t')
            self.state_4.append('T')
        elif pyxel.btnp(pyxel.MOUSE_LEFT_BUTTON) and pyxel.mouse_x > 119 and pyxel.mouse_x < 139 and pyxel.mouse_y < 119 and pyxel.mouse_y > 110:
            self.game_state = GameState.RESULTS
            

    def quantum_results(self):
        self.all_states = [self.state_1, self.state_2, self.state_3, self.state_4]

        self.RawGameResults, self.circuit_img_str = self.backend.play(self.all_states, 'MW')


    def handle_circuit(self):
        # if pyxel.btnp(pyxel.MOUSE_LEFT_BUTTON) and pyxel.mouse_x > 119 and pyxel.mouse_x < 139 and pyxel.mouse_y < 119 and pyxel.mouse_y > 110:
        #     self.game_state = GameState.CIRCUIT
        None

    def handle_results(self):
        if pyxel.btnp(pyxel.MOUSE_LEFT_BUTTON) and pyxel.mouse_x > 119 and pyxel.mouse_x < 139 and pyxel.mouse_y < 119 and pyxel.mouse_y > 110:
            self.game_state = GameState.CIRCUIT

    ### Pyxel Function Wrappers ###

    def pyxel_button(self, text, x, y, width, height, colour):

        try:
            pyxel.rect(x, y, width, height, colour)
            pyxel.text(x + 4, y + 3, text, 0)
        except AttributeError as e:
            pass
        return (x, y, x + width, y + height)


    # def pyxel_button_centered(self, text, y):
    #     offset = math.ceil(len(text) * 4 / 2) + 3
    #     x = math.floor(self._width / 2) - offset
    #     return self.pyxel_button(text, x, y)


GameTheoryApp()
