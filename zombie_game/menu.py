from os import path

from zombie_game.drawable import Drawable
from zombie_game.functions import quit_game
from zombie_game.settings import *
# import main

import global_variables

class MenuMob(Drawable, pg.sprite.Sprite):

    def __init__(self, game, x, y, width=20, height=20):
        super(MenuMob, self).__init__(width, height, x, y)
        pg.sprite.Sprite.__init__(self)
        self.image = self.surface
        self.game = game
        self.width = width
        self.height = height
        self.pic = None

    def animate(self, destination, area):
        self.pic = pg.image.load(path.join(self.game.img_folder, INTRO_IMG))
        self.pic = pg.transform.scale(self.pic, (self.width, self.height))
        self.surface.blit(self.pic, destination, area)


class Menu:

    def __init__(self, game):
        self.game = game
        # self.game_copy = game
        self.pos_x = 0
        self.pos_y = 0
        self.i = 0

    def game_intro(self):
        self.i = 0.36
        self.set_mob_limit(0.1, 220, 480, INTRO_SPRITE_POS_X, self.game.board.draw_menu, self.game_options, 40)
        if 100 < self.pos_y < 220:
            self.game_choosing_difficulty()
        elif 220 < self.pos_y < 300:
            self.game_about()
        elif 320 < self.pos_y < 357:
            self.game_rules()
        elif 385 < self.pos_y < 420:
            self.game_scoreboard()
        elif 450 < self.pos_y < 467:
            self.game_options()
        else:
            quit_game()

    def game_options(self):
        self.i = 0.31
        self.set_mob_limit(0.15, 196, 366, OPTIONS_SPRITE_POS_X, self.game.board.draw_options, self.game_intro)
        if 185 < self.pos_y < 187:
            self.game_controls()
        elif 275 < self.pos_y < 277:
            self.audio_controls()
        else:
            self.game_intro()

#-----------------------------------------------------------------------------------------------------------------------------------------
    def game_controls(self):
        self.i = 0.56
        self.set_mob_limit(0.1, 337, 450, CONTROL_SPRITE_POS_X, self.game.board.draw_game_controls, self.game_options, 40)
        if 330 < self.pos_y < 350:
            global_variables.game_control = 1
            self.game_intro() 
        elif 350 < self.pos_y < 400:
            global_variables.game_control = 2
            self.game_intro()
        else:
            self.game_intro()
    
    def audio_controls(self):
        self.i = 0.56
        self.set_mob_limit(0.1, 337, 450, CONTROL_SPRITE_POS_X, self.game.board.draw_audio_controls, self.game_options, 40)
        if 330 < self.pos_y < 350:
            global_variables.is_mute = True
        elif 350 < self.pos_y < 400:
            global_variables.is_mute = False
            self.game_intro()
        else:
            self.game_intro()

    def game_about(self):
        self.i = 0.75
        self.set_mob_limit(0.1, 450, 450, INTRO_SPRITE_POS_X, self.game.board.draw_about, self.game_intro)
        if 100 < self.pos_y < 450:
            self.game_intro()
    
    def game_rules(self):
        self.i = 0.75
        self.set_mob_limit(0.15, 450, 450, INTRO_SPRITE_POS_X, self.game.board.draw_rules, self.game_intro)
        if 450 < self.pos_y < 450:
            self.game_intro()
#-----------------------------------------------------------------------------------------------------------------------------------------

    def game_scoreboard(self):
        self.i = 0.75
        self.set_mob_limit(0.15, 450, 450, OPTIONS_SPRITE_POS_X, self.game.board.draw_scoreboard, self.game_intro)
        if 450 < self.pos_y < 450:
            self.game_intro()

    def game_choosing_difficulty(self):
        self.i = 0.16
        self.set_mob_limit(0.2, 97, 300, OPTIONS_SPRITE_POS_X, self.game.board.draw_choosing_difficulty, self.game_intro)
        if 95 < self.pos_y < 97:
            difficult = "easy"
            self.game_input(difficult)
        elif 215 < self.pos_y < 217:
            difficult = "hell"
            self.game_input(difficult)
        elif 335 < self.pos_y < 437:
            self.game_intro()
        # else:
            # difficult = "hell"

    def game_input(self, difficult):
        word = ""
        while True:
            pg.display.flip()
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    quit_game()
                if event.type == pg.KEYDOWN:
                    if event.key == pg.K_ESCAPE:
                        self.game_choosing_difficulty()
                    if event.unicode.isalpha():
                        word += event.unicode
                    if event.key == pg.K_BACKSPACE:
                        word = word[:-1]
                    if event.key == pg.K_RETURN:
                        if len(word) > 0:
                            self.game.run(difficult, word)
                self.game.board.draw_input(word, self.game.width / 2, self.game.height / 2)

    def game_over(self, scoreboard, message):
        while True:
            self.game.board.draw_game_over(scoreboard, message)
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    quit_game()
                elif event.type == pg.KEYDOWN:
                    if event.key == pg.K_q or event.key == pg.K_RETURN:
                        self.game.menu.game_intro()

    def set_mob_limit(self, i_value, top, bottom, pos, draw, previous, size=50):
        while True:
            self.set_position(pos)
            draw(self.set_the_mob(size))
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    quit_game()
                elif event.type == pg.KEYDOWN:
                    if event.key == pg.K_ESCAPE:
                        quit_game()
                    if event.key == pg.K_ESCAPE or event.key == pg.K_BACKSPACE:
                        previous()
                    if event.key == pg.K_UP or event.key == pg.K_w:
                        if self.pos_y > top:
                            self.i -= i_value
                    if event.key == pg.K_DOWN or event.key == pg.K_s:
                        if self.pos_y < bottom:
                            self.i += i_value
                    if event.key == pg.K_SPACE or event.key == pg.K_RETURN:
                        return False

    def set_position(self, x):
        self.pos_y = self.game.height * self.i
        self.pos_x = self.game.width * x

    def set_the_mob(self, size=50):
        intro_object = MenuMob(self.game, self.pos_x, self.pos_y, size, size)
        intro_object.animate((0, 0), (0, 0, self.pos_x, self.pos_y))
        return intro_object

