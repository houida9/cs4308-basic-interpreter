class Token:
    def __init__(self, type_, value=None, goto=None):
        self.type = type_
        self.value = value
        self.goto = goto

    def __repr__(self):
        if self.value != None and self.goto: return f'{self.type}:{self.value}:{self.goto}'
        if self.value != None: return f'{self.type}:{self.value}'
        return f'{self.type}'


class TokenType:
    # data types
    INT = 'INT'
    FLOAT = 'FLOAT'
    STRING = 'STRING'
    SINGLE_CHAR = 'CHAR'
    REMARK = 'REM'

    IDENTIFIER = 'IDENTIFIER'

    # escape characters
    SPACE = " "
    TAB = "\t"
    SINGLE_QUOTE = "\'"
    DOUBLE_QUOTE = "\""
    NEW_LINE = "\n"

    # single-character self.tokens
    special_chars = {
        "+": "PLUS",
        "-": "MINUS",
        "/": "DIVIDE",
        "*": "MULTIPLY",
        "=": "EQUAL",
        ":": "COLON",
        ";": "SEMI-COLON",
        ",": "COMMA",
        "#": "HASH",
        "(": "LEFT_PAREN",
        ")": "RIGHT_PAREN",
        "<": "LESS_THAN",
        ">": "GREATER_THAN",
    }

    # BASIC keywords
    KEYWORD = 'KEYWORD'

    keywords = [
        "REM",
        "INPUT",
        "IF",
        "THEN",
        "PRINT",
        "TEXT",
        "RETURN",
        "LET",
        "PR",
        "HOME",
        "GOSUB",
        "GOTO",
        "GET",
        "FOR",
        "WHILE",
        "NEXT",
        "NOT",
        "AND",
        "OR",
        "THEN"
        "INT",
        "CHR$",
        "STR$",
        "MOD",
        "END"
    ]

    NOT_EQUAL = "NOT_EQUAL"
    LESS_OR_EQUAL = "LESS_OR_EQUAL"
    GREATER_OR_EQUAL = "GREATER_OR_EQUAL"


class Scanner:
    def __init__(self):
        self.current_index = -1
        self.current_char = None
        self.basic_line_num = ""
        self.tokens = {}
        self.idFlag = False

    def scan(self, file_path):
        self.file_path = file_path
        self.text = open(file_path, "r+").read()
        self.advance()

    def advance(self):
        self.current_index += 1
        self.current_char = self.text[self.current_index] if self.current_index < len(self.text) else None

    def peek_ahead(self, pos=1):
        if self.current_index + pos < len(self.text):
            return self.text[self.current_index + pos]

    def ignore_comment(self):
        while self.current_char != None and self.peek_ahead() != TokenType.NEW_LINE:
            self.advance()
        self.advance()

    def is_alphanumeric(self, char):
        return char.isalpha() or char.isnumeric() or char == "_"

    def make_string(self):
        quote = [TokenType.SINGLE_QUOTE, TokenType.DOUBLE_QUOTE]

        if self.current_char in quote:
            string = TokenType.DOUBLE_QUOTE
            self.advance()

            while self.current_char and self.current_char not in quote:
                string += self.current_char
                self.advance()
            
            self.advance()
            return Token(TokenType.STRING, string + TokenType.DOUBLE_QUOTE)
        
        return Token(TokenType.STRING, "")

    def is_line_number(self):
        if self.current_char.isnumeric() and self.current_index == 0:
            return True
        elif self.current_char == "\n":
            return False

        prev_char = self.current_char
        current_index = self.current_index - 1

        while current_index >= 0:
            prev_char = self.text[current_index]
            if current_index == 0 or prev_char == "\n" and self.current_char.isnumeric():
                return True
            elif prev_char not in " \n":
                return False

            current_index -= 1

        return False

    def read_line_number(self):
        basic_line_num = ""
        while self.current_char != None and self.current_char.isnumeric():
            basic_line_num += f'{self.current_char}'
            self.advance()
        self.advance()
        self.basic_line_num = basic_line_num

    def create_tokens(self):

        while self.current_char != None:
            # check if the current character is a line number
            if (self.is_line_number()):
                # if self.tokens.get(self.basic_line_num) == []:
                #     del self.tokens[self.basic_line_num]
                self.read_line_number()

            # verify that the line number is added to the tokens dictionary
            if self.basic_line_num not in self.tokens:
                self.tokens.update({self.basic_line_num: []})
            
            # if the current character is a new line, add the current token to the tokens
            if self.current_char in [TokenType.NEW_LINE, TokenType.TAB, TokenType.SPACE]:
                self.advance()
                
            elif self.current_char in [TokenType.SINGLE_QUOTE, TokenType.DOUBLE_QUOTE]:
                self.add_token(self.make_string())

            elif self.current_char.isalpha():
                self.add_token(self.make_identifier())

            # check if the current character is a numeric character (and token not a variable)
            elif self.current_char.isnumeric():
                self.add_token(self.create_number())

            # check if the current character is a special character
            elif self.current_char in TokenType.special_chars:
                self.add_token(self.handle_special_keys())

        return self.tokens

    def add_token(self, token):
        self.tokens[self.basic_line_num].append(token)

    def handle_special_keys(self):

        # if the current character is a < or >, check whether the next character is an =
        if self.current_char == "<":
            if self.peek_ahead() == "=":
                self.advance()
                self.advance()
                return Token(TokenType.SINGLE_CHAR, TokenType.LESS_OR_EQUAL)
            elif self.peek_ahead() == ">":
                self.advance()
                self.advance()
                return Token(TokenType.SINGLE_CHAR, TokenType.NOT_EQUAL)
        elif self.current_char == ">":
            if self.peek_ahead() == "=":
                self.advance()
                self.advance()
                return Token(TokenType.SINGLE_CHAR, TokenType.GREATER_OR_EQUAL)

        # otherwise, if the current token is not blank, add the current token
        if self.current_char in TokenType.special_chars:
            char = self.current_char
            self.advance()
            return Token(TokenType.SINGLE_CHAR, TokenType.special_chars.get(str(char)))

    def create_number(self):
        num_str = ''
        is_float = False

        while self.current_char != None and (self.current_char.isnumeric() or self.current_char == '.'):
            if self.current_char == '.':
                is_float = True

            num_str += self.current_char
            self.advance()
            if self.current_char == ')': # solve right parenthesis
              break
            self.advance()

        if is_float:
          return Token(TokenType.FLOAT, float(num_str))
        else:
          return Token(TokenType.INT, int(num_str))
        
    def make_identifier(self):
      id_str = ''
      token_type = None

      while self.current_char != None and (self.current_char.isalnum() or self.current_char in '.' + '_'):
          id_str += self.current_char
          self.advance()
        
      if id_str in TokenType.keywords:
        token_type = TokenType.KEYWORD
        
        if id_str == "REM":
          self.ignore_comment()
          return Token(TokenType.KEYWORD, id_str)

        elif id_str.upper() == "GOTO":
          if self.peek_ahead().isnumeric():
            self.advance()
            return Token(TokenType.KEYWORD, id_str, self.get_goto_line())
        
      else:
        token_type = TokenType.IDENTIFIER
            
      return Token(token_type, id_str)

    def get_goto_line(self):
        return self.create_number().value

