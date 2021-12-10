import numpy as np
import random
from scipy import ndimage, misc
import copy
import time
from deap import base
from deap import creator
from deap import tools
import game


def f10(newstate, currentstate):

    f1, f2, f3, f4, f5, f6, f7, f8, f9 = 0, 0, 0, 0, 0, 0, 0, 0, 0
    ###
    flatstate = newstate.flatten()
    ###
    maxval= max(flatstate)
    ###
    secondmaxval = max(np.where(flatstate == maxval, 1, flatstate)) 
    secondmaxval = secondmaxval if secondmaxval != 1 else 0
    ###
    thirdmaxval = max(np.where(flatstate == secondmaxval, 1, flatstate)) 
    thirdmaxval = thirdmaxval if thirdmaxval != 1 else 0
    ###
    maxvalues = [maxval, secondmaxval, thirdmaxval]
    ###
    f5cells = [[0,0],[0,3],[1,1],[2,2],[3,0]]
    f6cells = [[2,3],[3,2],[0,1],[0,2],[1,1],[2,0],[1,3],[3,1]]
    ###
    newstateT = newstate.T

    highestValuesIndeces = [0,0]
    for nrow in range(4):

        for ncolumn in range(4):
            val = newstate[nrow,ncolumn]

            if val != 0: f4 += 1  
            if  val == maxval and (nrow,ncolumn) in [(0,0), (0,3), (3,3), (3,0)]: f1 = 1

            if val == secondmaxval: highestValuesIndeces[1] = [nrow,ncolumn]
            if val == maxval: highestValuesIndeces[0] = [nrow,ncolumn]

            if currentstate[nrow,ncolumn] != val: f3 += 1
            if val == maxval:
                # Check above
                if ncolumn-1 >= 0: 
                    nearbyvalue = newstate[nrow,ncolumn-1]
                    if nearbyvalue in maxvalues: f2 = 1
                    if nearbyvalue == val and [nrow, ncolumn] in f5cells: f5 += 1
                    if nearbyvalue == val and [nrow, ncolumn] in f6cells: f6 += 1

                # Check right
                if nrow+1 <= 3:
                    nearbyvalue = newstate[nrow+1,ncolumn]
                    if nearbyvalue in maxvalues: f2 = 1
                    if nearbyvalue == val and [nrow, ncolumn] in f5cells: f5 += 1
                    if nearbyvalue == val and [nrow, ncolumn] in f6cells: f6 += 1
                # Check below
                if ncolumn+1 <= 3:
                    nearbyvalue = newstate[nrow,ncolumn+1] 
                    if nearbyvalue in maxvalues: f2 = 1
                    if nearbyvalue == val and [nrow, ncolumn] in f5cells: f5 += 1
                    if nearbyvalue == val and [nrow, ncolumn] in f6cells: f6 += 1
                # Check left
                if nrow-1 >= 0:
                    nearbyvalue = newstate[nrow-1,ncolumn]
                    if nearbyvalue in maxvalues: f2 = 1
                    if nearbyvalue == val and [nrow, ncolumn] in f5cells: f5 += 1
                    if nearbyvalue == val and [nrow, ncolumn] in f6cells: f6 += 1
    

    # If the highest and second highest value is along the row
    if highestValuesIndeces[0][0] == highestValuesIndeces[1][0] and highestValuesIndeces[0][1] != highestValuesIndeces[1][1]:
        row = newstate[highestValuesIndeces[0][0]]
        if 0 not in newstate: f7 = 1
        if np.array_equiv(np.sort(row), row) or np.array_equiv(np.sort(row)[::-1], row): f8 = 1
        f9 = sum([1 for elem in row if elem != 0])/f4

    # If the highest and second highest value is along the column
    elif highestValuesIndeces[0][1] == highestValuesIndeces[1][1] and highestValuesIndeces[0][0] != highestValuesIndeces[1][0]:
        column = newstate[highestValuesIndeces[0][1]]
        if 0 not in newstateT: f7 = 1
        if np.array_equiv(np.sort(column), column) or np.array_equiv(np.sort(column)[::-1], column): f8 = 1
        f9 = sum([1 for elem in column if elem != 0])/f4
        
    else:
        f8 = 0
        f7 = 0

    return f1,f2,f3,f4,f5,f6,f7,f8,f9


# The state evaluation function
def stateEvaluation(w, currentstate, state):
    f1,f2,f3,f4,f5,f6,f7,f8,f9 = f10(state, currentstate)
    E = w[0]*f1 + w[1]*f2 + w[2]*f3 + w[3]*f4 + w[4]*f5 + w[5]*f6 + w[6]*f7 + w[7]*f8 + w[8]*f9
    return E



weights = [0.8870351642886638, 1.0, 4.384887169951358, 1.0, 1.0, 3.693619065991971e-06, 0.6856477241443923, -0.16700189754028072, 1.0]
moves = [0,1,2,3]

g = game.Game(True)

# Play game for 2000 moves
happy = True
while happy:
    statesEvaluation = []

    # Evaluate all possible moves (projections)
    for move in moves:
        state = g.project(move)
        if np.array_equal(state, g.grid): E = 0
        else: E = stateEvaluation(weights, g.grid, state)
        statesEvaluation.append(E)
            
        # Choose the best possible move with maximum E
        chosenMove = moves[np.argmax(statesEvaluation)]
        print(g.grid)

        try: g.move(chosenMove)
        except: 
            happy = False
            print("Game Over!")
            print("Score:", g.score)
            break
