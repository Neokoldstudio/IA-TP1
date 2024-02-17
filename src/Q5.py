# Simulated annealing, question 5.
# grid = "00504090070005055305..."
# matrix = une liste de 9 listes de 9 chiffres


################ Display as 2-D grid ################

def display(grid):
    for i in range(9):
        print(grid[i*9:i*9+3]+"|"+grid[i*9+3:i*9+6]+"|"+grid[i*9+6:i*9+9])
        if i==2 or i==5:
            print("_"*11)


################ Utilities ################
            
def from_file(filename, sep='\n'):
    "Parse a file into a list of strings, separated by sep."
    return open(filename).read().strip().split(sep)

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

# Remplis les "trous" d'une grille (les 0 et les .)
# En s'assurant qu'il n'y a qu'un seul exemplaire de chaque chiffre dans chaque carré
def remplirTrousGrille(grille):
    matrix = gridToMatrix(grille.replace(".","0"))
    fixedNums = [[False]*9 for _ in range(9)]
    for i in range(9):
        for j in range(9):
            if matrix[i][j] != '0':
                fixedNums[i][j] = True
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
        # for num in range(1, 10):                      # Mélange non-aléatoire des chiffres de 1 à 9
            num_str = str(num)
            if estValide(x, y, num_str):
                matrix[x][y] = num_str
                if remplirTrousRecurs(x, y + 1):
                    return True
                matrix[x][y] = '0'  # Réinitialiser la case si la solution n'est pas trouvée
        return False

    remplirTrousRecurs(0, 0)

    return (matrix, fixedNums)

# Prend un tuple (matrix, fixedNums)
# Renvoie une grille ou deux chiffres non-fixés du même carré ont été échangés
def getRandomNeighbor(tuple):
    matrix = tuple[0]
    fixedNums = tuple[1]
    while True:
        boxX = int(random.uniform(0,2))
        boxY = int(random.uniform(0,2))
        x1 = int(random.uniform(0,2))
        x2 = int(random.uniform(0,2))
        y1 = int(random.uniform(0,2))
        y2 = int(random.uniform(0,2))
        if(x1 == x2 and y1 == y2):continue
        if(fixedNums[boxX+x1][boxY+y1] or fixedNums[boxX+x2][boxY+y2]):continue
        copie = deepcopy(matrix)
        # On échange deux cases
        copie[boxX+x1][boxY+y1],copie[boxX+x2][boxY+y2] = copie[boxX+x2][boxY+y2],copie[boxX+x1][boxY+y1]
        return copie



# Implémentation du simulated Annealing
# Il ne s'arrête que s'il trouve une solution (auquel cas il return True)
# Ou si la température devient trop basse (on est coincés à un minimum local) (dans ce cas il return False)
def simAnnealingSudoku(tuple, alpha=0.99, initialTemp=3, minTemp=0.00001):
    fixedNums = tuple[1]
    matrix = tuple[0]
    minScore = numberOfErrors(matrix)
    temp = initialTemp

    while minScore > 0 and temp > minTemp:
        candidate = getRandomNeighbor((matrix, fixedNums))
        score = numberOfErrors(candidate)
        delta = score - minScore

        if delta < 0:
            matrix = candidate
            minScore = score
        else:
            prob = math.exp(-delta / temp)
            if random.uniform(0, 1) < prob:
                matrix = candidate
                minScore = score
        temp *= alpha
    if minScore == 0:
        return True
    return False

# return the number of times the same number appears in the same row or column
def numberOfErrors(matrix):
    count = 0
    copy = deepcopy(matrix)
    for i in range(9):
        count += (9-len(set(copy[i])))
        count += (9-len(set([col[i] for col in matrix])))
    return count

################ System test ################

import time, random
from copy import copy, deepcopy
import math
from statistics import mean

def solve_all(grids, name='', showif=0.0):
    start = time.process_time()
    def time_solve(grid):
        start = time.process_time()
        values = simAnnealingSudoku(remplirTrousGrille(grid))
        t = time.process_time()-start
        ## Display puzzles that take long enough
        return (t, values)
    times, results = zip(*[time_solve(grid) for grid in grids])
    N = len(grids)
    if N > 1:
        sumTimes = sum(times)
        if sumTimes == 0:
            sumTimes += 0.01
        print ("Solved %d of %d %s puzzles (avg %.2f secs (%d Hz), max %.2f secs)." % (
            sum(results), N, name, sumTimes/N, N/sumTimes, max(times)))
    return(sum(results)/N)

grid1  = '840000001070000400000000050000000504003604010000000609400902000900851000205007008'
grid2  = '4.....8.5.3..........7......2.....6.....8.4......1.......6.3.7.5..2.....1.4......'
hard1  = '.....6....59.....82....8....45........3........6..3.54...325..6..................'

if __name__ == '__main__':
    ratio95 = solve_all(from_file("data/top95.txt"), "95sudoku", None)
    ratio100 = solve_all(from_file("data/100sudoku.txt"), "100sudoku", None)
    ratio1000 = solve_all(from_file("data/1000sudoku.txt"), "1000sudoku", None)

    precision_percentage = mean([ratio95, ratio100, ratio1000]) * 100
    print("The precision percentage of this method is: {:.2f}%".format(precision_percentage))
    # solve_all(from_file("easy50.txt", '========'), "easy", None)
    # solve_all(from_file("easy50.txt", '========'), "easy", None)
    # solve_all(from_file("top95.txt"), "hard", None)
    # solve_all(from_file("hardest.txt"), "hardest", None)
    # solve_all([random_puzzle() for _ in range(99)], "random", 100.0)
