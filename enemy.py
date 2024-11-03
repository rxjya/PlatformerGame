try:
    import simplegui
except ImportError:
    import SimpleGUICS2Pygame.simpleguics2pygame as simplegui
from entity import Entity
from Vector import *
from globals import *


class Boar(Entity):
    def __init__(self, pos, image_size, health=100):
        super().__init__(pos, image_size, health, "boar")
        self.animations = {"idle": 4, "walking": 6, "running": 6, "hit": 4}
        self.load_assets("mob/boar")
        self.hitbox = Vector(25, 20)
        self.seen_player = False
        self.detection_range = 200
        self.attacking = False


        self.damage = 0.5
        self.walking_speed = 2
        self.running_speed = 4
        self.velocity = Vector(self.walking_speed, 0)

    def check_state(self):
        if self.pos.x >= SCREEN_WIDTH or self.pos.x <= 0:
            self.velocity.x *= -1

        if self.velocity.x != 0:
            if self.seen_player:
                self.state = "running"
            else:
                self.state = "walking"
                self.velocity.x = self.walking_speed * (1 if self.flip_direction else -1)
            if self.velocity.x > 0:
                self.flip_direction = True
            elif self.velocity.x < 0:
                self.flip_direction = False
        else:
            self.state = "idle"

    def chase_player(self, player_pos):
        self.velocity.x = player_pos.copy().subtract(self.pos).normalize().multiply(self.running_speed).x


class Bee(Entity):
    def __init__(self, pos, image_size, health=100):
        super().__init__(pos, image_size, health, "bee")
        self.animations = {"flying": 4, "attack": 4, "hit": 4}
        self.state = "flying"
        self.load_assets("mob/bee")
        self.seen_player = False
        self.detection_range = 500
        self.hitbox = Vector(20, 20)

        self.attacking = False

        self.flying_speed = 5
        self.velocity = Vector(0, 0)
        self.damage = 1

    def check_state(self):
        if self.pos.x >= SCREEN_WIDTH or self.pos.x <= 0:
            self.velocity.x *= -1

        if self.attacking:
            self.state = "attack"
        else:
            self.state = "flying"

        if not self.seen_player:
            self.velocity = Vector(0, 0)
        if self.velocity.x > 0:
            self.flip_direction = True
        elif self.velocity.x < 0:
            self.flip_direction = False

    def chase_player(self, player_pos):
        self.velocity = player_pos.copy().subtract(Vector(self.pos.x, self.pos.y)).normalize().multiply(self.flying_speed)
