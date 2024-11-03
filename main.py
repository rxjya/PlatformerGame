try:
    import simplegui
    from simplegui import _load_local_image as load_image
except ImportError:
    import SimpleGUICS2Pygame.simpleguics2pygame as simplegui
    from SimpleGUICS2Pygame.simpleguics2pygame import _load_local_image as load_image
from player import Player
from ui import *
from enemy import *
from platforms import *
import time

class Main:
    def __init__(self):
        print(ROOT_DIR)
        print(MAP_PATH)
        print(LEVEL_LAYOUT_PATH)
        print(SPRITE_ASSET_PATH)
        print(ROOT_DIR)

        self.map = load_image(MAP_PATH)

        # Initialise player and keyboard
        self.player = None
        self.health_bar = None

        self.keyboard = Keyboard()
        # Initialise enemies
        self.enemies = []
        self.clock = Clock()

        self.layout =  {
            "platform_collide": import_layout("game_map_platform_collide.csv"),
            "mob_barrier": import_layout("game_map_mob_barrier.csv"),
            "win_condition": import_layout("game_map_win_condition.csv"),
            "enemies": import_layout("game_map_enemies.csv"),
        }

        self.platforms = []
        self.mob_barriers = []
        self.win_conditions = []
        self.create_level()

        self.interaction = Interaction(self.player, self.keyboard, self.enemies, self.platforms, self.mob_barriers)

        self.running = False
        self.title_screen = Screen("THE GAME", "Press Space to Start", "title")
        self.win_screen = Screen("You Win!", "Press Space to return to the title screen", "win")
        self.game_over_screen = Screen("Game Over", "Press Space to return to the title screen", "game_over")
        self.current_screen = self.title_screen
        self.can_input = True

        # Initialize the frame and handlers
        self.frame = simplegui.create_frame('Game name here', SCREEN_WIDTH, SCREEN_HEIGHT)
        self.frame.set_canvas_background('black')
        self.frame.set_draw_handler(self.draw)
        self.frame.set_keydown_handler(self.keyboard.key_down)
        self.frame.set_keyup_handler(self.keyboard.key_up)

        self.last_time = time.time()
    def create_level(self):
        for style, layout in self.layout.items():
            for i, row in enumerate(layout):
                for j, tile in enumerate(row):
                    if tile != "-1":
                        x = j * TILE_SIZE
                        y = i * TILE_SIZE
                        if style == "platform_collide" or style == "mob_barrier" or style == "win_condition":
                            if tile == "0":
                                self.platforms.append(SolidPlatform(Vector(x, y), Vector(TILE_SIZE, TILE_SIZE)))
                            elif tile == "1":
                                self.platforms.append(PhasablePlatform(Vector(x, y), Vector(TILE_SIZE, TILE_SIZE)))
                            elif tile == "2":
                                self.win_conditions.append(WinCondition(Vector(x, y), Vector(TILE_SIZE, TILE_SIZE)))
                            elif tile == "3":
                                self.mob_barriers.append(MobBarrier(Vector(x, y), Vector(TILE_SIZE, TILE_SIZE)))
                        if style == "enemies":
                            if tile == "0":
                                self.enemies.append(Boar(Vector(x, y), Vector(48, 32)))
                            elif tile == "1":
                                self.enemies.append(Bee(Vector(x, y), Vector(64, 64)))

    def get_camera_offset(self):
        center_x = SCREEN_WIDTH / 2
        map_width = self.map.get_width()

        if self.player.pos.x < center_x:
            return 0
        elif self.player.pos.x > map_width - center_x:
           return SCREEN_WIDTH - map_width
        else:
           return center_x - self.player.pos.x

    def check_screen(self):
        if self.keyboard.space and self.can_input:
            if self.current_screen.type == "title":
                self.running = True
                self.reset()
            elif self.current_screen.type == "win" or self.current_screen.type == "game_over":
                self.running = False
                self.current_screen = self.title_screen

    def check_win(self):
        for win_condition in self.win_conditions:
            if win_condition.check_win(self.player):
                self.running = False
                self.current_screen = self.win_screen

    def kill_entity(self):
        for enemy in self.enemies:
            if enemy.dead:
                self.enemies.remove(enemy)
        if self.player.dead:
            self.running = False
            self.current_screen = self.game_over_screen

    def reset(self):
        self.player = Player(Vector(100, 500), Vector(30, 30))
        self.health_bar = HealthBar(self.player.health)
        self.platforms = []
        self.mob_barriers = []
        self.win_conditions = []
        self.enemies = []
        self.create_level()
        self.interaction = Interaction(self.player, self.keyboard, self.enemies, self.platforms, self.mob_barriers)

        self.game_score = 0

    def check_input(self):
        if self.keyboard.space and self.can_input:
            self.can_input = False
        elif not self.keyboard.space and not self.can_input:
            self.can_input = True

    def draw(self, canvas):
        if self.running:
            self.clock.tick()
            current_time = time.time()
            elapsed_time = current_time - self.last_time
            offset = self.get_camera_offset()
            self.last_time = current_time

            self.interaction.update(self.map)
            self.player.update(self.clock)
            self.kill_entity()

            canvas.draw_image(self.map, (self.map.get_width() / 2, self.map.get_height() / 2),
                              (self.map.get_width(), self.map.get_height()),
                              (self.map.get_width() / 2 + offset, SCREEN_HEIGHT / 2),
                              (self.map.get_width(), self.map.get_height()))

            for platform in self.platforms:
                if platform.type == "phasable":
                    platform.check_player_interaction(self.player, self.keyboard)

            canvas.draw_text(f"Time: {self.game_score:.0f}", (50, 50), 20, "Black")

            self.player.draw(canvas, offset)
            for enemy in self.enemies:
                enemy.update(self.clock)
                if enemy.in_screen(self.map, offset):
                    enemy.draw(canvas, offset)

            self.health_bar.draw(canvas, self.player.health)
            self.game_score += elapsed_time

        else:
            self.current_screen.draw(canvas)
            self.check_screen()
            self.check_input()


if __name__ == '__main__':
    main = Main()
    main.frame.start()
