from anytree import Node, RenderTree

from scanner import Scanner
from scanner import TokenType

class Parser:
    def __init__(self, tokens, keywords):
        self.tokens = tokens
        self.index = 0
        self.keywords = keywords
        self.Tree = Node("")
        self.currNode = self.Tree


        self.parseTokens()

    #Parse Tree Function
    def addNode(self, child, parent):
        child.parent = parent
        self.currNode = child

    #Token Types
    INT = 'INT'
    FLOAT = 'FLOAT'
    STRING = 'STRING'
    SINGLE_CHAR = 'CHAR'
    REMARK = 'REM'

    def advance(self):
        self.index += 1
        if self.index < len(self.tokens):
            self.current = self.tokens[self.index]

    def parseTokens(self):
        if len(self.tokens) > 0:
            root = self.program()
        for key in self.tokens:
            tok = [key,self.tokens[key]]

            #if key is a line number
            if tok[0].isnumeric:
                self.statement(tok[1])
            self.currNode = root

    def program(self):
        p = Node("Program")
        self.addNode(p, self.Tree)

        return p

    def statement(self,tok):
        statement = Node("Statement")
        self.addNode(statement, self.currNode)
        #if the #1 index contains a nested dictionary pass it back to through the function or
        #analyze entire dictionary in this function.

        for t in tok:
            if t.type == "KEYWORD":
                k = Node("Keyword")
                if t.goto != None:
                    self.keyword(t.value + ":" + str(t.goto), k)
                    self.currNode = k
                    self.addNode(k, statement)   
                else:
                    self.keyword(t.value, k)
                    self.currNode = k
                    self.addNode(k, statement)     

            if t.type == "CHAR":
                c = Node("Char")
                self.currNode = c
                self.addNode(Node(t.value), c)
                self.addNode(c, statement)

            if t.type == "STRING":
                s = Node("String")
                self.currNode = s
                self.addNode(Node(t.value), s)
                self.addNode(s, statement)
                
            if t.type == "INT":
                i = Node("Int")
                self.currNode = i
                self.addNode(Node(t.value), i)
                self.addNode(i, statement)

            if t.type == "IDENTIFIER":
                i = Node("Identifier")
                self.currNode = i
                self.addNode(Node(t.value), i)
                self.addNode(i, statement)



    def keyword(self, kw, currNode):
        if "GOTO" in kw or kw in self.keywords:
            self.addNode(Node(kw), currNode)

    def expression(self, ex, currNode):
        pass
    def factor(self):
        pass

    def term(self):
        pass
    def binary_op(self):
        pass
    def expression(self):
        pass
d = {
    '05': {'KEYWORD': 'REM'},
    '10': {'KEYWORD':'TEXT', 'CHAR':'COLON', 'STRING':'HOME'}
}

l = Scanner()
l.scan("basic_programs/example3.bas")
l.create_tokens()
print(l.tokens)
P = Parser(l.tokens, TokenType.keywords)

for pre, fill, node in RenderTree(P.Tree):
    print("%s%s" % (pre, node.name))
