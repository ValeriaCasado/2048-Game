import numpy as np
from scipy import ndimage, misc

class Game:
    def __init__(self, print_game=None):
        self.grid = np.zeros((4,4), dtype=np.int64)
        if print_game == None:
            self.p = False
        else: self.p = print_game
        self.addrandom(2)

        # print options
        if self.p==True: print(self.grid)

    def addrandom(self, k):
        # Find all empty indeces  
        emptyIndeces  = [i for i, val in enumerate(self.grid.flatten()) if val == 0]

        # Call game over
        if len(emptyIndeces) == 0:
            raise Exception("= = = GAME OVER = = =" )
        
        for _ in range(k):
            # Draw index from empty indeces
            index = np.random.choice(emptyIndeces)
            i, j = int(index/4), index-int(index/4)*4
            # Add number on that index
            self.grid[i,j] = 2

    def move(self, direction):
        # 0 = down
        # 1 = up
        # 2 = left
        # 3 = right
        if direction==0: temp_grid = self.grid
        if direction==1: temp_grid = self.grid[::-1]
        if direction==2: temp_grid = ndimage.rotate(self.grid,90)
        if direction==3: temp_grid = ndimage.rotate(self.grid,-90)

        for i in range(4):
            temp_grid[:,i] = self.merge(temp_grid[:,i])

        if direction==0: self.grid = temp_grid
        if direction==1: self.grid = self.grid[::-1]
        if direction==2: self.grid = ndimage.rotate(temp_grid,-90)
        if direction==3: self.grid = ndimage.rotate(temp_grid, 90)

        # Add new value
        self.addrandom(1)

        # print options
        if self.p==True: print(self.grid)


    def merge(self, column):
        tracker = [False]*len(column)
        column = column[::-1]
        for i in range(1,4):
            for j in range(i-1,-1,-1):
                if column[j]==column[j+1] and column[j]!=0 and tracker[j]==False and tracker[j+1]==False:
                    column[j]+=column[j]
                    column[j+1]=0
                    tracker[j]=True
                if column[j]==0 and column[j+1]!= 0:
                    column[j]=column[j+1]
                    column[j+1]=0
                    tracker[j+1] = False
                    tracker[j] = tracker[j+1]

        return column[::-1]