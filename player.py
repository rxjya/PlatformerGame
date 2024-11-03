try:
    import simplegui
except ImportError:
    import SimpleGUICS2Pygame.simpleguics2pygame as simplegui
from entity import Entity
from globals import *


class Player(Entity):
    def __init__(self, pos=Vector(0, 0),image_size=Vector(30, 30), health=100):
        super().__init__(pos, image_size, health, "player")
        self.animations = {"idle": 4, "running": 8, "jump": 15, "attack": 8, "death": 8}
        # Add more image variables for other states if needed
        self.load_assets("player")
        self.hitbox = Vector(20, 30)

        self.damage = 50

        # Jump mechanics
        self.jumping = False
        self.on_ground = True
        # Attack mechanics
        #self.attacking = False
        #self.can_attack = True
        #self.attack_speed = 500

    def check_state(self):
        if self.jumping:
            self.state = "jump"
            self.animations[self.state].current_frame = 0
        #elif self.attacking:
        #    self.state = "attack"
        #    self.animations[self.state].current_frame = 0
        elif self.velocity.x != 0:
            self.state = "running"
            self.animations[self.state].current_frame = 0
            if self.velocity.x < 0:
                self.flip_direction = True
            elif self.velocity.x > 0:
                self.flip_direction = False
        else:
            self.state = "idle"
            self.animations[self.state].current_frame = 0





