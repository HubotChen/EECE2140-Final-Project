import time
import random
import pygame
import colorsys

pygame.font.init()

ROWS = 20
COLS = 10
BLOCK_SIZE = 30
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
        """ constructor for Block
        :param x: an integer containing the x coordinate
        :param y: an integer containing the y coordinate
        :param color: a 3x1 tuple, containing RGB values
        """
        self.x = x
        self.y = y
        self.color = color

    def get_xy(self):
        """ accessor for the coordinates of a block
        :return: a 2x1 tuple, containing the x and y coordinates in integers
        """
        return self.x, self.y

    def get_x(self):
        """ accessor for the x coordinate of a block
        :return: x coordinate as an integer
        """
        return self.x

    def get_y(self):
        """ accessor for the y coordinate of a block
        :return: y coordinate as an integer
        """
        return self.y

    def descend(self):
        """ adds 1 to the y coordinate, lowering the block on the screen
        :return: None
        """
        self.y += 1


class Shape:
    """ Shape class, contains the coordinates of a shape and its color. Contains methods to get its potential
        coordinates after different moves in order to check for collision. Contains methods to paint a descended
        ghost.

    """

    def __init__(self, type):
        """ default constructor for a shape object
        :param type: an integer describing which type of shape it is
        """
        self.shape = type
        self.shape_coords = SHAPES[self.shape]
        self.color = self.shape
        self.x = 11 # position for the next piece window
        self.y = 5
        self.rotation = 0

    def move_to_pw(self):
        """ moves a piece to the top of the play window
        :return: None
        """
        self.x = 3
        self.y = 0

    def get_global_coords(self):
        """ gets the global coordinates of each part of the piece relative to the play window
        :return: a 4x1 list of 2x1 tuples each containing global coordinates of each part of a piece
        """
        return [(self.x + coord[0], self.y + coord[1]) for coord in self.shape_coords[self.rotation]]

    def get_descended_values(self, drop):
        """ gets the global coordinates of each part of the piece relative to the play window after being dropped a drop units
        :param drop: an integer
        :return: a 4x1 list of 2x1 tuples each containing global coordinates of each part of a piece after being dropped drop units
        """
        return [(self.x + coord[0], self.y + coord[1] + drop) for coord in self.shape_coords[self.rotation]]

    def get_shifted_left_values(self):
        """ gets the global coordinates of each part of the piece relative to the play window after being shifted left 1 unit
        :return: a 4x1 list of 2x1 tuples each containing global coordinates of each part of a piece after being shifted left 1 unit
        """
        return [(self.x + coord[0] - 1, self.y + coord[1]) for coord in self.shape_coords[self.rotation]]

    def get_shifted_right_values(self):
        """ gets the global coordinates of each part of the piece relative to the play window after being shifted right 1 unit
        :return: a 4x1 list of 2x1 tuples each containing global coordinates of each part of a piece after being shifted right 1 unit
        """
        return [(self.x + coord[0] + 1, self.y + coord[1]) for coord in self.shape_coords[self.rotation]]

    def get_rotated_values(self):
        """ gets the global coordinates of each part of the piece relative to the play window after being rotated
        :return: a 4x1 list of 2x1 tuples each containing global coordinates of each part of a piece after being rotated
        """
        return [(self.x + coord[0], self.y + coord[1]) for coord in
                self.shape_coords[(self.rotation + 1) % len(self.shape_coords)]]

    def get_rotated_shifted_right_values(self):
        """ gets the global coordinates of each part of the piece relative to the play window after being rotated and shifted right 1 unit
        :return: a 4x1 list of 2x1 tuples each containing global coordinates of each part of a piece after being rotated and shifted right 1 unit
        """
        return [(self.x + coord[0] + 1, self.y + coord[1]) for coord in
                self.shape_coords[(self.rotation + 1) % len(self.shape_coords)]]

    def get_rotated_shifted_left_values(self):
        """ gets the global coordinates of each part of the piece relative to the play window after being rotated and shifted left 1 unit
        :return: a 4x1 list of 2x1 tuples each containing global coordinates of each part of a piece after being rotated and shifted left 1 unit
        """
        return [(self.x + coord[0] - 1, self.y + coord[1]) for coord in
                self.shape_coords[(self.rotation + 1) % len(self.shape_coords)]]

    def get_rotated_shifted_2left_values(self):
        """ gets the global coordinates of each part of the piece relative to the play window after being rotated and shifted left 2 units
        :return: a 4x1 list of 2x1 tuples each containing global coordinates of each part of a piece after being rotated and shifted left 2 units
        """
        return [(self.x + coord[0] - 2, self.y + coord[1]) for coord in
                self.shape_coords[(self.rotation + 1) % len(self.shape_coords)]]

    def descend(self, drop):
        """ adds drop units to the y coordinate
        :param drop: an integer
        :return: None
        """
        self.y += drop

    def rotate(self):
        """ adds 1 to the rotation, loops back to 0 if there is no next rotation configuration
        :return: None
        """
        self.rotation = (self.rotation + 1) % len(self.shape_coords)

    def shift_left(self):
        """ subtracts 1 unit from the x coordinate, shifting it left
        :return: None
        """
        self.x -= 1

    def shift_right(self):
        """ adds 1 unit from the x coordinate, shifting it left
        :return: None
        """
        self.x += 1

    def paint(self):
        """ uses the pygame draw.rect function to paint the shape
        :return:None
        """
        for coord in self.shape_coords[self.rotation]:
            pygame.draw.rect(screen, colors[self.color],
                             (PW_X_OFFSET + ((coord[0] + self.x) * BLOCK_SIZE),
                              PW_Y_OFFSET + ((coord[1] + self.y) * BLOCK_SIZE), BLOCK_SIZE, BLOCK_SIZE), 0)

    def paint_ghost(self, drop):
        """ Uses the pygame draw.lines function to draw the ghost of shape drop units below
        :param drop: an integer
        :return: None
        """
        for coord in self.shape_coords[self.rotation]:
            pygame.draw.lines(screen, colors[self.color], True, (
                ((PW_X_OFFSET + ((coord[0] + self.x) * BLOCK_SIZE)),
                 (PW_Y_OFFSET + ((coord[1] + self.y + drop) * BLOCK_SIZE))),
                ((PW_X_OFFSET + ((coord[0] + self.x) * BLOCK_SIZE) + BLOCK_SIZE),
                 (PW_Y_OFFSET + ((coord[1] + self.y + drop) * BLOCK_SIZE))),
                ((PW_X_OFFSET + ((coord[0] + self.x) * BLOCK_SIZE) + BLOCK_SIZE),
                 (PW_Y_OFFSET + ((coord[1] + self.y + drop) * BLOCK_SIZE) + BLOCK_SIZE)),
                ((PW_X_OFFSET + ((coord[0] + self.x) * BLOCK_SIZE)),
                 (PW_Y_OFFSET + ((coord[1] + self.y + drop) * BLOCK_SIZE) + BLOCK_SIZE))
            ), 2)


class FrozenBlocks:
    """ Contains all the logic for the frozen blocks and the bottom of the tetris game. Contains a list of Block objects

    """

    def __init__(self):
        """ Constructor for FrozenBlocks class. Creates an empty list
        """
        self.blocks = []

    def create_blocks(self, shape_coords, color):
        """ Takes in a list of coordinates and a color, and creates block objects accordingly, and adds them to the list of blocks
        :param shape_coords: a 4x1 list of 2x1 tuples containing the coordinates of each part of a shape
        :param color: an integer, which is used to refer to a global variable list of colors
        :return: None
        """
        for coord in shape_coords:
            self.blocks.append(Block(coord[0], coord[1], color))

    def get_blocks_coords(self):
        """ gets all the coordinates of the blocks contained in frozen blocks
        :return: a list of 2x1 tuples containing the coordinates of the blocks in frozen blocks
        """
        return [block.get_xy() for block in self.blocks]

    def get_rows_to_clear(self):
        """ Checks for any rows that are completed
        :return: a list of rows that have more than 9 blocks in them, meaning that they are completed
        """
        yCoords = {} # uses a dictionary to count the blocks in each row
        rows_to_clear = []
        for block in self.blocks:
            yCoord = block.y
            if yCoord in yCoords:
                yCoords[yCoord] += 1
            else:
                yCoords[yCoord] = 1
        for yCoord, num in yCoords.items():
            if num > 9:
                rows_to_clear.append(yCoord)
        return rows_to_clear

    def clear_rows(self):
        """ Clears all the full rows after calling get_rows_to_clear(). Enters a loop that "pauses" the game while it plays a small animation of the blocks clearning
        :return: an integer of the number of rows cleared
        """
        rows_to_clear = self.get_rows_to_clear()
        if rows_to_clear:

            for x in range(5):
                i = 0
                # deletes all the blocks in each column, starting from the middle 2 and expanding outwards
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
        """ clears the play window by painting it all white
        :return: None
        """
        pygame.draw.rect(screen, (255, 255, 255), (PW_X_OFFSET + 1, PW_Y_OFFSET + 1, PW_WIDTH - 1, PW_HEIGHT - 1), 0)

    def paint(self):
        """ Draws out all the blocks stored in self.blocks using draw.rect function
        :return: None
        """
        for block in self.blocks:
            pygame.draw.rect(screen, colors[block.color], (
                block.x * BLOCK_SIZE + PW_X_OFFSET, block.y * BLOCK_SIZE + PW_Y_OFFSET, BLOCK_SIZE, BLOCK_SIZE), 0)


class Tetris:
    """ Contains all the high level logic for running the tetris game. Holds 3 other classes, Shape, Frozen blocks,
        and Blocks.
    """

    def __init__(self):
        """ default constructor for the tetris class
        """
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
        self.rows_to_level_up = 6
        self.next_shape = Shape(random.randint(0, 6))
        self.exclusion_list = [None, None] # this ensures that there are always 2 or 3 elements in the exclusion list
        self.drought_counter = 0

    def draw_outline(self):
        """ draws the outline for the play window using draw.lines function
        :return: None
        """
        pygame.draw.lines(screen, (0, 0, 0), True, (
            (PW_X_OFFSET, PW_Y_OFFSET), (PW_X_OFFSET, PW_Y_OFFSET + PW_HEIGHT),
            (PW_X_OFFSET + PW_WIDTH, PW_Y_OFFSET + PW_HEIGHT),
            (PW_X_OFFSET + PW_WIDTH, PW_Y_OFFSET)), 1)

    def check_game_lost(self, shape_coords):
        """ checks to see if the game has been lost by seeing if a shape has been frozen at the top of the screen,
        sets self.game_lost true if it has been
        :param shape_coords: a 4x1 list of 2x1 tuples for the coordinate of each part of a shape
        :return: None
        """
        for coord in shape_coords:
            if coord[1] < 2:
                self.game_lost = True

    def will_collide(self, shape, frozen_blocks, move):
        """ Checks to see if a shape given a move will collide with the frozen blocks or the map border
        :param shape: a Shape object
        :param frozen_blocks: a FrozenBlock object
        :param move: an integer between 0 - 6
        :return: True if a collision will happen, false if not
        """
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
        """ Chooses which combination of moves to use to allow for a shape to rotate. If a combination of rotating and
        shifting is allowed, it will perform that combination. Otherwise, it will do nothing
        :param shape: a Shape object
        :param frozen_blocks: a FrozenBlocks object
        :return: None
        """
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
        """ Attempts to lower a shape. If it will collide, it will convert it to block objects and add them to the
        frozen blocks object
        :param shape: a Shape object
        :param frozen_blocks: a FrozenBlocks object
        :return: None
        """
        if not self.will_collide(shape, frozen_blocks, 2):
            shape.descend(1)
        else:
            self.check_game_lost(shape.get_global_coords())
            frozen_blocks.create_blocks(shape.get_global_coords(), shape.color)
            new_rows_cleared = frozen_blocks.clear_rows()
            self.update_score(new_rows_cleared)
            self.need_new_shape = True

    def update_score(self, new_rows_cleared):
        """ updates the score. If a tetris is scored, where 4 rows are cleared at a time, bonus points will be added
        :param new_rows_cleared: an integer
        :return: None
        """
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
        """ Prints all the text on the side using the pygame functions
        :return: None
        """
        score = font.render("score: " + str(self.score_value), True, (0, 0, 0))
        screen.blit(score, (TEXT_X_OFFSET, TEXT_Y_OFFSET))
        level = font.render("level: " + str(self.level), True, (0, 0, 0))
        screen.blit(level, (TEXT_X_OFFSET, TEXT_Y_OFFSET + FONT_SIZE))
        rows = font.render("rows cleared: " + str(self.rows_cleared_total), True, (0, 0, 0))
        screen.blit(rows, (TEXT_X_OFFSET, TEXT_Y_OFFSET + 2 * FONT_SIZE))
        label = font.render("next piece: ", True, (0, 0, 0))
        screen.blit(label, (TEXT_X_OFFSET, TEXT_Y_OFFSET + 3 * FONT_SIZE))

    def level_up(self):
        """ Speeds up how fast the blocks fall, increases the level, and calls change_colors function
        :return: None
        """
        self.fall_time *= self.time_multiplier
        self.level += 1
        change_colors()

    def choose_new_shape(self):
        """ Chooses a new shape that is not in the exclusion list, then adds it to the exclusion list, and removes the oldest integer from the exclusion list
        Also forces the generation of an I shape if there has not been an I piece in the last 7 new shapes
        :return: an integer between 0 - 6 that represents what shape it is
        """
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
        """ All the logic for running the tetris game
            :return: None
        """
        frozen_blocks = FrozenBlocks()
        while not self.game_lost:
            if self.need_new_shape:
                shape = self.next_shape
                shape.move_to_pw()
                self.next_shape = Shape(self.choose_new_shape())
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
            self.next_shape.paint()
            shape.paint_ghost(drop - 1)
            shape.paint()
            self.draw_outline()

            # statements called at an interval that decreases as levels are passed
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
        colors[i] = (random.randint(70, 255), random.randint(70, 255), random.randint(70, 255))


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
