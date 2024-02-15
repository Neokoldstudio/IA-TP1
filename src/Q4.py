## Solve Every Sudoku Puzzle

## See http://norvig.com/sudoku.html

## Throughout this program we have:
##   r is a row,    e.g. 'A'
##   c is a column, e.g. '3'
##   s is a square, e.g. 'A3'
##   d is a digit,  e.g. '9'
##   u is a unit,   e.g. ['A1','B1','C1','D1','E1','F1','G1','H1','I1']
##   grid is a grid,e.g. 81 non-blank chars, e.g. starting with '.18...7...
##   values is a dict of possible values, e.g. {'A1':'12349', 'A2':'8', ...}

def cross(A, B):
    "Cross product of elements in A and elements in B."
    return [a+b for a in A for b in B]

digits   = '123456789'
rows     = 'ABCDEFGHI'
cols     = digits
squares  = cross(rows, cols)
unitlist = ([cross(rows, c) for c in cols] +
            [cross(r, cols) for r in rows] +
            [cross(rs, cs) for rs in ('ABC','DEF','GHI') for cs in ('123','456','789')])
units = dict((s, [u for u in unitlist if s in u])
             for s in squares)
peers = dict((s, set(sum(units[s],[]))-set([s]))
             for s in squares)

################ Display as 2-D grid ################

def display(grid):
    for i in range(9):
        print(grid[i*9:i*9+3]+"|"+grid[i*9+3:i*9+6]+"|"+grid[i*9+6:i*9+9])
        if i==2 or i==5:
            print("_"*11)


################ Utilities ################

def some(seq):
    "Return some element of seq that is true."
    for e in seq:
        if e: return e
    return False

def from_file(filename, sep='\n'):
    "Parse a file into a list of strings, separated by sep."
    return open(filename).read().strip().split(sep)

def shuffled(seq):
    "Return a randomly shuffled copy of the input sequence."
    seq = list(seq)
    random.shuffle(seq)
    return seq

################ Data manipulation ################

def gridToMatrix(grid):
    matrix = []
    for i in range(9):
        row = []
        for j in range(9):
            row.append(grid[i*9+j])
        matrix.append(row)
    return matrix

def matrixToGrid(matrix):
    grid = ""
    for i in range(len(matrix)):
        for j in range(len(matrix[i])):
            grid += matrix[i][j]
    return grid

def separateIntoSquares(matrix):
    matrices = []
    for i in range(0, 9, 3):
        for j in range(0, 9, 3):
            submatrix = [row[j:j+3] for row in matrix[i:i+3]]
            matrices.append(submatrix)
    return matrices

def squaresToMatrix(squares):
    matrix = [[0]*9 for i in range(9)]
    squareIndex = 0
    for i in range(0, 9, 3):
        for j in range(0, 9, 3):
            for k in range(3):
                for l in range(3):
                    matrix[i+k][j+l] = squares[squareIndex][k][l]
            squareIndex += 1

    return matrix

################ Hill Climbing ################

def remplirTrousGrille(grille):
    matrix = gridToMatrix(grille)
    # Fonction pour vérifier si un chiffre est valide dans une case donnée
    def estValide(x, y, num):
        # Vérification du carré 3x3 (et pas de ligne/colonne)
        start_row, start_col = 3 * (x // 3), 3 * (y // 3)
        for i in range(start_row, start_row + 3):
            for j in range(start_col, start_col + 3):
                if matrix[i][j] == num:
                    return False
        return True

    # Fonction récursive pour remplir les trous
    def remplirTrousRecurs(x, y):
        if x == 9:
            return True  # Tous les trous sont remplis avec succès
        if y == 9:
            return remplirTrousRecurs(x + 1, 0)
        if matrix[x][y] != '0':  # Passer aux cases déjà remplies
            return remplirTrousRecurs(x, y + 1)

        for num in random.sample(range(1, 10), 9):  # Mélange aléatoire des chiffres de 1 à 9
            num_str = str(num)
            if estValide(x, y, num_str):
                matrix[x][y] = num_str
                if remplirTrousRecurs(x, y + 1):
                    return True
                matrix[x][y] = '0'  # Réinitialiser la case si la solution n'est pas trouvée
        return False

    remplirTrousRecurs(0, 0)

    return matrix

def hillClimbingSudoku(grid, previousScore=83):
    square1 = [0,1,2,9,10,11,18,19,20]
    square2 = [3,4,5,12,13,14,12,22,23]
    square3 = [6,7,8,15,16,17,24,25,26]
    square4 = [27,28,29,36,37,38,45,46,47]
    square5 = [30,31,32,39,40,41,48,49,50]
    square6 = [33,34,35,42,43,44,51,52,53]
    square7 = [54,55,56,63,64,65,72,73,74]
    square8 = [57,58,59,66,67,68,75,76,77]
    square9 = [60,61,62,69,70,71,78,79,80]



################ System test ################

import time, random




grid1  = '003020600900305001001806400008102900700000008006708200002609500800203009005010300'
grid2  = '4.....8.5.3..........7......2.....6.....8.4......1.......6.3.7.5..2.....1.4......'
hard1  = '.....6....59.....82....8....45........3........6..3.54...325..6..................'

if __name__ == '__main__':
    print(display(matrixToGrid(remplirTrousGrille(grid1))))
    # solve_all(from_file("data/top95.txt"), "95sudoku", None)
    # solve_all(from_file("data/100sudoku.txt"), "100sudoku", None)
    # solve_all(from_file("data/1000sudoku.txt"), "1000sudoku", None)
    # # solve_all(from_file("easy50.txt", '========'), "easy", None)
    # # solve_all(from_file("easy50.txt", '========'), "easy", None)
    # # solve_all(from_file("top95.txt"), "hard", None)
    # # solve_all(from_file("hardest.txt"), "hardest", None)
    # solve_all([random_puzzle() for _ in range(99)], "random", 100.0)
