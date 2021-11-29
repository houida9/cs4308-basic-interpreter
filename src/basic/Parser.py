from anytree import Node, RenderTree

from scanner import Scanner
from scanner import TokenType, Token


class Parser:
    def __init__(self, tokens):
        self.tokens = tokens
        self.index = 0
        self.keywords = TokenType.keywords
        self.Tree = Node("")
        self.AST = Node("")
        self.currNode = self.Tree
        self.symbolTable = {}
        self.IDinUse = False
        self.parse_tokens()
        self.assignment = False

    # Parse Tree Function
    def add_node(self, child, parent):
        child.parent = parent
        self.currNode = child

    def parse_tokens(self):
        if len(self.tokens) > 0:
            root = self.program()
        for key in self.tokens:
            tok = [key, self.tokens[key]]

            # if key is a line number
            self.num = tok[0]
            if tok[0].isnumeric:
                self.statement(tok[1])
            self.currNode = root

    def program(self):
        p = Node("Program")
        self.add_node(p, self.Tree)

        return p

    def statement(self, tok):
        statement = Node("Statement")
        self.add_node(statement, self.currNode)
        # if the #1 index contains a nested dictionary pass it back to through the function or
        # analyze entire dictionary in this function.

        for t in tok:

            if not t.checked:
                if t.type == "KEYWORD":
                    k = Node("Keyword")
                    if t.goto is not None:
                        self.keyword(t.value + ":" + str(t.goto), k)
                        self.currNode = k
                        self.add_node(k, statement)
                    else:
                        if t.value == "LET":
                            self.assignment = True
                        self.keyword(t.value, k)
                        self.currNode = k
                        self.add_node(k, statement)

                if t.type == "CHAR":

                    if t.value == 'LEFT_PAREN':
                        c = Node("Char")
                        self.currNode = c
                        self.add_node(Node(t.value), c)
                        self.add_node(c, statement)
                        index = len(tok) - 1
                        for i in range(len(tok) - 1, 0, -1):
                            temp_token = Token('CHAR', 'RIGHT_PAREN')
                            if temp_token == tok[i]:
                                index = i
                                for n in tok[tok.index(t) + 1:index]:
                                    n.checked = True

                        self.expression(tok[tok.index(t) + 1:index], statement)
                    else:
                        c = Node("Char")
                        self.currNode = c
                        self.add_node(Node(t.value), c)
                        self.add_node(c, statement)

                        if t.value == 'EQUAL':
                            temp_token = tok[tok.index(t)]
                            index = tok.index(t)
                            while index < len(tok):
                                index += 1
                                if index != len(tok):
                                    temp_token = tok[index]
                                    temp_token.checked = True
                            self.expression(tok[tok.index(t) + 1:], statement, 'Assignment_Expression')

                if t.type in (TokenType.INT, TokenType.STRING, TokenType.IDENTIFIER, TokenType.FLOAT):
                    value = Node('Value', statement)
                    if t.type == "STRING":
                        s = Node("String")
                        self.currNode = s
                        self.add_node(Node(t.value), s)
                        self.add_node(s, value)

                    if t.type == "INT":
                        i = Node("Int")
                        self.currNode = i
                        self.add_node(Node(t.value), i)
                        self.add_node(i, value)

                    if t.type == "IDENTIFIER":
                        i = Node("Identifier")
                        self.currNode = i

                        self.add_node(Node(t.value), i)
                        if t.value not in self.symbolTable:
                            self.symbolTable[t.value] = ''

                        self.IDinUse = True

                        self.handle_identifier(t.value, tok[tok.index(t) + 1:])
                        self.add_node(i, value)

                t.checked = True
        self.assignment = False

    def keyword(self, kw, currNode):
        if "GOTO" in kw or kw in self.keywords:
            self.add_node(Node(kw), currNode)

    def create_expression_list(self, tok, currNode):
        expr_list = []
        l_count = 0
        for tk in tok:
            if tk.value != 'RIGHT_PAREN' and l_count == 0:
                if tk.value == 'LEFT_PAREN':
                    l_count += 1
                expr_list.append(tk)
            elif tk.value == 'RIGHT_PAREN' and l_count > 0:
                expr_list.append(tk)
                l_count -= 1
            else:
                self.expression(expr_list, currNode)

    def handle_identifier(self, iden, next_tokens):
        if self.IDinUse and self.assignment:
            if next_tokens and next_tokens[0] and next_tokens[0].value == 'EQUAL':
                self.symbolTable[iden] = next_tokens[1].value

    def expression(self, ex, curr_node, name='Expression'):
        s = curr_node
        e = Node(name, parent=curr_node)

        if ex and ex[0] and ex[0].value == 'LEFT_PAREN':
            self.create_expression_list(ex[1:], e)
        else:
            self.currNode = e
            for t in ex:
                if t.value == 'LEFT_PAREN':
                    index = len(ex) - 1
                    for i in range(len(ex) - 1, 0, -1):
                        temp_token = Token('CHAR', 'RIGHT_PAREN')
                        if temp_token == ex[i]:
                            index = i
                            for n in ex[ex.index(t) + 1:index]:
                                n.checked = True
                    self.expression(ex[ex.index(t) + 1:index], e)
                    self.expression(ex[index:], s)
                    return

                elif t.value != 'RIGHT_PAREN' and t.value != 'LEFT_PAREN':
                    self.add_node(Node(t.value), e)


def print_tree(parse_tree):
    for pre, fill, node in RenderTree(parse_tree.Tree):
        print("%s%s" % (pre, node.name))
#in progress
def create_ast(tree):
    pass
    '''
    if tree.children[0].name == 'Program':
        statements = tree.children[0].children
        for i in range(0,len(statements), 1):
            statement = statements[i].children
            for n in range(0, len(statement), 1):
                for temp in statement:
                    if temp.name in ('Expression','Assignment_Expression'):
                        expr = temp.children
                        for e in expr:
                            if 
    '''

def run(file_path):
    lexer = Scanner()
    lexer.scan(file_path)
    lexer.create_tokens()
    parse_tree = Parser(lexer.tokens)
    create_ast(parse_tree.Tree)
    print_tree(parse_tree)


run('basic_programs/example1.bas')
