import pygame
import math
import pickle
import os.path

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
KEEP_ALIVE = True
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

def load_game():
    global x_turn, o_turn, images

    x_turn = True
    o_turn = False
    pygame.display.set_caption("TicTacToe - X Turn")

    if os.path.isfile('tictactoe.cfg'):
        with open('tictactoe.cfg', 'rb') as cfg_file:
            game_array = pickle.load(cfg_file)
            num_chars_placed = 0
            for i in range(len(game_array)):
                for j in range(len(game_array[i])):
                    x, y, char, can_play = game_array[i][j]
                    if not can_play:
                        num_chars_placed+=1
                        if char == 'x':
                            images.append((x, y, X_IMAGE))
                        elif char == 'o':
                            images.append((x, y, O_IMAGE))

            if (num_chars_placed % 2) != 0:
                x_turn = False
                o_turn = True
                pygame.display.set_caption("TicTacToe - O Turn")

    else:
        #dis_to_cen = WIDTH  // ROWS  // 2
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

    # Mouse Position
    m_x, m_y = pygame.mouse.get_pos()
    print(str(m_x) + ' ' + str(m_y))
    pygame.display.set_caption("TicTacToe x")

    for i in range(len(game_array)):
        for j in range(len(game_array[i])):
            x, y, char, can_play = game_array[i][j]

            # Distance between mouse and the center of the square
            dis = math.sqrt((x - m_x) ** 2 + (y - m_y) ** 2)

            # if it's inside the square
            if dis < WIDTH // ROWS // 2 and can_play:
                print(dis)
                print(game_array)
                if x_turn:
                    images.append((x, y, X_IMAGE))
                    x_turn = False
                    o_turn = True
                    game_array[i][j] = (x, y, 'x', False)
                    pygame.display.set_caption("TicTacToe - O Turn")


                elif o_turn:
                    images.append((x, y, O_IMAGE))
                    o_turn = False
                    x_turn = True
                    game_array[i][j] = (x, y, 'o', False)
                    pygame.display.set_caption("TicTacToe - X Turn")

def has_won(game_array):

    for row in range(len(game_array)):
        if (game_array[row][0][2] == game_array[row][1][2] == game_array[row][2][2]) and game_array[row][0][2] != "":
            display_message(game_array[row][0][2].upper() + " has won!")
            return True

    for col in range(len(game_array)):
        if (game_array[0][col][2] == game_array[1][col][2] == game_array[2][col][2]) and game_array[0][col][2] != "":
            display_message(game_array[0][col][2].upper() + " has won!")
            return True

    if (game_array[0][0][2] == game_array[1][1][2] == game_array[2][2][2]) and game_array[0][0][2] != "":
        display_message(game_array[0][0][2].upper() + " has won!")
        return True

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

    # draw X's and O's
    for image in images:
        x, y, IMAGE = image
        win.blit(IMAGE, (x - IMAGE.get_width() // 2, y - IMAGE.get_height() // 2))

    pygame.display.update()

def save_game(game_array):
    with open('tictactoe.cfg', 'wb') as cfg_file:
        pickle.dump(game_array, cfg_file)

def main():
    global x_turn, y_turn, images, draw, dis_to_cen, KEEP_ALIVE

    images = []
    draw = False

    x_turn = True
    o_turn = False

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
