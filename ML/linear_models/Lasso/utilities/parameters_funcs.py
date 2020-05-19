import sys


#prints how to run program 
def usage():
    print("1) python3 lasso_regression.py <percentage (in %)> <input_file> <target parameter>")
    print("2) python3 lasso_regression.py --help")


# gets input arguments of program
def getArguments(argv):

    percentage = 0
    input_file = ''

    if argv[1] == "--help":
        usage()
        sys.exit(0)
    if len(argv) < 4:
        usage()
        sys.exit(1)
    
    
    try:
        percentage = int(argv[1])
    except ValueError:
        print("Couldn't convert parcentage to integer. You gave '{}'".format(argv[1]))
        sys.exit(2)

    input_file = argv[2]

    target= argv[3]

    return percentage, input_file, target
