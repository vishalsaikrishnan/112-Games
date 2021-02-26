#################################################
# hw4.py
#
# Your name: Vishal Saikrishnan
# Your andrew id: vsaikris
#################################################

import cs112_s21_week4_linter
from cmu_112_graphics import *
import random, string, math, time

# import sys
# print(f'sudo "{sys.executable}" -m pip install pillow')
# print(f'sudo "{sys.executable}" -m pip install requests')


# From here: https://www.cs.cmu.edu/~112/notes/notes-strings.html#basicFileIO

def readFile(path):
    with open(path, "rt") as f:
        return f.read()


def appStarted(app):
    app.guesses = 0
    app.found = 0
    app.mouse = False
    app.finish = 0
    app.correct = ''
    app.elapsedTime = 0
    app.fileContents = readFile('common-words.txt')
    app.word = random.choice(app.fileContents.splitlines())
    app.pressedKey = ''
    app.alphabet = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'
    app.pastKeys = ''

def mousePressed(app, event):
    app.mouse = not app.mouse
    if app.found == len(app.word):
        app.finish = 1
    else: app.finish = 0
    if app.finish == 1:
        appStarted(app)

def keyPressed(app, event):
    if app.found != len(app.word):
        app.guesses +=1
        app.pressedKey = event.key
        if event.key in (app.alphabet).lower():
            app.pastKeys += event.key
        if event.key in app.word:
            if (app.correct).count(event.key) < 1:
                app.correct += event.key
        app.found = 0
        for i in app.word:
            for j in app.correct:
                if j == i:
                    app.found +=1


def timerFired(app):
    if app.found == len(app.word):
        app.elapsedTime += 0
    else: app.elapsedTime += 1/10



#########################################
# redrawAll and drawing helper functions:
#########################################
def draw(app, canvas):
    canvas.create_line(0, app.height/4, app.width, app.height/4, 
                        fill = 'black')
    canvas.create_line(0, app.height/2, app.width, app.height/2, 
                        fill = 'black')
    canvas.create_line(0, 3*app.height/4, app.width, 3*app.height/4, 
                        fill = 'black')

def drawTitle(app, canvas):
    canvas.create_text(app.width/2, app.height/9,
                    text = 'Word Guessing Game',
                    font = 'Arial 30 bold',
                    fill = 'black')

def drawDisplayWord(app, canvas):
        colorText = ''
        colorUnder = ''
        underscoreIncrement = app.width/20
        start = (app.width/2) - (len(app.word)*(app.width/60))
        for letter in app.word:
            if app.mouse:
                colorText = 'black'
                colorUnder = 'white'
            else: 
                colorText = 'white' 
                colorUnder = 'black'
            canvas.create_text(start, app.height*0.38,
                            text = f'{letter.upper()} ' ,
                            font = 'Arial 40 bold',
                            fill = f'{colorText}')
            canvas.create_text(start-0.01*app.width, app.height*0.38,
                            text = '_',
                            font = 'Arial 40 bold',
                            fill = f'{colorUnder}')
            start += underscoreIncrement


def discoverWord(app, canvas):
    underscoreIncrement = app.width/20
    start = (app.width/2) - (len(app.word)*(app.width/60))
    whichLetter = ''
    for each in app.pastKeys:
        indexKey = each
        for guessedLetter in range(len(app.word)):
            if app.word[guessedLetter] == indexKey:
                whichLetter = app.word[guessedLetter]
                canvas.create_text(start+guessedLetter*underscoreIncrement,
                                    app.height*0.38,
                                    text = f'{whichLetter.upper()} ' ,
                                    font = 'Arial 40 bold',
                                    fill = 'black')
                canvas.create_text(start-0.01*app.width + 
                                guessedLetter*underscoreIncrement, 
                                app.height*0.38,
                                    text = '_',
                                    font = 'Arial 40 bold',
                                    fill = 'white')

                        
def drawAlphabet(app, canvas,):
    startRow = app.width*0.038
    increment = app.width/13
    row = app.height*0.57
    radius = 0.02*app.width
    y=0
    for x in range(2):
        for i in range(0+y,13+y):
            canvas.create_text(startRow, row,
                            text = f'{app.alphabet[i]}',
                            font = 'Arial 12',
                            fill = 'black' )
            startRow += increment
        startRow = app.width*0.038
        y+=13
        row *= 1.2


def drawColoredCircles(app, canvas):
    startRow = app.width*0.038
    increment = app.width/13
    row = 0
    radius = 0.02*app.width
    color = 'white'
    for each in app.pastKeys:
        indexKey = each
        for guessLetter in range(26):
            if (app.alphabet[guessLetter]).lower() == indexKey:
                letterToColor = app.alphabet[guessLetter]
                if letterToColor.lower() in app.word:
                    color = 'lightgreen'
                else: color = 'pink' 
                if letterToColor in 'NOPQRSTUVWXYZ': 
                    row = app.height*0.68
                else: row = app.height*0.57
                canvas.create_oval(
                                (startRow+(guessLetter%13)*increment)-radius, 
                                row - radius, 
                                (startRow+(guessLetter%13)*increment)+radius,
                                row+radius,
                                fill = f'{color}')
                canvas.create_text(startRow+(guessLetter%13)*increment, 
                                row,
                                text = f'{letterToColor}',
                                font = 'Arial 12')
        

def drawGuessCount(app, canvas):
    canvas.create_text(app.width*0.4, app.height*0.83,
                    text = 'Guesses: ' + f'{app.guesses}',
                    font = 'Arial 18 bold')

def drawElapsedTime(app, canvas):
    canvas.create_text(app.width*0.6, app.height*0.83,
                        text = 'Time: ' + f'{int(app.elapsedTime)}' + 's',
                        font = 'Arial 18 bold')

def drawMessage(app, canvas):
    upperPressed = ''
    start=(app.width/2) - (len(app.word)*(app.width/60))
    end=(app.width/2) + (len(app.word)*(app.width/60))
    if app.guesses == 0:
        canvas.create_text(app.width*0.5, app.height*0.92,
                    text = 'Guess a letter...', font = 'Arial 24 bold')
    elif app.found == len(app.word):
        canvas.create_text(app.width*0.5, app.height*0.92,
                text = 'You got it! (press the mouse to restart)',
                font = 'Arial 24 bold')
        canvas.create_rectangle(start-app.width/10,app.height*0.3,
                            end+app.width/10,app.height*0.46,
                    fill = 'light green',outline='black')
        canvas.create_text(app.width/2, app.height*0.375,
                    text = f'{(app.word).upper()}',
                    font = 'Nunito 40 bold')
    elif (app.pastKeys).count(app.pressedKey) >1:
        upperPressed = (app.pressedKey).upper()
        canvas.create_text(app.width*0.5, app.height*0.92,
                text = 'You already guessed '+upperPressed+'. Guess Again',
                font = 'Arial 24 bold')
    elif app.pressedKey.upper() not in app.alphabet:
        canvas.create_text(app.width*0.5, app.height*0.92,
                    text = f'{app.pressedKey}'+' is not a letter!', 
                    font = 'Arial 24 bold')
    elif app.pressedKey in app.word:
        canvas.create_text(app.width*0.5, app.height*0.92,
                    text = 'Good Job! Keep Guessing...',font = 'Arial 24 bold')
    elif app.pressedKey not in app.word:
        canvas.create_text(app.width*0.5, app.height*0.92,
                    text = 'Sorry... Guess Again', font = 'Arial 24 bold')
        

def redrawAll(app, canvas):
    draw(app, canvas)
    drawTitle(app, canvas)
    drawAlphabet(app, canvas)
    drawDisplayWord(app, canvas)
    drawColoredCircles(app, canvas)
    discoverWord(app, canvas)
    drawGuessCount(app, canvas)
    drawElapsedTime(app, canvas)
    drawMessage(app, canvas)

def main():
    cs112_s21_week4_linter.lint()
    runApp(width=600, height=400)


if __name__ == '__main__':
    main()