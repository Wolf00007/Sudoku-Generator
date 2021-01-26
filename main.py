import copy
import operator
import random
from random import randint, shuffle
import timeit
import numpy as np

grid = [[0 for x in range(9)] for y in range(9)]
numberList = [1, 2, 3, 4, 5, 6, 7, 8, 9]

# below are custom grids found online, one of the most difficult ones
# to use them, the section in rows 446 to 489 has to be commented out and the line in 491 has to be active
# then, you have to enter the chosen grid name in the copy.deepcopy(name) in lines 494-497
# do the same (replace "grid" with the chosen "name") in lines 501, 502 and likewise for other algorithms

puzzle21 = [[8, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 3, 6, 0, 0, 0, 0, 0],
            [0, 7, 0, 0, 9, 0, 2, 0, 0],
            [0, 5, 0, 0, 0, 7, 0, 0, 0],
            [0, 0, 0, 0, 4, 5, 7, 0, 0],
            [0, 0, 0, 1, 0, 0, 0, 3, 0],
            [0, 0, 1, 0, 0, 0, 0, 6, 8],
            [0, 0, 8, 5, 0, 0, 0, 1, 0],
            [0, 9, 0, 0, 0, 0, 4, 0, 0]
            ]

puzzle17_1 = [[0, 0, 0, 0, 0, 0, 0, 0, 0],
              [0, 0, 0, 0, 0, 3, 0, 8, 5],
              [0, 0, 1, 0, 2, 0, 0, 0, 0],
              [0, 0, 0, 5, 0, 7, 0, 0, 0],
              [0, 0, 4, 0, 0, 0, 1, 0, 0],
              [0, 9, 0, 0, 0, 0, 0, 0, 0],
              [5, 0, 0, 0, 0, 0, 0, 7, 3],
              [0, 0, 2, 0, 1, 0, 0, 0, 0],
              [0, 0, 0, 0, 4, 0, 0, 0, 9]
              ]

puzzle17_2 = [[0, 0, 0, 0, 4, 0, 0, 0, 0],
              [1, 2, 0, 0, 0, 0, 0, 7, 3],
              [0, 3, 0, 0, 0, 8, 0, 0, 0],
              [0, 0, 4, 0, 0, 0, 6, 0, 0],
              [0, 0, 0, 2, 0, 3, 0, 0, 0],
              [0, 0, 5, 0, 0, 0, 0, 0, 0],
              [0, 0, 6, 0, 9, 0, 5, 0, 0],
              [0, 7, 0, 0, 0, 0, 0, 2, 0],
              [0, 0, 0, 0, 0, 0, 0, 0, 0]
              ]

puzzle18_1 = [[0, 0, 0, 0, 0, 0, 0, 0, 0],
              [1, 2, 0, 0, 0, 0, 0, 8, 4],
              [0, 3, 0, 0, 0, 0, 0, 7, 0],
              [0, 0, 4, 0, 0, 0, 6, 0, 0],
              [0, 0, 0, 2, 0, 3, 0, 0, 0],
              [0, 0, 5, 0, 0, 0, 9, 0, 0],
              [0, 0, 6, 0, 9, 0, 5, 0, 0],
              [0, 7, 0, 0, 0, 0, 0, 2, 0],
              [0, 0, 0, 0, 5, 0, 0, 0, 0]
              ]

puzzle17_3 = [[0, 0, 0, 0, 0, 0, 0, 0, 1],
              [0, 0, 0, 0, 0, 0, 0, 2, 3],
              [0, 0, 4, 0, 0, 5, 0, 0, 0],
              [0, 0, 0, 1, 0, 0, 0, 0, 0],
              [0, 0, 0, 0, 3, 0, 6, 0, 0],
              [0, 0, 7, 0, 0, 0, 5, 8, 0],
              [0, 0, 0, 0, 6, 7, 0, 0, 0],
              [0, 1, 0, 0, 0, 4, 0, 0, 0],
              [5, 2, 0, 0, 0, 0, 0, 0, 0]
              ]

puzzle18_2 = [[0, 0, 0, 2, 1, 0, 0, 0, 0],
              [0, 0, 7, 3, 0, 0, 0, 0, 0],
              [0, 5, 8, 0, 0, 0, 0, 0, 0],
              [4, 3, 0, 0, 0, 0, 0, 0, 0],
              [2, 0, 0, 0, 0, 0, 0, 0, 8],
              [0, 0, 0, 0, 0, 0, 0, 7, 6],
              [0, 0, 0, 0, 0, 0, 2, 5, 0],
              [0, 0, 0, 0, 0, 7, 3, 0, 0],
              [0, 0, 0, 0, 9, 8, 0, 0, 0]
              ]

# validating the grid
def check_valid(mesh, r, c, n):
    valid = True
    # check row and column
    for x in range(9):
        if mesh[x][c] == n:
            valid = False
            break
    for y in range(9):
        if mesh[r][y] == n:
            valid = False
            break
    row_section = r // 3
    col_section = c // 3
    for x in range(3):
        for y in range(3):
            # check if section is valid
            if mesh[row_section * 3 + x][col_section * 3 + y] == n:
                valid = False
                break
    return valid


def check_valid_BF(grid):
    mesh = np.array(grid)
    for n in range(9):
        if len(set(mesh[:, n])) != 9:
            return False
        if len(set(mesh[n, :])) != 9:
            return False

    a = mesh[:3, :3]
    b = mesh[:3, 3:6]
    c = mesh[:3, 6:9]

    d = mesh[3:6, :3]
    e = mesh[3:6, 3:6]
    f = mesh[3:6, 6:9]

    g = mesh[6:9, :3]
    h = mesh[6:9, 3:6]
    i = mesh[6:9, 6:9]

    boxes = [a, b, c, d, e, f, g, h, i]

    for box in boxes:
        if len(np.unique(box)) != 9:
            return False

    return True


def check_possible_values_BB(grid):
    empties = find_all_empty(grid)
    mesh = np.array(grid)

    values = []
    numbers = [1, 2, 3, 4, 5, 6, 7, 8, 9, 0]

    boxes = np.array([[mesh[:3, :3], mesh[:3, 3:6], mesh[:3, 6:9]],
                      [[mesh[3:6, :3]], mesh[3:6, 3:6], mesh[3:6, 6:9]],
                      [mesh[6:9, :3], mesh[6:9, 3:6], mesh[6:9, 6:9]]])

    for empty in empties:
        horizontal_diff = np.setdiff1d(numbers, mesh[empty[0], :])
        vertical_diff = np.setdiff1d(numbers, mesh[:, empty[1]])
        box_diff = np.setdiff1d(numbers, boxes[empty[0] // 3, empty[1] // 3])
        helper = np.intersect1d(horizontal_diff, vertical_diff)
        possible_values = np.intersect1d(helper, box_diff)
        values.append([[empty[0], empty[1]], possible_values.tolist()])

    values = sorted(values, key=lambda x: len(x[1]))
    return values


# print the grid
def print_board(grid):
    cnt_i = 0
    for i in range(13):
        cnt_j = 0
        for j in range(13):
            if i % 4 == 0:
                print("+------------+------------+------------+", end="")
                cnt_i += 1
                break
            elif j % 4 == 0:
                print("|", end="")

                cnt_j += 1
            else:
                if (grid[i - cnt_i][j - cnt_j] == 0):
                    print("", " ", "", end="|")
                else:
                    print("", grid[i - cnt_i][j - cnt_j], "", end="|")
        print()


# find an empty square (0)
def find_empty(grid):
    for i in range(len(grid)):
        for j in range(len(grid[0])):
            if grid[i][j] == 0:
                return (i, j)  # row, col
    return None


def find_all_empty(grid):
    empties = []
    for i in range(len(grid)):
        for j in range(len(grid[0])):
            if grid[i][j] == 0:
                empties.append([i, j])  # row, col
    return empties


# A function to check if the grid is full
def checkGrid(grid):
    for row in range(0, 9):
        for col in range(0, 9):
            if grid[row][col] == 0:
                return False

    # We have a complete grid!
    return True


# solve sudoku with backtracking
def solveBT(grid):
    find = find_empty(grid)
    if not find:
        return True
    else:
        row, col = find

    for i in range(1, 10):
        if check_valid(grid, row, col, i):
            grid[row][col] = i

            if solveBT(grid):
                return True

            grid[row][col] = 0

    return False

# solve sudoku with bruteforce
def solveBF(grid):
    solved = check_valid_BF(grid)
    cells = find_all_empty(grid)

    for cell in cells:
        grid[cell[0]][cell[1]] = 1

    solution = 0

    for i in range(len(cells)):
        solution = solution + (pow(10, i))

    solved = check_valid_BF(grid)
    counter = 1

    while solved == False:
        counter += 1
        solution += 1
        string_solution = str(solution).replace("0", "1")
        solution = int(string_solution)
        for i in range(len(cells)):
            grid[cells[i][0]][cells[i][1]] = int(string_solution[i])
        # print_board(grid)
        solved = check_valid_BF(grid)

    return solved

# solve sudoku with alternative branch&bound
def solveBB_2(grid):
    def recursion(grid, possible_values):
        spot = possible_values[0]
        x = spot[0][0]
        y = spot[0][1]
        for value in spot[1]:

            if check_valid(grid, spot[0][0], spot[0][1], value):

                grid[x][y] = value

                find = find_empty(grid)
                if not find:
                    # print("Found a solution.\n")
                    return True

                if recursion(grid, possible_values[1:]):
                    return True

                grid[spot[0][0]][spot[0][1]] = 0
                # print_board(grid)
        return False

    possible_values = check_possible_values_BB(grid)

    if len(possible_values[0][1]) == 1:
        for spot in possible_values:
            if len(spot[1]) == 1:
                grid[spot[0][0]][spot[0][1]] = spot[1][0]
            else:
                return solveBB_2(grid)
    else:
        # print("Filled all possible single values. \n")
        # print_board(grid)
        return recursion(grid, possible_values)

    find = find_empty(grid)
    if not find:
        return True

    return False

# solve sudoku with branch&bound
def solveBB(grid):
    # noinspection PyInterpreter,PyInterpreter
    def recursion(grid, possible_values):
        spot = possible_values[0]
        x = spot[0][0]
        y = spot[0][1]
        for value in spot[1]:

            if check_valid(grid, spot[0][0], spot[0][1], value):

                grid[x][y] = value

                find = find_empty(grid)
                if not find:
                    # print("Found a solution.\n")
                    return True

                if recursion(grid, possible_values[1:]):
                    return True

                grid[spot[0][0]][spot[0][1]] = 0
                # print_board(grid)
        return False

    possible_values = check_possible_values_BB(grid)

    if len(possible_values[0][1]) == 1:
        i = 0
        for spot in possible_values:
            if len(spot[1]) == 1:
                grid[spot[0][0]][spot[0][1]] = spot[1][0]
                i += 1
            else:
                return recursion(grid, possible_values[i:])
    else:
        # print("Filled all possible single values. \n")
        # print_board(grid)
        return recursion(grid, possible_values)

    find = find_empty(grid)
    if not find:
        return True

    return False


# A backtracking/recursive function to check all possible combinations of numbers until a solution is found
def initialSolve(grid):
    global counter
    # Find next empty cell
    for i in range(0, 81):
        row = i // 9
        col = i % 9
        if grid[row][col] == 0:
            for value in range(1, 10):
                # Check that this value has not already be used on this row
                if not (value in grid[row]):
                    # Check that this value has not already be used on this column
                    if not value in (
                    grid[0][col], grid[1][col], grid[2][col], grid[3][col], grid[4][col], grid[5][col], grid[6][col],
                    grid[7][col], grid[8][col]):
                        # Identify which of the 9 squares we are working on
                        square = []
                        if row < 3:
                            if col < 3:
                                square = [grid[i][0:3] for i in range(0, 3)]
                            elif col < 6:
                                square = [grid[i][3:6] for i in range(0, 3)]
                            else:
                                square = [grid[i][6:9] for i in range(0, 3)]
                        elif row < 6:
                            if col < 3:
                                square = [grid[i][0:3] for i in range(3, 6)]
                            elif col < 6:
                                square = [grid[i][3:6] for i in range(3, 6)]
                            else:
                                square = [grid[i][6:9] for i in range(3, 6)]
                        else:
                            if col < 3:
                                square = [grid[i][0:3] for i in range(6, 9)]
                            elif col < 6:
                                square = [grid[i][3:6] for i in range(6, 9)]
                            else:
                                square = [grid[i][6:9] for i in range(6, 9)]
                        # Check that this value has not already be used on this 3x3 square
                        if not value in (square[0] + square[1] + square[2]):
                            grid[row][col] = value
                            if checkGrid(grid):
                                counter += 1
                                break
                            else:
                                if initialSolve(grid):
                                    return True
            break
    grid[row][col] = 0


# A backtracking/recursive function to check all possible combinations of numbers until a solution is found
def fillGrid(grid):
    global counter
    # Find next empty cell
    for i in range(0, 81):
        row = i // 9
        col = i % 9
        if grid[row][col] == 0:
            shuffle(numberList)
            for value in numberList:
                # Check that this value has not already be used on this row
                if not (value in grid[row]):
                    # Check that this value has not already be used on this column
                    if not value in (
                    grid[0][col], grid[1][col], grid[2][col], grid[3][col], grid[4][col], grid[5][col], grid[6][col],
                    grid[7][col], grid[8][col]):
                        # Identify which of the 9 squares we are working on
                        square = []
                        if row < 3:
                            if col < 3:
                                square = [grid[i][0:3] for i in range(0, 3)]
                            elif col < 6:
                                square = [grid[i][3:6] for i in range(0, 3)]
                            else:
                                square = [grid[i][6:9] for i in range(0, 3)]
                        elif row < 6:
                            if col < 3:
                                square = [grid[i][0:3] for i in range(3, 6)]
                            elif col < 6:
                                square = [grid[i][3:6] for i in range(3, 6)]
                            else:
                                square = [grid[i][6:9] for i in range(3, 6)]
                        else:
                            if col < 3:
                                square = [grid[i][0:3] for i in range(6, 9)]
                            elif col < 6:
                                square = [grid[i][3:6] for i in range(6, 9)]
                            else:
                                square = [grid[i][6:9] for i in range(6, 9)]
                        # Check that this value has not already be used on this 3x3 square
                        if not value in (square[0] + square[1] + square[2]):
                            grid[row][col] = value
                            if checkGrid(grid):
                                return True
                            else:
                                if fillGrid(grid):
                                    return True
            break
    grid[row][col] = 0


# Generate a Fully Solved Grid
fillGrid(grid)
gridSolved = copy.deepcopy(grid)

# Start Removing Numbers one by one
# Difficulty value entered in the while loop determines the amount of cells that will have a number in the grid
# Entering less than 25 will result in longer generating time

counter = 1
difficulty = 81
while difficulty > 30:
    difficulty = 0
    # Select a random cell that is not already empty
    row = randint(0, 8)
    col = randint(0, 8)
    while grid[row][col] == 0:
        row = randint(0, 8)
        col = randint(0, 8)
    # Remember its cell value in case we need to put it back
    backup = grid[row][col]
    grid[row][col] = 0

    # Take a full copy of the grid
    copyGrid = []
    for r in range(0, 9):
        copyGrid.append([])
        for c in range(0, 9):
            copyGrid[r].append(grid[r][c])

    # Count the number of solutions that this grid has (using a backtracking approach implemented in the initialSolve() function)
    counter = 0
    initialSolve(copyGrid)
    # If the number of solution is different from 1 then we need to cancel the change by putting the value we took away back in the grid
    if counter != 1:
        grid[row][col] = backup

    for i in range(0, 81):
        row = i // 9
        col = i % 9
        if grid[row][col] != 0:
            difficulty += 1

print("Difficulty: ", difficulty)
print_board(grid)
print("Sudoku Grid Ready")

#print_board(puzzle18_2)

bb_2_grid = copy.deepcopy(grid)
bb_grid = copy.deepcopy(grid)
bt_grid = copy.deepcopy(grid)
bf_grid = copy.deepcopy(grid)

# running and measuring time for the alternative branch&bound algorithm
bb_2_time = "solveBB_2(copy.deepcopy(grid))"
elapsed_time = timeit.timeit(bb_2_time, "from __main__ import solveBB_2, copy, grid", number=10)/10

solveBB_2(bb_2_grid)
print_board(bb_2_grid)
print("Alternative Branch & Bound algorithm time [ms]: ", elapsed_time * 1000)
print("Alternative Branch & Bound algorithm solution")

# running and measuring time for the standard branch&bound algorithm
bb_time = "solveBB(copy.deepcopy(grid))"
elapsed_time = timeit.timeit(bb_time, "from __main__ import solveBB, copy, grid", number=10)/10

solveBB(bb_grid)
print_board(bb_grid)
print("Branch & Bound algorithm time [ms]: ", elapsed_time * 1000)
print("Branch & Bound algorithm solution")

# running and measuring time for the backtracking algorithm
backtracking_time = "solveBT(copy.deepcopy(grid))"
elapsed_time = timeit.timeit(backtracking_time, "from __main__ import solveBT, copy, grid", number=10)/10

solveBT(bt_grid)
print_board(bt_grid)
print("Backtracking algorithm time [ms]: ", elapsed_time * 1000)
print("Backtracking algorithm solution")

# running and measuring time for the brute-force algorithm
# WARNING: will result in a very long wait time (too long to even consider in a test)

# bruteforce_time = "solveBF(copy.deepcopy(grid))"
# elapsed_time = timeit.timeit(bruteforce_time, "from __main__ import solveBF, copy, grid", number=1)
#
# solveBF(bf_grid)
# print_board(bf_grid)
# print("Bruteforce algorithm time [ms]: ", elapsed_time*1000)
# print("Bruteforce algorithm solution")
