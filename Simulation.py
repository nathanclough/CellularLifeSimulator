import threading
import math

CurrentStep = []
MaxRow = 0
MaxCol = 0
NextStep = []
OutputPath = ""
events = []
Continue = threading.Event()


def Run(ThreadCount, InputPath, outputPath):
    CreateMatrix(InputPath)
    global MaxRow
    global MaxCol
    global CurrentStep
    global NextStep
    global OutputPath
    global events

    OutputPath = outputPath
    # Initialize the next step to the current
    MaxRow = len(CurrentStep)-1
    MaxCol = len(CurrentStep[0])-2  # sutract 1 for /n and one for indexstart 0
    # InitializeNextStep to be current
    NextStep = [[char for char in row] for row in CurrentStep]

    # Partition the rows for thread assignments
    part = math.floor(len(CurrentStep)/ThreadCount)
    start = 0
    end = part

    # Create the threads
    threads = []
    events = []
    # For thread count - 1 add partition and add to the pool
    for x in range(ThreadCount-1):
        e = threading.Event()
        t = SimulationThread(start, end, e)
        events.append(e)
        threads.append(t)
        start += part
        end += part

    # Add the final thread truncing it to the MaxRow rather than end because end is > than size of
    e = threading.Event()
    t = SimulationThread(start, MaxRow+1, e)
    events.append(e)
    threads.append(t)

    for thread in threads:
        thread.start()

    for x in range(100):
        # Wait for  all the threads to finish calculating
        for event in events:
            event.wait()

        for row in range(MaxRow+1):
            for col in range(MaxCol + 1):
                CurrentStep[row][col] = NextStep[row][col]

        # Reset the events for this round
        for event in events:
            event.clear()

        # Notify them they can do the next step

        Continue.set()
        # Reset for the next run
        Continue.clear()

    WriteMatrix()
    SimulationThread.running = False
    Continue.set()


# Given a start row and end row this function will calculate next state for those rows


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


def WriteMatrix():
    outputFile = open(OutputPath, 'w')
    for row in CurrentStep:
        for char in row:
            print(char, sep="", end="", file=outputFile)


class SimulationThread(threading.Thread):
    running = True

    def __init__(self, StartRow, EndRow, CompletedStep):
        threading.Thread.__init__(self)
        self.StartRow = StartRow
        self.EndRow = EndRow
        self.CompletedStep = CompletedStep

    def run(self):
        while(self.running):
            for row in range(self.StartRow, self.EndRow):
                for col in range(MaxCol + 1):
                    CalculateNextState(row, col)
            self.CompletedStep.set()
            Continue.wait()
