import re
from caso_exception import CASOIllegalTokenError

class Token:
    def __init__(self, type_, value, line_num, char_pos):
        self.type = type_
        self.value = value
        self.line_num = line_num
        self.char_pos = char_pos

    def __repr__(self):
        return f"Token({repr(self.type)}, {repr(self.value)}, {repr(self.line_num)}, {repr(self.char_pos)})"

class CASOLexer:
    TOKEN_SPECIFICATION = [
        ("NUMBER", r"\d+(\.\d*)?"), # Integer or decimal numbers

        # Types
        ("INT", r"\bInt\b"), # Int type
        ("FLOAT", r"\bFloat\b"), # Float type
        ("BOOL", r"\bBool\b"), # Bool type
        ('LIST', r'\bList\b'), # List type
        ('STRING', r'\bString\b'), # String type
        ('ANY', r'\bAny\b'), # Any type
        ('EMPTY', r'\bEmpty\b'), # Empty type (used for void functions)

        # Keywords
        ('LET', r'\blet\b'), # Let keyword, used for variable declaration
        ('WHEN', r'\bwhen\b'), # When keyword, used for pattern matching
        ('FUNCTION', r'\bfnc\b'), # Function keyword, used for function declaration

        # Comparison operators
        ('EQ', r'=='), # Equality operator
        ('NEQ', r'!='), # Inequality operator
        ('LT', r'<'), # Less than operator
        ('LE', r'<='), # Less than or equal to operator
        ('GT', r'>'), # Greater than operator
        ('GE', r'>='), # Greater than or equal to operator
        ('UKN', r'\?'), # Unknown operator (used for pattern matching)

        # Operators
        ('ASSIGN', r'='), # Assignment operator
        ('REASSIGN', r':='), # Reassignment operator
        ('TYPE_ASSIGN', r':' ), # Type assignment operator
        ('ARROW', r'->'), # Arrow operator 
        ('PIPE', r'\|'), # Pipe operator

        # Characters
        ('OPEN_PAREN', r'\('), # Open parenthesis' 
        ('CLOSE_PAREN', r'\)'), # Close parenthesis
        ('OPEN_BRACKET', r'\['), # Open bracket
        ('CLOSE_BRACKET', r'\]'), # Close bracket
        ('OPEN_BRACE', r'\{'), # Open brace
        ('CLOSE_BRACE', r'\}'), # Close brace
        ("COMMENT" , r"//.*"), # Comment
        ("COMMA", r","), # Comma
        ("SEMICOLON", r";"), # Semicolon
        ('EXCLAMATION', r'!'), # Exclamation mark

        # Arithmetic operators (putting them after the other operators to avoid conflicts)
        ('PLUS', r'\+'), # Addition operator
        ('MINUS', r'-'), # Subtraction operator
        ('MUL', r'\*'), # Multiplication operator
        ('DIV', r'/'), # Division operator
        ('MOD', r'%'), # Modulo operato

        # Other
        ("ID", r"[A-Za-z0-9_]+"),  # Identifiers (allowing alphanumeric characters and underscore)
        ("NEWLINE", r"\n"), # Line endings
        ("SKIP", r"[ \t]+"), # Skip over spaces and tabs
    ]

    def __init__(self, source_code):
        self.source_code = source_code
        self.tokens = []
        self.current_position = 0
        self.tok_regex = re.compile("|".join("(?P<%s>%s)" % pair for pair in self.TOKEN_SPECIFICATION))

    def tokenize(self):
        line_num = 1
        line_start = 0

        while self.current_position < len(self.source_code):
            match = self.tok_regex.match(self.source_code, self.current_position)
            if match:
                type_ = match.lastgroup
                char_pos = match.start() - line_start

                if type_ == "NEWLINE":
                    line_start = match.end()
                    line_num += 1
                    # Add the NEWLINE token
                    self.tokens.append(Token(type_, '\n', line_num, char_pos))
                elif type_ != "SKIP" and type_ != "COMMENT":
                    value = match.group(type_)
                    if type_ == "NUMBER":
                        value = float(value) if '.' in value else int(value)
                    self.tokens.append(Token(type_, value, line_num, char_pos))

                self.current_position = match.end()
            else:
                raise CASOIllegalTokenError("Illegal character '%s'" % self.source_code[self.current_position], line_num, self.current_position)

        return self.tokens

