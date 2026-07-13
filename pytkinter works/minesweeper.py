from tkinter import *
import random
import time
import sys

sys.setrecursionlimit(50000)

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
    global firstclick, board, gwidth, gheight
    if hasattr(event, "widget"):
        cell = event.widget
    else:
        cell = event
    if cell.cget("text")=="F":
        return
    if (cell.cget("relief")==FLAT):
        return
    r,c=cell.grid_info()["row"],cell.grid_info()["column"]
    if firstclick and cell.cget("text")!="F":
        firstclick=0
        boardmaker(r,c)
    cell.config(relief=FLAT,text=board[r][c]) # point where its opened
    cellval=cell.cget("text")
    if cellval not in "xF ":
        colorations=["black","#0000ff","#008000","#ff0000","#000080","#800000","#008080","#000000","#808080","#c0cfb0"]
        cell.config(fg=colorations[int(cellval)])
    if (cellval==" "):
        if r!=0 and c!=0:
           if label_matrix[r-1][c-1].cget("relief")!=FLAT and label_matrix[r-1][c-1].cget("text")!="F":
                leftclick(label_matrix[r-1][c-1])
        if c!=gwidth-1:
            if label_matrix[r][c+1].cget("relief")!=FLAT and label_matrix[r][c+1].cget("text")!="F":
                leftclick(label_matrix[r][c+1])
        if r!=gheight-1 and c!=0:
            if label_matrix[r+1][c-1].cget("relief")!=FLAT and label_matrix[r+1][c-1].cget("text")!="F":
                leftclick(label_matrix[r+1][c-1])        
        if r!=0:
            if label_matrix[r-1][c].cget("relief")!=FLAT and label_matrix[r-1][c].cget("text")!="F":
                leftclick(label_matrix[r-1][c])
        if r!=gheight-1 and c!=gwidth-1:
            if label_matrix[r+1][c+1].cget("relief")!=FLAT and label_matrix[r+1][c+1].cget("text")!="F":
                leftclick(label_matrix[r+1][c+1])        
        if c!=0:
            if label_matrix[r][c-1].cget("relief")!=FLAT and label_matrix[r][c-1].cget("text")!="F":
                leftclick(label_matrix[r][c-1])
        if r!=0 and c!=gwidth-1:
            if label_matrix[r-1][c+1].cget("relief")!=FLAT and label_matrix[r-1][c+1].cget("text")!="F":
                leftclick(label_matrix[r-1][c+1])        
        if r!=gheight-1:
            if label_matrix[r+1][c].cget("relief")!=FLAT and label_matrix[r+1][c].cget("text")!="F":
                leftclick(label_matrix[r+1][c])        




def rightclick(event):
    global firstclick
    global board
    global gwidth
    global gheight
    cell=event.widget
    info = cell.grid_info()
    if cell.cget("relief")!=FLAT:
        if cell.cget("text")!="F":
            cell.config(text="F",fg="#ff0000")
        else:
            cell.config(text=" ",fg="#ff0000")


window=Tk()

window.title("Minesweeper")
icon=PhotoImage(file="minesweeper_mine.png")
window.iconphoto(True,icon)

gameframe=Frame(window,bg="#c0c0c0",relief=SUNKEN,bd=6)
gameframe.pack(side=TOP)
gametime=Label(window,text=0,)

label_matrix = [[None for _ in range(gwidth)] for _ in range(gheight)]

for i in range(gheight):
    for j in range(gwidth):
        cell=Label(gameframe,padx=6,text=" ",font=("Courier New",13,"bold"),bd=4,bg="#c0c0c0",relief=RAISED)
        cell.bind("<ButtonRelease-1>",leftclick)
        cell.bind("<ButtonRelease-3>",rightclick)
        cell.grid(row=i,column=j)
        label_matrix[i][j] = cell
window.mainloop()