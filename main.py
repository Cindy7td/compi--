from lexAnalysis import lexAnalysis

class Compiler:
    def __init__(self):
        file = open('test.txt', 'r')

        # Tiene que leer todo el documento, palabra por palabra 
        # para determinar que es cada cosa
        # Una vez que llega al final del doc, termina el codigo
        # Devuelve la explicacion de cada palabra/del/simbolo
        lexAnalysis().test_regex(file)
        file.close()

if __name__ == "__main__":
    Compiler().__init__()
