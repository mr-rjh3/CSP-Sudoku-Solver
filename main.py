from alive_progress import alive_bar
import argparse, math
from lib import CSP

# parser = argparse.ArgumentParser(description='A* algorithm for n-puzzle')
# parser.add_argument("-H", "--heuristic", help="The heuristic to use", choices=["manhattan", "displacement", "rowcol", "euclidean", "linear", "all"], default="manhattan")
# parser.add_argument("-n", "--numberOfPuzzles", help="The number of puzzles that will randomly generate.", type=int, default=100)
# parser.add_argument("-S", "--seed", help="The seed for the random number generator", type=int, default=None)
# parser.add_argument("-i", "--interactive", help="Interactive mode", default=True)
# parser.add_argument("-in", "--inputFile", help="Supplies the file for input", default=None)
# parser.add_argument("-o", "--outputFile", help="Supplies the file name to output text to.", default="output.txt")
# parser.add_argument("-csv", "--outputCSV", help="Supplies the file name to output to csv data to.", default="stats.csv")
# parser.add_argument("-d", "--debug", help="Supplies the file name to output to csv data to.", action="store_true")
# parser.add_argument("-p", "--puzzle", help="Supply a puzzle for the program to solve. e.g. '-p 1,5,2,4,3,7,6,8,0'", default=None, type=validPuzzle)
# args = parser.parse_args()

# sudoku represented by int array (0 = empty)
sudoku = [0, 0, 0, 0, 0, 0, 0, 0, 0,
          0, 0, 0, 0, 0, 3, 0, 8, 5,
          0, 0, 1, 0, 2, 0, 0, 0, 0,
          0, 0, 0, 5, 0, 7, 0, 0, 0,
          0, 0, 4, 0, 0, 0, 1, 0, 0,
          0, 9, 0, 0, 0, 0, 0, 0, 0,
          0, 0, 0, 0, 0, 0, 0, 3, 6,
          0, 0, 0, 0, 0, 0, 0, 4, 0,
          0, 0, 0, 0, 0, 0, 0, 0, 0]

csp = CSP(sudoku)

print("CSP generated")