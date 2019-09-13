import math
import pyxel
from enum import Enum
from functools import partial


class GameState(Enum):
    INTRO = 0
    PLAYER1 = 1
    PLAYER2 = 2
    RESULTS = 3


def is_within(x, y, pos):
    x1, y1, x2, y2 = pos
    return x >= x1 and x <= x2 and y >= y1 and y <= y2

class GameTheoryApp:
    def __init__(self, width=160, height=120):

        self.game_state = GameState.INTRO

        self._width = width
        self._height = height

        # self._h_gate = self.pyxel_button("H", 50, 45, 15, 15, 13)

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

        elif self.game_state == GameState.RESULTS:
            self.handle_results()


    def draw(self):
        pyxel.cls(0)

        # pyxel.text(55, 41, "Hello, Pyxel!", pyxel.frame_count % 16)
        # pyxel.blt(61, 66, 0, 0, 0, 38, 16)

        if self.game_state == GameState.INTRO:
            self.draw_introscreen()

        elif self.game_state == GameState.PLAYER1:
            self.draw_player1()

        elif self.game_state == GameState.PLAYER2:
            self.draw_player2()
            
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
        pyxel.text(67, 25, "Gates", pyxel.frame_count % 16)

        gates_list = ['H', 'X', 'I', 'Y', 'Z', 'A', 'B', 'C', 'D']

        width_nomargin = self._width / 5
        gates_len = len(gates_list)
        y = 45

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

        for x_pos, gate in zip(x_starting_pos, gate_labels):
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

        s = "Elapsed frame count is {}\n" "Current mouse position is ({},{})".format(
            pyxel.frame_count, pyxel.mouse_x, pyxel.mouse_y
        )
        pyxel.text(1, 1, s, 9)


    def draw_player2(self):
        None


    def draw_results(self):
        pyxel.text(67, 15, "Results", pyxel.frame_count % 16)
        pyxel.line(60,30,60,110,7)
        pyxel.text(20,40,"Player 1", 7)
        pyxel.text(80,40,"Result 1", 7)
        pyxel.text(20,60,"Player 2", 7)
        pyxel.text(80,60,"Result 2", 7)
        pyxel.text(20,80,"Player 3", 7)
        pyxel.text(80,80,"Result 3", 7)
        pyxel.text(20,100,"Player 4", 7)
        pyxel.text(80,100,"Result 4", 7)


    ### Event handlers ###

    def handle_intro_events(self):
        if pyxel.btnp(pyxel.MOUSE_LEFT_BUTTON):
            self.game_state = GameState.PLAYER1  
    

    def handle_player1(self):
        if pyxel.btnp(pyxel.MOUSE_LEFT_BUTTON) and pyxel.mouse_x > 31 and pyxel.mouse_x < 43 and pyxel.mouse_y < 56 and pyxel.mouse_y > 44:
            print("h")
            self.game_state = GameState.RESULTS  

        
    
    
    def handle_player2(self):
        None

    
    def handle_results(self):
        None

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
