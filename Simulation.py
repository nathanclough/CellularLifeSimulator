import threading
CurrentStep = []
MaxRow = 0
MaxCol = 0
NextStep = []


def Run(ThreadCount, InputPath, OutputPath):
    CreateMatrix(InputPath)
    global MaxRow
    global MaxCol
    global CurrentStep
    global NextStep

    # Initialize the next step to the current
    MaxRow = len(CurrentStep)-1
    MaxCol = len(CurrentStep[0])-2  # sutract 1 for /n and one for indexstart 0
    # InitializeNextStep to be current
    NextStep = [[char for char in row] for row in CurrentStep]

    WriteMatrix(OutputPath)
    # Create a matrix from the input file
    # iterate through currentStep and write values to next step
    for x in range(100):
        # Initialize empty matrix for tracking changes
        for row in range(MaxRow+1):
            for col in range(MaxCol+1):
                CalculateNextState(row, col)
        # set CurrentStep = to step Calculated in NextStep
        CurrentStep = [[char for char in row] for row in NextStep]
        WriteMatrix(OutputPath)
    # Iterate through the matrix simulating the next step
    WriteMatrix(OutputPath)

# Given the row, col index in CurrentStep calculates
# the next step for that position and writes it to NextStep


def CalculateNextState(row, col):
    CountAlive = 0
    # Indexes for finding neighbors in the matrix
    rowDown = row + 1
    rowUp = row - 1
    colRight = col + 1
    colLeft = col - 1

    if row == MaxRow:
        rowDown = 0
    elif row == 0:
        rowUp = MaxRow
    if col == 0:
        colLeft = MaxCol
    elif col == MaxCol:
        colRight = 0

    if(CurrentStep[rowDown][colRight] == 'O'):
        CountAlive += 1
    if(CurrentStep[rowUp][colLeft] == 'O'):
        CountAlive += 1
    if(CurrentStep[rowUp][colRight] == 'O'):
        CountAlive += 1
    if(CurrentStep[rowDown][colLeft] == 'O'):
        CountAlive += 1
    if(CurrentStep[row][colRight] == 'O'):
        CountAlive += 1
    if(CurrentStep[row][colLeft] == 'O'):
        CountAlive += 1
    if(CurrentStep[rowDown][col] == 'O'):
        CountAlive += 1
    if(CurrentStep[rowUp][col] == 'O'):
        CountAlive += 1

    isAlive = CurrentStep[row][col] == 'O'

    # if currently alive
    if isAlive:
        # and has 2 3 or 4 CountAlive
        if not(CountAlive == 2 or CountAlive == 3 or CountAlive == 4):
            NextStep[row][col] = '.'
    else:
        # currently dead
        if CountAlive > 0 and (CountAlive % 2 == 0):
            # Alive next step
            NextStep[row][col] = 'O'


def CreateMatrix(InputPath):
    f = open(InputPath)
    global CurrentStep

    temp = f.readlines()
    for row in temp:
        CurrentStep.append([char for char in row])


def WriteMatrix(OutputPath):
    outputFile = open(OutputPath, 'w')
    for row in CurrentStep:
        for char in row:
            print(char, sep="", end="", file=outputFile)
