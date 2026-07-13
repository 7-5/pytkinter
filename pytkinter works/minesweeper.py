from tkinter import *
import random
import time

# savegame
savefile=""

def readsave():
    file=open("minesweeper_savegame","r")
    global savefile
    savefile=eval(str(file.read()))

readsave()

def savegame():
    file=open("minesweeper_savegame","w")
    file.write(str(savefile))
    file.close()

boardsettings=[[9,16,30,savefile["customwidth"]],[9,16,16,savefile["customheight"]],[10,40,99,savefile["custommines"]]]
gwidth,gheight,gmine=boardsettings[0][savefile["difficulty"]],boardsettings[1][savefile["difficulty"]],boardsettings[2][savefile["difficulty"]]
firstclick=1

board = [[" " for __ in range(gwidth + 2)] for _ in range(gheight + 2)]

def boardmaker(boardx,boardy):
    global board
    global gwidth
    global gheight
    global gmine
    minesprocess=gmine
    processedtiles=gwidth*gheight-1
    for i in range(1,len(board)-1):
        for j in range(1,len(board[0])-1):
            if (i,j)!=(boardx+1,boardy+1):#problempoint-----------------------------------------------------------------
                if random.random()<minesprocess/max(1,processedtiles):
                    board[i][j]="x"
                    minesprocess-=1
                processedtiles-=1
    for i in range(1,len(board)-1):
        for j in range(1,len(board[0])-1):
            if board[i][j]!="x":
                c=0
                c+=int(board[i-1][j-1]=="x")
                c+=int(board[i-1][j]=="x")
                c+=int(board[i-1][j+1]=="x")
                c+=int(board[i][j-1]=="x")
                c+=int(board[i][j+1]=="x")
                c+=int(board[i+1][j-1]=="x")
                c+=int(board[i+1][j]=="x")
                c+=int(board[i+1][j+1]=="x")
                if c!=0:
                    board[i][j]=str(c)
    board=board[1:-1]
    board=[i[1:-1] for i in board]
    for i in board:
        print("".join(i))

def leftclick(event):
    global firstclick
    global board
    cell=event.widget
    info = cell.grid_info()
    if firstclick:
        firstclick=0
        boardmaker(info["row"],info["column"])
    cell.config(relief=FLAT,text=board[info["row"]][info["column"]])

    
def openspacearound():
    global board
    return

window=Tk()

window.title("Minesweeper")
icon=PhotoImage(file="minesweeper_mine.png")
window.iconphoto(True,icon)

gameframe=Frame(window,bg="#6fa615",relief=SUNKEN,bd=6)
gameframe.pack(side=TOP)
gametime=Label(window,text=0,)

for i in range(gheight):
    for j in range(gwidth):
        cell=Label(gameframe,text=" ",font=("Courier New",12),bg="#c0c0c0",relief=RAISED)
        cell.bind("<ButtonRelease-1>",leftclick)
        cell.grid(row=i,column=j)
window.mainloop()