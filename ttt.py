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

def click(game_array):
    global x_turn, o_turn, images

    # Mouse position
    m_x, m_y = pygame.mouse.get_pos()

    for i in range(len(game_array)):
        for j in range(len(game_array[i])):
            x, y, char, can_play = game_array[i][j]

            # Distance between mouse and the centre of the square
            dis = math.sqrt((x - m_x) ** 2 + (y - m_y) ** 2)

            # If it's inside the square
            if dis < dis_to_cen and can_play:
                if x_turn:  # If it's X's turn
                    images.append((x, y, X_IMAGE))
                    x_turn = False
                    o_turn = True
                    game_array[i][j] = (x, y, 'x', False)

                elif o_turn:  # If it's O's turn
                    images.append((x, y, O_IMAGE))
                    x_turn = True
                    o_turn = False
                    game_array[i][j] = (x, y, 'o', False)


def main():
    global x_turn, o_turn, images, draw, dis_to_cen
    game_array = initialize_grid()
    run = True
    while run:
      for event in pygame.event.get():
        if event.type == pygame.QUIT:
          pygame.quit()
        if event.type == pygame.MOUSEBUTTONDOWN:
          click(game_array)

      win.fill(WHITE)
      draw_grid()
      pygame.display.update()

while True:
    if __name__ == '__main__':
        main()