# This script builds all straight paths (horizontal, vertical, and diagonal) for queens on 8x8 chess board
# Developed by Igor Tikhonin in 2020
# Vestion 1.0

import pprint

board = [
    ['a8', 'b8', 'c8', 'd8', 'e8', 'f8', 'g8', 'h8'],
    ['a7', 'b7', 'c7', 'd7', 'e7', 'f7', 'g7', 'h7'],
    ['a6', 'b6', 'c6', 'd6', 'e6', 'f6', 'g6', 'h6'],
    ['a5', 'b5', 'c5', 'd5', 'e5', 'f5', 'g5', 'h5'],
    ['a4', 'b4', 'c4', 'd4', 'e4', 'f4', 'g4', 'h4'],
    ['a3', 'b3', 'c3', 'd3', 'e3', 'f3', 'g3', 'h3'],
    ['a2', 'b2', 'c2', 'd2', 'e2', 'f2', 'g2', 'h2'],
    ['a1', 'b1', 'c1', 'd1', 'e1', 'f1', 'g1', 'h1'],
]


ROW = len(board)
COL = len(board[0])

# rows
for row in board:
    for elem in row:
        for other_elem in row:
            if elem != other_elem:
                print('(path_exists ' + elem + ' ' + other_elem + ')')

# columns
for j in range(COL):
    for i in range(ROW):
        for other_i in range(ROW):
            if board[i][j] != board[other_i][j]:
                print('(path_exists ' + board[i][j] + ' ' + board[other_i][j] + ')')

# right diagonals
for line in range(1, ROW + COL) : 
    # Get column index of the first element 
    # in this line of output. The index is 0 
    # for first ROW lines and line - ROW for 
    # remaining lines  
    start_col = max(0, line - ROW) 
    # Get count of elements in this line. 
    # The count of elements is equal to 
    # minimum of line number, COL-start_col and ROW  
    count = min(line, COL - start_col, ROW)

    if count == 1:
        continue

    # Loop over line elements
    diag = []
    for j in range(0, count) : 
        diag.append(board[min(ROW, line) - j - 1][start_col + j])
    
    for elem in diag:
        for other_elem in diag:
            if elem != other_elem:
                print('(path_exists ' + elem + ' ' + other_elem + ')')

# left diagonals
for line in range(1, ROW + COL) : 
    # Get column index of the first element 
    # in this line of output. The index is COL 
    # for first ROW lines and ROW + COL - line for 
    # remaining lines  
    start_col = min(COL,  ROW + COL - line) 

    # Get count of elements in this line. 
    # The count of elements is equal to 
    # minimum of line number, start_col and ROW  
    count = min(line, start_col, ROW)

    if count == 1:
        continue

    # Loop over line elements
    diag = []
    for j in range(0, count):
        diag.append(board[min(ROW, line) - j - 1][start_col - j - 1])
    
    for elem in diag:
        for other_elem in diag:
            if elem != other_elem:
                print('(path_exists ' + elem + ' ' + other_elem + ')')
