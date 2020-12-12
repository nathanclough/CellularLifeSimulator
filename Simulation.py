import multiprocessing
import math
import re
import sys

CurrentStep = []
MaxRow = 0
MaxCol = 0
NextStep = []


def Run(ThreadCount, InputPath, OutputPath):

    global MaxRow
    global MaxCol
    global CurrentStep
    global NextStep

    # Create a matrix from the input file
    if not CreateMatrix(InputPath):
        print("Error file contains invalid values")
        sys.exit(2)
    # Else if file is clean run simulation
    else:
        # Initialize the next step to the current
        MaxRow = len(CurrentStep)-1
        # sutract 1 for /n and one for indexstart 0
        MaxCol = len(CurrentStep[0])-1

        # Initialize the partition value, process pool and a list for processes
        part = math.floor(len(CurrentStep)/ThreadCount)
        processes = []
        processPool = multiprocessing.Pool(processes=ThreadCount)
        for x in range(100):

            poolData = list()
            start = 0
            end = part

            # Create matrix data for each thread consisting of a copy of the CurrentStep matrix,
            # a start row and an end row
            for x in range(ThreadCount-1):
                matrixData = [CurrentStep, start, end]

                # Store the matrixData in poolData list
                poolData.append(matrixData)
                start += part
                end += part

            # For the last partition use MaxRow + 1 so that it can truncate in the case of
            # an uneven partition
            matrixData = [CurrentStep, start, MaxRow+1]
            poolData.append(matrixData)

            # Map each value in poolData to a SimulationJob
            # .map performs a scatter gather: starts the processes and waits for the results of each
            # storing them in finalData
            finalData = processPool.map(SimulationJob, poolData)

            # Iterate through final data and stitch together the CurrentStep matrix from the
            # results of each job
            CurrentStep = []
            for result in finalData:
                for row in result:
                    r = []
                    for item in row:
                        r.append(item)
                    CurrentStep.append(r)

        # Print to the output file
        outputFile = open(OutputPath, 'w')
        for row in CurrentStep:
            for char in row:
                print(char, sep="", end="", file=outputFile)
            print("", file=outputFile)


def SimulationJob(poolData):
    matrix = poolData[0]
    start = int(poolData[1])
    end = int(poolData[2])
    MaxRow = len(matrix)-1
    MaxCol = len(matrix[0])-1
    nextStep = []
    for row in range(start, end):
        r = []
        for col in range(MaxCol+1):
            result = matrix[row][col]
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

            if(matrix[rowDown][colRight] == 'O'):
                CountAlive += 1
            if(matrix[rowUp][colLeft] == 'O'):
                CountAlive += 1
            if(matrix[rowUp][colRight] == 'O'):
                CountAlive += 1
            if(matrix[rowDown][colLeft] == 'O'):
                CountAlive += 1
            if(matrix[row][colRight] == 'O'):
                CountAlive += 1
            if(matrix[row][colLeft] == 'O'):
                CountAlive += 1
            if(matrix[rowDown][col] == 'O'):
                CountAlive += 1
            if(matrix[rowUp][col] == 'O'):
                CountAlive += 1

            isAlive = matrix[row][col] == 'O'

            # if currently alive
            if isAlive:
                # and has 2 3 or 4 CountAlive
                if not(CountAlive == 2 or CountAlive == 3 or CountAlive == 4):
                    result = '.'
            else:
                # currently dead
                if CountAlive > 0 and (CountAlive % 2 == 0):
                    # Alive next step
                    result = 'O'
            r.append(result)
        nextStep.append(r)
    return nextStep


def CreateMatrix(InputPath):
    f = open(InputPath)
    global CurrentStep

    temp = f.readlines()
    for row in temp:
        row = row.strip('\n')
        r = []
        for char in row:
            if char == 'O' or char == '.' or char == '\n':
                r.append(char)
            else:
                return False
        CurrentStep.append(r)
    return True
