import pygame
import numpy as np
from AI_Solver import *

pygame.init()

# Screen setup
SCREEN_WIDTH, SCREEN_HEIGHT = 500, 600
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("8-Puzzle Game with AI agent")

# Colors
BACKGROUND_COLOR = pygame.Color('skyblue')
TILE_COLOR = pygame.Color('navy')
TEXT_COLOR = pygame.Color('white')
BUTTON_COLOR = pygame.Color('darkorange')
BUTTON_TEXT_COLOR = pygame.Color('white')
#padding between tiles
TILE_PADDING = 5  

# Fonts
FONT = pygame.font.Font(None, 40)

# Board setup
BOARD_SIZE = 3
TILE_SIZE = 100
BOARD_POS = (95, 150)

# Button setup
BUTTONS = {
    "Play": pygame.Rect(50, 30, 120, 50),
    "Solve": pygame.Rect(190, 30, 120, 50),
    "Quit": pygame.Rect(330, 30, 120, 50)
}

#Function to draw a puzzle board, it takes board starting state as parameter
#and creates puzzle board in the game window
def draw_board(board):
    for y in range(BOARD_SIZE):
        for x in range(BOARD_SIZE):
            tile = board[y][x]
            if tile != 0:
                # Calculate the position and size with padding
                tile_x = BOARD_POS[0] + x * (TILE_SIZE + TILE_PADDING) + TILE_PADDING // 2
                tile_y = BOARD_POS[1] + y * (TILE_SIZE + TILE_PADDING) + TILE_PADDING // 2
                tile_width = TILE_SIZE - TILE_PADDING
                tile_height = TILE_SIZE - TILE_PADDING
                #draw the tile
                tile_rect = pygame.Rect(tile_x, tile_y, tile_width, tile_height)
                pygame.draw.rect(screen, TILE_COLOR, tile_rect)
                #tile number
                tile_text = FONT.render(str(tile), True, TEXT_COLOR)
                text_rect = tile_text.get_rect(center=tile_rect.center)
                screen.blit(tile_text, text_rect)

#Function to draw buttons in game window
def draw_buttons():
    for text, rect in BUTTONS.items():
        pygame.draw.rect(screen, BUTTON_COLOR, rect)
        button_text = FONT.render(text, True, BUTTON_TEXT_COLOR)
        text_rect = button_text.get_rect(center=rect.center)
        screen.blit(button_text, text_rect)

#This function checks if button was clicked and returns name of that button
def check_button_clicks(pos):
    for text, rect in BUTTONS.items():
        if rect.collidepoint(pos):
            return text
    return None

#Function to count inversions in a given puzzle configuration.
#An inversion is a pair of tiles that are in the reverse order from where they should be. 
#in 8 puzzle if number of inversions is odd then the solution cannot be reached
def count_inversions(arr):
    inversions = 0
    for i in range(len(arr)):
        for j in range(i + 1, len(arr)):
            if arr[i] > arr[j] != 0:
                inversions += 1
    return inversions

#This function checks if a puzzle configuration is solvable.
#It flattens the board (one-dimensional array) and calls function to counts inversions
def is_solvable(board):
    flat_board = board.flatten()
    inversions = count_inversions(flat_board)
    return inversions % 2 == 0

#This function randomly generates the start configuration of the board
#It checks if generated configuration is solvable if not generate new one
def create_solvable_board():
    while True:
        board = np.random.permutation(np.arange(9)).reshape((3, 3))
        if is_solvable(board):
            return board

#This function checks if a tile can be moved and makes a move if possible.
# It also checks for a winning condition after each move.
def move_tile(board, row, col):
     
    #get position of empty tile
    empty_row, empty_col = np.where(board == 0)
    empty_row, empty_col = int(empty_row[0]), int(empty_col[0])

    #check if move is allowed
    if (abs(row - empty_row) == 1 and col == empty_col) or \
       (abs(col - empty_col) == 1 and row == empty_row):
        #swap the tiles
        board[empty_row, empty_col], board[row, col] = board[row, col], board[empty_row, empty_col]
        return True
    return False

#Function to check if the current board configuration matches the winning condition.
def check_win_condition(board):
    return np.array_equal(board, np.array([[1, 2, 3], [4, 5, 6], [7, 8, 0]]))

#Function to handle mouse clicks it get.
#if tile is clicked and move is allowed it then calls the function to swap tiles and checks for wining conditions
def handle_mouse_click(board, pos, solved):
    # If the puzzle is solved, disable moving tiles.
    if solved:
        return False
    #get row and column of tile clicked
    tile_x, tile_y = (pos[0] - BOARD_POS[0]) // TILE_SIZE, (pos[1] - BOARD_POS[1]) // TILE_SIZE
    if 0 <= tile_x < BOARD_SIZE and 0 <= tile_y < BOARD_SIZE:
        if move_tile(board, tile_y, tile_x):
            if check_win_condition(board):
                return True
    return False

#Function to display winning message when puzzles are solved
def display_winning_message(winning_message):
    
    message_surf = FONT.render(winning_message, True, TEXT_COLOR)
    message_y_position = BOARD_POS[1] + BOARD_SIZE * TILE_SIZE + 30
    message_rect = message_surf.get_rect(center=(SCREEN_WIDTH // 2, message_y_position))
    screen.blit(message_surf, message_rect)
