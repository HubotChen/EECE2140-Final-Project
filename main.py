import time
import random
import pygame
import colorsys

pygame.font.init()

ROWS = 20
COLS = 10
block_size = 30
W_WIDTH = 690
W_HEIGHT = 690
PW_WIDTH = 300
PW_HEIGHT = 600
PW_X_OFFSET = 30
PW_Y_OFFSET = 60
TEXT_X_OFFSET = PW_WIDTH + (2 * PW_X_OFFSET)
TEXT_Y_OFFSET = PW_Y_OFFSET
FONT_SIZE = 30

COLOR_BACKGROUND = (255, 255, 255)

# shapes
S = [[(1, 0), (2, 0), (0, 1), (1, 1)], [(0, 0), (0, 1), (1, 1), (1, 2)]]
Z = [[(0, 0), (1, 0), (1, 1), (2, 1)], [(1, 0), (0, 1), (1, 1), (0, 2)]]
T = [[(1, 1), (1, 0), (0, 1), (2, 1)], [(1, 1), (1, 0), (2, 1), (1, 2)], [(1, 1), (0, 1), (2, 1), (1, 2)],
     [(1, 1), (1, 0), (0, 1), (1, 2)]]
J = [[(1, 1), (0, 0), (0, 1), (2, 1)], [(1, 1), (1, 0), (2, 0), (1, 2)], [(1, 1), (0, 1), (2, 1), (2, 2)],
     [(1, 1), (1, 0), (0, 2), (1, 2)]]
L = [[(1, 1), (2, 0), (0, 1), (2, 1)], [(1, 1), (1, 0), (2, 2), (1, 2)], [(1, 1), (0, 1), (2, 1), (0, 2)],
     [(1, 1), (1, 0), (0, 0), (1, 2)]]
I = [[(1, 0), (1, 1), (1, 2), (1, 3)], [(0, 1), (1, 1), (2, 1), (3, 1)]]
O = [[(0, 0), (1, 0), (0, 1), (1, 1)]]

SHAPES = [S, Z, T, J, L, I, O]

# Set up the drawing window
screen = pygame.display.set_mode([W_WIDTH, W_HEIGHT])
pygame.display.set_caption('Tetris')
font = pygame.font.Font(pygame.font.get_default_font(), FONT_SIZE)


class Block:
    """ Block class contains a block object which is used by the frozen blocks class to store coordinates and colors

    """

    def __init__(self, x, y, color):
        self.x = x
        self.y = y
        self.color = color

    def get_xy(self):
        return self.x, self.y

    def get_x(self):
        return self.x

    def get_y(self):
        return self.y

    def descend(self):
        self.y += 1


class Shape:
    """ Shape class, contains the coordinates of a shape and its color. Contains methods to get its potential
        coordinates after different moves in order to check for collision. Contains methods to paint a descended
        ghost.

    """

    def __init__(self, type):
        self.shape = type
        self.shape_coords = SHAPES[self.shape]
        self.color = self.shape
        self.x = 11
        self.y = 5
        self.rotation = 0

    def move_to_pw(self):
        self.x = 3
        self.y = 0

    def get_global_coords(self):
        return [(self.x + coord[0], self.y + coord[1]) for coord in self.shape_coords[self.rotation]]

    def get_descended_values(self, drop):
        return [(self.x + coord[0], self.y + coord[1] + drop) for coord in self.shape_coords[self.rotation]]

    def get_shifted_left_values(self):
        return [(self.x + coord[0] - 1, self.y + coord[1]) for coord in self.shape_coords[self.rotation]]

    def get_shifted_right_values(self):
        return [(self.x + coord[0] + 1, self.y + coord[1]) for coord in self.shape_coords[self.rotation]]

    def get_rotated_values(self):
        return [(self.x + coord[0], self.y + coord[1]) for coord in
                self.shape_coords[(self.rotation + 1) % len(self.shape_coords)]]

    def get_rotated_shifted_right_values(self):
        return [(self.x + coord[0] + 1, self.y + coord[1]) for coord in
                self.shape_coords[(self.rotation + 1) % len(self.shape_coords)]]

    def get_rotated_shifted_left_values(self):
        return [(self.x + coord[0] - 1, self.y + coord[1]) for coord in
                self.shape_coords[(self.rotation + 1) % len(self.shape_coords)]]

    def get_rotated_shifted_2left_values(self):
        return [(self.x + coord[0] - 2, self.y + coord[1]) for coord in
                self.shape_coords[(self.rotation + 1) % len(self.shape_coords)]]

    def descend(self, drop):
        self.y += drop

    def rotate(self):
        self.rotation = (self.rotation + 1) % len(self.shape_coords)

    def shift_left(self):
        self.x -= 1

    def shift_right(self):
        self.x += 1

    def paint(self):
        for coord in self.shape_coords[self.rotation]:
            pygame.draw.rect(screen, colors[self.color],
                             (PW_X_OFFSET + ((coord[0] + self.x) * block_size),
                              PW_Y_OFFSET + ((coord[1] + self.y) * block_size), block_size, block_size), 0)

    def paint_ghost(self, drop):
        for coord in self.shape_coords[self.rotation]:
            pygame.draw.lines(screen, colors[self.color], True, (
                ((PW_X_OFFSET + ((coord[0] + self.x) * block_size)),
                 (PW_Y_OFFSET + ((coord[1] + self.y + drop) * block_size))),
                ((PW_X_OFFSET + ((coord[0] + self.x) * block_size) + block_size),
                 (PW_Y_OFFSET + ((coord[1] + self.y + drop) * block_size))),
                ((PW_X_OFFSET + ((coord[0] + self.x) * block_size) + block_size),
                 (PW_Y_OFFSET + ((coord[1] + self.y + drop) * block_size) + block_size)),
                ((PW_X_OFFSET + ((coord[0] + self.x) * block_size)),
                 (PW_Y_OFFSET + ((coord[1] + self.y + drop) * block_size) + block_size))
            ), 2)


class FrozenBlocks:
    """ Contains all the logic for the frozen blocks and the bottom of the tetris game. Contains a list of Block objects

    """

    def __init__(self):
        self.blocks = []

    def create_blocks(self, shape_coords, color):
        for coord in shape_coords:
            self.blocks.append(Block(coord[0], coord[1], color))

    def get_blocks_coords(self):
        return [block.get_xy() for block in self.blocks]

    def get_rows_to_clear(self):
        yCoords = {}
        rows_to_clear = []
        for block in self.blocks:
            yCoord = block.y
            if yCoord in yCoords:
                yCoords[yCoord] += 1
            else:
                yCoords[yCoord] = 1
        for yCoord, num in yCoords.items():
            if num == 10:
                rows_to_clear.append(yCoord)
        return rows_to_clear

    def clear_rows(self, rows_to_check):
        rows_to_clear = self.get_rows_to_clear()
        if rows_to_clear:
            for x in range(5):
                # for row in self.get_rows_to_clear(rows_to_check):
                i = 0
                while i < len(self.blocks):
                    if self.blocks[i].get_y() in rows_to_clear and (
                            self.blocks[i].get_x() == 4 - x or self.blocks[i].get_x() == 5 + x):
                        del self.blocks[i]
                    else:
                        i += 1
                self.clear_pw()
                self.paint()
                pygame.display.update((PW_X_OFFSET + 1, PW_Y_OFFSET + 1, PW_WIDTH - 1, PW_HEIGHT - 1))
                time.sleep(0.1)
            rows_to_clear.sort()
            for row in rows_to_clear:
                for block in self.blocks:
                    if block.get_y() < row:
                        block.descend()
        return len(rows_to_clear)

    def clear_pw(self):
        pygame.draw.rect(screen, (255, 255, 255), (PW_X_OFFSET + 1, PW_Y_OFFSET + 1, PW_WIDTH - 1, PW_HEIGHT - 1), 0)

    def paint(self):
        for block in self.blocks:
            pygame.draw.rect(screen, colors[block.color], (
                block.x * block_size + PW_X_OFFSET, block.y * block_size + PW_Y_OFFSET, block_size, block_size), 0)


class Tetris:
    """ Contains all the high level logic for running the tetris game. Holds 3 other classes, Shape, Frozen blocks,
        and Blocks.
    """

    def __init__(self):
        self.frozen_blocks = FrozenBlocks()
        self.game_lost = False
        self.last_instance = time.time()
        self.fall_time = 0.5
        self.time_multiplier = 0.8
        self.coords_to_check = []
        self.need_new_shape = True
        self.grace_period_start = 0.0
        self.grace_period_len = 0.3
        self.score_value = 0
        self.level = 1
        self.rows_cleared_total = 0
        self.rows_cleared = 0
        self.rows_to_level_up = 2
        self.next_piece = Shape(random.randint(0, 6))
        self.exclusion_list = [None, None]
        self.drought_counter = 0

    def draw_outline(self):
        pygame.draw.lines(screen, (0, 0, 0), True, (
            (PW_X_OFFSET, PW_Y_OFFSET), (PW_X_OFFSET, PW_Y_OFFSET + PW_HEIGHT),
            (PW_X_OFFSET + PW_WIDTH, PW_Y_OFFSET + PW_HEIGHT),
            (PW_X_OFFSET + PW_WIDTH, PW_Y_OFFSET)), 1)

    def check_game_lost(self, shape_coords):
        for coord in shape_coords:
            if coord[1] < 2:
                self.game_lost = True

    def will_collide(self, shape, frozen_blocks, move):
        # move - 0 left, 1 right, 2 down, 3 rotate, 4 rotate shift right, 5 rotate shift left, 6 rotate shift 2left
        if move == 0:
            self.coords_to_check = shape.get_shifted_left_values()
        elif move == 1:
            self.coords_to_check = shape.get_shifted_right_values()
        elif move == 2:
            self.coords_to_check = shape.get_descended_values(1)
        elif move == 3:
            self.coords_to_check = shape.get_rotated_values()
        elif move == 4:
            self.coords_to_check = shape.get_rotated_shifted_right_values()
        elif move == 5:
            self.coords_to_check = shape.get_rotated_shifted_left_values()
        else:
            self.coords_to_check = shape.get_rotated_shifted_2left_values()

        for coord in self.coords_to_check:
            if coord in frozen_blocks.get_blocks_coords() or coord[0] >= COLS or coord[0] < 0 or coord[1] >= ROWS:
                return True
        return False

    def choose_shape_rotation(self, shape, frozen_blocks):
        if not self.will_collide(shape, frozen_blocks, 3):
            shape.rotate()
            return
        if not self.will_collide(shape, frozen_blocks, 4):
            shape.rotate()
            shape.shift_right()
            return
        if not self.will_collide(shape, frozen_blocks, 5):
            shape.rotate()
            shape.shift_left()
            return
        if not self.will_collide(shape, frozen_blocks, 6):
            shape.rotate()
            shape.shift_left()
            shape.shift_left()
            return

    def descend_shape(self, shape, frozen_blocks):
        if not self.will_collide(shape, frozen_blocks, 2):
            shape.descend(1)
        else:
            self.check_game_lost(shape.get_global_coords())
            frozen_blocks.create_blocks(shape.get_global_coords(), shape.color)
            new_rows_cleared = frozen_blocks.clear_rows([xy[1] for xy in shape.get_global_coords()])
            self.update_score(new_rows_cleared)
            self.need_new_shape = True

    def update_score(self, new_rows_cleared):
        self.rows_cleared_total += new_rows_cleared
        self.rows_cleared += new_rows_cleared
        if new_rows_cleared == 4:
            self.score_value += 500
        else:
            self.score_value += 100 * new_rows_cleared
        if self.rows_cleared > self.rows_to_level_up:
            self.level_up()
            self.rows_cleared = 0

    def print_side(self):
        score = font.render("score: " + str(self.score_value), True, (0, 0, 0))
        screen.blit(score, (TEXT_X_OFFSET, TEXT_Y_OFFSET))
        level = font.render("level: " + str(self.level), True, (0, 0, 0))
        screen.blit(level, (TEXT_X_OFFSET, TEXT_Y_OFFSET + FONT_SIZE))
        rows = font.render("rows cleared: " + str(self.rows_cleared_total), True, (0, 0, 0))
        screen.blit(rows, (TEXT_X_OFFSET, TEXT_Y_OFFSET + 2 * FONT_SIZE))
        label = font.render("next piece: ", True, (0, 0, 0))
        screen.blit(label, (TEXT_X_OFFSET, TEXT_Y_OFFSET + 3 * FONT_SIZE))

    def level_up(self):
        self.fall_time *= self.time_multiplier
        self.level += 1
        change_colors()

    def choose_new_shape(self):
        new_shape = random.choice([i for i in range(0, 6) if i not in self.exclusion_list])
        self.exclusion_list.append(new_shape)
        self.exclusion_list.pop(0)
        if new_shape != 5:
            self.drought_counter += 1
            if self.drought_counter > 7:
                self.exclusion_list.append(5)
                self.exclusion_list.pop(0)
                self.drought_counter = 0
                return 5
        else:
            self.drought_counter = 0
        return new_shape

    def run_game(self):
        """ logic for running the tetris game
            :return: None
        """
        frozen_blocks = FrozenBlocks()
        while not self.game_lost:
            if self.need_new_shape:
                shape = self.next_piece
                shape.move_to_pw()
                self.next_piece = Shape(self.choose_new_shape())
                self.need_new_shape = False

            screen.fill((255, 255, 255))
            frozen_blocks.paint()

            outline_collide = False
            drop = 0
            while not outline_collide:
                drop += 1
                self.coords_to_check = shape.get_descended_values(drop)
                for coord in self.coords_to_check:
                    if coord in frozen_blocks.get_blocks_coords() or coord[0] >= COLS or coord[0] < 0 or coord[
                        1] >= ROWS:
                        outline_collide = True
            self.next_piece.paint()
            shape.paint_ghost(drop - 1)
            shape.paint()
            self.draw_outline()
            if time.time() - self.last_instance > self.fall_time:
                if self.will_collide(shape, frozen_blocks, 2):
                    if not self.grace_period_start:
                        self.grace_period_start = time.time()
                    if time.time() - self.grace_period_start > self.grace_period_len:
                        self.descend_shape(shape, frozen_blocks)
                        self.grace_period_start = 0.0
                else:
                    self.descend_shape(shape, frozen_blocks)
                    self.last_instance = time.time()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_DOWN:
                        self.descend_shape(shape, frozen_blocks)
                    if event.key == pygame.K_UP:
                        self.choose_shape_rotation(shape, frozen_blocks)
                    if event.key == pygame.K_LEFT:
                        if not self.will_collide(shape, frozen_blocks, 0):
                            shape.shift_left()
                    if event.key == pygame.K_RIGHT:
                        if not self.will_collide(shape, frozen_blocks, 1):
                            shape.shift_right()
                    if event.key == pygame.K_SPACE:
                        shape.descend(drop - 1)
                        self.descend_shape(shape, frozen_blocks)
            self.print_side()

            pygame.display.update()


button1_outline = (290, 90, 100, 50)
button2_outline = (290, 190, 100, 50)


def paint_start_menu():
    """ function to paint the menu screen
        :return: None
    """
    screen.fill((255, 255, 255))
    pygame.draw.rect(screen, (200, 200, 200), button1_outline, 0)
    pygame.draw.rect(screen, (200, 200, 200), button2_outline, 0)
    start = font.render("Start", True, (0, 0, 0))
    screen.blit(start, (300, 100))
    exit = font.render("Exit", True, (0, 0, 0))
    screen.blit(exit, (300, 200))
    pygame.display.update()


colors = [tuple(round(i * 255) for i in colorsys.hsv_to_rgb(x / 8, 1, 1)) for x in range(7)]


def change_colors():
    """ function that randomizes all of the colors. Used during level ups.
        :return: None
    """
    for i in range(len(colors)):
        colors[i] = (random.randint(10, 255), random.randint(10, 255), random.randint(10, 255))


def main():
    """ main function that contains the logic for the menu screen
        :return:
    """
    while True:
        mouse = pygame.mouse.get_pos()
        paint_start_menu()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if 0 <= mouse[0] - button1_outline[0] <= button1_outline[2] and 0 <= mouse[1] - button1_outline[1] <= \
                        button1_outline[3]:
                    tetris = Tetris()
                    tetris.run_game()
                if 0 <= mouse[0] - button2_outline[0] <= button2_outline[2] and 0 <= mouse[1] - button2_outline[1] <= \
                        button2_outline[3]:
                    pygame.quit()


if __name__ == "__main__":
    main()
