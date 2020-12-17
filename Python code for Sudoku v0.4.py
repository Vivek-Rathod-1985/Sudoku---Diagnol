rows = 'ABCDEFGHI'
cols = '123456789'

def cross(a, b):
    return [s+t for s in a for t in b]

boxes = cross(rows, cols)

row_units = [cross(r, cols) for r in rows]
column_units = [cross(rows, c) for c in cols]
square_units = [cross(rs, cs) for rs in ('ABC','DEF','GHI') for cs in ('123','456','789')]

diagonal_units = [[rows[i] + cols[i] for i in range(9)]] + [[rows[i] + cols[::-1][i] for i in range(9)]]

unitlist = row_units + column_units + square_units + diagonal_units
units = dict((s, [u for u in unitlist if s in u]) for s in boxes)
peers = dict((s, set(sum(units[s],[]))-set([s])) for s in boxes)

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
    return

def grid_values(grid):
    """
    Convert grid into a dict of {square: char} with '123456789' for empties.
    Input: A grid in string form.
    Output: A grid in dictionary form
            Keys: The boxes, e.g., 'A1'
            Values: The value in each box, e.g., '8'. If the box has no value, then the value will be '123456789'.
    """
    chars = []
    digits = '123456789'
    for c in grid:
        if c in digits:
            chars.append(c)
        if c == '.':
            chars.append(digits)
    assert len(chars) == 81
    return dict(zip(boxes, chars))


def naked_twins(values):
    """Eliminate values using the naked twins strategy.
    
    Parameters:
    values(dict)
        a dictionary of the form {"box_name": "123456789", ...}
    Returns:
    dict
        The values dictionary with the naked twins eliminated from peers
    """
    for unit in unitlist:
        for box in unit:
            # Look for boxes that have 2 digits
            if len(values[box]) == 2:
                # Search for a twin of the current box
                for peer in unit:
                    if box != peer and values[box] == values[peer]:
                        # Eliminate the naked twins as possibilities for their peers
                        for peer2 in unit:
                            if peer2 != box and peer2 != peer:
                                values = assign_value(values, peer2, values[peer2].replace(values[box][0],""))
                                values = assign_value(values, peer2, values[peer2].replace(values[box][1],""))
    return values
  

def eliminate(values):
    """
    Go through all the boxes, and whenever there is a box with a value, eliminate this value from the values of all its peers.
    Input: A sudoku in dictionary form.
    Output: The resulting sudoku in dictionary form.
    """
    solved_values = [box for box in values.keys() if len(values[box]) == 1]
    for box in solved_values:
        digit = values[box]
        for peer in peers[box]:
            values[peer] = values[peer].replace(digit,'')
    return values

def only_choice(values):
    """
    Go through all the units, and whenever there is a unit with a value that only fits in one box, assign the value to this box.
    Input: A sudoku in dictionary form.
    Output: The resulting sudoku in dictionary form.
    """
    for unit in unitlist:
        for digit in '123456789':
            dplaces = [box for box in unit if digit in values[box]]
            if len(dplaces) == 1:
                values[dplaces[0]] = digit
    return values

def reduce_puzzle(values):
    """
    Iterate eliminate() and only_choice(). If at some point, there is a box with no available values, return False.
    If the sudoku is solved, return the sudoku.
    If after an iteration of both functions, the sudoku remains the same, return the sudoku.
    Input: A sudoku in dictionary form.
    Output: The resulting sudoku in dictionary form.
    """
    solved_values = [box for box in values.keys() if len(values[box]) == 1]
    stalled = False
    while not stalled:
        solved_values_before = len([box for box in values.keys() if len(values[box]) == 1])
        values = eliminate(values)
        values = only_choice(values)
        
         # Use the Naked Twins Strategy
        values = naked_twins(values)
        
        solved_values_after = len([box for box in values.keys() if len(values[box]) == 1])
        stalled = solved_values_before == solved_values_after
        if len([box for box in values.keys() if len(values[box]) == 0]):
            return False
    return values


def search(values):
    "Using depth-first search and propagation, create a search tree and solve the sudoku."
    # First, reduce the puzzle using the previous function
    
    # Choose one of the unfilled squares with the fewest possibilities
    
    # Now use recursion to solve each one of the resulting sudokus, and if one returns a value (not False), return that answer!

    # If you're stuck, see the solution.py tab!
    
    "Using depth-first search and propagation, try all possible values."
    # First, reduce the puzzle using the previous function
    values = reduce_puzzle(values)
    if values is False:
        return False ## Failed earlier
    if all(len(values[s]) == 1 for s in boxes): 
        return values ## Solved!
    # Choose one of the unfilled squares with the fewest possibilities
    n,s = min((len(values[s]), s) for s in boxes if len(values[s]) > 1)
    # Now use recurrence to solve each one of the resulting sudokus, and 
    for value in values[s]:
        new_sudoku = values.copy()
        new_sudoku[s] = value
        attempt = search(new_sudoku)
        if attempt:
            return attempt
        

#grid = '..3.2.6..9..3.5..1..18.64....81.29..7.......8..67.82....26.95..8..2.3..9..5.1.3..'
#grid = '4.....8.5.3..........7......2.....6.....8.4......1.......6.3.7.5..2.....1.4......'
grid = '2.............62....1....7...6..8...3...9...7...6..4...4....8....52.............3'

grid_complete  = grid_values(grid)

print("\n Complete Soduku \n")

#display(grid_complete)


grid_nakedtwins = naked_twins(grid_complete)


print("\n Eliminated Soduku \n")

grid_eliminate = eliminate(grid_nakedtwins)

#display(grid_eliminate)

print("\n Only choice Soduku \n")

grid_onlychoice = only_choice(grid_eliminate)

#display(grid_onlychoice)

print("\n Reduce Soduku \n")

grid_reducepuzzle = reduce_puzzle(grid_onlychoice)

#display(grid_reducepuzzle)

print("\n Search Soduku \n")

grid_search = search(grid_reducepuzzle)

display(grid_search)

#Pune@city54321

