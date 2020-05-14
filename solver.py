# -*- coding: utf-8 -*-
"""
Created on Wed May  6 14:49:10 2020

@author: Nathan
"""
import random
from random import shuffle

import pygame, sys
from pygame.locals import *
from copy import copy, deepcopy

FPS = 10

WINDOWMULTIPLIER = 5
WINDOWSIZE = 81

WINDOWWIDTH = WINDOWSIZE * WINDOWMULTIPLIER
WINDOWHEIGHT = WINDOWSIZE * WINDOWMULTIPLIER

TOTALWIDTH = WINDOWWIDTH
TOTALHEIGHT = WINDOWHEIGHT + 60

SQUARESIZE = (WINDOWSIZE * WINDOWMULTIPLIER) // 3
CELLSIZE = SQUARESIZE // 3
NUMBERSIZE = CELLSIZE // 3

BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GREY = (200, 200, 200)
GREEN = (34, 130, 59)

numbers = [1,2,3,4,5,6,7,8,9]

def solver(grid):
    pos = (0, 0)

    result = find_empty(grid, pos)
    if not result[0]:
        return True, grid

    pos = result[1]

    for val in range(1, 10):
        if is_safe(grid, pos, val):
            grid[pos[0]][pos[1]] = val

            if (solver(grid)[0]):
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
    return not in_nonet(grid, (pos[0] - pos[0] % 3, pos[1] - pos[1] % 3), val) and not in_row(grid, pos[0],
                                                                                              val) and not in_col(grid,
                                                                                                                  pos[
                                                                                                                      1],
                                                                                                                  val)


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

def generate_puzzle():
    grid = None
    while grid is None:
        grid = make_board()

    counter = 0
    while counter <= 36:
        i = random.randint(0, 8)
        j = random.randint(0, 8)

        if grid[i][j] != 0:
            grid[i][j] = 0
            counter += 1

    return grid

def make_board():
    board = [[0 for _ in range(0, 9)] for _ in range(0, 9)]
    for i in range(0, 9):
        for j in range(0, 9):
            checking = numbers[:]
            random.shuffle(checking)
            x = -1
            while board[i][j] == 0:
                x += 1
                if x == 9:
                    return None
                checkMe = checking[x]
                if checkMe in board[i]:
                    continue
                checkis = False
                for checkRow in board:
                    if checkRow[j] == checkMe:
                        checkis = True
                if checkis:
                    continue
                if i % 3 == 1:
                    if j % 3 == 0 and checkMe in (board[i - 1][j + 1], board[i - 1][j + 2]):
                        continue
                    elif j % 3 == 1 and checkMe in (board[i - 1][j - 1], board[i - 1][j + 1]):
                        continue
                    elif j % 3 == 2 and checkMe in (board[i - 1][j - 1], board[i - 1][j - 2]):
                        continue
                elif i % 3 == 2:
                    if j % 3 == 0 and checkMe in (
                    board[i - 1][j + 1], board[i - 1][j + 2], board[i - 2][j + 1], board[i - 2][j + 2]):
                        continue
                    elif j % 3 == 1 and checkMe in (
                    board[i - 1][j - 1], board[i - 1][j + 1], board[i - 2][j - 1], board[i - 2][j + 1]):
                        continue
                    elif j % 3 == 2 and checkMe in (
                    board[i - 1][j - 1], board[i - 1][j - 2], board[i - 2][j - 1], board[i - 2][j - 2]):
                        continue
                board[i][j] = checkMe
    return board

def draw_grid():
    for x in range(0, WINDOWWIDTH, CELLSIZE):
        pygame.draw.line(DISPLAYSURF, GREY, (x, 0), (x, WINDOWHEIGHT))
    for y in range(0, WINDOWHEIGHT, CELLSIZE):
        pygame.draw.line(DISPLAYSURF, GREY, (0, y), (WINDOWWIDTH, y))

    for x in range(0, WINDOWWIDTH, SQUARESIZE):
        pygame.draw.line(DISPLAYSURF, BLACK, (x, 0), (x, WINDOWHEIGHT))
    for y in range(0, WINDOWHEIGHT + 1, SQUARESIZE):
        pygame.draw.line(DISPLAYSURF, BLACK, (0, y), (WINDOWWIDTH, y))

    return None

def initiate_cells(grid):
    currentGrid = {}
    for x in range(0, 9):
        for y in range(0, 9):
            currentGrid[x, y] = grid[x][y]
    return currentGrid

def clearCells(currentGrid):
    xFactor = 1
    yFactor = 1
    for item in currentGrid:  # item is x,y co-ordinate from 0 - 8
        clearCell((item[0] * CELLSIZE) + (xFactor * NUMBERSIZE),
                      (item[1] * CELLSIZE) + (yFactor * NUMBERSIZE))
    return None


def clearCell(x, y):
    cellSurf = BASICFONT.render(' ', True, BLACK)
    cellRect = cellSurf.get_rect()
    cellRect.topleft = (x, y)
    DISPLAYSURF.blit(cellSurf, cellRect)


def displayCells(currentGrid, color):
    # Create offset factors to display numbers in right location in cells.
    xFactor = 1
    yFactor = 1
    for item in currentGrid: # item is x,y co-ordinate from 0 - 8
        populateCells(currentGrid[item],(item[0]*CELLSIZE)+(xFactor*NUMBERSIZE),(item[1]*CELLSIZE)+(yFactor*NUMBERSIZE), color)
    return None


def populateCells(cellData, x, y, color):
    if cellData != 0:
        cellSurf = BASICFONT.render('%s' %(cellData), True, color)
        cellRect = cellSurf.get_rect()
        cellRect.topleft = (x, y)
        DISPLAYSURF.blit(cellSurf, cellRect)
    else:
        cellSurf = BASICFONT.render(' ', True, color)
        cellRect = cellSurf.get_rect()
        cellRect.topleft = (x, y)
        DISPLAYSURF.blit(cellSurf, cellRect)


def main():
    global FPSCLOCK, DISPLAYSURF
    pygame.init()
    FPSCLOCK = pygame.time.Clock()
    DISPLAYSURF = pygame.display.set_mode((TOTALWIDTH, TOTALHEIGHT))
    pygame.display.set_caption('Sudoku Solver')
    global BASICFONT, BASICFONTSIZE
    BASICFONTSIZE = 20
    BASICFONT = pygame.font.Font('freesansbold.ttf', BASICFONTSIZE)
    DISPLAYSURF.fill(WHITE)
    resetButton = pygame.Rect(0, WINDOWHEIGHT + 1, WINDOWWIDTH // 2, TOTALHEIGHT - WINDOWHEIGHT)
    startButton = pygame.Rect(resetButton.w, WINDOWHEIGHT+1, WINDOWWIDTH // 2 + 1, TOTALHEIGHT - WINDOWHEIGHT)

    resetSurf = BASICFONT.render("NEW PUZZLE", True, BLACK)
    resetRect = resetSurf.get_rect()
    resetRect.center = ((resetButton.x + resetButton.w // 2), (resetButton.y + resetButton.h // 2))

    startSurf = BASICFONT.render("START", True, WHITE)
    startRect = startSurf.get_rect()
    startRect.center = ((startButton.x + startButton.w // 2), (startButton.y + startButton.h // 2))

    GRID = generate_puzzle()

    grid = initiate_cells(GRID)
    displayCells(grid, BLACK)
    draw_grid()

    gridCopy = deepcopy(GRID)

    while True:
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = event.pos

                if resetButton.collidepoint(mouse_pos):
                    gridCopy = generate_puzzle()
                    grid = initiate_cells(gridCopy)
                    DISPLAYSURF.fill(WHITE)
                    draw_grid()
                    displayCells(grid, BLACK)


                elif startButton.collidepoint(mouse_pos):
                    result = solver(gridCopy)
                    if result[0]:
                        gridCopy = result[1]
                        grid = initiate_cells(gridCopy)
                        displayCells(grid, GREEN)

        pygame.draw.rect(DISPLAYSURF, BLACK, startButton)
        pygame.draw.rect(DISPLAYSURF, GREY, resetButton)
        DISPLAYSURF.blit(resetSurf, resetRect)
        DISPLAYSURF.blit(startSurf, startRect)

        pygame.display.update()
        FPSCLOCK.tick(FPS)


if __name__ == "__main__":
    main()
