from alive_progress import alive_bar
import argparse, math, time
from lib import CSP, Search, colorHelper

parser = argparse.ArgumentParser(description='CSP solver for sudoku')
parser.add_argument("-i", "--interactive", help="Interactive mode", default=True)

parser.add_argument("-in", "--inputFile", help="Supplies the file for input", default=None)
parser.add_argument("-o", "--outputFile", help="Supplies the file name to output text to.", default="output.txt")
parser.add_argument("-csv", "--csvFile", help="Supplies the file name to output csv to.", default="output.csv")

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

# Easy
# sudoku =   [9, 0, 0, 5, 0, 8, 0, 0, 7,
#             0, 8, 0, 3, 0, 2, 9, 0, 5,
#             0, 5, 4, 0, 0, 0, 0, 8, 0,
#             0, 7, 0, 6, 8, 0, 0, 3, 2,
#             1, 0, 0, 0, 0, 4, 0, 0, 8,
#             5, 0, 0, 2, 1, 9, 0, 6, 0,
#             0, 0, 0, 9, 0, 6, 0, 0, 0,
#             7, 2, 6, 0, 0, 1, 0, 0, 0,
#             0, 0, 0, 0, 0, 0, 0, 0, 0]

sudoku =   [1, 0, 0, 0, 0, 7, 0, 9, 0, 
            0, 3, 0, 0, 2, 0, 0, 0, 8, 
            0, 0, 9, 6, 0, 0, 5, 0, 0, 
            0, 0, 5, 3, 0, 0, 9, 0, 0, 
            0, 1, 0, 0, 8, 0, 0, 0, 2, 
            6, 0, 0, 0, 0, 4, 0, 0, 0, 
            3, 0, 0, 0, 0, 0, 0, 1, 0, 
            0, 4, 0, 0, 0, 0, 0, 0, 7, 
            0, 0, 7, 0, 0, 0, 3, 0, 0]

try:
    start = time.time()
    csp = CSP(sudoku, args.debug, args.plot)
    if(args.debug):print("CSP generated: ", len(csp.constraints), "constraints")
    if csp.isSolved:
        print("CSP is already solved by pre-processing!")
    else:
        Search.backtracking_search(csp)
    end = time.time()
    print("Time Taken: {:.4f}s".format(end - start))
    
    print(csp.stats)
except (Exception) as e:
    colorHelper.error("ERROR: No solution")
    print(e)