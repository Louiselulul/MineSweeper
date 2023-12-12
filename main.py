import pygame
import random
from settings import *
import settings
from sprites import *


################Xiaojun Chen########################################################
class Tile:
    """
    type list:
        "U" = unknown/unclicked block
        "M" = mine
        "n" = numbers shown on board as clues
        "." = blank/empty spot
    """

    def __init__(self, x, y, img, tile_type, reveal=False, flag=False):
        self.x = x * tile_size
        self.y = y * tile_size
        self.img = img
        self.tile_type = tile_type
        self.reveal = reveal
        self.flag = flag

    def make_board(self, board_surface):
        # We put either a mine or number on a revealed (clicked) tile
        # We also make sure that this tile has no flag
        if not self.flag and self.reveal:
            board_surface.blit(self.img, (self.x, self.y))
        # We put a flag on unknown (revealed) tile if right-clicked
        elif self.flag and not self.reveal:
            board_surface.blit(tile_flag, (self.x, self.y))
        # Placing unknown tile
        elif not self.reveal:
            board_surface.blit(tile_unknown, (self.x, self.y))

    def __repr__(self):
        """
        This can print the board in console
        """
        return self.tile_type


class GameBoard:
    def __init__(self):
        self.board_surface = pygame.Surface((default_width, default_height))
        self.board_element = [[Tile(c, r, tile_blank, ".")
                               for r in range(default_row)] for c in range(default_col)]
        self.lay_mine()
        self.put_numbers()
        self.uncover_history = []

    def lay_mine(self):
        for _ in range(num_mine):
            while True:
                # Generate a random location for laying mines
                x_val = random.randint(0, default_row - 1)
                y_val = random.randint(0, default_col - 1)
                # Change the existing blank tile to mine tile
                if self.board_element[x_val][y_val].tile_type == ".":
                    self.board_element[x_val][y_val].img = tile_mine
                    self.board_element[x_val][y_val].tile_type = "M"
                    break

    def put_numbers(self):
        for x in range(default_row):
            for y in range(default_col):
                if self.board_element[x][y].tile_type != "M":
                    mine_count = self.check_neighbors(x, y)
                    # If we found a block that needs a number in it
                    if mine_count > 0:
                        self.board_element[x][y].img = tile_list[mine_count-1]
                        self.board_element[x][y].tile_type = "n"

    def place_mines_post_first_click(self, first_click_x, first_click_y):
        # Define the safe zone around the first click
        safe_zone = [(x, y) for x in range(first_click_x - 1, first_click_x + 2)
                     for y in range(first_click_y - 1, first_click_y + 2)
                     if 0 <= x < default_row and 0 <= y < default_col]

        mines_placed = 0
        while mines_placed < num_mine:
            x = random.randint(0, default_row - 1)
            y = random.randint(0, default_col - 1)

            if (x, y) not in safe_zone and self.board_element[x][y].tile_type == ".":
                self.board_element[x][y].tile_type = "X"
                mines_placed += 1
        self.put_numbers()

    @staticmethod
    def boundary_check(x, y):
        """
        This is to check if we're inside the boards' boundary.
        """
        check = 0 <= x < default_row and 0 <= y < default_col
        return check

    def check_neighbors(self, x, y):
        mine_count = 0
        # coordinates of the neighbors around our tile of interest
        # starting from top left of it which is (-1,-1)
        for x1 in range(-1, 2):
            for y1 in range(-1, 2):
                nb_x = x + x1
                nb_y = y + y1
                # check if neighbor is within boundary
                if self.boundary_check(nb_x, nb_y):
                    # check if neighbor is a mine
                    if self.board_element[nb_x][nb_y].tile_type == "M":
                        mine_count += 1
        return mine_count

    def make_board(self, screen):
        for r in self.board_element:
            for tile in r:
                tile.make_board(self.board_surface)
        screen.blit(self.board_surface, (0, 0))  # top left corner of the screen

    def uncover(self, x, y):
        self.uncover_history.append((x, y))
        # If we uncover and hit a mine, mine explodes
        if self.board_element[x][y].tile_type == "M":
            self.board_element[x][y].reveal = True
            self.board_element[x][y].img = tile_mine_explode
            return False
        # If we uncover and hit a number
        elif self.board_element[x][y].tile_type == "n":
            self.board_element[x][y].reveal = True
            return True
        self.board_element[x][y].reveal = True
        # Recursively run this loop when we uncover and hit a blank tile
        # This loop will stop when it finds a number
        for r in range(max(0, x-1), min(default_row-1, x+1)+1):
            for c in range(max(0, y - 1), min(default_col - 1, y+1)+1):
                # check if the coordinate is already explored
                if (r, c) not in self.uncover_history:
                    self.uncover(r, c)
        return True


    def show_board(self):
        for r in self.board_element:
            print(r)



################Yuqing Lu########################################################
class PygameGame:
    def __init__(self):
        pygame.init()
        self.settings = settings
        self.screen = pygame.display.set_mode((self.settings.default_width, self.settings.default_height))
        pygame.display.set_caption(self.settings.title)
        self.clock = pygame.time.Clock()
        self.board = GameBoard()
        self.is_playing = False
        self.start_time = None
        self.first_click = True

    def start_new_game(self):
        self.board = GameBoard()
        self.board.show_board()
        self.start_time = pygame.time.get_ticks()

    def game_loop(self):
        self.is_playing = True
        while self.is_playing:
            self.clock.tick(self.settings.FPS)
            self.handle_events()
            self.update_screen()
            self.render_timer()
        else:
            self.show_end_screen()

    def update_screen(self):
        self.screen.fill(self.settings.bg_color)
        self.board.make_board(self.screen)
        pygame.display.flip()

    def render_timer(self):
        elapsed_time = (pygame.time.get_ticks() - self.start_time) // 1000  # Convert milliseconds to seconds
        timer_font = pygame.font.Font(None, 36)  # Choose an appropriate font and size
        timer_surface = timer_font.render(str(elapsed_time), True, self.settings.white)  # Render the time as text
        self.screen.blit(timer_surface, (10, 10))  # Position the timer on the screen
        pygame.display.update()

    def check_victory(self):
        for row in self.board.board_element:
            for tile in row:
                # If a non-mine tile is not revealed, return False
                if tile.tile_type != "M" and not tile.reveal:
                    return False
        # If all non-mine tiles are revealed, return True
        return True

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.is_playing = False
                pygame.quit()
                quit()

            if event.type == pygame.MOUSEBUTTONDOWN:
                mx, my = pygame.mouse.get_pos()
                x, y = mx // self.settings.tile_size, my // self.settings.tile_size

                if event.button == 1:
                    self.left_click_action(x, y)

                if event.button == 3:
                    self.right_click_action(x, y)

        if self.check_victory():
            self.declare_victory()

    def left_click_action(self, x, y):
        if self.first_click:
            self.board.place_mines_post_first_click(x, y)
            self.first_click = False

        if not self.board.board_element[x][y].flag:
            if not self.board.uncover(x, y):
                self.explode_mines()
                self.is_playing = False

    def right_click_action(self, x, y):
        tile = self.board.board_element[x][y]
        if not tile.reveal:
            tile.flag = not tile.flag

    def explode_mines(self):
        for row in self.board.board_element:
            for tile in row:
                if tile.tile_type == "M":
                    tile.reveal = True  # Reveal all mines
                    # tile.img = self.settings.tile_mine  # Show mine image
                if tile.flag and tile.tile_type != "M":
                    tile.flag = False
                    tile.reveal = True
                    tile.img = self.settings.tile_mine_wrong

    def show_end_screen(self):
        print("Game Over!")
        self.explode_mines()  # Reveal all tiles

        # Show the final state of the board for 2 minutes
        end_time = pygame.time.get_ticks() + 120000  # 120000 milliseconds = 2 minutes
        while pygame.time.get_ticks() < end_time:
            self.update_screen()
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    exit()

    def declare_victory(self):
        self.is_playing = False


if __name__ == "__main__":
    game = PygameGame()
    game.start_new_game()
    game.game_loop()
