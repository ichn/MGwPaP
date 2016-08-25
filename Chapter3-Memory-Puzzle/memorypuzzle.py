# Memory Puzzle
# By Al Sweigart al@inventwithpython.com
# http://inventwithpython.com/pygame
# Released under a "Simplified BSD" license

import random, pygame, sys
from pygame.locals import *

FPS = 30 # frames per second, the general speed of the program
WINDOWWIDTH = 640 # size of window's width in pixels
WINDOWHEIGHT = 480 # size of windows' height in pixels
REVEALSPEED = 8 # speed boxes' sliding reveals and covers
BOXSIZE = 40 # size of box height & width in pixels
GAPSIZE = 10 # size of gap between boxes in pixels
BOARDWIDTH = 10 # number of columns of icons
BOARDHEIGHT = 7 # number of rows of icons
assert (BOARDWIDTH * BOARDHEIGHT) % 2 == 0, 'Board needs to have an evennumber of boxes for pairs of matches.'
XMARGIN = int((WINDOWWIDTH - (BOARDWIDTH * (BOXSIZE + GAPSIZE))) / 2)
YMARGIN = int((WINDOWHEIGHT - (BOARDHEIGHT * (BOXSIZE + GAPSIZE))) / 2)

GRAY = (100, 100, 100)
NAVYBLUE = ( 60, 60, 100)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = ( 0, 255, 0)
BLUE = ( 0, 0, 255)
YELLOW = (255, 255, 0)
ORANGE = (255, 128, 0)
PURPLE = (255, 0, 255)
CYAN = ( 0, 255, 255)
BGCOLOR = NAVYBLUE
LIGHTBGCOLOR = GRAY
BOXCOLOR = WHITE
HIGHLIGHTCOLOR = BLUE

DONUT = 'donut'
SQUARE = 'square'
DIAMOND = 'diamond'
LINES = 'lines'
OVAL = 'oval'

ALLCOLORS = (RED, GREEN, BLUE, YELLOW, ORANGE, PURPLE, CYAN)
ALLSHAPES = (DONUT, SQUARE, DIAMOND, LINES, OVAL)
assert len(ALLCOLORS) * len(ALLSHAPES) * 2 >= BOARDWIDTH * BOARDHEIGHT, "Board is too big for the number of shapes/colors defined."

def main():
	global FPSCLOCK, DISPLAYSURF
	pygame.init()
	FPSCLOCK = pygame.time.Clock()
	DISPLAYSURF = pygame.display.set_mode((WINDOWWIDTH, WINDOWHEIGHT))
	mousex = 0 # used to store x coordinate of mouse event
	mousey = 0 # used to store y coordinate of mouse event
	pygame.display.set_caption('Memory Game')
	mainBoard = getRandomizedBoard()
	revealedBoxes = generateRevealedBoxesData(False)
	firstSelection = None # stores the (x, y) of the first box clicked.
	DISPLAYSURF.fill(BGCOLOR)
	startGameAnimation(mainBoard)
	while True: # main game loop
		mouseClicked = False
		DISPLAYSURF.fill(BGCOLOR) # drawing the window
		drawBoard(mainBoard, revealedBoxes)
		for event in pygame.event.get(): # event handling loop
		if event.type == QUIT or (event.type == KEYUP and event.key == K_ESCAPE):
			pygame.quit()
			sys.exit()
		elif event.type == MOUSEMOTION:
			mousex, mousey = event.pos
		elif event.type == MOUSEBUTTONUP:
			mousex, mousey = event.pos
			mouseClicked = True
			boxx, boxy = getBoxAtPixel(mousex, mousey)
		if boxx != None and boxy != None:
		# The mouse is currently over a box.
			if not revealedBoxes[boxx][boxy]:
				drawHighlightBox(boxx, boxy)
			if not revealedBoxes[boxx][boxy] and mouseClicked:
				revealBoxesAnimation(mainBoard, [(boxx, boxy)])
				revealedBoxes[boxx][boxy] = True # set the box as "revealed"
				if firstSelection == None: # the current box was the first box clicked
					firstSelection = (boxx, boxy)
				else: # the current box was the second box clicked
				# Check if there is a match between the two icons.
					icon1shape, icon1color = getShapeAndColor(mainBoard, firstSelection[0], firstSelection[1])
					icon2shape, icon2color = getShapeAndColor(mainBoard, boxx, boxy)
				if icon1shape != icon2shape or icon1color != icon2color:
					# Icons don't match. Re-cover up both selections.
					pygame.time.wait(1000) # 1000 milliseconds = 1 sec
					coverBoxesAnimation(mainBoard, [(firstSelection[0], firstSelection[1]), (boxx, boxy)])
					revealedBoxes[firstSelection[0]][firstSelection[1]] = False
					revealedBoxes[boxx][boxy] = False
				elif hasWon(revealedBoxes): # check if all pairs found
					gameWonAnimation(mainBoard)
					pygame.time.wait(2000)
					# Reset the board
					mainBoard = getRandomizedBoard()
					revealedBoxes = generateRevealedBoxesData(False)
					# Show the fully unrevealed board for a second.
					drawBoard(mainBoard, revealedBoxes)
					pygame.display.update()
					pygame.time.wait(1000)
					# Replay the start game animation.
					startGameAnimation(mainBoard)
					firstSelection = None # reset firstSelection variable
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
 numIconsUsed = int(BOARDWIDTH * BOARDHEIGHT / 2) # calculate how many
icons are needed
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
def splitIntoGroupsOf(groupSize, theList):
 # splits a list into a list of lists, where the inner lists have at
 # most groupSize number of items.
 result = []
 for i in range(0, len(theList), groupSize):
 result.append(theList[i:i + groupSize])
 return result
def leftTopCoordsOfBox(boxx, boxy):
 # Convert board coordinates to pixel coordinates
 left = boxx * (BOXSIZE + GAPSIZE) + XMARGIN
 top = boxy * (BOXSIZE + GAPSIZE) + YMARGIN
 return (left, top)
def getBoxAtPixel(x, y):
 for boxx in range(BOARDWIDTH):
 for boxy in range(BOARDHEIGHT):
 left, top = leftTopCoordsOfBox(boxx, boxy)
 boxRect = pygame.Rect(left, top, BOXSIZE, BOXSIZE)
 if boxRect.collidepoint(x, y):
 return (boxx, boxy)
 return (None, None)
def drawIcon(shape, color, boxx, boxy):
 quarter = int(BOXSIZE * 0.25) # syntactic sugar
 half =
 int(BOXSIZE * 0.5) # syntactic sugar
 left, top = leftTopCoordsOfBox(boxx, boxy) # get pixel coords from
board coords
 # Draw the shapes
 if shape == DONUT:
 pygame.draw.circle(DISPLAYSURF, color, (left + half, top + half),
half - 5)
 pygame.draw.circle(DISPLAYSURF, BGCOLOR, (left + half, top +
half), quarter - 5)
 elif shape == SQUARE:
 pygame.draw.rect(DISPLAYSURF, color, (left + quarter, top +
quarter, BOXSIZE - half, BOXSIZE - half))
 elif shape == DIAMOND:
 pygame.draw.polygon(DISPLAYSURF, color, ((left + half, top), (left
+ BOXSIZE - 1, top + half), (left + half, top + BOXSIZE - 1), (left, top +
half)))
 elif shape == LINES:
 for i in range(0, BOXSIZE, 4):
 pygame.draw.line(DISPLAYSURF, color, (left, top + i), (left +
i, top))
 pygame.draw.line(DISPLAYSURF, color, (left + i, top + BOXSIZE
- 1), (left + BOXSIZE - 1, top + i))
 elif shape == OVAL:
 pygame.draw.ellipse(DISPLAYSURF, color, (left, top + quarter,
BOXSIZE, half))
def getShapeAndColor(board, boxx, boxy):
203.
 # shape value for x, y spot is stored in board[x][y][0]
204.
 # color value for x, y spot is stored in board[x][y][1]
205.
 return board[boxx][boxy][0], board[boxx][boxy][1]
206.
207.
208. def drawBoxCovers(board, boxes, coverage):
209.
 # Draws boxes being covered/revealed. "boxes" is a list
210.
 # of two-item lists, which have the x & y spot of the box.
211.
 for box in boxes:
212.
 left, top = leftTopCoordsOfBox(box[0], box[1])
213.
 pygame.draw.rect(DISPLAYSURF, BGCOLOR, (left, top, BOXSIZE,
BOXSIZE))
214.
 shape, color = getShapeAndColor(board, box[0], box[1])
215.
 drawIcon(shape, color, box[0], box[1])
216.
 if coverage > 0: # only draw the cover if there is an coverage
217.
 pygame.draw.rect(DISPLAYSURF, BOXCOLOR, (left, top, coverage,
BOXSIZE))
218.
 pygame.display.update()
219.
 FPSCLOCK.tick(FPS)
220.
221.
222. def revealBoxesAnimation(board, boxesToReveal):
223.
 # Do the "box reveal" animation.
224.
 for coverage in range(BOXSIZE, (-REVEALSPEED) - 1, - REVEALSPEED):
225.
 drawBoxCovers(board, boxesToReveal, coverage)
226.
227.
228. def coverBoxesAnimation(board, boxesToCover):
229.
 # Do the "box cover" animation.
230.
 for coverage in range(0, BOXSIZE + REVEALSPEED, REVEALSPEED):
231.
 drawBoxCovers(board, boxesToCover, coverage)
232.
233.
234. def drawBoard(board, revealed):
235.
 # Draws all of the boxes in their covered or revealed state.
236.
 for boxx in range(BOARDWIDTH):
237.
 for boxy in range(BOARDHEIGHT):
238.
 left, top = leftTopCoordsOfBox(boxx, boxy)
239.
 if not revealed[boxx][boxy]:
240.
 # Draw a covered box.
241.
 pygame.draw.rect(DISPLAYSURF, BOXCOLOR, (left, top,
BOXSIZE, BOXSIZE))
242.
 else:
243.
 # Draw the (revealed) icon.
244.
 shape, color = getShapeAndColor(board, boxx, boxy)
245.
 drawIcon(shape, color, boxx, boxy)
246.
247.
248. def drawHighlightBox(boxx, boxy):
249.
 left, top = leftTopCoordsOfBox(boxx, boxy)
250.
 pygame.draw.rect(DISPLAYSURF, HIGHLIGHTCOLOR, (left - 5, top - 5,
BOXSIZE + 10, BOXSIZE + 10), 4)
251.
252.
253. def startGameAnimation(board):
254.
 # Randomly reveal the boxes 8 at a time.
255.
 coveredBoxes = generateRevealedBoxesData(False)
256.
 boxes = []
257.
 for x in range(BOARDWIDTH):
258.
 for y in range(BOARDHEIGHT):
259.
 boxes.append( (x, y) )
260.
 random.shuffle(boxes)
261.
 boxGroups = splitIntoGroupsOf(8, boxes)
262.
263.
 drawBoard(board, coveredBoxes)
264.
 for boxGroup in boxGroups:
265.
 revealBoxesAnimation(board, boxGroup)
266.
 coverBoxesAnimation(board, boxGroup)
267.
268.
269. def gameWonAnimation(board):
270.
 # flash the background color when the player has won
271.
 coveredBoxes = generateRevealedBoxesData(True)
272.
 color1 = LIGHTBGCOLOR
273.
 color2 = BGCOLOR
274.
275.
 for i in range(13):
276.
 color1, color2 = color2, color1 # swap colors
277.
 DISPLAYSURF.fill(color1)
278.
 drawBoard(board, coveredBoxes)
279.
 pygame.display.update()
280.
 pygame.time.wait(300)
281.
282.
283. def hasWon(revealedBoxes):
284.
 # Returns True if all the boxes have been revealed, otherwise False
285.
 for i in revealedBoxes:
286.
 if False in i:
287.
 return False # return False if any boxes are covered.
288.
 return True
289.
290.
291. if __name__ == '__main__':
292.
 main()
