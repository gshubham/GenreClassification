import pygame
pygame.init()

##width = 400
##height = 400
##NUM_SQUARES = 8
##SQUARE_WIDTH = width / NUM_SQUARES

DISPLAY_SIZE = 400
NUM_SQUARES = 8
SQUARE_SIZE = DISPLAY_SIZE / NUM_SQUARES
PIECE_RADIUS = int(   (SQUARE_SIZE/2)*.87   )
RED = (255,0,0)
GREEN = (0,255,0)
YELLOW = (255,255,0)
BLACK = (0,0,0)
GREY = (40,40,30)
WHITE = (255,255,255)
KING_FONT = pygame.font.Font(None, 40)
FONT_COLOR = (100,100,100)
CIRCLE_OUTLINE_WIDTH = 0

window = pygame.display.set_mode((DISPLAY_SIZE, DISPLAY_SIZE))

'''
This class handles all graphics involved for checkers. It
- draws the board
- lets you highlight squares when the user selects pieces
'''
class BoardDrawer:

    boardState = None
    @staticmethod 
    def draw(state):
        BoardDrawer.boardState = state
        for row in range(NUM_SQUARES):
            for col in range(NUM_SQUARES):
                color = RED if ((row+col)%2) else GREY #alternate based on even/odd sum
                BoardDrawer.drawSquare(row, col, color)
        pygame.display.flip()

    @staticmethod
    def drawSquare(row,col,color):
        rowcoord = row*SQUARE_SIZE
        colcoord = col*SQUARE_SIZE
        rectwidth = rectheight = SQUARE_SIZE
        pygame.draw.rect(window, color, (rowcoord, colcoord, rectwidth, rectheight))
           
    @staticmethod
    def highlightSquare(row,col,color):
        BoardDrawer.drawSquare(row,col,color)
        BoardDrawer.drawStateSquare(row, col, BoardDrawer.boardState[row][col])
        pygame.display.flip()

    
    @staticmethod
    def drawStateSquare(row,col,stateSquare):
        #stateSquare has a B for black, R for red
        # and K for king
        rowcenter = int( (row+.5)*SQUARE_SIZE)
        colcenter = int((col+.5)*SQUARE_SIZE)
        color = RED if 'R' in stateSquare else BLACK if 'B' in stateSquare else None
        if color:
            BoardDrawer.drawCircle(rowcenter, colcenter, color)

             #Now draw king if needed
            if 'K' in stateSquare:
##                kcolor = BLACK if color==RED else RED #opposite color so you can see it
                kcolor = GREY
                text = KING_FONT.render('K', True, FONT_COLOR)
                tw = text.get_width()
                th = text.get_height()
                window.blit(text, [rowcenter-tw/2, colcenter - th/2])

    @staticmethod
    def drawCircle(rowcenter, colcenter, color):
        outlineColor = BLACK if color==RED else RED
        pygame.draw.circle(window, outlineColor, (colcenter, rowcenter), PIECE_RADIUS, CIRCLE_OUTLINE_WIDTH)
        pygame.draw.circle(window, color, (colcenter, rowcenter), PIECE_RADIUS - CIRCLE_OUTLINE_WIDTH)

           
                
                
                

        
            
            
state = []        
for i in range(8):
    state.append(['RK']*8)
BoardDrawer.draw(state)
BoardDrawer.drawStateSquare(0,0,'KB')
BoardDrawer.highlightSquare(0,0,YELLOW)
pygame.display.flip()

