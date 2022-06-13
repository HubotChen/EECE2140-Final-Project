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

# shapes
s = [[(1, 0), (2, 0), (0, 1), (1, 1)], [(0, 0), (0, 1), (1, 1), (1, 2)]]
z = [[(0, 0), (1, 0), (1, 1), (2, 1)], [(1, 0), (0, 1), (1, 1), (0, 2)]]
t = [[(1, 1), (1, 0), (0, 1), (2, 1)], [(1, 1), (1, 0), (2, 1), (1, 2)], [(1, 1), (0, 1), (2, 1), (1, 2)], [(1, 1), (1, 0), (0, 1), (1, 2)]]
j = [[(1, 1), (0, 0), (0, 1), (2, 1)], [(1, 1), (1, 0), (2, 0), (1, 2)], [(1, 1), (0, 1), (2, 1), (2, 2)], [(1, 1), (1, 0), (0, 2), (1, 2)]]
l = [[(1, 1), (2, 0), (0, 1), (2, 1)], [(1, 1), (1, 0), (2, 2), (1, 2)], [(1, 1), (0, 1), (2, 1), (0, 2)], [(1, 1), (1, 0), (0, 0), (1, 2)]]
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
        self.x = random.randint(0, 10)
        self.y = 0

    def get_shape_coords(self):
        return self.shape_coords


class FrozenBlocks:
    """

    """

    def __init__(self):
        self.blocks = []

    def create_blocks(self, shape_coords, color):
        for coord in shape_coords:
            self.blocks.append(Block(coord[0], coord[1], color))

    def get_blocks_no_color(self):
        return [block.get_xy() for block in self.blocks]

    def check_rows(self, rows_to_check):
        yCoords = {}
        for block in [block for block in self.blocks if block.y in rows_to_check]:
            yCoord = block.y
            if yCoord in yCoords:
                yCoords[yCoord] += 1
            else:
                yCoords[yCoord] = 1
        for yCoord in yCoords:


class Tetris:
    """

    """

    def __init__(self, pw_width, pw_height, pw_x_offset, pw_y_offset):
        self.pw_width = pw_width
        self.pw_height = pw_height
        self.pw_x_offset = pw_x_offset
        self.pw_y_offset = pw_y_offset

    def draw_outline(self):
        pygame.draw.lines(screen, (0, 0, 0), True, ((self.pw_x_offset, self.pw_y_offset), (self.pw_x_offset, self.pw_y_offset + self.pw_height), (self.pw_x_offset + self.pw_width, self.pw_y_offset + self.pw_height), (self.pw_x_offset + self.pw_width, self.pw_y_offset)), 1)


# Run until the user asks to quit
running = True
tetris = Tetris(pw_width, pw_height, pw_x_offset, pw_y_offset)
while running:

    # Did the user click the window close button?
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    tetris.draw_outline()

    # Fill the background with white
    screen.fill((255, 255, 255))
    tetris.draw_outline()
    for coord in l[0]:
        pygame.draw.rect(screen, (0, 0, 255), (coord[0] * block_size, coord[1] * block_size, block_size, block_size), 0)

    # Flip the display
    pygame.display.flip()

# Done! Time to quit.
pygame.quit()