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

COLORS = [tuple(round(i * 255) for i in colorsys.hsv_to_rgb(x / 8, 1, 1)) for x in range(7)]
print(COLORS)


# Set up the drawing window
screen = pygame.display.set_mode([W_WIDTH, W_HEIGHT])


class Block:
    """

    """

    def __init__(self, x, y, color):
        self.x = x
        self.y = y
        self.color = color

    def get_xy(self):
        return self.x, self.y

    def get_y(self):
        return self.y

    def descend(self):
        self.y += 1


class Shape:
    """

    """

    def __init__(self):
        self.shape = random.randint(0, 6)
        self.shape_coords = SHAPES[self.shape]
        self.color = COLORS[self.shape]
        self.x = 3
        self.y = -1
        self.rotation = 0

    def get_global_coords(self):
        return [(self.x + coord[0], self.y + coord[1]) for coord in self.shape_coords[self.rotation]]

    def get_descended_values(self):
        return [(self.x + coord[0], self.y + coord[1] + 1) for coord in self.shape_coords[self.rotation]]

    def get_rotated_values(self):
        return [(self.x + coord[0], self.y + coord[1]) for coord in
                self.shape_coords[(self.rotation + 1) % len(self.shape_coords)]]

    def get_shifted_left_values(self):
        return [(self.x + coord[0] - 1, self.y + coord[1]) for coord in self.shape_coords[self.rotation]]

    def get_shifted_right_values(self):
        return [(self.x + coord[0] + 1, self.y + coord[1]) for coord in self.shape_coords[self.rotation]]

    def get_rotated_shifted_right_values(self):
        return [(self.x + coord[0] + 1, self.y + coord[1]) for coord in
                self.shape_coords[(self.rotation + 1) % len(self.shape_coords)]]

    def get_rotated_shifted_left_values(self):
        return [(self.x + coord[0] - 1, self.y + coord[1]) for coord in
                self.shape_coords[(self.rotation + 1) % len(self.shape_coords)]]

    def get_rotated_shifted_2left_values(self):
        return [(self.x + coord[0] - 2, self.y + coord[1]) for coord in
                self.shape_coords[(self.rotation + 1) % len(self.shape_coords)]]

    def descend(self):
        self.y += 1

    def rotate(self):
        self.rotation = (self.rotation + 1) % len(self.shape_coords)

    def shift_left(self):
        self.x -= 1

    def shift_right(self):
        self.x += 1

    def paint(self):
        for coord in self.shape_coords[self.rotation]:
            pygame.draw.rect(screen, self.color,
                             (PW_X_OFFSET + ((coord[0] + self.x) * block_size),
                              PW_Y_OFFSET + ((coord[1] + self.y) * block_size), block_size, block_size), 0)


class FrozenBlocks:
    """

    """

    def __init__(self):
        self.blocks = []

    def create_blocks(self, shape_coords, color):
        for coord in shape_coords:
            self.blocks.append(Block(coord[0], coord[1], color))

    def get_blocks_coords(self):
        return [block.get_xy() for block in self.blocks]

    def get_rows_to_clear(self, rows_to_check):
        yCoords = {}
        rows_to_clear = []
        for block in [block for block in self.blocks if block.y in rows_to_check]:
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
        for row in self.get_rows_to_clear(rows_to_check):
            i = 0
            while i < len(self.blocks):
                if self.blocks[i].get_y() == row:
                    del self.blocks[i]
                else:
                    if self.blocks[i].get_y() < row:
                        self.blocks[i].descend()
                    i += 1


    def paint(self):
        for block in self.blocks:
            pygame.draw.rect(screen, block.color, (
                block.x * block_size + PW_X_OFFSET, block.y * block_size + PW_Y_OFFSET, block_size, block_size), 0)


class Tetris:
    """

    """

    def __init__(self):
        self.frozen_blocks = FrozenBlocks()
        self.game_lost = False
        self.last_instance = time.time()
        self.fall_time = 0.1
        self.coords_to_check = []
        self.need_new_shape = True
        self.grace_period_start = 0.0
        self.grace_period_len = 0.3

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
            self.coords_to_check = shape.get_descended_values()
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
            shape.descend()
        else:
            self.check_game_lost(shape.get_global_coords())
            frozen_blocks.create_blocks(shape.get_global_coords(), shape.color)
            frozen_blocks.clear_rows([xy[1] for xy in shape.get_global_coords()])
            self.need_new_shape = True

    def run_game(self):
        frozen_blocks = FrozenBlocks()
        while not self.game_lost:
            if self.need_new_shape:
                shape = Shape()
                self.need_new_shape = False

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.game_lost = True
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

            screen.fill((255, 255, 255))
            frozen_blocks.paint()
            shape.paint()
            self.draw_outline()

            pygame.display.flip()



# Run until the user asks to quit
tetris = Tetris()
tetris.run_game()

pygame.quit()
