import math
import pyxel
from enum import Enum


class GameState(Enum):
    INTRO = 0
    PLAYER1 = 1
    PLAYER2 = 2
    RESULTS = 3


class GameTheoryApp:
    def __init__(self, width=153, height=170):

        self.game_state = GameState.INTRO

        self._width = width
        self._height = height

        # pyxel.init(160, 120, caption="Quantum Game Theory")
        # pyxel.image(0).load(0, 0, "assets/pyxel_logo_38x16.png")

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
        self.pyxel_button_centered('Play', 100)

    def draw_player1(self):
        None


    def draw_player2(self):
        None


    def draw_results(self):
        None


    ### Event handlers ###

    def handle_intro_events(self):
        None
    

    def handle_player1(self):
        None
    
    
    def handle_player2(self):
        None

    
    def handle_results(self):
        None

    ### Pyxel Function Wrappers ###

    def pyxel_button(self, text, x, y):
        x_offset = (len(text) * 4) + 6
        y_offset = 8

        try:
            pyxel.rect(x, y, x + x_offset, y + y_offset, 14)
            pyxel.text(x + 4, y + 2, text, 0)
        except AttributeError as e:
            pass
        return (x, y, x + x_offset, y + y_offset)

    def pyxel_button_centered(self, text, y):
        offset = math.ceil(len(text) * 4 / 2) + 3
        x = math.floor(self._width / 2) - offset
        return self.pyxel_button(text, x, y)


GameTheoryApp()
