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
        ('STRING', r'\bStr\b'), # String type
        ('ANY', r'\bAny\b'), # Any type
        ('EMPTY', r'\bEmpty\b'), # Empty type (used for void functions)

        # Keywords
        ('LET', r'\blet\b'), # Let keyword, used for variable declaration
        ('CONST', r'\bconst\b'), # Const keyword, used for constant declaration
        ('WHEN', r'\bwhen\b'), # When keyword, used for pattern matching
        ('FUNCTION', r'\bfnc\b'), # Function keyword, used for function declaration
        ('IF', r'\bif\b'), # If keyword, used for if statements
        ('ELSE', r'\belse\b'), # Else keyword, used for else statements
        ('ELSIF', r'\belsif\b'), # Else if keyword, used for else if statements
        ('LOOP', r'\bloop\b'), # Loop keyword, used for loops
        ('TO', r'\bto\b'), # To keyword, used for loops (example: loop (i, 10 to 20))
        ('USE', r'\buse\b'), # Use keyword, used for importing modules
        ('OBJECT', r'\bobj\b'), # Object keyword, used for object declaration (classses in Java)

        # Boolean values
        ('TRUE', r'\btrue\b'), # True keyword
        ('FALSE', r'\bfalse\b'), # False keyword

        # LERSILER (Lexer, Parser, Transpiler) delimiters, these will be - likely - not used by the user but rather at the parser, transpiler and lexer level
        ('NATIVE_JAVA_START', r'\bcaso___native_java_start\b'), # Native Java start keyword
        ('NATIVE_JAVA_END', r'\bcaso___native_java_end\b'), # Native Java end keyword
        ('PARSER_PAUSE', r'\bcaso___parser_pause\b'), # Parser pause keyword
        ('PARSER_RESUME', r'\bcaso___parser_resume\b'), # Parser resume keyword
        ('TRANSPILE_PAUSE', r'\bcaso___transpile_pause\b'), # Transpiler pause keyword
        ('TRANSPILE_RESUME', r'\bcaso___transpile_resume\b'), # Transpiler resume keyword
        ('GENERAL_JAVA_TOKEN', r'\bcaso___general_java_token\b'), # General Java token keyword

        # Comparison operators
        ('EQ', r'=='), # Equality operator
        ('NEQ', r'!='), # Inequality operator
        ('LT', r'<'), # Less than operator
        ('LE', r'<='), # Less than or equal to operator
        ('GT', r'>'), # Greater than operator
        ('GE', r'>='), # Greater than or equal to operator
        ('UKN', r'\?'), # Unknown operator (used for pattern matching)
        ('AND', r'&&'), # And operator
        ('OR', r'\|\|'), # Or operator

        # Operators
        ('ASSIGN', r'='), # Assignment operator
        ('REASSIGN', r':='), # Reassignment operator
        ('TYPE_ASSIGN', r':' ), # Type assignment operator
        ('ARROW', r'->'), # Arrow operator 
        ('PIPE', r'\|'), # Pipe operator (for now used for returns)
        ('DOT', r'\.'), # Dot operator (used for object properties)

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
        self.java_blocks = [] # Stores the extracted Java blocks

    def preprocess_java_blocks(self):
        """Extracts Java blocks and replaces them with placeholders in the source code."""
        java_start_tag = 'caso___native_java_start'
        java_end_tag = 'caso___native_java_end'
        placeholder_format = "<JAVA_BLOCK_{}>"

        start_pos = 0
        block_counter = 0

        while True:
            start_index = self.source_code.find(java_start_tag, start_pos)
            if start_index == -1:
                break  # No more Java blocks

            end_index = self.source_code.find(java_end_tag, start_index)
            if end_index == -1:
                raise CASOIllegalTokenError("Unmatched 'caso___native_java_start'", 0, start_index)

            # Extract and store the Java block
            java_code = self.source_code[start_index + len(java_start_tag):end_index].strip()
            self.java_blocks.append(java_code)

            # Replace the Java block in the source code with a placeholder
            placeholder = placeholder_format.format(block_counter)
            before_block = self.source_code[:start_index]
            after_block = self.source_code[end_index + len(java_end_tag):]
            self.source_code = before_block + placeholder + after_block

            start_pos = start_index + len(placeholder)  # Update start_pos to continue search
            block_counter += 1

    def tokenize(self):
        self.preprocess_java_blocks()  # Handle Java blocks first

        line_num = 1
        line_start = 0

        while self.current_position < len(self.source_code):
            # Check for Java block placeholders in the simplified source code
            if self.source_code[self.current_position:].startswith('<JAVA_BLOCK_'):
                end_index = self.source_code.find('>', self.current_position)
                placeholder = self.source_code[self.current_position:end_index+1]
                block_index = int(placeholder.strip('<JAVA_BLOCK_>').strip('>'))
                java_code = self.java_blocks[block_index]

                # Add a token for the entire Java block
                self.tokens.append(Token("GENERAL_JAVA_TOKEN", java_code, line_num, self.current_position - line_start))

                # Update current_position to skip over the placeholder
                self.current_position = end_index + 1
                continue  # Move to the next segment of the source code

            match = self.tok_regex.match(self.source_code, self.current_position)
            if match:
                type_ = match.lastgroup
                char_pos = match.start() - line_start

                if type_ == "NEWLINE":
                    line_start = match.end()
                    line_num += 1
                    
                    # Adding the newline token to the list of tokens
                    self.tokens.append(Token(type_, '\n', line_num, char_pos))

                elif type_ != "SKIP" and type_ != "COMMENT":
                    value = match.group(type_)
                    if type_ == "NUMBER":
                        value = float(value) if '.' in value else int(value)
                    self.tokens.append(Token(type_, value, line_num, char_pos))

                self.current_position = match.end()
            else:
                # This block will catch any unrecognized characters or sequences
                raise Exception(f"Illegal character '{self.source_code[self.current_position]}' at line {line_num}")

        return self.tokens
