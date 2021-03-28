#################################################
# hw6b: One-Dimensional Connect Four
# name: Vishal Saikrishnan  
# andrew id: vsaikris
#
# collaborator(s) names and andrew ids: Victoria Zhang, vzhang
# 
#################################################

import cs112_s21_week6_linter
from cmu_112_graphics import *
import random, string, math, time

#################################################
# Helper functions
#################################################

def almostEqual(d1, d2, epsilon=10**-7): #helper-fn
    # note: use math.isclose() outside 15-112 with Python version 3.5 or later
    return (abs(d2 - d1) < epsilon)

import decimal
def roundHalfUp(d): #helper-fn
    # Round to nearest with ties going away from zero.
    rounding = decimal.ROUND_HALF_UP
    # See other rounding options here:
    # https://docs.python.org/3/library/decimal.html#rounding-modes
    return int(decimal.Decimal(d).to_integral_value(rounding=rounding))

#################################################
# main app
#################################################

def appStarted(app):
    app.player1 = random.randint(0,1)
    app.player2 = 1-app.player1
    app.currentPlayer = app.player1
    app.color = ['blue','green']
    app.numOfCircles = 10
    app.board = [app.player1, app.player2] * int(app.numOfCircles/2)
    app.selection = []
    app.selectedCircles = []
    app.selectionLegal = False
    app.clicked = -1
    app.pinkBox = False
    app.moveIt = False
    app.gameOver = False
    app.message = 'Select your 3-piece block'
    logistics(app)


def logistics(app):##This will reset these variables when the dimensions change
    app.cellWidth = app.width/app.numOfCircles
    app.cy = 0.5*app.height
    app.r = 0.4*app.cellWidth

##This helper function will return True if Selection is Legal and False if
##Selection is Illegal.
def isSelectionLegal(app, event, position, center):
    app.moveIt = False
    logistics(app)
    if app.cy-app.r <= event.y <= app.cy + app.r:  ##click to be in the row
        if center-app.r <= event.x <= center+app.r: ##which circle was clicked
            if app.clicked == 0 or app.clicked == len(app.board)-1: #Illegal
                if app.selectionLegal: #But if this is to move circles,
                    app.moveIt = True  #it is legal
                app.selectionLegal = False
            elif position == 1 or position == len(app.board)-2: #illegal
                app.selectionLegal = False
                app.pinkBox = True  #rectangle will be pink
            else: 
                app.selectionLegal = True #Legal if it passes everything above
        else: app.selectionLegal = False
    else: app.selectionLegal = False



def mousePressed(app, event):
    ## First if statement prevents mouseclick from registering when we're 
    ## changing dimensions of the canvas
    if app.gameOver == False and app.height*0.3<event.y<app.height*0.7:
        app.clicked = getPiecePosition(app, event.x) # which circle was clicked
        (center, y, r) = getPieceCYR(app, app.clicked) #Get coordinates
        app.pinkBox = False
        isSelectionLegal(app, event, app.clicked, center) #check if legal
        if app.moveIt == False: ##Still on the selection click
            pos = app.clicked
            app.selection = [pos-1, pos, pos+1, pos+2]
            if pos < len(app.board)-1 and pos > 1:
                app.selectedCircles=([app.board[pos-1], app.board[pos], 
                                    app.board[pos+1]])
        if app.moveIt: ##This will remove the selection and place at either end
            if app.clicked == 0:
                app.board = (app.selectedCircles + app.board[:app.selection[0]]+
                                app.board[app.selection[3]:])
            else:
                app.board=(app.board[:app.selection[0]]+
                            app.board[app.selection[3]:]+app.selectedCircles)
            if app.currentPlayer == app.player1: #Switches player after this
                app.currentPlayer = app.player2
            else: app.currentPlayer = app.player1


def keyPressed(app, event):
    if app.gameOver== False: 
        if event.key == 'Down' or event.key == 'Left': ##Removes circles
            if app.numOfCircles > 6:
                app.numOfCircles -= 2
                logistics(app)
        elif event.key == 'Up' or event.key == 'Right': ##Adds circles
            if app.numOfCircles < 20:
                app.numOfCircles += 2
                logistics(app)
        if event.key == 'p':   ##Switches player
            if app.currentPlayer == app.player1:
                app.currentPlayer = app.player2
            else: app.currentPlayer = app.player1
        if event.key == 'c': ##switches selected circles' colors to player color
            for each in app.selection[:-1]:
                if app.currentPlayer == app.player1:
                    app.board[each] = app.player1
                else: app.board[each] = app.player2
    if event.key == 'r':  #restart game
        appStarted(app)


##This helper function will return circle center, height, and radius
def getPieceCYR(app, position):
    cellWidth = app.width/app.numOfCircles
    center = cellWidth*position + (cellWidth/2)
    cy = 0.5*app.height
    r = 0.4*cellWidth
    return (center, cy, r)

## This helper function will return the position of the circle clicked
def getPiecePosition(app, x):
    cellWidth = app.width/app.numOfCircles
    position = int(x/cellWidth)
    return position


##This helper function will decide which message to display
def whichMessage(app):
    if app.gameOver:
        app.message = 'Game Over!!!!'
    elif app.pinkBox:
        app.message = 'End cannot be in block'
    elif app.selectionLegal:
        app.message = 'Select end to move block'
    elif app.clicked == 0 or app.clicked == app.numOfCircles-1: #end circles
        if app.moveIt:
            app.message = 'Select your 3-piece block'
        else: app.message = 'Cannot move illegal selection'
    else: 
        app.message = 'Select your 3-piece block'


## Checks if the Game has ended
def isGameOver(app):
    prev = app.board[0]
    count = 1
    winner = None
    winningIndex = None
    for i in range(1, len(app.board)): ##iterates through the board
        if app.board[i] == prev: ## checks to see how many same color circles
            count += 1           ## are in a row
        else: count = 1
        if count == 4: ## If 4 in a row, exit the function/game has ended
            app.gameOver = True
            if app.board[i] == app.player1:
                winner = app.player1 #return which player won
            else: winner = app.player2
            winningIndex = i #return the winning circle (last circle in the row)
            return (winner, winningIndex)
        prev = app.board[i]
    

##check if game over always
##check which message should be displayed always
def timerFired(app):
    isGameOver(app)
    whichMessage(app)



################################
### All the draw functions
################################

def drawTitle(app, canvas): ##Draws the Game title
    canvas.create_text(app.width/2, app.height*0.07,
                        text = "One-Dimensional Connect Four!",
                        font = 'Arial 30 bold')


def drawInstructions(app, canvas): 
    yIncrement = 0.036*app.height
    count = 0
    messages = ['See rules below.',
                'Click interior piece to select center of 3-piece block.',
                'Click end piece to move that block to that end.',
                'Change board size (and then restart) with arrow keys.',
                'For debugging, press c to set the color of selected block.',
                'For debugging, press p to change the current player.',
                'Press r to restart.',
               ]
    for line in messages: ##draws each line in the instructions
        canvas.create_text(app.width/2, app.height*0.12 + count*yIncrement,
                        text = f'{line}',
                        font = 'Arial 15 bold')
        count += 1


def drawRules(app, canvas):
    yIncrement = 0.036*app.height
    count = 0
    messages = [
  "The Rules of One-Dimensional Connect Four:",
  "Arrange N (10 by default) pieces in a row of alternating colors.",
  "Players take turns to move three pieces at a time, where:",
  "      The pieces must be in the interior (not on either end)",
  "      The pieces must be adjacent (next to each other).",
  "      At least one moved piece must be the player's color.",
  "The three pieces must be moved in the same order to either end of the row.",
  "The gap must be closed by sliding the remaining pieces together.",
  "The first player to get four (or more) adjacent pieces of their color wins!",
               ]
    for line in messages: ##draws each line in the rules
        canvas.create_text(10, app.height*0.65 + count*yIncrement,
                        text = f'{line}',
                        font = 'Arial 16 bold',
                        anchor = 'sw')
        count += 1




## Which player is going right now and which color are they associated with
def drawCurrentPlayer(app, canvas):
    if app.currentPlayer == app.player1: ##Find the correct color
            color = app.color[app.currentPlayer]
    else: color = app.color[app.currentPlayer]
    if app.gameOver: ##If game over, don't switch the color to other player
        (winner, winningIndex) = isGameOver(app)
        if winner == app.currentPlayer: ##Display the winner's colors
            color = app.color[app.currentPlayer]
        else: color = app.color[1-app.currentPlayer]
    canvas.create_text(app.width*0.5, app.height*0.39,
                        text = 'Current Player: ',
                        font = 'Arial 16 bold', fill = f'{color}',
                        anchor = 'e')
    canvas.create_oval(app.width*0.525 - 9, app.height*0.39 - 9, 
                        app.width*0.525 + 9, app.height*0.39 + 9,
                        fill = 'light' + f'{color}', 
                        outline = f'{color}', width = 4)


## Display message
def drawCurrentMessage(app, canvas):
    if app.currentPlayer == app.player1: ##Find the current player's color
        color = app.color[app.currentPlayer]
    else: color = app.color[app.currentPlayer]
    if app.gameOver:  ##If a player has won already, find that player's color
        (winner, winningIndex) = isGameOver(app) 
        if winner == app.currentPlayer: 
            color = app.color[app.currentPlayer]
        else: color = app.color[1-app.currentPlayer]
    canvas.create_text(app.width*0.55, app.height*0.39,
                        text = f'{app.message}', ##message from whichMessage()
                        fill = f'{color}', font = 'Arial 16 bold',
                        anchor = 'w')


##Draw the actual selection box
def drawSelection(app, canvas):
    if app.gameOver: ##Box should disappear
        color = 'white'
    elif app.pinkBox: ##Illegal selection
        color = 'pink'
    else: color = 'orange'
    if app.selectionLegal or app.pinkBox: #Draw the rectangle
        (left,h,r) = getPieceCYR(app, app.selection[0]) #Left circle center
        (right,h,r) = getPieceCYR(app, app.selection[2])# Right Circle center
        change = r + 0.01*app.width
        canvas.create_rectangle(left-change, h-change, 
                                right+change,h+change,
                                fill = f'{color}', width = 0)
        drawBoard(app, canvas)
    if app.moveIt: ##board has shifted, so draw board again
        drawBoard(app, canvas)


## Main drawing function of the circles
def drawBoard(app, canvas):
    center = 0
    for circle in range(len(app.board)):
        if app.board[circle] == 1: ## Determines which color
            color = app.color[1]
        else: color = app.color[0]
        (center,h,r) = getPieceCYR(app, circle) ##gets coordinates
        canvas.create_oval(center-r, h-r, center+r, h+r,
                        fill = 'light' + f'{color}', 
                        outline = f'{color}', width = 5)


##Draws the Game Over black line
def drawGameOver(app, canvas):
    winningIndex = None
    winner = None
    if app.gameOver:
        (winner, winningIndex) = isGameOver(app) #get winner and winningCircle
        (x0,y0,r) = getPieceCYR(app, (winningIndex-3)) ##Leftmost circle center
        (x1,y1,r) = getPieceCYR(app, winningIndex) ##Rightmost circle center
        canvas.create_line(x0,y0,x1,y1, fill= 'black', width = 4)


def redrawAll(app, canvas):
    drawTitle(app, canvas)
    drawInstructions(app, canvas)
    drawCurrentPlayer(app, canvas)
    drawCurrentMessage(app, canvas)
    drawBoard(app, canvas)
    drawRules(app, canvas)
    if app.selection != []: ##prevent out of index error
        drawSelection(app, canvas)
    drawGameOver(app, canvas)


def main():
    cs112_s21_week6_linter.lint()
    runApp(width=650, height=550)

if __name__ == '__main__':
    main()