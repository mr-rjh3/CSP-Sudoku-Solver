# CSP-Sudoku-Solver

## Purpose
Tool that can be used to solve a given sudoku board using **CSP Consistency and Backtracking algorithms**.

## Usage
1. Download and install [Python](https://www.python.org/downloads/)
2. Clone the repository
3. Run `pip -r requirements.txt` to install all required libraries
4. Run `python ./main.py -in FILENAME [-OPTIONS]`

### Options
`-in INPUTFILE`, `--inputFile INPUTFILE`
  - The filename that holds the given sudoku. Must be a 9x9 board of numbers with either '0' or ' ' to represent the blank spaces
    
```
Examples of valid boards:

100007090     9  5 8  7
030020008      8 3 29 5
009600500      54    8 
005300900      7 68  32
010080002     1    4  8
600004000     5  219 6 
300000010        9 6   
040000007     726  1   
007000300 
```

`-o OUTPUTFILE`, `--outputFile OUTPUTFILE`
  - Supplies the filename to output text to, default is output.txt.

`-d, --debug`
  - Tells the program to run in debug mode

`-p`, `--plot`
  - Tells the program to run in plot mode which will provide a graph during preprocessing:
  
  ![image](https://user-images.githubusercontent.com/98052534/201010458-75146c1b-a3da-4641-8be9-c238b9865187.png)

## License
MIT © License can be found [here](https://github.com/SamsonGoodenough/n-puzzle-solver/blob/main/LICENSE).
