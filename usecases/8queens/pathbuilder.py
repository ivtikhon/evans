# This script builds all straight paths (horizontal, vertical, and diagonal) for queens on 8x8 chess board
# Developed by Igor Tikhonin in 2020
# Vestion 1.0

import pprint

board = [
    ['h1', 'h2', 'h3', 'h4', 'h5', 'h6', 'h7', 'h8'],
    ['g1', 'g2', 'g3', 'g4', 'g5', 'g6', 'g7', 'g8'],
    ['f1', 'f2', 'f3', 'f4', 'f5', 'f6', 'f7', 'f8'],
    ['e1', 'e2', 'e3', 'e4', 'e5', 'e6', 'e7', 'e8'],
    ['d1', 'd2', 'd3', 'd4', 'd5', 'd6', 'd7', 'd8'],
    ['c1', 'c2', 'c3', 'c4', 'c5', 'c6', 'c7', 'c8'],
    ['b1', 'b2', 'b3', 'b4', 'b5', 'b6', 'b7', 'b8'],
    ['a1', 'a2', 'a3', 'a4', 'a5', 'a6', 'a7', 'a8'],
]


# rows
for row in board:
    for elem in row:
        for other_elem in row:
            if elem != other_elem:
                print('(path_exists ' + elem + ' ' + other_elem + ')')

# columns
for j in range(len(board[0])):
    for i in range(len(board)):
        for other_i in range(len(board)):
            if board[i][j] != board[i][other_i]:
                print('(path_exists ' + board[i][j] + ' ' + board[i][other_i] + ')')

# right diagonals
ROW = len(board)
COL = len(board[0])
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
