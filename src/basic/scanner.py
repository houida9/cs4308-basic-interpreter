import pprint

class Scanner:
    tokens = {

    }
    keywords = {
                "REM": "remark",
                "INPUT": "input",
                "IF": "if_stmt",
                "PRINT": "print",
                "TEXT": "text",
                "RETURN": "return",
                "LET": "let",
                "PR": "pr",
                "HOME": "home",
                "GOSUB": "gosub",
                "GOTO": "goto",
                "GET": "get",
                "FOR": "for",
                "NEXT": "next",
                "NOT": "not",
                "AND": "and",
                "OR": "or",
                "THEN": "then",
                "INT": "integer",
                "CHR$": "char",
                "STR$": "string",
                "WHILE": "while",
                "MOD": "mod",
                "END": "end"
    }
    special_chars = {" ": "space",
                     "+": "plus_sign",
                     "-": "minus_sign",
                     "/": "division_sign",
                     "=": "equal_sign",
                     "*": "multiply_sign",
                     ",": "comma",
                     "\"": "quote",
                     "(": "open_par",
                     ")": "close_par",
                     "<": "less_than",
                     ">": "greater_than"}
    def __init__(self):
        self.infile = None
        self.lineCount = 0
        self.tCount = 0
        self.bracketCount = 0
        self.progNodes = []
        self.current = None
        self.inQuotes = False

    # prepares java file for parser by creating tokens
    def scan(self, f):
        self.infile = open(f, "r+")
        self.lineCount = len(self.infile.readlines())
        self.infile.seek(0)
        self.scanLines()
        print(self.infile.readline())
        self.infile.close()


    # used by prep file to scan lines from file
    def scanLines(self):
        pos = 0
        while pos < self.lineCount:
            # might remove
            tempLine = self.infile.readline()
            cPos = 0
            token = ""
            while cPos < len(tempLine):
                curr_char = tempLine[cPos]
                if curr_char not in self.special_chars:
                    token = token + curr_char
                elif curr_char in self.special_chars:
                    self.addToken(token, False)
                    if curr_char != ' ' and curr_char != '\"':
                        self.addToken(curr_char, False)
                    elif curr_char == '\"':
                        cPos = self.handleString(token,tempLine, cPos + 1)
                    token = ""
                cPos += 1
            pos += 1
    def handleString(self, token, tempLine, cPos):
        curr_char = tempLine[cPos]
        while curr_char != '\"' and cPos < len(tempLine):
            token += curr_char
            cPos += 1
            if cPos < len(tempLine) - 1:
                curr_char = tempLine[cPos]
        self.addToken(token, True)
        return cPos
    def handleRemark(self, token, tempLine, cPos):
        while curr_char != '\"' and cPos < len(tempLine):
            token += curr_char
            cPos += 1
            if cPos < len(tempLine) - 1:
                curr_char = tempLine[cPos]
    def addToken(self, tk, string):
        if tk in self.special_chars:
            self.tokens.update({"t"+str(self.tCount): {str(tk): str(self.special_chars.get(tk))}})
            self.tCount += 1
        elif tk in self.keywords:
            self.tokens.update({"t" + str(self.tCount): {str(tk): str(self.keywords.get(tk))}})
            self.tCount += 1
        elif string:
            self.tokens.update({"t" + str(self.tCount): {str(tk): "string"}})
            self.tCount += 1
        else:
            self.tokens.update({"t" + str(self.tCount): {str(tk): "none"}})
            self.tCount += 1



    #used by prepfile
    # def addLine(self, line):
    #     tempN = Node(line)
    #     if len(tempN.tokens) != 0:
    #         self.progNodes.append(tempN)
    #
    # def addComment(self, line):
    #     index = line.find("//")
    #     comLine = ""
    #     if index != -1:
    #         comLine = line[:index] + line[index+2:]
    #     index = line.find("/*")
    #     if index != -1:
    #         comLine = line[:index] + line[index+2:]
    #     index = line.find("*/")
    #     if index != -1:
    #         comLine = line[:index] + line[index+2:]
    #
    #     node = Node()
    #     node.tokens = [Token(comLine, "comment")]
    #
    #     self.progNodes.append(node)
    #
    # def showLine(self, num):
    #     print(len(self.progNodes))
    #     temp = self.progNodes[num]
    #     for x in temp.tokens:
    #         print(str(x.word) + ", " + str(x.id))

test = Scanner()
test.scan("basic_programs/example1.bas")
print(test.tokens)

# pprint._sorted = lambda x:x
# pprint.pprint(test.tokens)