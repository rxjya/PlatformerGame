from interaction import *
from Vector import *
from globals import *
import csv

class Platform:
    def __init__(self, pos, hitbox):
        self.pos = pos
        self.hitbox = hitbox

class SolidPlatform:
    def __init__(self, pos, hitbox):
        self.pos = pos
        self.hitbox = hitbox
        self.type = "solid"

    def collide(self, entity):
        # Check for collision
        if (entity.pos.x < self.pos.x + self.hitbox.x and
                entity.pos.x + entity.image_size.x > self.pos.x and
                entity.pos.y < self.pos.y + self.hitbox.y and
                entity.pos.y + entity.image_size.y > self.pos.y):
            # Further check if the entity is above the platform and moving downwards
            if entity.velocity.y > 0 and entity.pos.y + entity.hitbox.y <= self.pos.y + self.hitbox.y:
                # Adjust player's y-position to the top of the platform and set vertical velocity to 0
                entity.pos.y = self.pos.y - entity.hitbox.y
                entity.velocity.y = 0
                entity.on_platform = True
                entity.jumping = False


class PhasablePlatform(Platform):
    def __init__(self, pos, hitbox):
        super().__init__(pos, hitbox)  # Call the parent class constructor
        self.type = "phasable"

    def collide(self, entity):
        if (entity.pos.x < self.pos.x + self.hitbox.x and
                entity.pos.x + entity.image_size.x > self.pos.x):

            current_bottom_y = entity.pos.y + entity.hitbox.y
            prev_bottom_y = current_bottom_y - entity.velocity.y  # Calculate previous bottom Y based on movement

            # Introduce a small tolerance for collision detection
            tolerance = 5  # Adjust this value based on your game's scale and typical entity speeds

            # Adjust the condition to include a tolerance
            if entity.velocity.y > 0 and (prev_bottom_y < self.pos.y + tolerance):
                if current_bottom_y >= self.pos.y:
                    entity.pos.y = self.pos.y - entity.hitbox.y  # Place entity on top of the platform
                    entity.velocity.y = 0
                    entity.on_platform = True
                    entity.jumping = False
                    return

    def check_player_interaction(self, player, keyboard):
        pass


class MobBarrier:
    def __init__(self, pos, hitbox):
        self.pos = pos
        self.hitbox = hitbox
        self.type = "mob_barrier"


class WinCondition:
    def __init__(self, pos, hitbox):
        self.pos = pos
        self.hitbox = hitbox

    def check_win(self, player):
        if self.pos.x <= player.pos.x <= self.pos.x + self.hitbox.x:
            if self.pos.y <= player.pos.y <= self.pos.y + self.hitbox.y:
                return True
        return False
