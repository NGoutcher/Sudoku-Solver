# -*- coding: utf-8 -*-
"""
Created on Wed May  6 14:49:10 2020

@author: Nathan
"""

def solver(grid):
    pos = (0,0)
    
    result = find_empty(grid, pos)
    if not result[0]:
        return True, grid
    
    pos = result[1]
    
    for val in range(1,10):
        if is_safe(grid, pos, val):
            grid[pos[0]][pos[1]] = val
            
            if(solver(grid)[0]):
                return True, grid
            
            grid[pos[0]][pos[1]] = 0
            
    return False, None

def in_row(grid, row, val):
    for i in range(len(grid)):
        if grid[row][i] == val:
            return True
        
    return False

def in_col(grid, col, val):
    for i in range(len(grid)):
        if grid[i][col] == val:
            return True
        
    return False

def is_safe(grid, pos, val):
    return not in_nonet(grid, (pos[0] - pos[0]%3, pos[1] - pos[1]%3), val) and not in_row(grid, pos[0], val) and not in_col(grid, pos[1], val)

def find_empty(grid, pos):
    for row in range(len(grid)):
        for col in range(len(grid)):
            if grid[row][col] == 0:
                pos = row, col
                return True, pos
            
    return False, None

def in_nonet(grid, pos, val):
    for i in range(3):
        for j in range(3):
            if grid[i + pos[0]][j + pos[1]] == val:
                return True
            
    return False

def output_grid(grid):
    for row in range(len(grid)):
        print (grid[row])

if __name__=="__main__": 
      
    # creating a 2D array for the grid 
    grid=[[0 for x in range(9)]for y in range(9)] 
      
    # assigning values to the grid 
    grid=[[3,0,6,5,0,8,4,0,0], 
          [5,2,0,0,0,0,0,0,0], 
          [0,8,7,0,0,0,0,3,1], 
          [0,0,3,0,1,0,0,8,0], 
          [9,0,0,8,6,3,0,0,5], 
          [0,5,0,0,9,0,6,0,0], 
          [1,3,0,0,0,0,2,5,0], 
          [0,0,0,0,0,0,0,7,4], 
          [0,0,5,2,0,6,3,0,0]] 
    output_grid(grid)
    print("---------------------------")
    # if success print the grid
    result = solver(grid)
    if(result[0]): 
        output_grid(result[1]) 
    else: 
        print("No solution exists")