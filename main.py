import pygame
import math
import socket
import pickle
import os.path

# Initializing Pygame
pygame.init()

# Screen
WIDTH = 500
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
X_IMAGE = pygame.transform.scale(pygame.image.load("images/x.png"), (150, 150))
O_IMAGE = pygame.transform.scale(pygame.image.load("images/o.png"), (150, 150))

# Fonts
END_FONT = pygame.font.SysFont('courier', 40)

KEEP_ALIVE = True
def draw_grid():
    gap = WIDTH // ROWS
    # Starting points
    x = 0
    y = 0

    for i in range(ROWS):
        x = i * gap

        pygame.draw.line(win, GRAY, (x, 0), (x, WIDTH), 3) # cols
        pygame.draw.line(win, GRAY, (0, x), (WIDTH, x), 3) # rows


def load_game():
    global x_turn, o_turn, images
    x_turn = True
    o_turn = False

    # Initializing the array
    if os.path.isfile('tictactoe.cfg'):
        with open('tictactoe.cfg', 'rb') as cfg_file:
            game_array = pickle.load(cfg_file)
            num_chars_placed = 0
            for i in range(len(game_array)):
                for j in range(len(game_array[i])):
                    x, y, char, can_play = game_array[i][j]
                    if not can_play:
                        if char == 'x':
                            images.append((x, y, X_IMAGE))
                            num_chars_placed+=1
                        elif char == 'o':
                            images.append((x, y, O_IMAGE))
                            num_chars_placed+=1

            if (num_chars_placed % 2) != 0:
                x_turn = False
                o_turn = True
    else:
        game_array = reset_grid()

    return game_array

def reset_grid():
    global images
    images = []
    game_array = [[None, None, None], [None, None, None], [None, None, None]]
    for i in range(len(game_array)):
        for j in range(len(game_array[i])):
            x = dis_to_cen * (2 * j + 1)
            y = dis_to_cen * (2 * i + 1)
            game_array[i][j] = (x, y, "", True)
    save_game(game_array)
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


# Checking if someone has won
def has_won(game_array):
    # Checking rows
    # @gearoidc, added row positional check to fix edge cases where wins would not be picked up
    for row in range(len(game_array)):
        if (game_array[row][0][2] == game_array[row][1][2] == game_array[row][2][2]) and game_array[row][0][2] != "":
            display_message(game_array[row][0][2].upper() + " has won!")
            return True

    # Checking columns
    # @gearoidc, added col positional check to fix edge cases where wins would not be picked up
    for col in range(len(game_array)):
        if (game_array[0][col][2] == game_array[1][col][2] == game_array[2][col][2]) and game_array[0][col][2] != "":
            display_message(game_array[0][col][2].upper() + " has won!")
            return True

    # Checking main diagonal
    if (game_array[0][0][2] == game_array[1][1][2] == game_array[2][2][2]) and game_array[0][0][2] != "":
        display_message(game_array[0][0][2].upper() + " has won!")
        return True

    # Checking reverse diagonal
    if (game_array[0][2][2] == game_array[1][1][2] == game_array[2][0][2]) and game_array[0][2][2] != "":
        display_message(game_array[0][2][2].upper() + " has won!")
        return True

    return False


def has_drawn(game_array):
    for i in range(len(game_array)):
        for j in range(len(game_array[i])):
            if game_array[i][j][2] == "":
                return False

    display_message("It's a draw!")
    return True


def display_message(content):
    pygame.time.delay(500)
    win.fill(WHITE)
    end_text = END_FONT.render(content, 1, BLACK)
    win.blit(end_text, ((WIDTH - end_text.get_width()) // 2, (WIDTH - end_text.get_height()) // 2))
    pygame.display.update()
    pygame.time.delay(3000)


def render():
    win.fill(WHITE)
    draw_grid()

    # Drawing X's and O's
    for image in images:
        x, y, IMAGE = image
        win.blit(IMAGE, (x - IMAGE.get_width() // 2, y - IMAGE.get_height() // 2))

    pygame.display.update()

def save_game(game_array):
    with open('tictactoe.cfg', 'wb') as cfg_file:
        pickle.dump(game_array, cfg_file)

def main():
    global x_turn, o_turn, images, draw, dis_to_cen, KEEP_ALIVE

    images = []
    draw = False

    # @gearoidc : created dis_to_cen global
    dis_to_cen = WIDTH // ROWS // 2

    game_array = load_game()

    while KEEP_ALIVE:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                save_game(game_array)
                KEEP_ALIVE = False
                break
            if event.type == pygame.MOUSEBUTTONDOWN:
                click(game_array)

        render()

        if has_won(game_array) or has_drawn(game_array):
            game_array = reset_grid()

while True:
    if __name__ == '__main__':
        if KEEP_ALIVE:
            main()
        else:
            pygame.quit()
            break