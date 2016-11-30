def classify(v, r, c):
    # Input: value, value's row, value's column
    # Return: circular dependency error, 'cell', 'number', or 'operator'
    if v[0] in alphabet:
        if v[0] == r and int(v[1:]) == c:
            print('Error:circular dependency!')
        else:
            return 'cell'
    elif v == '+' or v == '-' or v == '*' or v == '/':
        return 'operator'
    else:
        try:
            if type(int(v)) == int:
                return 'number'
        except ValueError:
            print('Error:invalid input')

def update_pointers(sol, index, circ_check):
    # Updates all cells that point to the index cell
    for v in pointers[index]:
        row = v[0]
        col = int(v[1:])
        classify(v, circ_check[0], int(circ_check[1:]))
        spreadsheet[row][col] = sol
        if v in pointers:
            update_pointers(sol, v, circ_check)

class QueuedCalc:
    # Class to keep track of expressions that need to be evaluated later
    def __init__(self, line, row, column):
        self.l = line
        self.r = row
        self.c = column

def calculate(line, curr_row, curr_col):
    # Calculates line according to Reverse Polish Notation
    curr_index = curr_row + str(curr_col)
    input_stack = []

    for value in line:
        classification = classify(value, curr_row, curr_col)

        if classification == 'cell':
            cell_row = value[0]
            cell_col = int(value[1:])
            cell_value = spreadsheet[cell_row][cell_col]
            if cell_value == None:
                return False
            input_stack.append(float(cell_value))
        elif classification == 'number':
            if value == None:
                return False
            input_stack.append(float(value))
        elif classification == 'operator':
            operand1 = input_stack.pop()
            operand2 = input_stack.pop()
            if operand1 == None or operand2 == None:
                return False

            if value == '+':
                ans = operand2 + operand1
                input_stack.append(ans)
            elif value == '-':
                ans = operand2 - operand1
                input_stack.append(ans)
            elif value == '*':
                ans = operand2 * operand1
                input_stack.append(ans)
            elif value == '/':
                ans = operand2 / operand1
                input_stack.append(ans)

    sol = input_stack.pop()
    spreadsheet[curr_row][curr_col] = sol
    if curr_index in pointers:
        update_pointers(sol, curr_index, curr_index)
    return True


dimensions = input().split(' ')
num_col = int(dimensions[0])
num_row = int(dimensions[1])
alphabet = [chr(i) for i in range(ord('A'), ord('Z')+1)]

spreadsheet = {}
calc_queue = []
pointers = {}

# Note: Creates an extra col 0 that is not used to allow ease of starting from 1
for i in range(0, num_row):
    spreadsheet[alphabet[i]] = [None for x in range(0, num_col+1)]

# Iterate through lines and set cell and number values
for i in range(1, num_col*num_row+1):
    curr_row = alphabet[int((i-1) / num_col)]
    curr_col = i % num_col or num_col
    curr_index = curr_row + str(curr_col)
    line = input().split(' ')

    # STRANGE PROBLEM IN 4TH TEST CASE
    for l in line:
        if l == '':
            raise ValueError

    if len(line) == 1:
        value = line[0]
        classification = classify(value, curr_row, curr_col)

        if classification == 'cell':
            cell_row = value[0]
            cell_col = int(value[1:])
            spreadsheet[curr_row][curr_col] = spreadsheet[cell_row][cell_col]

            if value not in pointers:
                pointers[value] = []
            pointers[value].append(curr_index)

        elif classification == 'number':
            spreadsheet[curr_row][curr_col] = float(value)
    else:
        # Queue RPN expressions for after all cells and numbers are set
        calc_queue.append(QueuedCalc(line, curr_row, curr_col))

# Iterate through again to make sure that any pointers are up to date
for i in range(1, num_col*num_row+1):
    curr_row = alphabet[int((i-1) / num_col)]
    curr_col = i % num_col or num_col
    curr_index = curr_row + str(curr_col)

    if curr_index in pointers:
        update_pointers(spreadsheet[curr_row][curr_col], curr_index, curr_index)

# Calculate RPN expressions
for c in calc_queue:
    if not calculate(c.l, c.r, c.c):
        calc_queue.append(c)

# Print out the output of cells
for i in range(1, num_col*num_row+1):
    curr_row = alphabet[int((i-1) / num_col)]
    curr_col = i % num_col or num_col

    print(format(spreadsheet[curr_row][curr_col], '.5f'))
