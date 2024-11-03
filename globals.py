try:
    import simplegui
    from simplegui import _load_local_image as load_image
except ImportError:
    import SimpleGUICS2Pygame.simpleguics2pygame as simplegui
    from SimpleGUICS2Pygame.simpleguics2pygame import _load_local_image as load_image
import os
from Vector import Vector
from csv import reader

# GLBOAL VARIABLES
# Defining screen dimensions
SCREEN_WIDTH = 1280
SCREEN_HEIGHT = 720

TILE_SIZE = 16
FRAME_SPEED = 5

# Get the root directory of the project
ROOT_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# Define the paths to the resource directories
SPRITE_ASSET_PATH = os.path.join(ROOT_DIR, 'res', 'sprite')
LEVEL_LAYOUT_PATH = os.path.join(ROOT_DIR, 'res', 'layout')
MAP_PATH = os.path.join(LEVEL_LAYOUT_PATH, 'game_map.png')

# Defining player characteristics
PLAYER_SPEED = 8

GRAVITY = 0.4

# GLOBAL FUNCTIONS
def import_layout(path):
    layer = []
    file_path = os.path.join(LEVEL_LAYOUT_PATH, path)
    with open(file_path) as level:
            layout = reader(level, delimiter=',')
            for row in layout:
                layer.append(list(row))
    return layer


# GLOBAL CLASSES
class Spritesheet:
    def __init__(self, path, rows, columns):
        # Initialize the Spritesheet class with the given URL, number of rows, and columns in the spritesheet image #
        self.image = load_image(path)
        self.rows = rows
        self.columns = columns
        self.current_row = 0
        self.current_column = 0
        self.frame_index = 0

        # dimensions of image known only after being loaded
        self.width = None
        self.height = None
        self.frame_width = None
        self.frame_height = None

    def draw(self, canvas, pos, flip_direction=False):
        # Draw the current frame of the spritesheet on the canvas #
        if self.width is None or self.height is None:
            self.width = self.image.get_width()
            self.height = self.image.get_height()
            self.frame_width = self.width / self.columns
            self.frame_height = self.height / self.rows

        center_source = (self.frame_width * (0.5 + self.current_column),
                         self.frame_height * (0.5 + self.current_row))
        center_dest = (pos.x, pos.y)

        if flip_direction:
            canvas.draw_image(self.image, center_source, (self.frame_width, self.frame_height),
                              center_dest, (self.frame_width, self.frame_height), 600)
        else:
            canvas.draw_image(self.image, center_source, (self.frame_width, self.frame_height),
                          center_dest, (self.frame_width, self.frame_height))

    def set_tile(self, tile):
        self.frame_index = tile
        self.current_row = self.frame_index // self.columns
        self.current_column = self.frame_index % self.columns

    def next_frame(self):
        # Update to the next frame in the spritesheet
        self.frame_index += 1
        if self.frame_index >= self.rows * self.columns:
            self.frame_index = 0
        self.current_row = self.frame_index // self.columns
        self.current_column = self.frame_index % self.columns


class Clock:
    def __init__(self):
        # Initialize the Clock class #
        self.time = 0

    def tick(self):
        # Increment the time by 1 #
        self.time += 1

    def transition(self, frame_duration):
        # Check if it's time for frame transition based on frame duration #
        return self.time % frame_duration == 0


class Tile:
    def __init__(self, pos, image, type):
        self.pos = pos
        self.hitbox = (16, 16)
        self.image = image
        self.type = type

    def draw(self, canvas):
        canvas.draw_image(self.image, (8, 8), (16, 16), self.pos.get_p(), (16, 16))

