import random
import pygame
pygame.font.init()

row = 20
col = 10
block_size = 30
w_width = 800
w_height = 800
pw_width = 300
pw_height = 600

# shapes
s = [[(1, 0), (2, 0), (0, 1), (1, 1)], [(0, 0), (0, 1), (1, 1), (1, 2)]]
z = [[(0, 0), (1, 0), (1, 1), (2, 1)], [(1, 0), (0, 1), (1, 1), (0, 2)]]
t = [[(1, 1), (1, 0), (0, 1), (2, 1)], [(1, 1), (1, 0), (2, 1), (1, 2)], [(1, 1), (0, 1), (2, 1), (1, 2)], [(1, 1), (1, 0), (0, 1), (1, 2)]]
j = [[(1, 1), (0, 0), (0, 1), (2, 1)], [(1, 1), (1, 0), (2, 0), (1, 2)], [(1, 1), (0, 1), (2, 1), (2, 2)], [(1, 1), (1, 0), (0, 2), (1, 2)]]
l = [[(1, 1), (2, 0), (0, 1), (2, 1)], [(1, 1), (1, 0), (2, 2), (1, 2)], [(1, 1), (0, 1), (2, 1), (0, 2)], [(1, 1), (1, 0), (0, 0), (1, 2)]]
i = [[(1, 0), (1, 1), (1, 2), (1, 3)], [(0, 1), (1, 1), (2, 1), (3, 1)]]
o = [[(0, 0), (1, 0), (0, 1), (1, 1)]]

# Set up the drawing window
screen = pygame.display.set_mode([w_width, w_height])




# Run until the user asks to quit
running = True
while running:

    # Did the user click the window close button?
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Fill the background with white
    screen.fill((255, 255, 255))

    # Draw a solid blue circle in the center

    for coord in l[0]:
        pygame.draw.rect(screen, (0, 0, 255), (coord[0] * block_size, coord[1] * block_size, block_size, block_size), 0)

    # Flip the display
    pygame.display.flip()

# Done! Time to quit.
pygame.quit()