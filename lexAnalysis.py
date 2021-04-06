import re

#ID = re.findall([a-zA-Z])
#num = re.findall([0-9])
state = 0

class lexAnalysis:
    # Se inicializan aquí porque es el analizador léxico y porque eso no cambia
    # a diferencia de las variables las cuales conforme se crean, se guardan.
    def __init__(self):
        # Ordenados por ASCII
        # https://www.ascii-code.com/
        self.delimiters = [' ', '!', '(', ')', '*', '+', ',', '-', '/',
                            ';', '<', '=', '>', '[', ']', '{', '}']
        self.keywords = ['else', 'if', 'input', 'int', 'output', 'return', 'void', 'while'] 

    # https://www.geeksforgeeks.org/binary-search/
    # The array used must be sorted from smallest to longest
    def binarySearch (self, arr, l, r, x):
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

    # Hacer que sirva para los keywords y los delimitadores separarlos por tipo, tal vez un if 
    def test_regex(self, words):
        nKey = len(self.keywords)
        nDel = len(self.delimiters)

        result = self.binarySearch(self.keywords, 0, nKey-1, words)
        result2 = self.binarySearch(self.delimiters, 0, nDel-1, words)
        
        if result != -1:
            print ("Element is present at index %d" % result)
        elif result2 != -1:
            print ("Element is present at index %d" % result2)
        else:
            print ("Element is not present in array")


if __name__ == "__main__":
    print("A ver escribe algo")
    word = input()
    lexAnalysis().test_regex(word)
    #print(lexAnalysis().main_analysis(1))

