from alive_progress import alive_bar
import argparse, math

def generateBinaryConstraintsRow(csp): # Generates binary constraints for rows
    """
    ----------------------------------------------------------
    Description: Generates binary constraints for rows
    Use: generateBinaryConstraintsRow(csp)
    ----------------------------------------------------------
    Parameters:
        csp - array of constraints
    ----------------------------------------------------------
    """
    row = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I']
    col = ['1', '2', '3', '4', '5', '6', '7', '8', '9']
    for letter in row:
        for number in col:
            id = letter + number # Get id of first box to compare
            for j in range(int(number), len(col)): # Loop through all boxes after id in the row
                id2 = letter + col[j] # id of second box to compare
                if(number != col[j]): # if the boxes are not the same
                    csp.append((id,id2)) # add the constraint

def generateBinaryConstraintsCol(csp): # Generates binary constraints for columns
    row = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I']
    col = ['1', '2', '3', '4', '5', '6', '7', '8', '9']
    for number in col:
        for letter in row:
            id = letter + number # id of firstbox
            for j in range(row.index(letter), len(row)):
                id2 = row[j] + number # id of second box
                if(letter != row[j] and (id, id2) not in csp): # if the boxes are not the same and the constraint is not already in the list
                    csp.append((id,id2)) # add the constraint

def generateBinaryConstraintsGrid(csp): # Generates binary constraints for grids
    row = [['A', 'B', 'C'], ['D', 'E', 'F'], ['G', 'H', 'I']]
    col = [['1','2','3'],['4','5','6'],['7','8','9']]
    # Generate grids to get constraints of
    for i in range(len(row)):
        grid = []
        for letter in row[i]:
            for number in col[i]:
                id = letter + number # id of box
                grid.append(id) # append to grid array
                
        # Generate constraints for each grid by comparing each box to every other box
        for j in range(len(grid)):
            for k in range(j+1, len(grid)):
                if(grid[j] != grid[k] and (grid[j], grid[k]) not in csp):
                    csp.append((grid[j], grid[k]))
        

def generateBinaryConstraints(csp): # Generates all binary constraints
    generateBinaryConstraintsRow(csp)
    generateBinaryConstraintsCol(csp)
    generateBinaryConstraintsGrid(csp)

# parser = argparse.ArgumentParser(description='A* algorithm for n-puzzle')
# parser.add_argument("-H", "--heuristic", help="The heuristic to use", choices=["manhattan", "displacement", "rowcol", "euclidean", "linear", "all"], default="manhattan")
# parser.add_argument("-n", "--numberOfPuzzles", help="The number of puzzles that will randomly generate.", type=int, default=100)
# parser.add_argument("-S", "--seed", help="The seed for the random number generator", type=int, default=None)
# parser.add_argument("-o", "--outputFile", help="Supplies the file name to output text to.", default="output.txt")
# parser.add_argument("-csv", "--outputCSV", help="Supplies the file name to output to csv data to.", default="stats.csv")
# parser.add_argument("-d", "--debug", help="Supplies the file name to output to csv data to.", action="store_true")
# parser.add_argument("-p", "--puzzle", help="Supply a puzzle for the program to solve. e.g. '-p 1,5,2,4,3,7,6,8,0'", default=None, type=validPuzzle)
# args = parser.parse_args()



csp = []
generateBinaryConstraints(csp)

print(csp)


# for i in csp:
#     print(i)