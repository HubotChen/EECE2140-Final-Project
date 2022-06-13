import time
import random
import pygame

pygame.font.init()

row = 20
col = 10
block_size = 30
w_width = 690
w_height = 690
pw_width = 300
pw_height = 600
pw_x_offset = 30
pw_y_offset = 60

background = (255, 255, 255)

# shapes
s = [[(1, 0), (2, 0), (0, 1), (1, 1)], [(0, 0), (0, 1), (1, 1), (1, 2)]]
z = [[(0, 0), (1, 0), (1, 1), (2, 1)], [(1, 0), (0, 1), (1, 1), (0, 2)]]
t = [[(1, 1), (1, 0), (0, 1), (2, 1)], [(1, 1), (1, 0), (2, 1), (1, 2)], [(1, 1), (0, 1), (2, 1), (1, 2)],
     [(1, 1), (1, 0), (0, 1), (1, 2)]]
j = [[(1, 1), (0, 0), (0, 1), (2, 1)], [(1, 1), (1, 0), (2, 0), (1, 2)], [(1, 1), (0, 1), (2, 1), (2, 2)],
     [(1, 1), (1, 0), (0, 2), (1, 2)]]
l = [[(1, 1), (2, 0), (0, 1), (2, 1)], [(1, 1), (1, 0), (2, 2), (1, 2)], [(1, 1), (0, 1), (2, 1), (0, 2)],
     [(1, 1), (1, 0), (0, 0), (1, 2)]]
i = [[(1, 0), (1, 1), (1, 2), (1, 3)], [(0, 1), (1, 1), (2, 1), (3, 1)]]
o = [[(0, 0), (1, 0), (0, 1), (1, 1)]]

shapes = [s, z, t, j, l, i, o]

# Set up the drawing window
screen = pygame.display.set_mode([w_width, w_height])


class Block:
    """

    """

    def __init__(self, x, y, color):
        self.x = x
        self.y = y
        self.color = color

    def get_xy(self):
        return self.x, self.y


class Shape:
    """

    """

    def __init__(self):
        self.shape_coords = shapes[random.randint(0, 6)]
        self.x = 3
        self.y = 0
        self.rotation = 0

    def get_shape_coords(self):
        return self.shape_coords

    def get_descended_values(self):
        return [(self.x + coord[0], self.y + coord[1] + 1) for coord in self.shape_coords[self.rotation]]

    def get_rotated_values(self):
        return [(self.x + coord[0], self.y + coord[1]) for coord in self.shape_coords[(self.rotation + 1) // len(self.shape_coords)]]

    def get_shifted_left_values(self):
        return [(self.x + coord[0] - 1, self.y + coord[1]) for coord in self.shape_coords[self.rotation]]

    def get_shifted_right_values(self):
        return [(self.x + coord[0] + 1, self.y + coord[1]) for coord in self.shape_coords[self.rotation]]

    def descend(self):
        self.y += 1

    def rotate(self):
        self.rotation = (self.rotation + 1) // len(self.shape_coords)

    def shift_left(self):
        self.x -= 1

    def shift_right(self):
        self.x += 1

    def paint(self):
        for coord in self.shape_coords[self.rotation]:
            pygame.draw.rect(screen, (0, 0, 255),
                             (pw_x_offset + ((coord[0] + self.x) * block_size),  pw_y_offset + ((coord[1] + self.y) * block_size), block_size, block_size), 0)

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

    def check_rows(self, rows_to_check):
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

    def paint(self):
        for block in self.blocks:
            pygame.draw.rect(screen, block.color,(block.x * block_size + pw_x_offset, block.y * block_size + pw_y_offset, block_size, block_size), 0)

class Tetris:
    """

    """

    def __init__(self, pw_width, pw_height, pw_x_offset, pw_y_offset):
        self.pw_width = pw_width
        self.pw_height = pw_height
        self.pw_x_offset = pw_x_offset
        self.pw_y_offset = pw_y_offset

        self.frozen_blocks = FrozenBlocks()
        self.game_lost = False
        self.last_instance = time.time()
        self.fall_time = 0.50
        self.coords_to_check = []

    def draw_outline(self):
        pygame.draw.lines(screen, (0, 0, 0), True, (
        (self.pw_x_offset, self.pw_y_offset), (self.pw_x_offset, self.pw_y_offset + self.pw_height),
        (self.pw_x_offset + self.pw_width, self.pw_y_offset + self.pw_height),
        (self.pw_x_offset + self.pw_width, self.pw_y_offset)), 1)

    def is_game_lost(self, shape_coords):
        for block in shape_coords:
            if block[1] < 0:
                return True

    def will_collide(self, shape, frozen_blocks, move):
        # move - 0 rotate, 1 right, 2 left, 3 down
        if move == 0:
            self.coords_to_check = shape.get_rotated_values()
        elif move == 1:
            self.coords_to_check = shape.get_shifted_right_values()
        elif move == 2:
            self.coords_to_check = shape.get_shifted_left_values()
        else:
            self.coords_to_check = shape.get_descended_values()

        for coord in self.coords_to_check:
            if coord in frozen_blocks.get_blocks_coords() or coord[0] >= col or coord[0] < 0 or coord[1] >= row:
                return True
        return False

    def erase(self, coords):
        pass

    def run_game(self):
        shape = Shape()
        while not self.game_lost:
            if time.time() - self.last_instance > self.fall_time:
                shape.descend()
                self.last_instance = time.time()




# Run until the user asks to quit
running = True
tetris = Tetris(pw_width, pw_height, pw_x_offset, pw_y_offset)
shape = Shape()
while running:
    shape.paint()
    # Did the user click the window close button?
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Fill the background with white
    screen.fill((255, 255, 255))

    shape.paint()
    tetris.draw_outline()
#    for coord in l[0]:
#        pygame.draw.rect(screen, (0, 0, 255), (coord[0] * block_size, coord[1] * block_size, block_size, block_size), 0)

    # Flip the display
    pygame.display.flip()

# Done! Time to quit.
pygame.quit()
