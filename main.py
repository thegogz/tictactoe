import pygame
import math

pygame.init()

# Screen
WIDTH = 300
ROWS = 3
win = pygame.display.set_mode((WIDTH, WIDTH))
pygame.display.set_caption("TicTacToe")

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GRAY = (200, 200, 200)
RED = (255, 0, 0)
BLUE = (0, 0, 255)

# Images
X_IMAGE = pygame.transform.scale(pygame.image.load("images/x.png"), (80, 80))
O_IMAGE = pygame.transform.scale(pygame.image.load("images/o.png"), (80, 80))

# Fonts
END_FONT = pygame.font.SysFont('courier', 40)

# Draw Grid
def draw_grid():
    gap = WIDTH // ROWS 

    # Starting Points
    x = 0
    y = 0

    for i in range(ROWS):
        x  =  i * gap

        pygame.draw.line(win, GRAY, (x, 0), (x, WIDTH), 3)
        pygame.draw.line(win, GRAY, (0, x), (WIDTH, x), 3)

def initialize_grid():
    dis_to_cen = WIDTH  // ROWS  // 2

    # Initializing  the  game array
    game_array = [[None, None, None], [None, None, None], [None, None, None]]

    for i in range(len(game_array)):
        for j in range(len(game_array[i])):
            x = dis_to_cen * (2 * j + 1)
            y = dis_to_cen * (2 * i + 1)

            # Adding center coordinates
            game_array[i][j] = (x, y, "", True)
    
    return game_array

def main():
    win.fill(WHITE)
    draw_grid()
    pygame.display.update()

while True:
    if __name__ == '__main__':
        main()
