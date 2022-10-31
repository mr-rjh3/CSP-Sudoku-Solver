# Node Consistency
# def node_consistency(csp)

# path consistency (PC-2)
# Path consistency guarantees binary consistency for all variables in a path.
# if there are variables X and Y that are arc consistent, then there is a third variable Z that is arc consistent with both X and Y in order for it to be arc consistent.
# def PC2(csp)



class Node:
    """
    ----------------------------------------------------------
    Description : Node class, used to represent a node in the CSP / box in the sudoku
    Use: use
    ----------------------------------------------------------
    Variables:
        ID - ID of the node (A1, B2, etc.)
        domain - Array of possible values the node may use (if this is ever empty then the puzzle is impossible)
        neighbours - Array of nodes that are neighbours of this node (Neighbours in the CSP not in the puzzle)
        constraints - Array of constraints that are applied to this node (maybe not use??)
        Value - vaue of the node
    Methods:
        generateBinaryConstraints(csp) - Generates binary constraints.
        NC(self.CSP) - Node Consistency algorithm
        
    """

class Sudoku:
    """
    ----------------------------------------------------------
    Description : Sudoku class, holds the algortihms for solving the sudoku puzzle along with the puzzle itself.
    Use: use
    ----------------------------------------------------------
    Variables:
        board = array (of nodes?)
        heuristic = heuristic function
        path = path to solution
        CSP = generateBinaryConstraints(csp)
    Methods:
        AC3(self.CSP) - Arc Consistency algorithm (AC3)
        _reviseDomain(self.CSP, i, j) - Helper function for AC3 that changes domain to be arc consistant between i and j
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