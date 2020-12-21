import random

# the sudoku grid

# +-------+-------+-------+
# | 0 0 0 | 0 0 0 | 0 0 0 |
# | 0 0 0 | 0 0 0 | 0 0 0 |
# | 0 0 0 | 0 0 0 | 0 0 0 |    #The classic Sudoku game involves a grid of 81 squares.
# +-------+-------+-------+    # The grid is divided into nine blocks, each containing nine squares.
# | 0 0 0 | 0 0 0 | 0 0 0 |    # The rules of the game are simple:
# | 0 0 0 | 0 0 0 | 0 0 0 |       # each of the nine blocks has to contain all the numbers 1-9 within its squares.
# | 0 0 0 | 0 0 0 | 0 0 0 |       # Each number can only appear once in a row, column or box.
# +-------+-------+-------+       # The difficulty lies in that each vertical nine-square column,
# | 0 0 0 | 0 0 0 | 0 0 0 |       # or horizontal nine-square line across, within the larger square,
# | 0 0 0 | 0 0 0 | 0 0 0 |       # must also contain the numbers 1-9, without repetition or omission.
# | 0 0 0 | 0 0 0 | 0 0 0 |    # Every puzzle has just one correct solution.
# +-------+-------+-------+

# option to choose difficulty level

print("Level of Difficulty")
print("     1. Beginner")
print("     2. Intermediate")
print("     3. Advanced")
print()
print("Enter the level of difficulty as per your choice:  ",end="")
level = int(input())
if level==1:
    q = 35
elif level==2:
    q = 20
else:
    q = 8
#place to store the grid

grid = [[0 for x in range(9)] for y in range(9)]

# validating the grid

def check_valid(mesh,r,c,n):
    valid = True
    #check row and column
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
            #check if section is valid
            if mesh[row_section * 3 + x][col_section * 3 + y] == n:
                valid = False
                break
    return valid

# generating random values for the grid
for i in range(q):
    row = random.randrange(9)
    col = random.randrange(9)
    num = random.randrange(1,10)
    while not check_valid(grid,row,col,num) or grid[row][col]!=0:
        row = random.randrange(9)
        col = random.randrange(9)
        num = random.randrange(1,10)
    grid[row][col]=num


# print the grid

cnt_i = 0
for i in range(13):
    cnt_j = 0
    for j in range(13):
        if i%4==0:
            print("+---------+---------+---------+",end="")
            cnt_i+=1
            break
        elif j%4==0:
            print("|",end="")
            cnt_j+=1
        else:
            print("",grid[i-cnt_i][j-cnt_j],"" ,end="")
    print()