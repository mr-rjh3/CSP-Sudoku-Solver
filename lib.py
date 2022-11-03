class Slot:
    """
    ----------------------------------------------------------
    Description : Slot class, used to represent a slot in the CSP / box in the sudoku
    Use: use
    ----------------------------------------------------------
    Variables:
        domain - Binary representation of domain (if this ever == 000000000, then the puzzle is impossible)
        neighbours - Array of nodes that are neighbours of this node (Neighbours in the CSP not in the puzzle) (TODO: Might not use this)
        Value - value of the node
    """
    def __init__(self, value):
        self.domain = 0b111111111
        if(value == 0):
            self.value = None
        else:
            self.value = value
        
class CSP:
    """
    ----------------------------------------------------------
    Description: CSP class, used to represent the CSP of the sudoku
    Use: use
    ----------------------------------------------------------
    Variables:
        slots - Dictionary of slots in the CSP
        constraints - Array of constraints in the CSP
    Methods:
        generateBinaryConstraints(self) - Generates binary constraints for this node.
            _generateBinaryConstraintsRow(self) - Helper function for generateBinaryConstraints that generates binary constraints for rows
            _generateBinaryConstraintsCol(self) - Helper function for generateBinaryConstraints that generates binary constraints for columns
            _generateBinaryConstraintsBox(self) - Helper function for generateBinaryConstraints that generates binary constraints for boxes
        NC(self) - Node Consistency algorithm (TODO: Christine)
        AC3(self) - Arc Consistency algorithm (TODO: Samson)
            _reviseDomain(self, slot1, slot2) - Helper function for AC3 (TODO: Samson)
        PC2(self) - Path Consistency algorithm (TODO: Might not use)
    """
    def __init__(self, sudoku):
        
        self.slots = {}
        count = 0
        for i in ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I']:
            for j in ['1', '2', '3', '4', '5', '6', '7', '8', '9']:
                slot = Slot(sudoku[count])
                self.slots[i+j] = slot
                count += 1
        self.constraints = self.generateBinaryConstraints()
        
        # self.NC()
        # self.AC3()
    
    def _generateBinaryConstraintsRow(self, constraints): # Generates binary constraints for rows
        """
        ----------------------------------------------------------
        Description: Generates binary constraints for rows
        Use: _generateBinaryConstraintsRow()
        ----------------------------------------------------------
        Parameters:
            constraints - Array of binary constraints
        Returns: 
            constraints - Array of binary constraints
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
                        constraints.add((id,id2)) # add the constraint
        return constraints

    def _generateBinaryConstraintsCol(self, constraints): # Generates binary constraints for columns
        """
        ----------------------------------------------------------
        Description: Generates binary constraints for coloumns
        Use: _generateBinaryConstraintsCol()
        ----------------------------------------------------------
        Parameters:
            constraints - Array of binary constraints
        Returns: 
            constraints - Array of binary constraints
        ----------------------------------------------------------
        """
        row = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I']
        col = ['1', '2', '3', '4', '5', '6', '7', '8', '9']
        for number in col:
            for letter in row:
                id = letter + number # id of firstbox
                for j in range(row.index(letter), len(row)): # loop through all boxes after id in the column
                    id2 = row[j] + number # id of second box
                    if(letter != row[j]): # if the boxes are not the same
                        constraints.add((id,id2)) # add the constraint

    def _generateBinaryConstraintsBox(self, constraints): # Generates binary constraints for grids
        """
        ----------------------------------------------------------
        Description: Generates binary constraints for the 3x3 boxes 
        Use: _generateBinaryConstraintsBox()
        ----------------------------------------------------------
        Parameters:
            constraints - Array of binary constraints
        Returns: 
            constraints - Array of binary constraints
        ----------------------------------------------------------
        """
        row = [['A', 'B', 'C'], ['D', 'E', 'F'], ['G', 'H', 'I']]
        col = [['1','2','3'],['4','5','6'],['7','8','9']]
        # Generate boxes to get constraints of
        for i in range(len(row)):
            for j in range(len(col)):
                box = []
                for letter in row[i]:
                    for number in col[j]:
                        id = letter + number # id of box
                        box.append(id) # append to box array
                # Generate constraints for each grid by comparing each slot to every other slot in the grid
                for j in range(len(box)):
                    for k in range(j+1, len(box)):
                        if(box[j] != box[k]): # if the slot are not the same
                            constraints.add((box[j], box[k]))

    def generateBinaryConstraints(self): # Generates all binary constraints
        """
        ----------------------------------------------------------
        Description: Generates binary constraints for the CSP.
        Use: constraints = generateBinaryConstraints()
        ----------------------------------------------------------
        Returns:
            constraints - Array of binary constraints
        ----------------------------------------------------------
        """
        constraints = set()
        self._generateBinaryConstraintsRow(constraints)
        self._generateBinaryConstraintsCol(constraints)
        self._generateBinaryConstraintsBox(constraints)
        return constraints

class Search:
    """
    ----------------------------------------------------------
    Description : Sudoku class, holds the algortihms for solving the sudoku puzzle along with the puzzle itself.
    Use: use
    ----------------------------------------------------------
    Variables:
        heuristic = heuristic function
        path = path to solution
        CSP = CSP object
    Methods:
        backtracking_search(self.CSP) - backtracking search algorithm
        _backtrack(assignment, self.CSP) - helper function for the backtracking search algorithm
    ----------------------------------------------------------
    """

class Heuristic:
    """
    ----------------------------------------------------------
    Description : Heuristics class, holds the algorithms for generating heuristics for the sudoku puzzle.
    Use: use
    ----------------------------------------------------------
    Variables:
        MINREMAININGVALUES - holds the minimum remaining values heuristic function
        DEGREE - holds the degree heuristic function
        LEASTCONSTRAININGVALUE - holds the least constraining value heuristic function
        FORWARDCHECKING - holds the forward checking heuristic function
        MAC - holds the MAC heuristic function
    Methods:
        minRemainingValues(csp) - minimum remaining values heuristic function
        degree(csp) - degree heuristic function
        leastConstrainingValue(csp) - least constraining value heuristic function
        minConflicts(csp) - min conflicts heuristic function
        forwardChecking(csp) - forward checking heuristic function
        MAC(csp) - MAC heuristic function
        heuristic_to_string(heuristic) - converts heuristic function to string
        string_to_heuristic(heuristic) - converts string to heuristic function
    ----------------------------------------------------------
    """

