import pygame
import random
#from time import sleep
import tkinter as tk
from tkinter import messagebox

pygame.init()

# Initializaing window and font
WIN_WIDTH = 600
win = pygame.display.set_mode((WIN_WIDTH, WIN_WIDTH))
STAT_FONT = pygame.font.SysFont("comicsans", 50)
pygame.mouse.set_cursor(*pygame.cursors.broken_x)

# Tuples containing RGB values
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
BLUE = (0, 0, 255)


# Functionality for each spot on the tictactoe board
class Section:
    def __init__(self, x, y, name):
        self.x = x
        self.y = y
        self.name = name
        self.open = True
        self.width = 180
        self.image = pygame.Rect(self.x, self.y, self.width, self.width)
        self.label = name[-1:]

class Player:
    def __init__(self, draw_object, turn):
        self.draw_object = draw_object
        self.turn = turn

class Board:
    def __init__(self):
        self.board = []
        self.board_shapes = []

def place(win, section, p1, p2):
    if p1.turn and section.open:
        pygame.draw.circle(win, RED, (section.x + 90, section.y + 90), 70)
        section.name = "circle"
        p1.turn = False
        p2.turn = True
        section.open = False
    elif p2.turn and section.open:
        pygame.draw.rect(win, BLUE, (section.x + 20, section.y + 20, 140, 140))
        section.name = "rectangle"
        p2.turn = False
        p1.turn = True
        section.open = False

def print_board(board):
    names = []
    for section in board:
        names.append(section.name)
    print(names)

def open_spots(board):
    count = 0
    for section in board:
        if section.open:
            count += 1
    return count

# Dialog box
def message_box(subject, content):
    root = tk.Tk()
    root.attributes("-topmost", True)
    root.withdraw()
    messagebox.showinfo(subject, content)
    try:
        root.destroy()
    except:
        pass


def get_winner(board, p1, p2):
    winner = None
    if board[0].name == board[1].name and board[0].name == board[2].name:
        if board[0].name == "circle":
            winner = p1
        elif board[0].name == "rectangle":
            winner = p2
    elif board[3].name == board[4].name and board[3].name == board[5].name:
        if board[3].name == "circle":
            winner = p1
        elif board[3].name == "rectangle":
            winner = p2
    elif board[6].name == board[7].name and board[6].name == board[8].name:
        if board[6].name == "circle":
            winner = p1
        elif board[6].name == "rectangle":
            winner = p2
    elif board[0].name == board[3].name and board[0].name == board[6].name:
        if board[0].name == "circle":
            winner = p1
        elif board[0].name == "rectangle":
            winner = p2
    elif board[1].name == board[4].name and board[1].name == board[7].name:
        if board[1].name == "circle":
            winner = p1
        elif board[1].name == "rectangle":
            winner = p2
    elif board[2].name == board[4].name and board[2].name == board[6].name:
        if board[2].name == "circle":
            winner = p1
        elif board[2].name == "rectangle":
            winner = p2
    elif board[0].name == board[4].name and board[0].name == board[8].name:
        if board[0].name == "circle":
            winner = p1
        elif board[0].name == "rectangle":
            winner = p2
    elif board[2].name == board[4].name and board[2].name == board[6].name:
        if board[2].name == "circle":
            winner = p1
        elif board[2].name == "rectangle":
            winner = p2
    elif open_spots(board) == 0:
        return "tie"
    return winner


def reset(board, p1, p2, winner):
    for section in board:
        section.open = True
        section.name = ""
        pygame.draw.rect(win, WHITE, section.image)
    p1.turn = True
    p2.turn = False

# Minimax algorithm that the computer uses
def minimax(board, depth, max_player, p1, p2, scores):
    result = get_winner(board, p1, p2)
    if result != None:
        return scores[result]
    if max_player:
        maxEval = float("-inf")
        for section in board:
            if section.open:
                # Simulating a move and evaluating that particular move
                section.name = "circle"
                section.open = False
                eval = minimax(board, depth+1, False, p1, p2, scores) # Recursive call
                section.name = "blank"
                section.open = True
                maxEval = max(eval, maxEval)
        return maxEval
    else:
        minEval = float("inf")
        for section in board:
            if section.open:
                section.name = "rectangle"
                section.open = False
                eval = minimax(board, depth+1, True, p1, p2, scores)
                section.name = "blank"
                section.open = True
                minEval = min(eval, minEval)
        return minEval


first = Section(15, 15, "blank1")
second = Section(210, 15, "blank2")
third = Section(405, 15, "blank3")
fourth = Section(15, 210, "blank4")
fifth = Section(210, 210, "blank5")
sixth = Section(405, 210, "blank6")
seventh = Section(15, 405, "blank7")
eight = Section(210, 405, "blank8")
ninth = Section(405, 405, "blank9")

board = [first, second, third, fourth, fifth, sixth, seventh, eight, ninth]
board_shapes = []

turn_decider = random.randrange(0, 2)

p1 = Player("circle", True)
p2 = Player("rectangle", False)
scores = {p1: 1, p2: -1, "tie": 0}

run = True
clock = pygame.time.Clock()

for section in board:
    pygame.draw.rect(win, WHITE, section.image)

while run:
    clock.tick(30)
    winner = get_winner(board, p1, p2)
    if winner == p1:
        message_box("Player 1 Wins!!", "Play again...")
        reset(board, p1, p2, winner)
    if winner == p2:
        message_box("Player 2 Wins!!", "Play again...")
        reset(board, p1, p2, winner)
    if winner == "tie":
        message_box("Tie!", "Play again...")
        reset(board, p1, p2, winner)
    if p1.turn:
        if open_spots(board) == 9:
            place(win, first, p1, p2)
        else:
            best_score = float("-inf")
            best_move = None
            for section in board:
                if section.open:
                    section.name = "circle"
                    section.open = False
                    score = minimax(board, 0, False, p1, p2, scores)
                    section.name = "blank"
                    section.open = True
                    if score > best_score:
                        best_score = score
                        best_move = section
            place(win, best_move, p1, p2)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
        if pygame.mouse.get_pressed()[0]:
            pos = pygame.mouse.get_pos()
            for section in board:
                if section.image.collidepoint(pos) and p2.turn:
                    place(win, section, p1, p2)
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                reset(board, p1, p2, winner)

    pygame.display.update()

pygame.quit()
quit()