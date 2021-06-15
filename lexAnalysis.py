# Library imported to use regular expressions
import re

"""
    The lexical analysis class is the first phase in the compilation process.
    It takes a character stream that pass through the analyzer and returns
    a token stream for all the lexemes (delimiters, keywords, numbers and variables)
    found in the character stream.
"""

class lexAnalysis:

    # Initialize the arrays
    def __init__(self):
        self.symbolTable = []
        self.errors = []
        self.varTable = []
        self.numTable = []
        self.delimiters = [' ', '!=', '(', ')', '*', '+', ',', '-', '/',
                            ';', '<', '=', '>', '[', ']', '{', '}']
        self.keywords = ['else', 'if', 'input', 'int', 'output', 'return', 'void', 'while']

    # Function to traverse through the arrays
    # The array values must be in order
    # From the lowest to the highest
    def binarySearch(self, arr, l, r, x):
        if r >= l:
            mid = l + (r - l) // 2
    
            if arr[mid] == x:
                return mid
            elif arr[mid] > x:
                return self.binarySearch(arr, l, mid-1, x)
            else:
                return self.binarySearch(arr, mid + 1, r, x)
        else:
            return -1

    # Function which takes the content in the file
    # and classifies it.
    def analizer(self, phrase):
        each = 0
        comm = False
        n_key = len(self.keywords)
        n_del = len(self.delimiters)

        # It traverse each of the words from the main input file
        for each in phrase:

            # Regular expressions are used to classify each word
            num = re.search(r'[0-9]', each)
            letter = re.search(r'[a-zA-Z]', each)

            # Since delimiters and keywords are already known by the 
            # compiler, a binary search is made to look for a certain
            # symbol or word
            result = self.binarySearch(self.keywords, 0, n_key-1, each)
            result2 = self.binarySearch(self.delimiters, 0, n_del-1, each)

            # According to each data type, it is stored in their respective
            # array, also comm is used in case there is a comment
            if num and comm == False:
                self.numTable.append("num," + each)
            elif result != -1 and comm == False:
                self.symbolTable.append(each)
            elif result2 != -1 and comm == False:
                self.symbolTable.append(each)
            elif letter and comm == False:
                self.varTable.append("id," + each)
            elif each == '/*':
                comm = True
            elif comm == True:
                pass
            elif each == '*/':
                comm = False
            else:
                self.errors.append(each)
                print("Error in " + each + "\n")

        # The varTable and the numTable are extended to the 
        # symbolTable to form a single array
        self.symbolTable.extend(self.varTable + self.numTable)

        print("Symbol table: ")
        for n in self.symbolTable:
            print("<" + str(n) + ">", end=" ")
        print("\n")

        print("\nError list: ")
        for n in self.errors:
            print("<" + str(n) + ">")
        print("\n")

