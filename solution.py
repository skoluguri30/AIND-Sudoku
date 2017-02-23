from collections import defaultdict

assignments = []

def assign_value(values, box, value):
    """
    Please use this function to update your values dictionary!
    Assigns a value to a given box. If it updates the board record it.
    """
    values[box] = value
    if len(value) == 1:
        assignments.append(values.copy())
    return values



def cross(a, b):
    "Cross product of elements in A and elements in B."
    return [s+t for s in a for t in b]
    
#strings
rows = 'ABCDEFGHI'
cols = '123456789'

#creating boxes
boxes = cross(rows, cols)

#row_units[0] = ['A1', 'A2', 'A3', 'A4', 'A5', 'A6', 'A7', 'A8', 'A9']
row_units = [cross(r, cols) for r in rows]

# column_units[0] = ['A1', 'B1', 'C1', 'D1', 'E1', 'F1', 'G1', 'H1', 'I1']
column_units = [cross(rows, c) for c in cols]

# square_units[0] = ['A1', 'A2', 'A3', 'B1', 'B2', 'B3', 'C1', 'C2', 'C3'] , this is the top left square
square_units = [cross(rs, cs) for rs in ('ABC','DEF','GHI') for cs in ('123','456','789')]

# diagonal units_1 
diag_units1 = [val+cols[index] for index, val in enumerate(rows)]
print(diag_units1)

# reverse the columns
reverse_cols = cols[::-1]
# diagonal units_2
diag_units2 = [val+reverse_cols[index] for index, val in enumerate(rows)]
print(diag_units2)

# total diagonal_units
diagonal_units = [diag_units1] + [diag_units2]
print(diagonal_units)

# the list of units 
unitlist = row_units + column_units + square_units + diagonal_units

# dictionaries
units = dict((s, [u for u in unitlist if s in u]) for s in boxes)
peers = dict((s, set(sum(units[s],[])) - set([s])) for s in boxes)




def naked_twins(values):
    """Eliminate values using the naked twins strategy.
    Args:
        values(dict): a dictionary of the form {'box_name': '123456789', ...}

    Returns:
        the values dictionary with the naked twins eliminated from peers.
    """
    
    for unit in unitlist:
        value_boxes = defaultdict(list)
        [value_boxes[values[box]].append(box) for box in unit if len(values[box]) == 2]
        
        for value, box_list in value_boxes.items():
            if len(box_list) == 2:
                peer_boxes = set(unit) - set(box_list)
                [assign_value(values, peer, values[peer].replace(item, '')) \
                    for peer in peer_boxes for item in value if item in values[peer]]
                            
    return values




def grid_values(grid):
    """Convert grid string into {<box>: <value>} dict with '123456789' value for empties.
    Args:
        grid: Sudoku grid in string form, 81 characters long
    Returns:
        Sudoku grid in dictionary form:
        - keys: Box labels, e.g. 'A1'
        - values: Value in corresponding box, e.g. '8', or '123456789' if it is empty.
    """
    values = []
    all_digits = '123456789'
    for c in grid:
        if c == '.':
            values.append(all_digits)
        elif c in all_digits:
            values.append(c)
    assert len(values) == 81
    return dict(zip(boxes, values))



def display(values):
    """
    Display the values as a 2-D grid.
    Input: The sudoku in dictionary form
    Output: None
    """
    width = 1+max(len(values[s]) for s in boxes)
    line = '+'.join(['-'*(width*3)]*3)
    for r in rows:
        print(''.join(values[r+c].center(width)+('|' if c in '36' else '')
                      for c in cols))
        if r in 'CF': print(line)
    print
    


def eliminate(values):
    """
    Go through all the boxes, and whenever there is unit box with a value , eliminate this value from the set of all its peers.
    
    Args: 
       Input : A Sudoku in dictionary form   
       Output : The resulting sudoku in dictionary form
    """
    solved_values = [box for box in values.keys() if len(values[box]) == 1]

    for solved_val in solved_values:
        digit = values[solved_val]
        peers_solv = peers[solved_val]
        for peer in peers_solv:
            values[peer] = values[peer].replace(digit,'')
    return values



def only_choice(values):
    
   """
   Go through all the boxes, and whenever there is a unit with a value that only fits in one box, assign the value to this box.
   
   Args: 
      Input : A Sudoku in dictionary form   
      Output : The resulting sudoku in dictionary form
   """
   for unit in unitlist:
       for digit in '123456789':
           dplaces = [box for box in unit if digit in values[box]]
           if len(dplaces)==1:
               # calling the assign_value function 
               assign_value(values, dplaces[0], digit)
   return values



def reduce_puzzle(values):
    """
    Iterate eliminate() and only_choice(). If at some point, there is a box with no available values, return False.
    If the sudoku is solved, return the sudoku.
    If after an iteration of both functions, the sudoku remains the same, return the sudoku.
    """
    
    solved_values = [box for box in values.keys() if len(values[box]) == 1]
    stalled = False
    while not stalled:
        solved_values_before = len([box for box in values.keys() if len(values[box]) == 1])
        values = eliminate(values)
        values = only_choice(values)
        values = naked_twins(values)

        solved_values_after = len([box for box in values.keys() if len(values[box]) == 1])
        stalled = solved_values_before == solved_values_after
        if len([box for box in values.keys() if len(values[box]) == 0]):
            return False
    return values



def search(values):
    "Using depth-first search and propagation, try all possible values"
    
    #  reduce the puzzle 
    values = reduce_puzzle(values)
    if values == False:
        return False

    if all(len(values[s]) == 1 for s in boxes):
        return values ## Solved!

    n,s = min((len(values[s]), s) for s in boxes if len(values[s]) > 1)
    for value in values[s]:
        new_sudoku = values.copy()
        new_sudoku[s] = value
        attempt = search(new_sudoku)
        if attempt:
            return attempt



def solve(grid):
    """
    Find the solution to a Sudoku grid.
    Args:
        grid(string): a string representing a sudoku grid.
            Example: '2.............62....1....7...6..8...3...9...7...6..4...4....8....52.............3'
    Returns:
        The dictionary representation of the final sudoku grid. False if no solution exists.
    """
    values = grid_values(grid)
    values = search(values)

    return values



if __name__ == '__main__':

    diag_sudoku_grid = '2.............62....1....7...6..8...3...9...7...6..4...4....8....52.............3'
    
    values = grid_values(diag_sudoku_grid)
    display(values)
    display(solve(diag_sudoku_grid))

    try:
        from visualize import visualize_assignments
        
        visualize_assignments(assignments)
    
    except SystemExit:
        pass
    except:
        print('We could not visualize your board due to a pygame issue. Not a problem! It is not a requirement.')