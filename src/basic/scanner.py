class Token:
  def __init__(self, type_, value=None, goto=None):
        self.type = type_
        self.value = value
        self.goto = goto
        
  def __repr__(self):
        if self.value and self.goto: return f'{self.type}:{self.value}:{self.goto}'
        if self.value: return f'{self.type}:{self.value}'
        return f'{self.type}'
      
class TokenType:
  # data types
  TT_INT		           = 'INT'
  TT_FLOAT             = 'FLOAT'
  TT_STRING            = 'STRING'
  TT_SINGLE_CHARACTER  = 'CHAR'
  
  # escape characters
  TT_SPACE          = " "
  TT_TAB            = "\t"
  TT_SINGLE_QUOTE   = "\'"
  TT_DOUBLE_QUOTE   = "\""
  TT_NEW_LINE       = "\n"

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
  
  NOT_EQUAL = "NOT_EQUAL"
  LESS_OR_EQUAL = "LESS_OR_EQUAL"
  GREATER_OR_EQUAL = "GREATER_OR_EQUAL"
    
  # BASIC keywords
  TT_KEYWORD = 'KEYWORD'
  
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

      
class Scanner:  
  def __init__(self):
        self.current_index = -1
        self.current_char = None
        self.basic_line_num = ""
        self.tokens = {}
        
  def scan(self, file_path):
        self.file_path = file_path
        self.text = open(file_path, "r+").read()
        self.advance()
    
  def advance(self):
      self.current_index += 1
      self.current_char = self.text[self.current_index] if self.current_index < len(self.text) else None
      
  def peek_ahead(self):
    if self.current_index + 1 < len(self.text):
      return self.text[self.current_index + 1]
    
  def ignore_comment(self):
    while self.current_char != None and self.peek_ahead() != TokenType.TT_NEW_LINE:
      self.advance()
  
  def is_alphanumeric(self, char):
    return char.isalpha() or char.isnumeric() or char == "_"
      
  def handle_string(self):
    quote = [TokenType.TT_SINGLE_QUOTE, TokenType.TT_DOUBLE_QUOTE]
    
    if self.current_char in quote:
      string = TokenType.TT_DOUBLE_QUOTE
      self.advance()
      
      while self.current_char and self.current_char not in quote:
        string += self.current_char
        self.advance()
        
      return string + TokenType.TT_DOUBLE_QUOTE
    return ""
  
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
    self.basic_line_num = basic_line_num
    

  def create_tokens(self):
      current_token = ""
      clear_current_token = True
      
      while self.current_char != None:
          if clear_current_token:
            current_token = ""
          clear_current_token = True
            
          # check if the current character is a line number
          if (self.is_line_number()):
            if self.tokens.get(self.basic_line_num) == []:
              del self.tokens[self.basic_line_num]
            self.read_line_number()
            
          # verify that the line number is added to the tokens dictionary
          if self.basic_line_num not in self.tokens:
            self.tokens.update({self.basic_line_num: []})
            
          # if the current character is a new line, add the current token to the tokens
          if self.current_char == TokenType.TT_NEW_LINE:
            self.add_token(TokenType.TT_STRING, current_token)
            
          # check if the current character is a numeric character
          elif self.current_char.isnumeric():
            self.tokens[self.basic_line_num].append(self.create_number())
              
          # check if the current characyer is a special character
          elif self.current_char in TokenType.special_chars:
            scanned_char = False
          
            # check if the current token name is a keyword
            if current_token.upper() in TokenType.keywords:
              self.add_token(TokenType.TT_KEYWORD, current_token)
              
            # if the current character is a < or >, check whether the next character is an =
            elif self.current_char == "<":
                if self.peek_ahead() == "=":
                  self.add_token(TokenType.LESS_OR_EQUAL)
                  self.advance()
                  scanned_char = True
                elif self.peek_ahead() == ">":
                  self.add_token(TokenType.NOT_EQUAL)
                  self.advance()
                  scanned_char = True
            elif self.current_char == ">":
                if self.peek_ahead() == "=":
                  self.add_token(TokenType.GREATER_OR_EQUAL)
                  self.advance()
                  scanned_char = True

            # otherwise, if the current token is not blank, add the current token
            elif current_token:
                self.add_token(TokenType.TT_STRING, current_token)
            
            if not scanned_char:
              self.add_token(TokenType.TT_SINGLE_CHARACTER, TokenType.special_chars.get(str(self.current_char)))
            
          elif self.current_char in [TokenType.TT_SINGLE_QUOTE, TokenType.TT_DOUBLE_QUOTE]:
            self.add_token(TokenType.TT_STRING, self.handle_string())
              
          elif self.current_char in [TokenType.TT_SPACE, TokenType.TT_TAB]:
            
            if current_token == "REM":
              self.ignore_comment()
              clear_current_token = True
              
            elif current_token and current_token.upper() in TokenType.keywords:
              if current_token.upper() == "GOTO":
                if self.peek_ahead().isnumeric():
                  self.advance()
                  self.add_token(TokenType.TT_KEYWORD, current_token, self.get_goto_line())
              else:
                self.add_token(TokenType.TT_KEYWORD, current_token)
              
            elif current_token:
              self.add_token(TokenType.TT_STRING, current_token)
                          
          elif self.is_alphanumeric(self.current_char):
            clear_current_token = False
            current_token += self.current_char
          
          self.advance()
          
      if current_token and not self.current_char:
        if current_token.upper() in TokenType.keywords:
          self.add_token(TokenType.TT_KEYWORD, current_token)

      return self.tokens
    
    
  def add_token(self, token_type, current_token=None, goto=None):
    if current_token:
      self.tokens[self.basic_line_num].append(Token(token_type, current_token, goto))
  
  
  def create_number(self):
    num_str = ''
    is_float = False

    while self.current_char != None and (self.current_char.isnumeric() or self.current_char == '.'):
        if self.current_char == '.':
            is_float = True
        
        num_str += self.current_char
        self.advance()
        
        if is_float: return Token(TokenType.TT_FLOAT, float(num_str)) 
        else: return Token(TokenType.TT_INT, int(num_str))
        
  def get_goto_line(self):
    return self.create_number().value
