# This is the main driver file for the engine. It is responsible for handling user input and displaying the current GameState object

import pygame as p
import ChessEngine

Width = Height = 400
# Dimensions of the chess board is 8
Dimension = 8
SQ_Size = Height // Dimension
Max_FPS = 15
Images = {}

# Loading images will initialize a global dictionary of images. This will be called only once in ChessMain

def loadImages():
    pieces = ["wp", "wR", "wN", "wB", "wK", "wQ", "bp", "bR", "bN", "bB", "bK", "bQ"]
    for piece in pieces: 
        Images[piece] = p.transform.scale(p.image.load("chess_engine/images/" + piece + ".png"), (SQ_Size, SQ_Size))
    # The image can be accessed by saying "Images["wp"]"


# The main driver of the code is below. This will handle user input and update graphics
def main():
    p.init()
    screen = p.display.set_mode((Width, Height))
    clock = p.time.Clock()
    screen.fill(p.Color("white"))
    gs = ChessEngine.GameState()
    loadImages()
    running = True
    sqSelected = () # no square is selected it will keep track of the last click made by the user
    playerClicks = []     # keeps track of player clicks
    while running:
        for e in p.event.get():
            if e.type == p.quit:
                running = False
            elif e.type == p.MOUSEBUTTONDOWN: 
                location = p.mouse.get_pos() # (X,Y) location of mouse
                col = location[0]//SQ_Size
                row = location[1]//SQ_Size
                if sqSelected == (row,col): # prevents the user from clicking the same square twice in a row
                    sqSelected = ()
                    playerClicks = []
                else:
                    sqSelected = (row, col)
                    playerClicks.append(sqSelected) # appends for both first and second clicks here
                if len(playerClicks) == 2: # after 2nd click
                    move = ChessEngine.Move(playerClicks[0], playerClicks[1], gs.board)
                    print(move.getChessNotation())
                    gs.makeMove(move) 
                    sqSelected = () # reset user clicks
                    playerClicks = []
            elif e.type == p.KEYDOWN:
                if e.key == p.K_z:
                    gs.undoMove()

        drawGameState(screen, gs)
        clock.tick(Max_FPS)
        p.display.flip()


# Draws the squares on the board and is responsible for all the graphics within current game state
def drawGameState(screen, gs):
    drawBoard(screen)
    drawPieces(screen, gs.board)


# Draws the squares. The top left square should be white
# r = row and c = column
def drawBoard(screen):
    colors = [p.Color("white"), p.Color("gray")]
    for r in range(Dimension):
        for c in range(Dimension):
            color = colors[((r+c) % 2)]
            p.draw.rect(screen, color, p.Rect(c*SQ_Size, r*SQ_Size, SQ_Size, SQ_Size))

# Draws the pieces on the board within the game state
def drawPieces(screen, board):
    for r in range(Dimension):
        for c in range(Dimension):
            piece = board[r][c]
            if piece != "--":
                screen.blit(Images[piece], p.Rect(c*SQ_Size, r*SQ_Size, SQ_Size, SQ_Size))




# if __name__ == " main ":
main()

