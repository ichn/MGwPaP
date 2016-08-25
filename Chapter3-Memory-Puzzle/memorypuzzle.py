
import random, pygame, sys
from pygame.locals import *

FPS=30  #Frames per second
WINDOWHEIGHT=640 #Height of  window in pixels
WINDOWWIDTH=480 #Width of  window in pixels
REVEALSPEED=8 #Speed box reveals & covers
BOXSIZE=40 #height&width of each square box
GAPSIZE=10 #pixels between boxes
BOARDWIDTH=3 #Number of columns of boxes
BOARDHEIGHT=4 #Number of rows of boxes
assert(BOARDWIDTH*BOARDHEIGHT)%2 == 0, 'BOARD MUST HAVE AN EVEN NUMBER OF TILES'
XMARGIN = int((WINDOWWIDTH - (BOARDWIDTH * (BOXSIZE + GAPSIZE))) / 2)
YMARGIN = int((WINDOWHEIGHT - (BOARDHEIGHT * (BOXSIZE + GAPSIZE))) / 2)

#            R    G    B
GRAY     = (100, 100, 100)
NAVYBLUE = ( 60,  60, 100)
WHITE    = (255, 255, 255)
RED      = (255,   0,   0)
GREEN    = (  0, 255,   0)
BLUE     = (  0,   0, 255)
YELLOW   = (255, 255,   0)
ORANGE   = (255, 128,   0)
PURPLE   = (255,   0, 255)
CYAN     = (  0, 255, 255)

BGCOLOR=NAVYBLUE
LIGHTBGCOLOR=GRAY
BOXCOLOR=WHITE
HIGHLIGHTCOLOR=BLUE

DONUT = 'donut'
SQUARE = 'square'
DIAMOND = 'diamond'
LINES = 'lines'
OVAL = 'oval'

ALLCOLORS = (RED, GREEN, BLUE, YELLOW, ORANGE, PURPLE, CYAN)
ALLSHAPES = (DONUT, SQUARE, DIAMOND, LINES, OVAL)
assert len(ALLCOLORS)*len(ALLSHAPES)*2 >= BOARDWIDTH*BOARDHEIGHT, "Too many boxes for shapes/colours"

def main():
    # Main program code goes here
    global FPSCLOCK, DISPLAYSURF
    pygame.init()
    FPSCLOCK = pygame.time.Clock()
    DISPLAYSURF = pygame.display.set_mode((WINDOWWIDTH, WINDOWHEIGHT))

    pygame.display.set_caption('Coderdojo Memory Game')

    mainBoard = getRandomizedBoard()
    revealedBoxes = generateRevealedBoxesData(False)

    firstSelection = None # stores the (x, y) of the first box clicked.

    DISPLAYSURF.fill(BGCOLOR)

    while True: # main game loop

        DISPLAYSURF.fill(BGCOLOR) # drawing the window
        drawBoard(mainBoard, revealedBoxes)

        for event in pygame.event.get(): # event handling loop
            if event.type == QUIT or (event.type == KEYUP and event.key == K_ESCAPE):
                pygame.quit()
                sys.exit()

        # Redraw the screen and wait a clock tick.
        pygame.display.update()
        FPSCLOCK.tick(FPS)


def generateRevealedBoxesData(val):
    revealedBoxes = []
    for i in range(BOARDWIDTH):
        revealedBoxes.append([val] * BOARDHEIGHT)
    return revealedBoxes


def getRandomizedBoard():
    # Get a list of every possible shape in every possible color.
    icons = []
    for color in ALLCOLORS:
        for shape in ALLSHAPES:
            icons.append( (shape, color) )

    random.shuffle(icons) # randomize the order of the icons list
    numIconsUsed = int(BOARDWIDTH * BOARDHEIGHT / 2) # calculate how many icons are needed
    icons = icons[:numIconsUsed] * 2 # make two of each
    random.shuffle(icons)

    # Create the board data structure, with randomly placed icons.
    board = []
    for x in range(BOARDWIDTH):
        column = []
        for y in range(BOARDHEIGHT):
            column.append(icons[0])
            del icons[0] # remove the icons as we assign them
        board.append(column)
    return board


def drawBoard(board, revealed):
    # Draws all of the boxes in their covered or revealed state.
    for boxx in range(BOARDWIDTH):
        for boxy in range(BOARDHEIGHT):
            left, top = leftTopCoordsOfBox(boxx, boxy)
            if not revealed[boxx][boxy]:
                # Draw a covered box.
                pygame.draw.rect(DISPLAYSURF, BOXCOLOR, (left, top, BOXSIZE, BOXSIZE))
            else:
                # Draw the (revealed) icon.
                shape, color = getShapeAndColor(board, boxx, boxy)
                drawIcon(shape, color, boxx, boxy)


def leftTopCoordsOfBox(boxx, boxy):
    # Convert board coordinates to pixel coordinates
    left = boxx * (BOXSIZE + GAPSIZE) + XMARGIN
    top = boxy * (BOXSIZE + GAPSIZE) + YMARGIN
    return (left, top)


def getShapeAndColor(board, boxx, boxy):
    # shape value for x, y spot is stored in board[x][y][0]
    # color value for x, y spot is stored in board[x][y][1]
    return board[boxx][boxy][0], board[boxx][boxy][1]


def drawIcon(shape, color, boxx, boxy):
    quarterBox = int(BOXSIZE * 0.25) # syntactic sugar
    halfBox =    int(BOXSIZE * 0.5)  # syntactic sugar
    DONUT_HALF_THICKNESS = 5

    left, top = leftTopCoordsOfBox(boxx, boxy) # get pixel coords from board coords
    # Draw the shapes
    if shape == DONUT:
        centre = (left + halfBox, top + halfBox)
        outerRadius = halfBox - DONUT_HALF_THICKNESS
        pygame.draw.circle(DISPLAYSURF, color, centre, outerRadius)
        innerRadius = quarterBox - DONUT_HALF_THICKNESS
        pygame.draw.circle(DISPLAYSURF, BGCOLOR, centre, innerRadius)
    elif shape == SQUARE:
        leftRect = left + quarterBox
        topRect = top + quarterBox
        width = height = BOXSIZE - halfBox
        rectangle = (leftRect, topRect, width, height)
        pygame.draw.rect(DISPLAYSURF, color, rectangle)
    elif shape == DIAMOND:
        p1 = (left + halfBox, top)
        p2 = (left + BOXSIZE - 1, top + halfBox)
        p3 = (left + halfBox, top + BOXSIZE - 1)
        p4 = (left, top + halfBox)
        pygame.draw.polygon(DISPLAYSURF, color, (p1, p2, p3, p4))
    # TO DO: shape == LINES and shape == OVAL

if __name__ == '__main__':
    main()
