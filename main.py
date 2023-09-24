import pygame
from board import Board

pygame.init()
BOARD_SIZE = 800
SCORE_AREA_SIZE = 600
TITLE_FONT_SIZE = 48
FONT_SIZE = 36

screen = pygame.display.set_mode((BOARD_SIZE + SCORE_AREA_SIZE, BOARD_SIZE))
pygame.display.set_caption("Reversi")
title_font = pygame.font.Font("./ubuntufont.ttf", TITLE_FONT_SIZE)
font = pygame.font.Font("./ubuntufont.ttf", FONT_SIZE)
clock = pygame.time.Clock()
board = Board()

def mouse_to_board_coords(mouse_x, mouse_y):
    square_size = (BOARD_SIZE // Board.SIZE)
    return (mouse_y // square_size, mouse_x // square_size)

def render_score_area(screen, board):
    white_count = board.get_count(Board.WHITE)
    black_count = board.get_count(Board.BLACK)

    title_surface = title_font.render("REVERSI", True, "black")
    title_rect = title_surface.get_rect()
    title_rect.center = (BOARD_SIZE + SCORE_AREA_SIZE // 2, BOARD_SIZE // 4)

    black_count_surface = font.render("BLACK: " + str(black_count), True, "black")
    black_count_rect = black_count_surface.get_rect()
    black_count_rect.center = (BOARD_SIZE + SCORE_AREA_SIZE // 2, BOARD_SIZE // 2)

    white_count_surface = font.render("WHITE: " + str(white_count), True, "white")
    white_count_rect = white_count_surface.get_rect()
    white_count_rect.center = (BOARD_SIZE + SCORE_AREA_SIZE // 2, BOARD_SIZE // 2 + BOARD_SIZE // 8)

    if board.game_ended():
        win_color = "black" if black_count >= white_count else "white"
        win_msg = "TIE!" if black_count == white_count else win_color.upper() + " WINS!"
        win_surface = font.render(win_msg, True, win_color)
        win_rect = win_surface.get_rect()
        win_rect.center = (BOARD_SIZE + SCORE_AREA_SIZE // 2, BOARD_SIZE // 2 + BOARD_SIZE // 4)
        screen.blit(win_surface, win_rect)
    else:
        turn_color = "black" if board.turn == Board.BLACK else "white"
        turn_surface = font.render("TURN: " + turn_color.upper(), True, turn_color)
        turn_rect = turn_surface.get_rect()
        turn_rect.center = (BOARD_SIZE + SCORE_AREA_SIZE // 2, BOARD_SIZE // 2 + BOARD_SIZE // 4)
        screen.blit(turn_surface, turn_rect)

    screen.blit(title_surface, title_rect)
    screen.blit(black_count_surface, black_count_rect)
    screen.blit(white_count_surface, white_count_rect)

running = True
while running:
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    
    mouse_x, mouse_y = pygame.mouse.get_pos()
    left, middle, right = pygame.mouse.get_pressed()

    if left:
        board_row, board_col = mouse_to_board_coords(mouse_x, mouse_y)
        board.handle_input(board_row, board_col)
    
    board.render_board(pygame, screen, BOARD_SIZE)
    render_score_area(screen, board)

    pygame.display.flip()
    clock.tick(60)

pygame.quit()