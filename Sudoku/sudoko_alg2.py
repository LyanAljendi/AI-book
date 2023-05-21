def find_empty(board):
    """
    Finds an empty cell and returns its position as a tuple

    :param board: the board to search
    """
    for i in range(9):
        for j in range(9):
            if board[i][j] == 0:
                return i, j


def valid(board, pos, num):
    """
    Whether a number is valid in that cell, returns a bool

    :param board: the board to check
    :param pos: position of the cell to check
    :param num: the number to test at the position
    """
    for i in range(9):
        # make sure it isn't the same number we're checking for by comparing coords
        if board[i][pos[1]] == num and (i, pos[1]) != pos:
            return False

    for j in range(9):
        # Same row but not same number
        if board[pos[0]][j] == num and (pos[0], j) != pos:
            return False

    # ex. 5-5%3 = 3 and thats where the grid starts
    start_i = pos[0] - pos[0] % 3
    start_j = pos[1] - pos[1] % 3
    for i in range(3):
        for j in range(3):
            # adds i and j as needed to go from start of grid to where we need to be
            if (
                board[start_i + i][start_j + j] == num
                and (start_i + i, start_j + j) != pos
            ):
                return False
    return True


def solve(board):
    """
    Solves the Sudoku board via the backtracking algorithm

    :param board: the board to solve
    """
    empty = find_empty(board)
    if not empty:  # no empty spots are left so the board is solved
        # print_board(board)
        return True

    for nums in range(9):
        if valid(board, empty, nums + 1):
            board[empty[0]][empty[1]] = nums + 1

            if solve(board):  # recursive step
                return True
            # this number is wrong so we set it back to 0
            board[empty[0]][empty[1]] = 0
    return False
