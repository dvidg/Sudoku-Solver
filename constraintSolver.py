import numpy as np
import copy
  
sudoku = np.array([ #sudoku grid is a numpy 2D array
    [8, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 3, 6, 0, 0, 0, 0, 0],
    [0, 7, 0, 0, 9, 0, 2, 0, 0],
    [0, 5, 0, 0, 0, 7, 0, 0, 0],
    [0, 0, 0, 0, 4, 5, 7, 0, 0],
    [0, 0, 0, 1, 0, 0, 0, 3, 0],
    [0, 0, 1, 0, 0, 0, 0, 6, 8],
    [0, 0, 8, 5, 0, 0, 0, 1, 0],
    [0, 9, 0, 0, 0, 0, 4, 0, 0],
], np.int32)


print("Input Grid")
print(sudoku)

#Forming a list of all cell IDs (A1 being the top left) ['A1', 'A2', 'A3'....'I8', 'I9'] as an array
digits   = '123456789'
rows     = 'ABCDEFGHI'
columns     = '123456789'
squareID = []
for x in rows:
    for y in digits:
        squareID.append(x + y) #combing a letter (rows: A, B, C...) and a number (cols: 1, 2, 3)


#I could not be bothered programming a rule for creating boxes (a sudoku grid is 9 boxes of 9 numbers)
boxes = [['A1', 'A2', 'A3', 'B1', 'B2', 'B3', 'C1', 'C2', 'C3'],
         ['A4', 'A5', 'A6', 'B4', 'B5', 'B6', 'C4', 'C5', 'C6'],
         ['A7', 'A8', 'A9', 'B7', 'B8', 'B9', 'C7', 'C8', 'C9'],
         ['D1', 'D2', 'D3', 'E1', 'E2', 'E3', 'F1', 'F2', 'F3'],
         ['D4', 'D5', 'D6', 'E4', 'E5', 'E6', 'F4', 'F5', 'F6'],
         ['D7', 'D8', 'D9', 'E7', 'E8', 'E9', 'F7', 'F8', 'F9'],
         ['G1', 'G2', 'G3', 'H1', 'H2', 'H3', 'I1', 'I2', 'I3'],
         ['G4', 'G5', 'G6', 'H4', 'H5', 'H6', 'I4', 'I5', 'I6'],
         ['G7', 'G8', 'G9', 'H7', 'H8', 'H9', 'I7', 'I8', 'I9']]


b = [int(x) for x in (sudoku.ravel())] #flattens the 2D numpy array into a 1D list
grid = dict(zip(squareID,b)) #makes a dictionary: {'A1': 0, 'A2': 0, 'A3': 4,...'I9': 3}

def getRow(cell, inputGrid): #function to scan across rows given a cell and the current grid
    row = cell[0] #cell 'A1' is row A
    rowList = []
    for x in range(9): #make a list of numbers in this row
        thisNum = inputGrid[row + str(x+1)]
        if(thisNum in rowList and thisNum != 0):
            return [-1] #if this number is already in this row: return -1 (eg row has two 5s - impossible)
        else:
            rowList.append(thisNum)
    return rowList
    
def getCol(cell, inputGrid): #function to scan across columns
    col = cell[1] #cell 'A1' is column A
    colList = []
    for x in range(9): #make a list of numbers in this column
        thisNum = inputGrid[rows[x] + str(col)]
        if(thisNum in colList and thisNum != 0):
            return [-1]
        else:
            colList.append(thisNum)
    return colList

def getBox(cell, inputGrid): #function to scan across the boxes
    thisBox = []
    boxList = []
    for x in range(9): #scan across boxes array: if cell is found, this is out box
        for y in range(9):
            if(boxes[x][y] == cell):
                boxIndex = x
                break
                break

    for x in range(9):
        thisBox.append(boxes[boxIndex][x])
        thisNum = inputGrid[thisBox[x]]
        if (thisNum in boxList and thisNum != 0):
            return [-1]
        else:
            boxList.append(thisNum)
    return boxList

def fixGrid(inputGrid,inputCell,inputNum):
    grid[inputCell] = inputNum

def firstCheck(thisGrid):
    localDict = {}
    for cell in squareID:
        possNums = []
        if thisGrid[cell] == 0: #skip cells already filled
            notList = set(getBox(cell, thisGrid) + getCol(cell, thisGrid) + getRow(cell, thisGrid)) #numbers in row/col/box
            if(-1 in notList): #exit if find inconsistency
                return -1
            else:
                for x in range(9):
                    if x + 1 in notList:
                        continue
                    else:
                        possNums.append(x + 1) #append numbers not in row/col/box
                if(len(possNums) == 1): #if length1: only 1 number -> fix to grid
                    fixGrid(thisGrid,cell,possNums[0])
                else:
                    localDict[cell] = possNums
                continue
        else:
            continue
    return localDict    


def failGrid(inputGrid):
    for cell in squareID:
        inputGrid[cell] = -1    

def checkGrid(inputGrid):
    for cell in squareID:
        if inputGrid[cell]==0:
            return False
    return True

def mainAlgorithm(inputDict, inputGrid):
    for cell in squareID:
        if(inputGrid[cell] == 0):
            for value in inputDict[cell]:
                if(value not in set(getBox(cell, inputGrid) + getCol(cell, inputGrid) + getRow(cell, inputGrid))):
                    inputGrid[cell] = value
                    if(checkGrid(inputGrid)):        
                        return True
                    else:
                        if mainAlgorithm(inputDict, inputGrid):
                            return True
            break
    inputGrid[cell]=0


possDict = firstCheck(grid)
if(possDict == -1):
    failGrid(grid) #fill grid with -1 if unsolvable
    print("Grid unsolvable!")
else:
    if(not mainAlgorithm(possDict, grid)):
        failGrid(grid)
        print("Grid unsolvable!")
    else:
        solved_sudoku = [[]]
        solved_vals = list(grid.values())
        solved_sudoku = np.array(solved_vals).reshape(9,9)
        print("Solved grid")
        print(solved_sudoku)   