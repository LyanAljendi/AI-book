import numpy as np
import time


class EmptyCell:
    """
    Class representing an empty cell, characterized by its position
    and its degree of freedom.
    """
    def __init__(self, board, line: int, col: int):
        """
        Initializes the emtpy cell
        @param board: the board on which the empty cell is
        @param line: the vertical position
        @param col: the horizontal position
        """
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
        @param other: another empty cell
        @return: true if they are, false otherwise
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
    """
    A buffer that is used to stock and access the emtpy cells
    in efficient time.
    """
    def __init__(self, board):
        self.size = 0       # the number of empty cells present in the bufer
        self.buffer = [[] for _ in range(9)] # the ith list contains the cells that have a dof of i+1
        self.board = board  # the matrix representing the board on which the empty cells are
        self.fill_buffer_from_board()

    def fill_buffer_from_board(self):
        """
        Puts all the empty cells of a board into the buffer
        """
        for line in range(9):
            for col in range(9):
                if self.board[line][col] == 0:
                    cell = EmptyCell(self.board, line, col)
                    self.push(cell)

    def push(self, empty_cell: EmptyCell):
        """
        Adds an empty cell to the buffer
        @param empty_cell: the pushed empty cell
        """
        self.buffer[empty_cell.dof - 1].append(empty_cell)
        self.size += 1

    def pop_heuristic1(self, min_dof: int):
        """
        Pops the cell that has the smallest degree of freedom
        @param min_dof: the minimum degree of freedom of a cell
        @return: the empty cell that has the min dof
        """
        if len(self.buffer[min_dof - 1]) > 0:
            self.size -= 1
            return self.buffer[min_dof-1].pop()
        return None

    def pop_heuristic2(self, min_dof: int, last_filled=None):
        """
        Pops the cell that has the smallest degree of freedom. In case
        of equality, privileges the cells that are on the same line /
        column / square than the last filled cell.
        @param min_dof: the minimum degree of a cell
        @param last_filled: the last filled empty cell
        @return: the cell that is popped
        """
        if len(self.buffer[min_dof - 1]) > 0:
            self.size -= 1
            for i in range(len(self.buffer[min_dof - 1])):
                if (last_filled is None) or (self.buffer[min_dof - 1][i].is_impacted(last_filled)):
                    return self.buffer[min_dof-1].pop(i)
            return self.buffer[min_dof - 1].pop()
        return None

    def update_all_DOFs(self, last_filled=None):
        """
        Updates all the degrees of freedoms of the cells on the same
        line / column / square than the last filled cell.
        @param last_filled: the last filled empty cell
        @return: the minimum degree of freedom of a cell after the update
        """
        updated = []
        min_dof = 9
        for dof in range(9):
            j = 0
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
        """
        @return: true if some cells have a DOF of 1, false otherwise
        """
        return len(self.buffer[0]) > 0

    def is_empty(self):
        """
        @return: true if there are no empty cells in the buffer, false otherwise
        """
        return self.size == 0


class OptimizedSearchSolver:
    """
    Main search algorithm to solve a Sudoku game 9x9
    """

    def __init__(self, game, start_time: float, use_improved_heuristic: bool):
        """
        Initializes the optimized search solver
        @param game: the game we are currently playing
        @param start_time: the time when we pressed space
        @param use_improved_heuristic: true if we want to privilege the cells impacted by the last filled cell
        """
        self.empty_cells = EmptyCellsBuffer(game.board)
        self.board = game.board
        self.game = game
        self.use_improved_heuristic = use_improved_heuristic
        self.start_time = start_time

    def visualSolve(self, wrong):
        """
        Solves the sudoku
        @return: true if it was successfully solved, false otherwise
        """
        # Checking that the game is not already over
        if self.empty_cells.is_empty():
            return True

        # Filling the cells that have a DOF of 1
        self.simplify_board()

        if self.backtrack_solve():
            self.display_board(wrong)
            return True
        else:
            return False

    def simplify_board(self):
        """
        Fills all the cells that have a degree of freedom of 1
        """
        min_dof = 1
        while min_dof == 1:
            # this loop checks if there are still DOFs of 1 after the update
            while True:
                # this loop fills all the DOFs of 1 without updating
                current_cell = self.empty_cells.pop_heuristic1(1)
                if current_cell is not None:
                    value = current_cell.get_possible_values()[0]
                    self.board[current_cell.line][current_cell.col] = value
                else:
                    break
            min_dof = self.empty_cells.update_all_DOFs()

    def backtrack_solve(self, last_filled: EmptyCell = None) -> bool:
        """
        Solves the sudoku by performing a DFS using a heuristic function
        @param last_filled: the last filled cell by the backtrack_solve function
        @return: true if the sudoku was successfully solved, false otherwise
        """
        # End condition : if there are no empty cells anymore, then the sudoku is solved
        if self.empty_cells.is_empty():
            return True
        # We make sure all the DOFs are up to date before choosing a cell
        min_dof = self.empty_cells.update_all_DOFs(last_filled)
        # Then we choose the cell that has the minimal DOF
        if self.use_improved_heuristic:
            current_cell = self.empty_cells.pop_heuristic2(min_dof, last_filled)
        else:
            current_cell = self.empty_cells.pop_heuristic1(min_dof)

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

    def display_board(self, wrong):
        """
        Displays the board after the solving is complete
        """
        for line in range(9):
            for col in range(9):
                if self.game.tiles[line][col].value == 0:
                    self.game.tiles[line][col].correct = True
                    self.game.tiles[line][col].correct = False
                self.game.tiles[line][col].value = self.game.board[line][col]
        self.game.redraw({}, wrong, time.time() - self.start_time)
