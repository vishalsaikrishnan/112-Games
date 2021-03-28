#################################################
# hw8.py: 2d Lists + Tetris!
#
# Your name: Vishal Saikrishnan
# Your andrew id: vsaikis
#
# Your partner's name: Victoria Zhang, Miles Matbia
# Your partner's andrew id: vzhang, mmatbia
#################################################

import cs112_s21_week8_linter
import math, copy, random

from cmu_112_graphics import *

#################################################
# Helper functions
#################################################

def almostEqual(d1, d2, epsilon=10**-7):
    # note: use math.isclose() outside 15-112 with Python version 3.5 or later
    return (abs(d2 - d1) < epsilon)

import decimal
def roundHalfUp(d):
    # Round to nearest with ties going away from zero.
    rounding = decimal.ROUND_HALF_UP
    # See other rounding options here:
    # https://docs.python.org/3/library/decimal.html#rounding-modes
    return int(decimal.Decimal(d).to_integral_value(rounding=rounding))

#################################################
# Functions for you to write
#################################################

def isRectangular(L):
    for each in L:
        if not isinstance(each, list): return False
    rows = len(L)
    if rows <= 1: return False
    cols = len(L[0])
    for row in L:
        if cols != len(row):
            return False
    return True


def makeMagicSquare(n):
    if n <= 0 or n%2 == 0: return None  ## Negative or even numbers
    result =[] 
    for rows in range(n): ## Make the initial 2-D list with just '1' in it
        temp = []
        for cols in range(n):
            if rows == 0 and cols == n//2:
                temp += [1] ## Add '1' to the middle of the first row
            else: temp += [0]  ## Add '0' everywhere else
        result.append(temp)
    result = siameseNumbers(result, n) ## do the siamese pattern everywhere else
    return result
    

def siameseNumbers(result, n):
    num = 1
    rowNum = n
    colNum = n//2
    for rows in range(n**2-1):
        num += 1   
        if colNum >= n-1:  # if col is outside bounds, wrap around
            colNum = 0
        else: colNum +=1
        if rowNum <= 0:  # if row is outside bounds, wrap around
            rowNum = n-1
        else: rowNum -=1
        if result[rowNum][colNum] != 0: ## If another number in the position
            rowNum = tempRow + 1   ## put number below below the prev number
            colNum = tempCol
        result[rowNum][colNum] = num 
        tempRow = rowNum  
        tempCol = colNum
    return result


##########################
## TETRIS
##########################

## Make the width and height of canvas using dimensions
def playTetris():
    (rows, cols, cellWidth, margin) = gameDimensions()
    width = (cols*cellWidth) + (margin*2) 
    height = (rows*cellWidth) + (margin*2)
    runApp(width = width, height = height)


def gameDimensions(): ### Rows, columns, cellWidth, and margin
    r = 15
    c = 10
    cw = 20
    m = 25
    return (r, c, cw, m)


## create the 2-D list that stores 'blue' for the board
def createBoard(app, r, c, color):
    result = []
    for rows in range(r):
        temp = []
        for cols in range(c):
            temp += [color]
        result.append(temp)
    return result


def appStarted(app):
    (app.rows, app.cols, app.cellWidth, app.margin) = gameDimensions()
    app.emptyColor = 'blue'
    app.board = createBoard(app, app.rows, app.cols, app.emptyColor)
    app.tetrisPieces = tetrisPieces(app)
    app.tetrisPieceColors = (["red","yellow","magenta","pink",
                                "cyan","green","orange"])
    newFallingPiece(app)
    app.specialTurns = 0
    app.time = 0
    app.score = 0
    app.gameOver = False
    


def tetrisPieces(app): ## The different types of pieces
    iPiece = [
        [  True,  True,  True,  True ]
    ]
    jPiece = [
        [  True, False, False ], 
        [  True,  True,  True ]
    ]
    lPiece = [
        [ False, False,  True ],
        [  True,  True,  True ]
    ]
    oPiece = [
        [  True,  True ],
        [  True,  True ]
    ]
    sPiece = [
        [ False,  True,  True ],
        [  True,  True, False ]
    ]
    tPiece = [
        [ False,  True, False ],
        [  True,  True,  True ]
    ]
    zPiece = [
        [  True,  True, False ],
        [ False,  True,  True ]
    ]
    return [iPiece, jPiece, lPiece, oPiece, sPiece, tPiece, zPiece]



def newFallingPiece(app): ## Randomly get a new piece
    num = random.randint(0, len(app.tetrisPieces) - 1)
    app.fallingPiece = app.tetrisPieces[num]
    app.fallingColor = app.tetrisPieceColors[num] 
    app.frow = 0  ## Falling piece row
    app.fcol = app.cols//2 - (len(app.fallingPiece[0])//2) ## Falling piece col
    if (fallingPieceIsLegal(app) == False) and app.frow == 0: ##check if legal
        app.gameOver = True


def moveFallingPiece(app, vert, hor): ## Move the piece left, right, down
    if app.gameOver: return
    drow = vert
    dcol = hor
    app.frow += drow
    app.fcol += dcol
    if fallingPieceIsLegal(app) == False: ## reverse changes if move isn't legal
        app.frow -= drow
        app.fcol -= dcol
        return False
    return True


def fallingPieceIsLegal(app):  ## Check if move is legal
    for row in range(len(app.fallingPiece)):
        for col in range(len(app.fallingPiece[0])):
            if app.fallingPiece[row][col]:  
                ## Movement has to be in the grid
                if ((app.frow + row >= app.rows) or (app.frow + row < 0) or
                        (app.fcol + col >= app.cols) or (app.fcol + col <0)):
                    return False
                ## Movement can't go into a spot thats already taken
                if app.board[app.frow + row][app.fcol + col] != 'blue':
                    return False
                

def rotateFallingPiece(app):
    fallingPiece = app.fallingPiece ##temp var in case rotation isn't legal
    oldRows, oldCols = len(app.fallingPiece), len(app.fallingPiece[0])
    newRows, newCols = oldCols, oldRows
    rotatedPiece = [] 
    if (app.fallingPiece == [[  True,  True,  True,  True ]] or 
                app.fallingPiece == [[True],[True],[True],[True]]):
        specialCaseRotation(app) ##This is for the red 1x4 piece
        return
    ## For all other pieces
    for i in range(newRows):
        temp = []
        for j in range(newCols):
            temp += [None]
        rotatedPiece.append(temp) ## Make new list with 'None' as placeholders

    for row in range(oldRows):
        for col in range(oldCols):
            ## input the Trues and Falses by switching rows and columns
            rotatedPiece[oldCols-col-1][row] = app.fallingPiece[row][col]
    app.fallingPiece = rotatedPiece

    if fallingPieceIsLegal(app) == False: ## If rotation isn't legal
        app.fallingPiece = fallingPiece   ## reset piece to the temp from before



def specialCaseRotation(app): ## Special rotation for the red 1x4 piece
    tempC = app.fcol
    tempR = app.frow
    temp = app.fallingPiece
    if app.fallingPiece == [[  True,  True,  True,  True ]]: 
        app.fallingPiece = [[True],[True],[True],[True]]
        app.fcol += 2   ## Recenter piece
        app.frow -= 2            
    else:
        app.fallingPiece = [[  True,  True,  True,  True ]]
        app.frow += 2   ## Recenter piece
        app.fcol -= 2
    if fallingPieceIsLegal(app) == False: ## Reset piece if rotation isn't legal
        app.fallingPiece = temp
        app.fcol = tempC
        app.frow = tempR
        

def placeFallingPiece(app): ## Integrate piece into board once set
    for row in range(len(app.fallingPiece)):
        for col in range(len(app.fallingPiece[row])):
            if app.fallingPiece[row][col]: 
                app.board[app.frow+row][app.fcol+col] = [app.fallingColor]
                

def removeFullRows(app):  ## Remove row if its filled (score goes up)
    count = 0
    score = 0
    for row in range(app.rows): ## Iterate through rows and see if all
        count = 0               ## Colors are NOT blue
        for col in range(app.cols):
            if app.board[row][col] != 'blue':
                count += 1
            if count == app.cols: ## if row is full, remove row and add new one
                app.board.pop(row) 
                app.board = [['blue' for i in range(app.cols)]] + app.board
                score += 1
    app.score += score**2 


def howFarDrop(app): ## See how many rows the space bar should 'hard drop'
    for row in range(app.rows):
        ## Check within the columns taken up by the piece
        for col in range(app.fcol, app.fcol + len(app.fallingPiece[0])):
            if app.board[row][col] != 'blue':
                return (row-2) 
    return (app.rows-2)

## Get x,y coordinates to make the grid and pieces
def getCellXY(app, row, col):
    x0 = app.margin + (col*app.cellWidth)
    x1 = x0 + app.cellWidth
    y0 = app.margin + (row*app.cellWidth)
    y1 = y0 + app.cellWidth
    return (x0,y0,x1,y1)


def keyPressed(app, event):
    if event.key == 'r':
        appStarted(app)
    if app.gameOver: return 
    if event.key == 'Up': 
        rotateFallingPiece(app)
    if event.key == 'Space': ## hard drop the piece
        num = howFarDrop(app)
        if app.frow < num: 
            moveFallingPiece(app, num-app.frow, 0)
    elif event.key == 'Down':
        moveFallingPiece(app,1,0)
    if event.key == 'Right':
        moveFallingPiece(app,0,1)
    if event.key == 'Left':
        moveFallingPiece(app,0,-1)


def timerFired(app):
    removeFullRows(app) ## check to remove
    temp = None
    app.time += 1 
    if app.time % 3 == 0:  ## automatically move piece down
        temp = moveFallingPiece(app,1,0) ## Find when piece can't go further
    if temp == False: 
        placeFallingPiece(app)  ## integrate old piece
        newFallingPiece(app)    ## New piece comes at the top


########################################
###########  DRAW FUNCTIONS   ##########
########################################

def drawCell(app, canvas):    ## Draw the grid
    for row in range(app.rows):
        for col in range(app.cols):
            (x0,y0,x1,y1) = getCellXY(app, row, col)
            canvas.create_rectangle(x0,y0,x1,y1, fill = app.board[row][col],
                                width = 4)


def drawBoard(app, canvas):  ## Draw orange margin
    canvas.create_rectangle(0,0,app.width,app.height, fill = 'orange')


def drawScore(app, canvas): ## Draw score at top
    canvas.create_text(app.width/2, app.margin/2,
                        text = 'Score = '+ f'{app.score}', fill = 'navy',
                        font = 'Arial 16 bold')


def drawFallingPiece(app, canvas):  ## Draw the falling piece at the top
    if app.gameOver: return
    frow = app.frow
    fcol = app.fcol
    for row in range(len(app.fallingPiece)):
        for col in range(len(app.fallingPiece[row])):
            if app.fallingPiece[row][col]:
                (x0,y0,x1,y1) = getCellXY(app, row + frow, col + fcol)
                canvas.create_rectangle(x0,y0,x1,y1, 
                                fill = app.fallingColor, width = 4)


def drawGameOver(app, canvas): ## Draw the game over banner
    if app.gameOver:
        canvas.create_rectangle(0, app.height*0.2, app.width, app.height*0.4,
                                fill = 'black')
        canvas.create_text(app.width/2, app.height*0.3,
                            text = 'Game Over!', font = 'Arial 30 bold',
                            fill = 'yellow')


def redrawAll(app, canvas):
    drawBoard(app, canvas)
    drawCell(app, canvas)
    drawFallingPiece(app, canvas)
    drawScore(app, canvas)
    drawGameOver(app, canvas)


#################################################
# Test Functions
#################################################

def testIsRectangular():
    print('Testing isRectangular()...', end='')
    assert(isRectangular([[1,2],[3,4]]) == True)
    assert(isRectangular([[1,2],[3,4,5]]) == False)
    assert(isRectangular([[1],[2]]) == True)
    assert(isRectangular([[],[]]) == True)
    assert(isRectangular([]) == False)
    assert(isRectangular(["this", "is", "silly"]) == False)
    assert(isRectangular([["this"], "is", "silly"]) == False)
    assert(isRectangular([["this"], ["is"], ["fine"]]) == True)
    assert(isRectangular([[1], [2,3], [4]]) == False)
    assert(isRectangular([[1,2], [3], [4]]) == False)
    assert(isRectangular([12, [3], [4]]) == False)
    assert(isRectangular(["abc", [1,2,3]]) == False)
    print('Passed!')

def testMakeMagicSquare():
    print('Testing makeMagicSquare()...', end='')
    L1 = [[1]]
    L3 = [[8 , 1 , 6],
          [3 , 5 , 7],
          [4 , 9 , 2]]
    L5 = [[17 , 24 ,  1 ,   8 , 15],
          [23 ,  5 ,  7 ,  14 , 16],
          [ 4 ,  6 , 13 ,  20 , 22],
          [10 , 12 , 19 ,  21 ,  3],
          [11 , 18 , 25 ,   2 ,  9]]
    L9 = [[47,58,69,80,1,12,23,34,45],
          [57,68,79,9,11,22,33,44,46],
          [67,78,8,10,21,32,43,54,56],
          [77,7,18,20,31,42,53,55,66],
          [6,17,19,30,41,52,63,65,76],
          [16,27,29,40,51,62,64,75,5],
          [26,28,39,50,61,72,74,4,15],
          [36,38,49,60,71,73,3,14,25],
          [37,48,59,70,81,2,13,24,35]]
    assert(makeMagicSquare(1) == L1)
    assert(makeMagicSquare(3) == L3)
    assert(makeMagicSquare(5) == L5)
    assert(makeMagicSquare(9) == L9)
    assert(makeMagicSquare(0) == None)
    assert(makeMagicSquare(2) == None)
    assert(makeMagicSquare(4) == None)
    assert(makeMagicSquare(-3) == None)
    print('Passed!')

def testAll():
    testIsRectangular()
    testMakeMagicSquare()

#################################################
# main
#################################################

def main():
    cs112_s21_week8_linter.lint()
    testAll()
    playTetris()

if __name__ == '__main__':
    main()
