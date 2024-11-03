try:
    import simplegui
except ImportError:
    import SimpleGUICS2Pygame.simpleguics2pygame as simplegui
from globals import *

class HealthBar:
    def __init__(self, max_health):
        self.pos = (10, 10)
        self.size = (200,20)
        self.max_health = max_health
        self.health = max_health

    def draw(self, canvas, health):
        self.health = health
        canvas.draw_line(self.pos, (self.pos[0] + self.size[0], self.pos[1]), self.size[1], "Red")
        canvas.draw_line(self.pos, (self.pos[0] + self.size[0] * (self.health / self.max_health), self.pos[1]), self.size[1], "Green")


class Screen:
    def __init__(self, heading, prompt, type):
        self.heading = heading
        self.prompt = prompt
        self.type = type

        self.font_family = "sans-serif"

        self.heading_pos = (SCREEN_WIDTH / 2, SCREEN_HEIGHT / 3)
        self.heading_size = 48

        self.prompt_pos = (SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2)
        self.prompt_size = 24

    def draw(self, canvas):
        canvas.draw_text(self.heading, self.heading_pos, self.heading_size, "White", self.font_family)
        canvas.draw_text(self.prompt, self.prompt_pos, self.prompt_size, "White", self.font_family)