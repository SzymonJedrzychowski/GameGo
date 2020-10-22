from os import system, name
from copy import deepcopy
import tkinter as tk

##############################
global size
size = 11

width = 400/(size-1)
print(width)


inboard = []

def clear(): 
    if name == 'nt': 
        _ = system('cls')  
    else: 
        _ = system('clear')

def createBoard():
    board = []
    for _ in range(size*size):
        inboard.append(None)
        board.append(0)
    return board

def printBoard(board):
    d = ["_", "o", "x"]
    for i in range(size*size):
        if i%size == size-1:
            print(d[board[i]])
        else:
            print(d[board[i]], end = " ")

def playStone(board, player, place, previousBoard):
    
    if board[place] == 0:
        nearStones = [place]
        checkedStones = []
        while True:
            if len(nearStones) > 0:
                stone = nearStones[0]
                nearStones.pop(0)
            else:
                if canKill(board, player, place):
                    if board == previousBoard[1]:
                        return False
                    return True
                else:
                    board[place] = 0
                    return False
            ans = getNeighbours(board, player, stone, nearStones, checkedStones)
            if len(ans) == 1:
                canKill(board, player, place)
                return True
            else:
                nearStones = ans[0]
                checkedStones = ans[1]
        
    else:
        return False

def getNeighbours(board, player, place, nearStones, checkedStones):
    if place > size-1 and checkedStones.count(place-size) == 0:
        if board[place-size] == player:
            nearStones.append(place-size)
        elif board[place-size] == 0:
            return [True]
    if place%size != size-1 and checkedStones.count(place+1) == 0:
        if board[place+1] == player:
            nearStones.append(place+1)
        elif board[place+1] == 0:
            return [True]
    if place < (size-1)*size and checkedStones.count(place+size) == 0:
        if board[place+size] == player:
            nearStones.append(place+size)
        elif board[place+size] == 0:
            return [True]
    if place%size != 0 and checkedStones.count(place-1) == 0:
        if board[place-1] == player:
            nearStones.append(place-1)
        elif board[place-1] == 0:
            return [True]
    checkedStones.append(place)
    return [nearStones, checkedStones]

def getOposites(board, player, place, nearStones, checkedStones):
    if place > size-1 and checkedStones.count(place-size) == 0:
        if board[place-size] == player:
            nearStones.append(place-size)
    if place%size != size-1 and checkedStones.count(place+1) == 0:
        if board[place+1] == player:
            nearStones.append(place+1)
    if place < (size-1)*size and checkedStones.count(place+size) == 0:
        if board[place+size] == player:
            nearStones.append(place+size)
    if place%size != 0 and checkedStones.count(place-1) == 0:
        if board[place-1] == player:
            nearStones.append(place-1)
    checkedStones.append(place)
    return [nearStones, checkedStones]

def canKill(board, player, place):
    board[place] = player
    allNearStones = getOposites(board, -player, place, [], [])[0]
    nearStones = []
    checkedStones = []
    safeStones = []
    unsafeStones = []
    toBreak = False
    while True:
        if len(nearStones) > 0:
            stone = nearStones[0]
            nearStones.pop(0)
        else:
            while True:
                if len(allNearStones) > 0:
                    stone = allNearStones[0]
                    allNearStones.pop(0)
                    if (safeStones+unsafeStones).count(stone) == 0:
                        break
                else:
                    toBreak = True
                    break    
            if toBreak:
                if len(unsafeStones) > 0:
                    for i in unsafeStones:
                        board[i] = 0
                    return True
                else:
                    return False 
        ans = getNeighbours(board, -player, stone, nearStones, checkedStones)
        if len(ans) == 1:
            safeStones += checkedStones
            checkedStones = []
            nearStones = []
        else:
            nearStones = ans[0]
            checkedStones = ans[1]
            if len(nearStones) == 0:
                unsafeStones += checkedStones
                checkedStones = []


board = createBoard()
previousBoard = [0, 0]
currentPlayer = -1
pas = [None, False, False]
end = [False, None, None]

def getorigin(eventorigin):
    global x0,y0, inboard, board, previousBoard, currentPlayer, turn, pas, end
    x0 = eventorigin.x
    y0 = eventorigin.y
    if end[0] == True and x0 >= 50 and x0 <= 550 and y0 >= 50 and y0 <= 550:
        end[0] = False
        canvas.delete(end[1])
        canvas.delete(end[2])
        end[1] = None
        end[2] = None
        pas[1] = False
        pas[2] = False
        for i in inboard:
            if i!= None:
                canvas.delete(i)
        inboard = []
        board = createBoard()
        previousBoard = [0, 0]
        currentPlayer = 1
        #score = [None, 0, 0]
        #canvas.itemconfig(scorein[1], text = '0')
        #canvas.itemconfig(scorein[2], text = '0')
        canvas.itemconfig(turn[0], fill = 'white')
        canvas.itemconfig(turn[1], fill = 'gray60')
        pas = [None, False, False]
    elif x0 >= 50 and x0 <= 550 and y0 >= 50 and y0 <= 550:
        distance = []
        for i in range(size*size):
            distance.append((x0-((i%size)*width+100))**2 + (y0-((i//size)*width+100))**2 <= (.4*width)**2)
        try:
            new_stone = distance.index(True)
            if playStone(board, currentPlayer, int(new_stone), previousBoard):
                previousBoard[1] = deepcopy(previousBoard[0])
                previousBoard[0] = deepcopy(board)
                pas[currentPlayer] = False
                if currentPlayer == 1:
                    canvas.itemconfig(turn[0], fill = 'gray60')
                    canvas.itemconfig(turn[1], fill = 'black')
                    inboard[new_stone] = canvas.create_oval((new_stone%size)*(width)+(100-.4*width), (new_stone//size)*(width)+(100-.4*width), (new_stone%size)*(width)+(100+.4*width), (new_stone//size)*(width)+(100+.4*width), fil = 'white', outline = 'black')
                else:
                    canvas.itemconfig(turn[0], fill = 'white')
                    canvas.itemconfig(turn[1], fill = 'gray60')
                    inboard[new_stone] = canvas.create_oval((new_stone%size)*(width)+(100-.4*width), (new_stone//size)*(width)+(100-.4*width), (new_stone%size)*(width)+(100+.4*width), (new_stone//size)*(width)+(100+.4*width), fil = 'black', outline = 'black')
                distance = []
                if board != inboard:
                    for i in range(len(board)):
                        if board[i] == 0 and inboard[i] != None:
                            #score[currentPlayer] += 1
                            canvas.delete(inboard[i])
                            inboard[i] = None
                    #canvas.itemconfig(scorein[currentPlayer], text = str(score[currentPlayer]))
                currentPlayer = -currentPlayer
            else:
                board = deepcopy(previousBoard[0])
        except:
            pass
    elif x0 >= 220 and x0 <= 380 and y0 >= 600 and y0 <= 650:
        for i in inboard:
            if i!= None:
                canvas.delete(i)
        inboard = []
        board = createBoard()
        previousBoard = [0, 0]
        currentPlayer = -1
        #score = [None, 0, 0]
        #canvas.itemconfig(scorein[1], text = '0')
        #canvas.itemconfig(scorein[2], text = '0')
        canvas.itemconfig(turn[0], fill = 'gray60')
        canvas.itemconfig(turn[1], fill = 'white')
        pas = [None, False, False]
    elif (x0-75)**2 + (y0-625)**2 <= 1600 and currentPlayer == 1:
        currentPlayer = -1
        pas[1] = True
        canvas.itemconfig(turn[0], fill = 'gray60')
        canvas.itemconfig(turn[1], fill = 'black')
    elif (x0-525)**2 + (y0-625)**2 <= 1600 and currentPlayer == -1:
        currentPlayer = 1
        pas[2] = True
        canvas.itemconfig(turn[0], fill = 'white')
        canvas.itemconfig(turn[1], fill = 'gray60')
    if pas[1] + pas[2] == 2:
        end[0] = True
        end[1] = canvas.create_rectangle(120, 250, 480, 450, fill = 'white', outline = 'black')
        end[2] = canvas.create_text(300, 350, font= ('none', 24), text = 'Score: ')

        #TUTAJ BEDZIE LICZENIE


root = tk.Tk()
root.title("Go")

canvas = tk.Canvas(root, width=600, height=700)
canvas.bind("<Button 1>", getorigin)


canvas.create_rectangle(50, 50, 550, 550, fil = 'tan1', outline = 'black')
for i in range(size):
    canvas.create_rectangle(100, 100+i*width, 500, 100+i*width, fil = 'tan3', outline = 'black')

for i in range(size):
    canvas.create_line(100+width*i, 100, 100+width*i, 500)

canvas.create_rectangle(25, 575, 575, 675, fill = 'tan1', outline = 'black')

turn = []
turn.append(canvas.create_oval(35, 585, 115, 665, fill = 'gray60', outline = 'black'))
turn.append(canvas.create_oval(485, 585, 565, 665, fill = 'black', outline = 'black'))

canvas.create_rectangle(220, 600, 380, 650, fill = 'red4', outline = 'black')
canvas.create_text(300, 625, font = ('none', 26), text = 'Reset')

#score = [None, 0, 0]

#scorein = [None]
#scorein.append(canvas.create_text(167, 625, font = ('none', 26), text = '0'))
#scorein.append(canvas.create_text(433, 625, font = ('none', 26), text = '0'))

canvas.pack()
root.mainloop()