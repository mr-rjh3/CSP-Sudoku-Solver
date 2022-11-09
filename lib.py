from copy import deepcopy
import matplotlib.pyplot as plt
import math

class colorHelper:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKCYAN = '\033[96m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'

    def error(text):
        print(colorHelper.FAIL + text + colorHelper.ENDC)

    def yellowPrint(text, end='\n'):
        print(colorHelper.WARNING + text + colorHelper.ENDC, end=end)

class Slot:
    """
    ----------------------------------------------------------
    Description : Slot class, used to represent a slot in the CSP / box in the sudoku
    Use: use
    ----------------------------------------------------------
    Variables:
        domain - Binary representation of domain (if this ever == 000000000, then the puzzle is impossible)
        updatedValue - Boolean to check if the value has been updated
        Value - value of the node
        binaryDomain - String representation of the binary domain (for debugging)
    """
    def __init__(self, value, debug=False):
        self.domain = 0b111111111
        if debug: self.binaryDomain = "{0:09b}".format(self.domain)
        self.updatedValue = False
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
        nodeConsistency(self) - Node Consistency algorithm
        arcConsistency3(self) - Arc Consistency algorithm
            _reviseDomain(self, slot1, slot2) - Helper function for AC3
        updateSudoku(self, sudoku) - Updates the sudoku array with the values in the CSP
        printSudoku(self, sudoku) - Prints the sudoku array
        generateBinaryConstraints(self) - Generates binary constraints for this node.
            _generateBinaryConstraintsRow(self) - Helper function for generateBinaryConstraints that generates binary constraints for rows
            _generateBinaryConstraintsCol(self) - Helper function for generateBinaryConstraints that generates binary constraints for columns
            _generateBinaryConstraintsBox(self) - Helper function for generateBinaryConstraints that generates binary constraints for boxes
    """
    MAX_VALUE = 9
    
    def __init__(self, sudoku, debug=False, plot=False):

        print("INPUT SUDOKU")
        self.debug = debug
        self.plot = plot
    
        self.slots = {}
        count = 0
        for i in ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I']:
            for j in ['1', '2', '3', '4', '5', '6', '7', '8', '9']:
                slot = Slot(sudoku[count])
                self.slots[i+j] = slot
                count += 1
        self.constraints = self.generateBinaryConstraints()

        self.printSudoku(sudoku)

        self.nodeConsistency()
        if not self.arcConsistency3():
            colorHelper.error("ERROR: No solution")
            return

        if(self.updateSudoku(sudoku)):
            print("\n UPDATED SUDOKU")
            self.printSudoku(sudoku)
            
    def nodeConsistency(self):
        """
        ----------------------------------------------------------
        Description: Ensures all nodes in the CSP passed, are node consistent
        At this stage, all domains are initalized to [1, 2, 3, 4, 5, 6, 7, 8, 9].
        Each domain will come out either the same, or minimized to match the slot's value
        Use: csp.nodeConsistency()
        ----------------------------------------------------------
        Variables:
            self - the CSP the function is called on
        """
        # For each key corresponding to a slot in CSP (which is a dictionary) 
        for key in self.slots:
            
            # DEBUG: Print the key and it's corresponding slot object's value and domain (in binary)
            slot = self.slots[key]
            
            # If the value is None, the domain of [1, 2, 3, 4, 5, 6, 7, 8, 9] is good,
            # Otherwise, find the binary representation of the value for the domain and update 
            if slot.value != None:
                slot.domain = (1 << (slot.value - 1))  
                if self.debug: slot.binaryDomain = "{0:09b}".format(slot.domain)
                if self.debug: print(key, "->", slot.value, " Domain: {0:09b}".format(slot.domain))
        return

    def arcConsistency3(self, constraints=None):
        """
        ----------------------------------------------------------
        Description: Ensures all arcs in the CSP are consistent
        Use: csp.arcConsistency3()
        ----------------------------------------------------------
        Variables:
            self - the CSP the function is called on
        ----------------------------------------------------------
        Returns:
            True if the CSP is arc consistent, False otherwise
        """

        if constraints == None:
            queue = deepcopy(self.constraints)
        else:
            queue = deepcopy(constraints)

        if self.plot:
            queueLength = []
            queueIndex = []
            count = 0
        while len(queue) > 0:
            c = queue.pop()
            if self.plot: 
                queueLength.append(len(queue))
                queueIndex.append(count)
                count += 1
            if self._reviseDomain(c):
                if self.slots[c[0]].domain == 0:
                    return False
                
                for n in self._getNeighbors(c[0]):
                    queue.add((n, c[0]))
        if self.plot:
            plt.plot(queueIndex, queueLength)
            plt.xlabel("Iteration")
            plt.ylabel("Queue Length")
            plt.title("Queue Length vs. Iteration")
            plt.show()
        return True
    
    def _reviseDomain(self, constraint):
        """
        ----------------------------------------------------------
        Description: Helper function for arcConsistency3
        Use: self._reviseDomain(constraint)
        ----------------------------------------------------------
        Variables:
            self - the CSP the function is called on
            constraint - the constraint to revise the domain of
        """
        s1, s2 = constraint
        revised = False
        for bit in range(CSP.MAX_VALUE): # loop over all bits in the domain
            d = 1 << bit
            if self.slots[s1].domain & d == 0: # skip if 0
                continue
            
            xor = d ^ self.slots[s2].domain # check if domain of s2 satisfies constraint
            if xor == 0: # if not
                self.slots[s1].domain = self.slots[s1].domain & ~d # delete d from self.slots[s1].domain
                if self.debug: self.slots[s1].binaryDomain = "{0:09b}".format(self.slots[s1].domain)
                if (self.slots[s1].domain != 0) and ((self.slots[s1].domain & (self.slots[s1].domain - 1)) == 0):
                    self.slots[s1].value = int(math.log(self.slots[s1].domain, 2) + 1)
                    self.slots[s1].updatedValue = True
                revised = True
                if self.debug: print("reviseDomain: ", s1, s2, self.slots[s1].domain)
                
        return revised
        
    def getUnsetSlots(self):
        """
        ----------------------------------------------------------
        Description: Returns a list of all unset slots
        Use: csp.getUnsetSlots()
        ----------------------------------------------------------
        Variables:
            self - the CSP the function is called on
        ----------------------------------------------------------
        Returns:
            A list of all unset slot's ids
        """
        unsetSlots = []
        for key in self.slots:
            if self.slots[key].value == None:
                unsetSlots.append(key)
        return unsetSlots
        
    def updateSudoku(self, sudoku):
        """
        ----------------------------------------------------------
        Description: Updates the sudoku array with the values in the CSP
        Use: csp.updateSudoku(sudoku)
        ----------------------------------------------------------
        Variables:
            self - the CSP the function is called on
            sudoku - the sudoku array to be updated
        """
        updated = False
        i = 0
        for slot in self.slots:
            if(sudoku[i] == 0 and self.slots[slot].updatedValue):
                if self.debug: print("Updating", slot, "to", self.slots[slot].value)
                sudoku[i] = self.slots[slot].value
                updated = True
            i += 1
        return updated
    
    def printSudoku(self, sudoku):
        """
        ----------------------------------------------------------
        Description: Prints the sudoku in a nice format
        Use: csp.printSudoku(sudoku)
        ----------------------------------------------------------
        Variables:
            self - the CSP the function is called on
            sudoku - the sudoku to be printed
        """
        print("+-----------------------+")
        i = 0
        for slot in self.slots:
            if(i % 3 == 0):
                print("|", end=" ")
            if(self.slots[slot].updatedValue):
                colorHelper.yellowPrint(str(sudoku[i]), end=" ")
            else:
                print(sudoku[i], end=" ")
            i += 1
            if(i % 9 == 0):
                print("|")
                if(i % 27 == 0 and i != 81):
                    print("|-------+-------+-------|")
        print("+-----------------------+")
        
        return
            
    def _getNeighbors(self, slot):
        """
        ----------------------------------------------------------
        Description: Returns a list of all neighbors of a slot
        Use: csp._getNeighbors(slot)
        ----------------------------------------------------------
        Variables:
            self - the CSP the function is called on
            slot - the slot to find neighbors of
        ----------------------------------------------------------
        Returns: A list of all neighbors of a slot
        ----------------------------------------------------------
        """
        neighbors = []
        letters = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I']
        numbers = ['1', '2', '3', '4', '5', '6', '7', '8', '9']
        # rows
        for n in numbers:
            if (slot[0] + n) != slot:
                neighbors.append(slot[0] + n)
        
        # cols
        for l in letters:
            if (l+ slot[1]) != slot:
                neighbors.append(l + slot[1])
        
        # boxes
        box_x = (int(slot[1])-1) // 3
        box_y = ((ord(slot[0])-65)) // 3
        
        for i in range(box_x*3, box_x*3+3):
            for j in range(box_y*3, box_y*3+3):
                s = letters[j] + numbers[i]
                if slot != s:
                    if s not in neighbors:
                        neighbors.append(s)
                    
        return neighbors
    
    def getConstraints(self, slot):
        """
        ----------------------------------------------------------
        Description: Returns a list of all constraints of a slot
        Use: csp.getConstraints(slot)
        ----------------------------------------------------------
        Variables:
            self - the CSP the function is called on
            slot - the slot to find constraints of
        ----------------------------------------------------------
        Returns: A list of all constraints of a slot
        ----------------------------------------------------------
        """
        constraints = set()
        for n in self._getNeighbors(slot):
            constraints.add((n, slot))
        return constraints

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
                for j in range(len(col)): # Loop through all boxes after id in the row
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
                for j in range(len(row)): # loop through all boxes after id in the column
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
                    for k in range(len(box)):
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
    
    def backtracking_search(csp):
        """
        ----------------------------------------------------------
        Description: Backtracking search algorithm
        Use: path = backtracking_search(CSP)
        ----------------------------------------------------------
        Parameters:
            csp - CSP object
        Returns:
            suduku - solved sudoku puzzle
        ----------------------------------------------------------
        """
        solution = Search._backtrack(csp)
        sudoku = [solution.slots[n].value for n in solution.slots]
        solution.printSudoku(sudoku)
        return solution
    
    def _backtrack(csp, unset=None):
        """
        ----------------------------------------------------------
        Description: Helper function for backtracking search algorithm
        Use: path = _backtrack(CSP)
        ----------------------------------------------------------
        Parameters:
            csp - CSP object
        Returns:
            path - path to solution
        ----------------------------------------------------------
        """ 
        csp = deepcopy(csp)
        unsetlen = len(unset) if unset else 0
        if unset is None:
            unset = csp.getUnsetSlots()
            
        if len(unset) == 0:
            return csp
        
        id = unset.pop(0)
        domain = csp.slots[id].domain
        
        # loop over the domain
        for bit in range(CSP.MAX_VALUE): # loop over all bits in the domain
            d = 1 << bit
            if domain & d == 0: # skip if 0
                continue
            
            value = bit + 1
            csp.slots[id].value = value
            csp.slots[id].domain = d
            
            constraints = csp.getConstraints(id)
            if not csp.arcConsistency3(constraints):
                return False
            else:
                result = Search._backtrack(csp, deepcopy(unset))
                if result is not False:
                    return result
            
        return False

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

