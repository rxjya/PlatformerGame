try:
    import simplegui
except ImportError:
    import SimpleGUICS2Pygame.simpleguics2pygame as simplegui
from globals import *
from platforms import *


class Keyboard:
    def __init__(self):
        self.right = False
        self.left = False
        self.space = False
        self.down = False

    def key_down(self, key):
        if key == simplegui.KEY_MAP['right']:
            self.right = True
        elif key == simplegui.KEY_MAP['left']:
            self.left = True
        elif key == simplegui.KEY_MAP['space']:
            self.space = True
        elif key == simplegui.KEY_MAP['down']:  # Handle down arrow key press
            self.down = True

    def key_up(self, key):
        if key == simplegui.KEY_MAP['right']:
            self.right = False
        elif key == simplegui.KEY_MAP['left']:
            self.left = False
        elif key == simplegui.KEY_MAP['space']:
            self.space = False
        elif key == simplegui.KEY_MAP['down']:  # Handle down arrow key release
            self.down = False


class Interaction:
    def __init__(self, player, keyboard, enemies, platforms, mob_barriers):
        self.player = player
        self.keyboard = keyboard
        self.enemies = enemies
        self.platforms = platforms
        self.mob_barriers = mob_barriers

    def collide_platforms(self):
        entities = self.enemies + [self.player]
        for platform in self.platforms:
            for entity in entities:
                # Check platform's type attribute instead of using isinstance
                if platform.type == "phasable" and self.keyboard.down and entity == self.player:
                    # Skip the collision check for phasable platforms if the down key is pressed
                    continue
                platform.collide(entity)

    def detect_player(self):
        for enemy in self.enemies:
            if (enemy.pos.x + enemy.detection_range > self.player.pos.x > enemy.pos.x - enemy.detection_range
                    and enemy.pos.y + enemy.detection_range > self.player.pos.y > enemy.pos.y - enemy.detection_range):
                enemy.seen_player = True
                enemy.chase_player(self.player.pos)
            else:
                enemy.seen_player = False

    def damage_player(self):
        for enemy in self.enemies:
            if (enemy.pos.x + enemy.hitbox.x > self.player.pos.x > enemy.pos.x - enemy.hitbox.x
                    and enemy.pos.y + enemy.hitbox.y > self.player.pos.y > enemy.pos.y - enemy.hitbox.y):
                #self.player.health -= enemy.damage
                if not enemy.attacking:
                    enemy.attacking = True
            elif enemy.attacking:
                enemy.attacking = False

    def collide_barrier(self):
        for barrier in self.mob_barriers:
            for enemy in self.enemies:
                if enemy.type == "boar":
                    if (barrier.pos.x <= enemy.pos.x <= barrier.pos.x + barrier.hitbox.x and
                            barrier.pos.y <= enemy.pos.y <= barrier.pos.y + barrier.hitbox.y):
                        enemy.velocity.x *= -1

    def accelerate(self, map):
        movement_speed = PLAYER_SPEED

        if self.keyboard.space and self.player.on_platform:
            self.player.jump()
        elif not self.keyboard.space:
            self.player.can_jump = True
        if self.keyboard.right and self.player.right() < map.get_width() - movement_speed:
            self.player.velocity.x = movement_speed
        elif self.keyboard.left and self.player.left() > 0 + movement_speed:
            self.player.velocity.x = -movement_speed
        else:
            self.decelerate()

    def decelerate(self):
        if abs(self.player.velocity.copy().x) > 0:
            self.player.velocity.x *= 0.8
            if abs(self.player.velocity.x) < 0.5:
                self.player.velocity.x = 0

    def apply_gravity(self):
        self.player.velocity.y += GRAVITY

    def update(self, map):
        self.accelerate(map)
        self.decelerate()
        self.apply_gravity()
        self.collide_platforms()
        self.detect_player()
        self.damage_player()
        self.collide_barrier()




