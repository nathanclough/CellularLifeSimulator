import multiprocessing
import math


class Simulation:
    def __init__(self, T, inputFile, OutputFile):
        self.m = multiprocessing.Manager()
        self.CurrentStep = self.m.list()
        self.NextStep = self.m.list()
        self.inputPath = inputFile
        self.lock = multiprocessing.Lock()
        self.ThreadCount = T
        self.events = []
        self.processes = []
        self.running = True
        self.Continue = multiprocessing.Event()
        self.CreateMatrix()
        self.MaxRow = len(self.CurrentStep)-1
        self.MaxCol = len(self.CurrentStep[0])-2

    def CreateMatrix(self):
        f = open(self.inputPath)
        temp = f.readlines()
        for row in temp:
            self.CurrentStep.append([char for char in row])

    def Begin(self):
        # Partition the rows for thread assignments
        part = math.floor(len(self.CurrentStep)/self.ThreadCount)
        start = 0
        end = part
        for x in range(self.ThreadCount-1):
            e = multiprocessing.Event()
            p = multiprocessing.Process(
                target=self.SimulateSection, args=(self, start, end, e))
            self.events.append(e)
            self.processes.append(p)
            start += part
            end += part

        e = multiprocessing.Event()
        p = multiprocessing.Process(
            target=self.SimulateSection, args=(self, start, self.MaxRow+1, e))
        self.events.append(e)
        self.processes.append(p)

        for p in self.processes:
            p.start()
        for x in range(100):
            # Wait for  all the threads to finish calculating the next step in simulation
            for event in self.events:
                event.wait()

            # Write simulation to Current Step
            for row in range(MaxRow+1):
                for col in range(MaxCol + 1):
                    self.CurrentStep[row][col] = self.NextStep[row][col]

            # Reset the events for this round
            for event in self.events:
                event.clear()

            # Notify them they can do the next step
            self.Continue.set()

            # Reset for the next iteration
            self.Continue.clear()
        self.WriteMatrix()
        self.SimulationProcess.running = False
        self.Continue.set()

    def SimulateSection(self, start, end, CompletedStep):
        while(self.running):
            for row in range(start, end, m):
                for col in range(self.MaxCol + 1):
                    CalculateNextState(row, col)
            CompletedStep.set()
            Continue.wait()
        return

    def CalculateNextState(self, row, col):
        CountAlive = 0
        # Indexes for finding neighbors in the matrix
        rowDown = row + 1
        rowUp = row - 1
        colRight = col + 1
        colLeft = col - 1
        print(row, col)

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
                lock.acquire()
                self.NextStep[row][col] = '.'
                lock.release()
        else:
            # currently dead
            if CountAlive > 0 and (CountAlive % 2 == 0):
                # Alive next step
                lock.acquire()
                self.NextStep[row][col] = 'O'
                lock.release()

    def WriteMatrix(self):
        outputFile = open(self.OutputPath, 'w')
        for row in CurrentStep:
            for char in row:
                print(char, sep="", end="", file=outputFile)
