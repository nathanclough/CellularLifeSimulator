import sys
import os
import getopt
import Simulation


def main(argv):
    InputPath = ""
    OutputPath = ""
    ThreadCount = 1
    # Read in the input
    try:
        opts, args = getopt.getopt(argv, "hi:o:t:", ["ifile=", "ofile="])
    except getopt.GetoptError:
        print('test.py -i <inputfile> -o <outputfile>')
        sys.exit(2)

    # Parse Arguments
    for opt, arg in opts:
        # Help option
        if opt == '-h':
            print('test.py -i <inputfile> -o <outputfile>')
            sys.exit()
        # Input file option
        elif opt in ("-i", "--ifile"):
            InputPath = arg
        # Output file option
        elif opt in ("-o", "--ofile"):
            OutputPath = arg
        elif opt in ("-t", "--cthreads"):
            ThreadCount = int(arg)
    print("Project :: R11568824")
    # Validate Arguments are given
    if ThreadCount <= 0:
        print("Error ThreadCount -t must be > 0")
        sys.exit(2)
    elif InputPath == "":
        print("Error InputPath -i is requried")
        sys.exit(2)
    elif OutputPath == "":
        print("Error OutputPath -o is requried")
        sys.exit(2)

    # Validate InputFile exists
    if os.path.isfile(InputPath) != True:
        print("Error input file " + InputPath + " does not exist")
        sys.exit(2)

    # Validate OutputFile path exists?

    # Begin Simulation
    s = Simulation.Simulation(ThreadCount, InputPath, OutputPath)
    s.Begin()


if (__name__ == "__main__"):
    main(sys.argv[1:])
