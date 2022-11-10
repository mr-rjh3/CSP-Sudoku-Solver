import argparse, time
from lib import CSP, Search, colorHelper

SUDOKU_WIDTH = 9

parser = argparse.ArgumentParser(description='CSP solver for sudoku')

parser.add_argument("-in", "--inputFile", help="Supplies the file(s) for input", default=None, action="extend", nargs="+", required=True)
parser.add_argument("-o", "--outputFile", help="Supplies the file name to output text to.", default="output.txt")
# parser.add_argument("-csv", "--csvFile", help="Supplies the file name to output csv to.", default="output.csv")

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

# check if user supplied an input file
if args.inputFile != None:
    sudokus = {}
    if isinstance(args.inputFile, str):
        files = [args.inputFile]
    else:
        files = args.inputFile
        
    for file in files:
        sudoku = []
        with open(file, 'r') as f:
            for line in f:
                line = line.strip('\n')
                if len(line) > SUDOKU_WIDTH:
                    line = line[0:SUDOKU_WIDTH]
                    colorHelper.warning(str(file)+":")
                    colorHelper.warning("\tLine too long, truncating to " + str(SUDOKU_WIDTH) + " characters")
                elif len(line) < SUDOKU_WIDTH:
                    colorHelper.warning(str(file)+":")
                    colorHelper.warning("\tLine too short, padding with 0's")
                    line = line.ljust(SUDOKU_WIDTH, '0')
                    
                for c in line:
                    if c.isdigit():
                        sudoku.append(int(c))
                    else:
                        sudoku.append(0)
                
                if len(sudoku) > SUDOKU_WIDTH * SUDOKU_WIDTH:
                    colorHelper.warning("Too many characters in file, ignoring the rest")
                    sudoku = sudoku[0:SUDOKU_WIDTH * SUDOKU_WIDTH]
                    break
            
            if len(sudoku) < SUDOKU_WIDTH * SUDOKU_WIDTH:
                colorHelper.warning(str(file)+":")
                colorHelper.warning("\tToo few characters in file, padding with 0's")
                while len(sudoku) < SUDOKU_WIDTH * SUDOKU_WIDTH:
                    sudoku.append(0)
        sudokus[str(file)] = sudoku

# clear output file
file = open(args.outputFile, "w")
file.close()

for name in sudokus:
    sudoku = sudokus[name]
    try:
        file = open(args.outputFile, "a")
        colorHelper.info("Solving " + str(name) + "...")
        file.write("Solving " + str(name) + "...\n")
        start = time.time()
        csp = CSP(sudoku, file, args.debug, args.plot)
        if(args.debug):print("CSP generated: ", len(csp.constraints), "constraints")
        if csp.isSolved:
            print("CSP is already solved by pre-processing!")
            file.write("CSP is already solved by pre-processing!\n")
        else:
            Search.backtracking_search(csp, file)
        end = time.time()
        print("Time Taken: {:.4f}s".format(end - start))
        file.write("Time Taken: {:.4f}s\n\n".format(end - start))
        file.close()
    except (Exception) as e:
        colorHelper.error("ERROR: No solution")
        print(e)