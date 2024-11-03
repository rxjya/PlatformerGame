try:
    import simplegui
except ImportError:
    import SimpleGUICS2Pygame.simpleguics2pygame as simplegui
from platforms import *
from interaction import *


class Entity:
    def __init__(self, pos=Vector(0, 0), image_size=Vector(30, 30), health=100, type = "entity"):
        self.pos = pos
        self.velocity = Vector(0, 0)
        self.image_size = image_size
        self.hitbox = image_size
        self.health = health
        self.type = type

        self.on_platform = False
        self.frame_speed = FRAME_SPEED
        self.state = "idle"
        self.flip_direction = False
        self.dead = False

    def right(self):
        return self.pos.x + self.hitbox.x/2

    def left(self):
        return self.pos.x - self.hitbox.x/2

    def top(self):
        return self.pos.y - self.hitbox.y/2

    def bottom(self):
        return self.pos.y + self.hitbox.y/2

    def load_assets(self, path):
        for state in self.animations:
            img_path = os.path.join(SPRITE_ASSET_PATH, path, (state + ".png"))
            self.animations[state] = Spritesheet(img_path, 1, self.animations[state])

    def draw(self, canvas, offset=0):
        self.animations[self.state].draw(canvas, Vector(self.pos.x + offset, self.pos.y))

    def in_screen(self, map, offset):
        return self.right() > offset and self.left() < map.get_width() + offset

    def check_death(self):
        if self.health <= 0 or self.pos.y > SCREEN_HEIGHT:
            self.dead = True

    def update(self, clock):
        if not self.dead:
            self.check_death()
            # Handle entity state updates
            if self.type != "bee":
                self.velocity.y += GRAVITY

            # apply gravity if not on platform
            if not self.on_platform:
                self.velocity.y += GRAVITY

            # update position based on gravity
            self.pos.y += self.velocity.y

            self.check_state()
            self.pos.add(self.velocity)
            if clock.transition(self.frame_speed):
                self.animations[self.state].next_frame()

    def jump(self):
        if self.on_platform:
            self.velocity.y = -12
            self.on_platform = False


