"""
    The syntax analysis class is the second phase in the compilation process.
    It takes the token stream the lexical analyzer returned and validate them 
    by comparing its order with the grammatical rules that were stablished.

"""

class syntaxAnalysis:

    # Initialize the main methods and variables
    def __init__(self, tokenTable):
        self.current = 0
        self.tokens = tokenTable
        self.tokens.append('$')
        self.declarationList()

        # At the end of the syntax analysis it indicates
        # whether it was successful or not
        if self.tokens[self.current] == '$':
            print("Syntax is OK!")
        else:
            raise Exception("Error with the Syntax Analyzer")

    # It validates the expected terminal token and the current token 
    # are the same value, if they are, it pass to the next token
    def match(self, expectedTerminal):
        # It verifies if it is a list because the ids and nums are 
        # inside another list.
        if type(self.tokens[self.current]) == list:
            if self.tokens[self.current][0] == expectedTerminal:
                self.current += 1
        elif self.tokens[self.current] == expectedTerminal:
            self.current += 1

    # First production rule, it enters when the current token is int or void.
    # Since it doesn't have a terminal symbol, it goes to the other productions inside it.
    def declarationList(self):
        if self.tokens[self.current] == 'int' or self.tokens[self.current] == 'void':
            self.declaration()
            self.declarationListPrime()

    # Next production rule, the condition is the same as the one above however since this
    # production have an epsilon, the elif indicates when it enters there it would return
    def declarationListPrime(self):
        if self.tokens[self.current] == 'int' or self.tokens[self.current] == 'void':
            self.declaration()
            self.declarationListPrime()
        elif self.tokens[self.current] == '$':
            return
    
    # A production rule with non-terminal symbols. 
    def declaration(self):
        self.funDeclaration()
        self.varDeclaration()
    
    # A production rule with non-terminal and terminal symbols.
    # When the terminal ones are reached it calls the match function
    # to verify it and finally returns it. 
    def varDeclaration(self):
        if self.tokens[self.current] == 'int':
            self.match('int')
            self.match('id')
            self.varDeclarationPrime()

    # A production rule with terminal symbols.
    # According to the current token value it may
    # match a different scenario.
    def varDeclarationPrime(self):
        if self.tokens[self.current] == ';':
            self.match(';')
        elif self.tokens[self.current] == '[':
            self.match('[')
            self.match('num')
            self.match(']')
            self.match(';')

    # A production rule with terminal symbols.
    # According to the current token value it may
    # match a different scenario.
    def typeSpecifier(self):
        if self.tokens[self.current] == 'int':
            self.match('int')
        elif self.tokens[self.current] == 'void':
            self.match('void')

    # Next production rule, it enters when the current token is int or void.
    # A production rule with non-terminal and terminal symbols.
    def funDeclaration(self):
        if self.tokens[self.current] == 'int' or self.tokens[self.current] == 'void':
            self.typeSpecifier()
            self.match('id')
            self.match('(')
            self.params()
            self.match(')')
            self.compoundStmt()
    
    # A production rule with terminal symbols.
    def params(self):
        self.paramList()
        if self.tokens[self.current] == 'void':
            self.match('void')

    # A production rule with non-terminal symbols.     
    def paramList(self):
        self.param()
        self.paramListPrime()

    # A production rule with non-terminal and terminal symbols.
    # When the terminal ones are reached it calls the match function
    # to verify it and finally returns it.
    def paramListPrime(self):
        if self.tokens[self.current] == ',':
            self.match(',')
            self.param()
            self.paramListPrime()
        elif self.tokens[self.current] == ')':
            self.match(')')

    # A production rule with non-terminal and terminal symbols.
    # When the terminal ones are reached it calls the match function
    # to verify it and finally returns it.
    def param(self):
        if self.tokens[self.current] == 'int':
            self.match('int')
            self.match('id')
            self.paramPrime()

    # A production rule with terminal symbols, and an e-production.
    def paramPrime(self):
        if self.tokens[self.current] == '[':
            self.match('[')
            self.match(']')
        elif self.tokens[self.current] == ',' or self.tokens[self.current] == ')':
            return

    # A production rule with non-terminal and terminal symbols.
    # When the terminal ones are reached it calls the match function
    # to verify it and finally returns it.
    def compoundStmt(self):
        if self.tokens[self.current] == '{':
            self.match('{')
            self.localDeclarations()
            self.statementList()
            self.match('}')
    
    # A production rule with non-terminal symbols. 
    def localDeclarations(self):
        self.localDeclarationsPrime()

    # A production rule with non-terminal symbols, and an e-production.
    def localDeclarationsPrime(self):
        if self.tokens[self.current] == 'int':
            self.varDeclaration()
            self.localDeclarationsPrime()
        # It verifies if it is a list because the id is 
        # inside another list.
        elif type(self.tokens[self.current]) == list:
            if self.tokens[self.current][0] == 'id':
                return
        elif (self.tokens[self.current] =='output' or self.tokens[self.current] == '{' or
            self.tokens[self.current] == 'if' or self.tokens[self.current] == 'while' or 
            self.tokens[self.current] == 'return' or self.tokens[self.current] == 'input'):
            return

    # A production rule with non-terminal symbols. 
    def statementList(self):
        self.statement()
        self.statementListPrime()

    # A production rule with non-terminal symbol, and an e-production.
    def statementListPrime(self):
        self.statement()
        if self.tokens[self.current] == '}':
            return

    # A production rule with non-terminal symbols. 
    def statement(self):
        self.assignmentStmt()
        self.callStmt()
        self.compoundStmt()
        self.selectionStmt()
        self.iterationStmt()
        self.returnStmt()
        self.inputStmt()
        self.outputStmt()

    def assignmentStmt(self):
        # It verifies if it is a list because the id is 
        # inside another list.
        if type(self.tokens[self.current]) == list:
            if self.tokens[self.current][0] == 'id':
                self.var()
                self.match('=')
                self.expression()
                self.match(';')

    # A production rule with non-terminal and terminal symbols.
    # When the terminal ones are reached it calls the match function
    # to verify it and finally returns it.
    def callStmt(self):
        self.call()
        if self.tokens[self.current] == ';':
            self.match(';')

    # A production rule with non-terminal and terminal symbols.
    # When the terminal ones are reached it calls the match function
    # to verify it and finally returns it.
    def selectionStmt(self):
        if self.tokens[self.current] == 'if':
            self.match('if')
            self.match('(')
            self.expression()
            self.match(')')
            self.statement()
            self.selectionStmtPrime()

    # A production rule with non-terminal and terminal symbols.
    # When the terminal ones are reached it calls the match function
    # to verify it and finally returns it.
    def selectionStmtPrime(self):
        if self.tokens[self.current] == 'else':
            self.match('else')
            self.statement()
        # It verifies if it is a list because the id is inside another list.
        elif type(self.tokens[self.current]) == list:
            if self.tokens[self.current][0] == 'id':
                return
        elif (self.tokens[self.current] == '{' or self.tokens[self.current] == 'if' or 
            self.tokens[self.current] == 'while' or self.tokens[self.current] == 'return' or 
            self.tokens[self.current] == 'input' or self.tokens[self.current] == 'output' or 
            self.tokens[self.current] == '}' or self.tokens[self.current] == 'else'):
            return

    # A production rule with non-terminal and terminal symbols.
    # When the terminal ones are reached it calls the match function
    # to verify it and finally returns it.
    def iterationStmt(self):
        if self.tokens[self.current] == 'while':
            self.match('while')
            self.match('(')
            self.expression()
            self.match(')')
            self.statement()

    # A production rule with non-terminal and terminal symbols.
    # When the terminal ones are reached it calls the match function
    # to verify it and finally returns it.
    def returnStmt(self):
        if self.tokens[self.current] == 'return':
            self.match('return')
            self.returnStmtPrime()

    # A production rule with terminal symbols.
    def returnStmtPrime(self): 
        if self.tokens[self.current] == ';':
            self.match(';')
        # It verifies if it is a list because the id and num are 
        # inside another list.
        elif type(self.tokens[self.current]) == list:
            if (self.tokens[self.current][0] == 'id' or 
                self.tokens[self.current][0] == 'num'):
                self.expression()
                self.match(';')
        elif self.tokens[self.current] == '(':
            self.expression()
            self.match(';')

    # A production rule with non-terminal and terminal symbols.
    # When the terminal ones are reached it calls the match function
    # to verify it and finally returns it.
    def inputStmt(self):
        if self.tokens[self.current] == 'input':
            self.match('input')
            self.var()
            self.match(';')

    # A production rule with non-terminal and terminal symbols.
    # When the terminal ones are reached it calls the match function
    # to verify it and finally returns it.
    def outputStmt(self):
        if self.tokens[self.current] == 'output':
            self.match('output')
            self.expression()
            self.match(';')

    # A production rule with non-terminal and terminal symbols.
    # When the terminal ones are reached it calls the match function
    # to verify it and finally returns it.
    def var(self):
        # It verifies if it is a list because the id is 
        # inside another list.
        if type(self.tokens[self.current]) == list:
            if self.tokens[self.current][0] == 'id':
                self.match('id')
                self.varPrime()

    # A production rule with non-terminal and terminal symbols.
    # When the terminal ones are reached it calls the match function
    # to verify it and finally returns it.
    def varPrime(self):
        if self.tokens[self.current] == '[':
            self.match('[')
            self.arithmeticExpression()
            self.match(']')
        elif (self.tokens[self.current] == ';' or self.tokens[self.current] == ',' or 
            self.tokens[self.current] == '=' or self.tokens[self.current] == '*' or 
            self.tokens[self.current] == '/' or self.tokens[self.current] == '+' or 
            self.tokens[self.current] == '-' or self.tokens[self.current] == ']' or 
            self.tokens[self.current] == '<=' or self.tokens[self.current] == '<' or 
            self.tokens[self.current] == '>' or self.tokens[self.current] == '>=' or 
            self.tokens[self.current] == '==' or self.tokens[self.current] == '!=' or 
            self.tokens[self.current] == ')' or self.tokens[self.current] == ','):
            return

    # A production rule with non-terminal symbols. 
    def expression(self):
        self.arithmeticExpression()
        self.expressionPrime()

    # A production rule with non-terminal symbols, and an e-production.
    def expressionPrime(self):
        self.relop()
        self.arithmeticExpression()
        if self.tokens[self.current] == ')' or self.tokens[self.current] ==  ';':
            return

    # A production rule with terminal symbols.
    def relop(self):
        if self.tokens[self.current] == '<=':
            self.match('<=')
        elif self.tokens[self.current] == '<':
            self.match('<')
        elif self.tokens[self.current] == '>':
            self.match('>')
        elif self.tokens[self.current] == '>=':
            self.match('>=')
        elif self.tokens[self.current] == '==':
            self.match('==')
        elif self.tokens[self.current] == '!=':
            self.match('!=')

    # A production rule with non-terminal symbols. 
    def arithmeticExpression(self):
        self.term()
        self.arithmeticExpressionPrime()

    # A production rule with non-terminal symbols, and an e-production.
    def arithmeticExpressionPrime(self):
        if self.tokens[self.current] == '+' or self.tokens[self.current] == '-':
            self.addop()
            self.term()
            self.arithmeticExpressionPrime()
        elif (self.tokens[self.current] == ']' or self.tokens[self.current] == '<=' or
            self.tokens[self.current] == '<' or self.tokens[self.current] == '>' or 
            self.tokens[self.current] == '>=' or self.tokens[self.current] == '==' or 
            self.tokens[self.current] == '!=' or self.tokens[self.current] == ')' or 
            self.tokens[self.current] == ';' or self.tokens[self.current] == ','):
            return

    # A production rule with terminal symbols.
    def addop(self):
        if self.tokens[self.current] == '+':
            self.match('+')
        elif self.tokens[self.current] == '-':
            self.match('-')

    # A production rule with non-terminal symbols. 
    def term(self):
        self.factor()
        self.termPrime()

    # A production rule with non-terminal symbols, and an e-production.
    def termPrime(self):
        if self.tokens[self.current] == '*' or self.tokens[self.current] == '/':
            self.mulop()
            self.factor()
            self.termPrime()
        elif (self.tokens[self.current] == '+' or self.tokens[self.current] == '-' or 
            self.tokens[self.current] == ']' or self.tokens[self.current] == '<=' or 
            self.tokens[self.current] == '<' or self.tokens[self.current] == '>' or 
            self.tokens[self.current] == '>=' or self.tokens[self.current] == '==' or 
            self.tokens[self.current] == '!=' or self.tokens[self.current] == ')' or 
            self.tokens[self.current] == ';' or self.tokens[self.current] == ','):
            return

    # A production rule with terminal symbols.
    def mulop(self):
        if self.tokens[self.current] == '*':
            self.match('*')
        elif self.tokens[self.current] == '/':
            self.match('/')

    # A production rule with non-terminal and terminal symbols.
    # When the terminal ones are reached it calls the match function
    # to verify it and finally returns it.
    def factor(self):
        if self.tokens[self.current] == '(':
            self.match('(')
            self.arithmeticExpression()
            self.match(')')
        # It verifies if it is a list because the id and num are 
        # inside another list.
        elif type(self.tokens[self.current]) == list:
            if self.tokens[self.current][0] == 'id': 
                if self.tokens[self.current+1] != '(':
                    self.var()
            elif self.tokens[self.current][0] == 'id': 
                if self.tokens[self.current+1] == '(':
                    self.call()
            elif self.tokens[self.current][0] == 'num':
                self.match('num')

    # A production rule with non-terminal and terminal symbols.
    # When the terminal ones are reached it calls the match function
    # to verify it and finally returns it.
    def call(self):
        # It verifies if it is a list because the id is 
        # inside another list.
        if type(self.tokens[self.current]) == list:
            if self.tokens[self.current][0] == 'id':
                self.match('id')
                self.match('(')
                self.args()
                self.match(')')

    # A production rule with non-terminal symbol, and an e-production.
    def args(self):
        self.argsList()
        if self.tokens[self.current] == ')':
            return

    # A production rule with non-terminal symbols. 
    def argsList(self):
        self.arithmeticExpression()
        self.argsListPrime()
    
    # A production rule with non-terminal and terminal symbols.
    # When the terminal ones are reached it calls the match function
    # to verify it and finally returns it.
    def argsListPrime(self):
        if self.tokens[self.current] == ',':
            self.match(',')
            self.arithmeticExpression()
            self.argsListPrime()
        elif self.tokens[self.current] == ')':
            return
