# TODO: Finish implementing list parsing

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

class ASSIGNMENTnode(ASTnode):
    def __init__(self, variable_name, expression_string):
        super().__init__(NodeType.VARIABLE_ASSIGNMENT)
        self.variable_name = variable_name
        self.variable_value = expression_string

    def __repr__(self):
        return f"ASSIGNMENTnode({repr(self.variable_name)}, {repr(self.variable_value)})"

class CASOParser:
    def __init__(self, tokens):
        self.tokens = tokens
        self.current_position = 0
        self.nodes = [] # This will be the list of nodes that will be returned by the parse() method
        self.variables = {} # This will be the dictionary of variables that will be returned by the parse() method

    # Useful constants
    TYPES = ['LIST', 'STRING', 'INT', 'FLOAT', 'BOOLEAN']
    ARITHMETIC_OPERATORS = ['PLUS', 'MINUS', 'MUL', 'DIV', 'MOD']

    def parse(self):
        while self.current_position < len(self.tokens):
            self.nodes.append(self.parse_statement())
        return self.nodes

    def parse_statement(self):
        current_token = self.tokens[self.current_position]

        if current_token.type == "LET":
            self.parse_declaration()
        elif current_token.type == "ID":
            self.parse_assignment()
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
        # Check if the variable name is already in the dictionary of variables
        if variable_name in self.variables:
            raise CASOSyntaxError(f"Variable {variable_name} already declared", variable_name_token.line_num, variable_name_token.char_pos)
        self.variables[variable_name] = None # Add the variable name to the dictionary of variables

        # Now should come the type assignment operator
        self.current_position += 1 # Skip the variable name token
        type_assignment_token = self.tokens[self.current_position]
        if type_assignment_token.type != "TYPE_ASSIGN":
            raise CASOSyntaxError(f"Expected type assignment operator, got {type_assignment_token.type}", type_assignment_token.line_num, type_assignment_token.char_pos)

        # Now should come the variable type
        self.current_position += 1 # Skip the type assignment token
        variable_type_token = self.tokens[self.current_position]
        if variable_type_token.type not in self.TYPES:
            raise CASOSyntaxError(f"Expected variable type, got {variable_type_token.type}", variable_type_token.line_num, variable_type_token.char_pos)
        
        if variable_type_token.type == "LIST": # This means that the variable type is a list
            variable_type = self.parse_list()
        else:
            variable_type = variable_type_token.value
        self.current_position += 1 # Skip the variable type token

        # Now should come the assignment operator
        assignment_token = self.tokens[self.current_position]
        if assignment_token.type != "ASSIGN":
            raise CASOSyntaxError(f"Expected assignment operator, got {assignment_token.type}", assignment_token.line_num, assignment_token.char_pos)

        # Now should come the variable value, which can be either an expression or a list
        self.current_position += 1 # Skip the assignment token
        variable_value_token = self.tokens[self.current_position]
        variable_value = self.parse_expression()

        # After all the above, we can add the declaration node to the list of nodes
        append_node = DECLARATIONnode(variable_name, variable_type, variable_value)
        self.nodes.append(append_node)

    # This function will be used to parse the assignment statement
    def parse_assignment(self):
        # The first token should be the variable name
        variable_name_token = self.tokens[self.current_position]
        if variable_name_token.type != "ID":
            raise CASOSyntaxError(f"Expected variable name, got {variable_name_token.type}", variable_name_token.line_num, variable_name_token.char_pos)
        variable_name = variable_name_token.value

        # Check if the variable name is in the dictionary of variables
        if variable_name not in self.variables:
            raise CASOSyntaxError(f"Variable {variable_name} not declared", variable_name_token.line_num, variable_name_token.char_pos)

        # Now should come the assignment operator
        self.current_position += 1
        assignment_token = self.tokens[self.current_position]
        if assignment_token.type != "REASSIGN":
            raise CASOSyntaxError(f"Expected assignment operator, got {assignment_token.type}", assignment_token.line_num, assignment_token.char_pos)

        # Now should come the variable value, which is an expression
        self.current_position += 1 # Skip the assignment token
        variable_value = self.parse_expression()
        if variable_value == '':
            raise CASOSyntaxError(f"Expected expression, got {variable_value}", assignment_token.line_num, assignment_token.char_pos)
   
        # After all the above, we can add the assignment node to the list of nodes
        append_node = ASSIGNMENTnode(variable_name, variable_value)
        self.nodes.append(append_node)

    # This is the method that will parse ALL expressions
    def parse_expression(self) -> str:
        expression_tokens = []

        # Checking if the expression is a list
        if self.tokens[self.current_position].type == 'OPEN_BRACKET':
            self.parse_list_expression()

        # Collect all the tokens until the end of the line
        while self.current_position < len(self.tokens) and self.tokens[self.current_position].type != 'NEWLINE':
            if self.tokens[self.current_position].type in self.ARITHMETIC_OPERATORS:
                expression_tokens.append(self.tokens[self.current_position])
            elif self.tokens[self.current_position].type == 'ID':
                # Checking if the variable is declared
                if self.tokens[self.current_position].value in self.variables:
                    expression_tokens.append(self.tokens[self.current_position])
                else:
                    raise CASOSyntaxError(f"Expression variable {self.tokens[self.current_position].value} not declared", self.tokens[self.current_position].line_num, self.tokens[self.current_position].char_pos)
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

    def parse_list_expression(self):
        # Checking for correct syntax
        self.current_position += 1 # Skip the open bracket token

        # Parsing the list
        list_values = []
        while self.tokens[self.current_position].type != 'CLOSE_BRACKET':
            list_values.append(self.tokens[self.current_position].value)
            self.current_position += 1

            # Checking for correct syntax
            if self.tokens[self.current_position].type == 'COMMA':
                self.current_position += 1 # Skip the comma token

        # Checking for correct syntax
        if self.tokens[self.current_position].type != 'CLOSE_BRACKET':
            raise CASOSyntaxError(f"Expected close bracket, got {self.tokens[self.current_position].type}", self.tokens[self.current_position].line_num, self.tokens[self.current_position].char_pos)

        # Finally finish parsing the list
        self.current_position += 1 # Skip the close bracket token
        return list_values

    # This is the method that will parse lists
    def parse_list(self):
        # Checking for correct syntax
        self.current_position += 1 # Skip the LIST token
        list_content_type = 'List['
        open_bracket_token = self.tokens[self.current_position]
        if open_bracket_token.type != "OPEN_BRACKET":
            raise CASOSyntaxError(f"Expected open bracket, got {open_bracket_token.type}", open_bracket_token.line_num, open_bracket_token.char_pos)

        # Recursively parse the list
        self.current_position += 1 # Skip the open bracket token
        list_content_type += str(self.parse_list_content())

        # Checking for correct syntax
        close_bracket_token = self.tokens[self.current_position]
        if close_bracket_token.type != "CLOSE_BRACKET":
            raise CASOSyntaxError(f"Expected close bracket, got {close_bracket_token.type}", close_bracket_token.line_num, close_bracket_token.char_pos)

        # Finally finish parsing the list
        return list_content_type + ']'

    def parse_list_content(self):
        current_token = self.tokens[self.current_position]
        if current_token.type == "LIST": # Checking if the list contains another list
            self.parse_list()
        elif current_token.type in self.TYPES: # Checking if the list contains a primitive type
            self.current_position += 1 # Skip the type token
            return current_token.value
        else:
            raise CASOSyntaxError(f"Expected list content, got {current_token.type}", current_token.line_num, current_token.char_pos)
