import sys
import time
import numpy as np
import pygame
from random import choice
from queue import PriorityQueue


class SearchSolver:
    """
    Main search algorithm to solve a Sudoku game 9x9
    """

    def __init__(self, game, startTime):
        self.empty_cells = self.get_all_empty_cells(game.board)
        self.board = game.board
        self.game = game

    '''def display_result(self):
        for i in range(9):
            for j in range(9):
                self.game.tiles[i][j].value = self.game.board[i][j]
                '''

    def get_all_empty_cells(self, board):

        res = PriorityQueue()

        for i in range(9):
            for j in range(9):
                if board[i][j] == 0:
                    cell = EmptyCell(board, i, j)
                    res.put(cell)
        # print(res)
        return res

    def update_all_DOFs(self, n, last_filled=None):
        new = PriorityQueue()
        # print("updating")
        # print(self.empty_cells.queue)
        if last_filled == None:
            # print(len(self.empty_cells.queue))
            for k in range(len(self.empty_cells.queue)):
                cell = self.empty_cells.queue[k]
                #print(cell, end=" ")
                cell.set_DOF(self.board)
                # if cell.i == 1 and cell.j == 5:
                # print("   ", "Warning : ")
                #print(cell, cell.DOF)
                new.put(cell)
            n = False
            self.empty_cells = new
            # print(cell)
        else:
            for k in range(len(self.empty_cells.queue)):
                cell = self.empty_cells.queue[k]
                if cell.is_impacted(last_filled):
                    cell.set_DOF(self.board)
                    # we can do something else here, just negate the value used before

    def visualSolve(self, wrong):
       # print(self.empty_cells.qsize())
        if self.empty_cells.empty():  # no empty spots are left so the board is solved
            # print_board(board)
            return True

        # fill the cells that have a DOF of 1
        # remove them from empty_cells (remember them)

        current_cell = self.empty_cells.get()
       # print("getting ", current_cell)
       # print(current_cell, " first cell ")

        # two while loops for after updating the DOFs,
        # in case we got new cells that have a DOFs of 1
        # searching for the new cells with DOFs of 1
       # print("before \n", self.board)

        while current_cell.DOF == 1:
            #print("New cells with DOF 1")
            # fill all cells with DOFs of 1 without updating
            # print( current_cell, current_cell.is_valid)
            while current_cell.DOF == 1:
               # print("more DOF 1 initially")

                value = current_cell.get_possible_values()[0]
                self.board[current_cell.i][current_cell.j] = value
                #print("filled value ", value)
                current_cell = self.empty_cells.get()
                #print("getting ", current_cell)

            #print("adding", current_cell)
            self.empty_cells.put(current_cell)
           # print(len(self.empty_cells.queue))
            # print(self.empty_cells.queue)
            # print(self.empty_cells.queue)
            self.update_all_DOFs(True)
            # print(self.empty_cells.queue)
            current_cell = self.empty_cells.get()
        # TODO check if we are not done
        # print(self.board)
        #print("no more changes in DOFs")
        self.empty_cells.put(current_cell)
        return self.backtrack_solve(1)
       # self.display_result()

    def backtrack_solve(self, i, level=0):

        if self.empty_cells.empty():  # no empty spots are left so the board is solved
            # print_board(board)
            return True
        # print("   " * level, "Board \n", self.board)
        # print("   " * level, "Empty cells : ", self.empty_cells.queue)
        self.update_all_DOFs(False)
        # if i == 1:
        #print("   ", "Last update : ")
        # print(self.empty_cells.queue)
        #i += 1

        current_cell = self.empty_cells.get()

        for value in current_cell.get_possible_values():
            self.board[current_cell.i][current_cell.j] = value
            was_solved = self.backtrack_solve(0, level + 1)
            if (was_solved):
                #print(current_cell.i, " , ", current_cell.j, " solved")
                return True
        self.empty_cells.put(current_cell)
        self.board[current_cell.i][current_cell.j] = 0
        # print("" * level, "Chosen cell: ", current_cell)
        # print("" * level, "Possible values : ",
        # current_cell.get_possible_values())
        return False


class EmptyCell:
    def __init__(self, board, i, j):
        self.i = i      # line
        self.j = j      # column
        self.DOF = 9    # degree of freedom, will be updated in set_DOF
        # will be updated in set_DOF
        self.is_valid = np.array(
            [True, True, True, True, True, True, True, True, True])
        self.set_DOF(board)

    def set_DOF(self, board):
        self.is_valid = np.array(
            [True, True, True, True, True, True, True, True, True])

        for i in range(9):
            # loop on the column
            if board[i][self.j] > 0:
                self.is_valid[board[i][self.j] - 1] = False

        for j in range(9):
            # loop on the line
            if board[self.i][j] > 0:
                self.is_valid[board[self.i][j] - 1] = False

        start_i = self.i - self.i % 3
        start_j = self.j - self.j % 3
        for i in range(start_i, start_i + 3):
            for j in range(start_j, start_j + 3):
                # loop on the square
                if board[i][j] > 0:
                    self.is_valid[board[i][j] - 1] = False

        self.DOF = np.count_nonzero(self.is_valid)

    def is_impacted(self, other):
        # checks if 2 cells are on the same line / col / square
        return ((self.i == other.i) or (self.j == other.j) or (self.i // 3 == other.i // 3 and self.j // 3 == other.j // 3))

    def __lt__(self, other):
        return self.DOF < other.DOF

    def __eq__(self, other):
        return self.DOF == other.DOF
    # getting the indicies of the boolean variables array

    def __repr__(self) -> str:
        return "(" + str(self.i) + ", " + str(self.j) + "   " + str(self.DOF) + ")"

    def __str__(self) -> str:
        return "(" + str(self.i) + ", " + str(self.j) + "   " + str(self.DOF) + ")"

    def get_possible_values(self):
        res = [i+1 for i, x in enumerate(self.is_valid) if x]
        return res
