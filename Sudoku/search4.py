import numpy as np
# import sys
# import time
# import pygame
# from random import choice


class SearchSolver:
    """
    Main search algorithm to solve a Sudoku game 9x9
    """

    def __init__(self, game, startTime):
        self.empty_cells = EmptyCellsBuffer(game.board)
        self.board = game.board
        self.game = game

    def visualSolve(self, wrong):
        # Checking that the game is not already over
        if self.empty_cells.is_empty():
            return True

        # Filling the cells that have a DOF of 1
        self.simplify_board()

        # TODO check if we are not done
        if self.backtrack_solve():
            print(self.board)
            return True
        else:
            return False

    def simplify_board(self):
        min_dof = 1
        while min_dof == 1:
            # this loop checks if there are still DOFs of 1 after the update
            while True:
                # this loop fills all the DOFs of 1 without updating
                current_cell = self.empty_cells.pop(1)
                if current_cell is not None:
                    value = current_cell.get_possible_values()[0]
                    self.board[current_cell.line][current_cell.col] = value
                else:
                    break
            min_dof = self.empty_cells.update_all_DOFs()

    def backtrack_solve(self, last_filled=None):
        # End condition : if there are no empty cells anymore, then the sudoku is solved
        if self.empty_cells.is_empty():
            return True
        # We make sure all the DOFs are up to date before choosing a cell
        min_dof = self.empty_cells.update_all_DOFs(last_filled)
        # Then we choose the cell that has the minimal DOF
        current_cell = self.empty_cells.pop(min_dof, last_filled)

        # Trying to fill the cell :
        for value in current_cell.get_possible_values():
            self.board[current_cell.line][current_cell.col] = value
            was_solved = self.backtrack_solve(current_cell)
            if was_solved:
                return True
        # If we could not fill the cell, then we undo everything we did and warn our parent that the solving failed
        self.empty_cells.push(current_cell)
        self.board[current_cell.line][current_cell.col] = 0
        self.empty_cells.update_all_DOFs(current_cell)
        return False


class EmptyCell:
    def __init__(self, board, line, col):
        self.line = line
        self.col = col
        self.dof = 9    # degree of freedom, will be updated at the end of the init
        self.is_valid = np.array(
            [True, True, True, True, True, True, True, True, True])
        self.is_updated = False
        self.set_dof(board)

    def set_dof(self, board):
        """
        Computes the degree of freedom (dof) of an emtpy cell, i.e. the number of possible values
        it could possibly take
        """
        self.is_valid = np.array(
            [True, True, True, True, True, True, True, True, True])

        for i in range(9):
            # loop on the column
            if board[i][self.col] > 0:
                self.is_valid[board[i][self.col] - 1] = False

        for j in range(9):
            # loop on the line
            if board[self.line][j] > 0:
                self.is_valid[board[self.line][j] - 1] = False

        start_i = self.line - self.line % 3
        start_j = self.col - self.col % 3
        for i in range(start_i, start_i + 3):
            for j in range(start_j, start_j + 3):
                # loop on the square
                if board[i][j] > 0:
                    self.is_valid[board[i][j] - 1] = False

        self.dof = np.count_nonzero(self.is_valid)

    def get_possible_values(self):
        """
        Returns a list of all the values that the empty cell could possibly take
        """
        res = [i+1 for i, x in enumerate(self.is_valid) if x]
        return res

    def is_impacted(self, other):
        """
        checks if 2 cells are on the same line / col / square
        """
        res = (self.line == other.line) or (self.col == other.col) or (
            self.line // 3 == other.line // 3 and self.col // 3 == other.col // 3)
        return res

    def __lt__(self, other):
        return self.dof < other.dof

    def __eq__(self, other):
        return self.dof == other.dof

    def __repr__(self) -> str:
        return "(" + str(self.line) + ", " + str(self.col) + "   " + str(self.dof) + ")"

    def __str__(self) -> str:
        return "(" + str(self.line) + ", " + str(self.col) + "   " + str(self.dof) + ")"


class EmptyCellsBuffer:
    def __init__(self, board):
        self.size = 0
        self.buffer = [[] for _ in range(9)]
        self.board = board
        self.fill_buffer_from_board()

    def fill_buffer_from_board(self):
        for line in range(9):
            for col in range(9):
                if self.board[line][col] == 0:
                    cell = EmptyCell(self.board, line, col)
                    self.push(cell)

    def push(self, empty_cell):
        self.buffer[empty_cell.dof - 1].append(empty_cell)
        self.size += 1

    def pop(self, min_dof, last_filled=None):

        if len(self.buffer[min_dof - 1]) > 0:
            self.size -= 1
            for i in range(len(self.buffer[min_dof - 1])):
                if (last_filled is None) or (self.buffer[min_dof - 1][i].is_impacted(last_filled)):
                    return self.buffer[min_dof-1].pop(i)
            return self.buffer[min_dof-1].pop()
        return None

    def update_all_DOFs(self, last_filled=None):
        updated = []
        min_dof = 9
        #new_buffer = [[] for _ in range(9)]
        for dof in range(9):
            j = 0
            # for cell in self.buffer[dof]:
            while j != len(self.buffer[dof]):

                cell = self.buffer[dof][j]
                if (last_filled is None) or (cell.is_impacted(last_filled)):

                    cell.set_dof(self.board)
                    del self.buffer[dof][j]
                    j -= 1
                    updated.append(cell)
                if cell.dof < min_dof:
                    min_dof = cell.dof
                j += 1

        for cell in updated:
            self.buffer[cell.dof-1].append(cell)

        return min_dof

    def has_DOFs_of_1(self):
        return len(self.buffer[0]) > 0

    def is_empty(self):
        return self.size == 0
