from alive_progress import alive_bar
import argparse, math
from lib import CSP

parser = argparse.ArgumentParser(description='CSP solver for sudoku')
parser.add_argument("-H", "--heuristic", help="The heuristic to use", choices=["manhattan", "displacement", "rowcol", "euclidean", "linear", "all"], default="manhattan") #TODO change to real heuristics

parser.add_argument("-n", "--numberOfPuzzles", help="The number of puzzles that will randomly generate.", type=int, default=1)
parser.add_argument("-S", "--seed", help="The seed for the random number generator", type=int, default=None)

parser.add_argument("-i", "--interactive", help="Interactive mode", default=True)

parser.add_argument("-in", "--inputFile", help="Supplies the file for input", default=None)
parser.add_argument("-o", "--outputFile", help="Supplies the file name to output text to.", default="output.txt")
parser.add_argument("-csv", "--outputCSV", help="Supplies the file name to output to csv data to.", default="stats.csv")

parser.add_argument("-d", "--debug", help="Tells the program to run in debug mode", action="store_true")
parser.add_argument("-p", "--plot", help="Tells the program to run in plot mode", action="store_true")
args = parser.parse_args()

# Visualization of the sudoku indexes
# A1 A2 A3 | A4 A5 A6 | A7 A8 A9
# B1 B2 B3 | B4 B5 B6 | B7 B8 B9
# C1 C2 C3 | C4 C5 C6 | C7 C8 C9
# ---------+----------+---------
# D1 D2 D3 | D4 D5 D6 | D7 D8 D9
# E1 E2 E3 | E4 E5 E6 | E7 E8 E9
# F1 F2 F3 | F4 F5 F6 | F7 F8 F9
# ---------+----------+---------
# G1 G2 G3 | G4 G5 G6 | G7 G8 G9
# H1 H2 H3 | H4 H5 H6 | H7 H8 H9
# I1 I2 I3 | I4 I5 I6 | I7 I8 I9


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

# sudoku =   [1, 2, 3, 4, 5, 6, 7, 8, 0,
#             0, 0, 0, 0, 0, 0, 0, 0, 0,
#             0, 0, 0, 0, 0, 0, 0, 0, 0,
#             0, 0, 0, 0, 0, 0, 0, 0, 0,
#             0, 0, 0, 0, 0, 0, 0, 0, 0,
#             0, 0, 0, 0, 0, 0, 0, 0, 0,
#             0, 0, 0, 0, 0, 0, 0, 0, 0,
#             0, 0, 0, 0, 0, 0, 0, 0, 0,
#             0, 0, 0, 0, 0, 0, 0, 0, 0]

# sudoku =   [1, 2, 3, 4, 0, 6, 7, 8, 0,
#             4, 5, 6, 7, 8, 0, 1, 2, 3,
#             7, 8, 0, 1, 2, 3, 4, 5, 6,
#             2, 3, 4, 5, 6, 7, 8, 0, 1,
#             5, 6, 0, 8, 0, 1, 2, 3, 4,
#             8, 0, 1, 2, 3, 4, 5, 6, 7,
#             3, 4, 5, 6, 7, 8, 0, 1, 2,
#             6, 0, 8, 0, 1, 2, 3, 0, 5,
#             0, 1, 2, 3, 4, 5, 6, 7, 8]

csp = CSP(sudoku, args.debug, args.plot)

print("CSP generated: ", len(csp.constraints), "constraints")
