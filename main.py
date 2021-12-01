import pygame as pg, sys, numpy as np
from math import inf as infinity
from pygame.font import Font
import random

pg.init()
pg.font.init()

WIDTH = 600
HEIGHT = 600
LINE_WIDTH = 15
WIN_LINE_WIDTH = 15
BOARD_ROWS = 3
BOARD_COLS = 3
SQUARE_SIZE = 200
O_RADIUS = 60
O_WIDTH = 15
X_WIDTH = 25
SPACE = 55

TITLEFONT = pg.font.SysFont('Comic Sans MS', 60)
INFOFONT = pg.font.SysFont('Comic Sans MS', 20)
SCOREFONT = pg.font.SysFont('Comic Sans MS', 30)
BACKGROUND = (139, 0, 0)
LINE_COLOR = (0, 0, 0)
O_COLOR = (0, 0, 0)
X_COLOR = (255, 255, 255)

playerscore = 0
computerscore = 0
ties = 0

screen = pg.display.set_mode((1200, 600))
pg.display.set_caption("Tic Tac Toe")
screen.fill(BACKGROUND)

canvas = pg.Surface((600, 600))

GameDisplay = pg.Rect(600, 0, 600, 1200)
Controls = pg.Rect(0, 0, 600, 600)

board = np.zeros((BOARD_ROWS, BOARD_COLS))

def draw_lines():
    pg.draw.line(screen, LINE_COLOR, (0, SQUARE_SIZE), (WIDTH,
                     SQUARE_SIZE), LINE_WIDTH)
    pg.draw.line(screen, LINE_COLOR, (0, 2 * SQUARE_SIZE), (WIDTH,
                     2 * SQUARE_SIZE), LINE_WIDTH)
    pg.draw.line(screen, LINE_COLOR, (SQUARE_SIZE, 0),
                     (SQUARE_SIZE, HEIGHT), LINE_WIDTH)
    pg.draw.line(screen, LINE_COLOR, (2 * SQUARE_SIZE, 0), (2
                     * SQUARE_SIZE, HEIGHT), LINE_WIDTH)

def draw_XO():
    for row in range(BOARD_ROWS):
        for column in range(BOARD_COLS):
            if board[row][column] == -1:
                pg.draw.circle(screen, O_COLOR, (int(column
                                   * SQUARE_SIZE + SQUARE_SIZE // 2),
                                   int(row * SQUARE_SIZE + SQUARE_SIZE
                                   // 2)), O_RADIUS, O_WIDTH)
            elif board[row][column] == 1:
                pg.draw.line(screen, X_COLOR, (column
                                 * SQUARE_SIZE + SPACE, row
                                 * SQUARE_SIZE + SQUARE_SIZE - SPACE),
                                 (column * SQUARE_SIZE + SQUARE_SIZE
                                 - SPACE, row * SQUARE_SIZE + SPACE),
                                 X_WIDTH)
                pg.draw.line(screen, X_COLOR, (column
                                 * SQUARE_SIZE + SPACE, row
                                 * SQUARE_SIZE + SPACE), (column
                                 * SQUARE_SIZE + SQUARE_SIZE - SPACE,
                                 row * SQUARE_SIZE + SQUARE_SIZE
                                 - SPACE), X_WIDTH)

def mark_square(row, column, player):
    board[row][column] = player

def available_square(row, column):
    return board[row][column] == 0

def is_board_full():
    for row in range(BOARD_ROWS):
        for column in range(BOARD_COLS):
            if board[row][column] == 0:
                return False
    return True

def check_win(player):
    global playerscore
    global computerscore
    for column in range(BOARD_COLS):
        if board[0][column] == player and board[1][column] == player \
            and board[2][column] == player:
            vertical_winning_line(column, player)
            if player == -1:
                playerscore += 1
            elif player == 1:
                computerscore += 1
            return True

    for row in range(BOARD_ROWS):
        if board[row][0] == player and board[row][1] == player \
            and board[row][2] == player:
            horizontal_winning_line(row, player)
            if player == -1:
                playerscore += 1
            elif player == 1:
                computerscore += 1
            return True

    if board[2][0] == player and board[1][1] == player and board[0][2] == player:
        draw_asc_diagonal(player)
        if player == -1:
                playerscore += 1
        elif player == 1:
            computerscore += 1
        return True

    if board[0][0] == player and board[1][1] == player and board[2][2] == player:
        draw_desc_diagonal(player)
        if player == -1:
                playerscore += 1
        elif player == 1:
            computerscore += 1
        return True
    return False


def vertical_winning_line(column, player):
    posX = column * SQUARE_SIZE + SQUARE_SIZE // 2
    if player == -1:
        color = O_COLOR
    elif player == 1:
        color = X_COLOR
    pg.draw.line(screen, color, (posX, 15), (posX, HEIGHT - 15),
                     LINE_WIDTH)


def horizontal_winning_line(row, player):
    posY = row * SQUARE_SIZE + SQUARE_SIZE // 2
    if player == -1:
        color = O_COLOR
    elif player == 1:
        color = X_COLOR
    pg.draw.line(screen, color, (15, posY), (WIDTH - 15, posY),
                     WIN_LINE_WIDTH)


def draw_asc_diagonal(player):
    if player == -1:
        color = O_COLOR
    elif player == 1:
        color = X_COLOR
    pg.draw.line(screen, color, (15, HEIGHT - 15), (WIDTH - 15,
                     15), WIN_LINE_WIDTH)


def draw_desc_diagonal(player):
    if player == -1:
        color = O_COLOR
    elif player == 1:
        color = X_COLOR
    pg.draw.line(screen, color, (15, 15), (WIDTH - 15, HEIGHT
                     - 15), WIN_LINE_WIDTH)

# Checks game state for ties
def check_tie():
    global ties
    if len(empty_cells(board)) == 0:
        ties += 1
        return True
    return False

# Checks if there are any avaiable moves and displays them
def empty_cells(board):
    cells = []
    for x, row in enumerate(board):
        for y, cell in enumerate(row):
            if cell == 0:
                cells.append([x, y])

    return cells

# Draws game info to the screen
def draw_information():
    TITLE = TITLEFONT.render("TIC-TAC-TOE", False, (255, 255, 255))
    RESTARTINFO = INFOFONT.render("To restart the game press 'r'", False, (255, 255, 255))
    QUITINFO = INFOFONT.render("Quit by pressing 'q'", False, (255, 255, 255))
    DIFFINFO = INFOFONT.render("1:PVP     2:PVE (Hard)    3:PVE (Easy)", False, (255, 255, 255))
    PLAYERSCORE = SCOREFONT.render((f"Player Score: {str(playerscore)}"), False, (255, 255, 255))
    COMPUTERSCORE = SCOREFONT.render((f"Computer Score: {str(computerscore)}"), False, (255, 255, 255))
    TIESCORE = SCOREFONT.render((f"Tie(s): {str(ties)}"), False, (255, 255, 255))
    screen.blit(canvas, (0, 0), GameDisplay)
    screen.blit(canvas, (600, 0), Controls)
    screen.blit(TITLE, (700,0), Controls)
    screen.blit(RESTARTINFO, (610, 570), Controls)
    screen.blit(QUITINFO, (1000,570), Controls)
    screen.blit(DIFFINFO, (720, 540), Controls)
    screen.blit(PLAYERSCORE, (630, 380), Controls)
    screen.blit(COMPUTERSCORE, (910, 380), Controls)
    screen.blit(TIESCORE, (820, 450), Controls)

#### AI Stuff
# Decides if this is a good play
def evaluate(board):
    if wins(board, 1):
        score = +1
    elif wins(board, -1):
        score = -1
    else:
        score = 0

    return score

# Did Someone Win
def wins(board, player):
    for column in range(BOARD_COLS):
        if board[0][column] == player and board[1][column] == player \
            and board[2][column] == player:
            return True

    for row in range(BOARD_ROWS):
        if board[row][0] == player and board[row][1] == player \
            and board[row][2] == player:
            return True

    if board[2][0] == player and board[1][1] == player and board[0][2] == player:
        return True

    if board[0][0] == player and board[1][1] == player and board[2][2] == player:
        return True
    return False

# Minimax
def minimax(board, depth, player=1):
    if player == 1:
        best = [-1, -1, -infinity]
    else:
        best = [-1, -1, +infinity]

    if depth == 0 or (wins(board, -1) or wins(board, 1)):
        score = evaluate(board)
        return [-1, -1, score]

    for cell in empty_cells(board):
        x, y = cell[0], cell[1]
        board[x][y] = player
        score = minimax(board, depth - 1, -player)
        board[x][y] = 0
        score[0], score[1] = x, y

        if player == 1:
            if score[2] > best[2]:
                best = score
        else:
            if score[2] < best[2]:
                best = score
    return best

#Code To Restart Game
def restart():
    screen.fill(BACKGROUND)
    draw_lines()
    for row in range(BOARD_ROWS):
        for column in range(BOARD_COLS):
            board[row][column] = 0
    screen.blit(canvas, (0, 0), GameDisplay)
    screen.blit(canvas, (600, 0), Controls)
    draw_information()


draw_lines()
draw_information()
player = -1
mode = 2
game_over = False

#Keeps the game running
while True:
    for event in pg.event.get():
        #Gets Clicks
        # PVP
        if mode == 1:
            if event.type == pg.MOUSEBUTTONDOWN and not game_over:
                mouseX = event.pos[0]
                mouseY = event.pos[1]
                clicked_row = int(mouseY // SQUARE_SIZE)
                clicked_column = int(mouseX // SQUARE_SIZE)
                try:
                    #Player Turn
                    if available_square(clicked_row, clicked_column):
                        mark_square(clicked_row, clicked_column, player)
                        draw_XO()
                        if check_win(player) or check_tie():
                            draw_information()
                            game_over = True
                            break
                        player = -player
                except:
                    pass
        # AI Bot
        elif mode == 2:
            if event.type == pg.MOUSEBUTTONDOWN and not game_over:
                mouseX = event.pos[0]
                mouseY = event.pos[1]
                clicked_row = int(mouseY // SQUARE_SIZE)
                clicked_column = int(mouseX // SQUARE_SIZE)
                try:
                    #Player Turn
                    if available_square(clicked_row, clicked_column):
                        mark_square(clicked_row, clicked_column, player)
                        draw_XO()
                        if check_win(player) or check_tie():
                            draw_information()
                            game_over = True
                            break
                        player = 1

                        #AI Turn
                        depth = len(empty_cells(board))
                        if depth >= 6:
                            move = minimax(board, 6)
                        else:
                            move = minimax(board, depth)
                        row, column = move[0], move[1]
                        mark_square(row, column, player)
                        draw_XO()
                        if check_win(player) or check_tie():
                            draw_information()
                            game_over = True
                            break
                        player = -1
                except:
                    pass
        #Random Bot
        elif mode == 3:
            if event.type == pg.MOUSEBUTTONDOWN and not game_over:
                mouseX = event.pos[0]
                mouseY = event.pos[1]
                clicked_row = int(mouseY // SQUARE_SIZE)
                clicked_column = int(mouseX // SQUARE_SIZE)
                try:
                    #Player Turn
                    if available_square(clicked_row, clicked_column):
                        mark_square(clicked_row, clicked_column, player)
                        draw_XO()
                        if check_win(player) or check_tie():
                            draw_information()
                            game_over = True
                            break
                        player = 1
                        
                        #AI Turn
                        cells = empty_cells(board)
                        xy = cells[random.randint(0, (len(cells)-1))]
                        mark_square(xy[0], xy[1], player)
                        draw_XO()
                        if check_win(player) or check_tie():
                            draw_information()
                            game_over = True
                            break
                        player = -1
                except:
                    pass
        #Restart Game
        if event.type == pg.KEYDOWN:
            if event.key == pg.K_r:
                restart()
                player = -1
                game_over = False
                
        # Change modes
        if event.type == pg.KEYDOWN:
            #Mode 1
            if event.key == pg.K_1:
                player = -1
                game_over = False
                playerscore = 0
                computerscore = 0
                ties = 0
                restart()
                mode = 1
            #Mode 2
            if event.key == pg.K_2:
                player = -1
                game_over = False
                playerscore = 0
                computerscore = 0
                ties = 0
                restart()
                mode = 2
            #Mode 3
            if event.key == pg.K_3:
                player = -1
                game_over = False
                playerscore = 0
                computerscore = 0
                ties = 0
                restart()
                mode = 3

        #Exits Game
        if event.type == pg.QUIT or event.type == pg.KEYDOWN \
            and event.key == pg.K_q:
            sys.exit()
    
    #Refresheses desplay
    pg.display.update()    
