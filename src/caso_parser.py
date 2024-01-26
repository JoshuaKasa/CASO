from enum import Enum
from caso_exception import CASOSyntaxError

class NodeType(Enum):
    VARIABLE_DECLARATION = 1
    VARIABLE_ASSIGNMENT = 2
    EXPRESSION = 3

class ASTnode:
    def __init__(self, node_type, children=None): # We will use this to set the node type and children
        self.node_type = node_type
        self.children = children if children is not None else []

    def __repr__(self):
        return f"ASTnode({repr(self.node_type)}, {repr(self.children)})"

class DECLARATIONnode(ASTnode):
    def __init__(self, variable_name, variable_type, expression_string):
        super().__init__(NodeType.VARIABLE_DECLARATION)
        self.variable_name = variable_name
        self.variable_type = variable_type
        self.variable_value = expression_string

    def __repr__(self):
        return f"DECLARATIONnode({repr(self.variable_name)}, {repr(self.variable_type)}, {repr(self.variable_value)})"

class CASOParser:
    def __init__(self, tokens):
        self.tokens = tokens
        self.current_position = 0
        self.nodes = [] # This will be the list of nodes that will be returned by the parse() method

    # Useful constants
    TYPES = ["INT", "FLOAT", "BOOL"]
    ARITHMETIC_OPERATORS = ["PLUS", "MINUS", "MUL", "DIV", "MOD"]

    def parse(self):
        while self.current_position < len(self.tokens):
            self.nodes.append(self.parse_statement())
        return self.nodes

    def parse_statement(self):
        current_token = self.tokens[self.current_position]

        if current_token.type == "LET":
            self.parse_declaration()
        else:
            if current_token.type == "NEWLINE":
                self.current_position += 1
            else:
                raise CASOSyntaxError(f"Unexpected token {current_token.type}", current_token.line_num, current_token.char_pos)

    # List of the methods that will parse the different types of statements
    def parse_declaration(self):
        self.current_position += 1 # Skip the LET token
        
        # The next token should be the variable name
        variable_name_token = self.tokens[self.current_position]
        if variable_name_token.type != "ID":
            raise CASOSyntaxError(f"Expected variable name, got {variable_name_token.type}", variable_name_token.line_num, variable_name_token.char_pos)
        variable_name = variable_name_token.value # Save the variable name

        # Now should the type assignment operator
        self.current_position += 1 # Skip the variable name token
        type_assignment_token = self.tokens[self.current_position]
        if type_assignment_token.type != "TYPE_ASSIGN":
            raise CASOSyntaxError(f"Expected type assignment operator, got {type_assignment_token.type}", type_assignment_token.line_num, type_assignment_token.char_pos)

        # Now should come the variable type
        self.current_position += 1
        variable_type_token = self.tokens[self.current_position]
        if variable_type_token.type not in self.TYPES:
            raise CASOSyntaxError(f"Expected variable type, got {variable_type_token.type}", variable_type_token.line_num, variable_type_token.char_pos)
        variable_type = variable_type_token.type

        # Now should come the assignment operator
        self.current_position += 1
        assignment_token = self.tokens[self.current_position]
        if assignment_token.type != "ASSIGN":
            raise CASOSyntaxError(f"Expected assignment operator, got {assignment_token.type}", assignment_token.line_num, assignment_token.char_pos)

        # Now should come the variable value, which is an expression
        self.current_position += 1 # Skip the assignment token
        variable_value = self.parse_expression()        

        # After all the above, we can add the declaration node to the list of nodes
        append_node = DECLARATIONnode(variable_name, variable_type, variable_value)
        self.nodes.append(append_node)

    def parse_expression(self) -> str:
        expression_tokens = []

        # Collect all the tokens until the end of the line
        while self.current_position < len(self.tokens) and self.tokens[self.current_position].type != 'NEWLINE':
            if self.tokens[self.current_position].type in self.ARITHMETIC_OPERATORS:
                expression_tokens.append(self.tokens[self.current_position])
            elif self.tokens[self.current_position].type == 'ID':
                expression_tokens.append(self.tokens[self.current_position])
            elif self.tokens[self.current_position].type == 'NUMBER':
                expression_tokens.append(self.tokens[self.current_position])
            else:
                raise CASOSyntaxError(f"Unexpected token {self.tokens[self.current_position].type}", self.tokens[self.current_position].line_num, self.tokens[self.current_position].char_pos)
            self.current_position += 1

        # Skip the 'NEWLINE' token
        if self.current_position < len(self.tokens) and self.tokens[self.current_position].type == 'NEWLINE':
            self.current_position += 1

        # Convert to raw string (ensuring all values are strings)
        expression_string = ' '.join(str(token.value) for token in expression_tokens)
        return expression_string

