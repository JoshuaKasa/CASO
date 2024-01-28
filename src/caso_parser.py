# TODO: Finish implementing list parsing

from enum import Enum
from caso_exception import CASOSyntaxError

class NodeType(Enum):
    VARIABLE_DECLARATION = 1
    VARIABLE_ASSIGNMENT = 2
    EXPRESSION = 3
    WHEN = 4
    MATCHCASE = 5
    FUNCTION_DECLARATION = 6
    FUNCTION_CALL = 7
    RETURN = 8

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

class WHENnode(ASTnode):
    def __init__(self, variable_name, match_cases):
        super().__init__(NodeType.WHEN)
        self.variable_name = variable_name
        self.match_cases = match_cases

    def __repr__(self):
        return f"WHENnode({repr(self.variable_name)}, {repr(self.match_cases)})"

class MATCHCASEnode(ASTnode):
    def __init__(self, match_type, match_value=None):
        super().__init__(NodeType.MATCHCASE)
        self.match_type = match_type
        self.match_value = match_value
        self.children = [] # What happens if the match case is matched

    def __repr__(self):
        return f"MATCHCASEnode({repr(self.match_type)}, {repr(self.match_value)}, {repr(self.children)})"

class FUNCTIONDECLARATIONnode(ASTnode):
    def __init__(self, function_name, function_args, return_type, function_body):
        super().__init__(NodeType.FUNCTION_DECLARATION)
        self.function_name = function_name
        self.function_args = function_args
        self.return_type = return_type
        self.function_body = function_body

    def __repr__(self):
        return f"FUNCTIONDECLARATIONnode({repr(self.function_name)}, {repr(self.function_args)}, {repr(self.return_type)}, {repr(self.function_body)})"

class FUNCTIONCALLnode(ASTnode):
    def __init__(self, function_name, function_args):
        super().__init__(NodeType.FUNCTION_CALL)
        self.function_name = function_name
        self.function_args = function_args

    def __repr__(self):
        return f"FUNCTIONCALLnode({repr(self.function_name)}, {repr(self.function_args)})"

class RETURNnode(ASTnode):
    def __init__(self, return_value):
        super().__init__(NodeType.RETURN)
        self.return_value = return_value

    def __repr__(self):
        return f"RETURNnode({repr(self.return_value)})"

class CASOParser:
    def __init__(self, tokens):
        self.tokens = tokens
        self.current_position = 0
        self.nodes = [] # This will be the list of nodes that will be returned by the parse() method
        self.variables = {} # This will be the dictionary of variables that will be returned by the parse() method
        self.functions = {} # This will be the dictionary of functions that will be returned by the parse() method    

    # Useful constants
    TYPES = ['LIST', 'STRING', 'INT', 'FLOAT', 'BOOLEAN']
    ARITHMETIC_OPERATORS = ['PLUS', 'MINUS', 'MUL', 'DIV', 'MOD']
    COMPARISON_OPERATORS = ['EQ', 'NEQ', 'LT', 'LE', 'GT', 'GE', 'UKN']

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
        elif current_token.type == "WHEN":
            self.parse_when()
        elif current_token.type == "FUNCTION":
            self.parse_function_declaration()
        elif current_token.type == "PIPE":
            self.parse_return()
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
        
        # Check if the variable type is a list
        is_list = False
        if variable_type_token.type == "LIST": # This means that the variable type is a list
            variable_type = self.parse_list()
            is_list = True # Set the is_list flag to True
        else:
            variable_type = variable_type_token.value
            self.current_position += 1 # Skip the variable type token

        # Now should come the assignment operator
        assignment_token = self.tokens[self.current_position]
        if assignment_token.type != "ASSIGN":
            raise CASOSyntaxError(f"Expected assignment operator, got {assignment_token.type}", assignment_token.line_num, assignment_token.char_pos)

        # Now should come the variable value, which can be either an expression or a list
        self.current_position += 1 # Skip the assignment token
        if is_list:
            variable_value = self.parse_list_expression()
        else:
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
        open_bracket_token = self.tokens[self.current_position]
        if open_bracket_token.type != "OPEN_BRACKET":
            raise CASOSyntaxError(f"Expected open bracket, got {open_bracket_token.type}", open_bracket_token.line_num, open_bracket_token.char_pos)
        list_content_type = 'List['

        # Recursively parse the list
        self.current_position += 1 # Skip the open bracket token
        list_content_type += str(self.parse_list_content())

        # Checking for correct syntax
        close_bracket_token = self.tokens[self.current_position]
        if close_bracket_token.type != "CLOSE_BRACKET":
            raise CASOSyntaxError(f"Expected close bracket, got {close_bracket_token.type}", close_bracket_token.line_num, close_bracket_token.char_pos)

        # Finally finish parsing the list
        self.current_position += 1 # Skip the close bracket token
        return list_content_type + ']'

    def parse_list_content(self):
        current_token = self.tokens[self.current_position]
        if current_token.type == "LIST": # Checking if the list contains another list
            return self.parse_list() 
        elif current_token.type in self.TYPES: # Checking if the list contains a primitive type
            self.current_position += 1 # Skip the type token
            return current_token.value
        else:
            raise CASOSyntaxError(f"Expected list content, got {current_token.type}", current_token.line_num, current_token.char_pos)

    # Method that will parse the when statement
    def parse_when(self):
        self.current_position += 1 # Skip the WHEN token
        if self.tokens[self.current_position].type != 'ID':
            raise CASOSyntaxError(f"Expected variable name, got {self.tokens[self.current_position].type}", self.tokens[self.current_position].line_num, self.tokens[self.current_position].char_pos)

        # Checking if the variable name is in the dictionary of variables
        variable_name = self.tokens[self.current_position].value
        if variable_name not in self.variables:
            raise CASOSyntaxError(f"Variable {variable_name} not declared", self.tokens[self.current_position].line_num, self.tokens[self.current_position].char_pos)
        
        # Correct syntax check
        self.current_position += 1 # Skip the variable name token
        if self.tokens[self.current_position].type != 'OPEN_BRACE':
            raise CASOSyntaxError(f"Expected open bracket, got {self.tokens[self.current_position].type}", self.tokens[self.current_position].line_num, self.tokens[self.current_position].char_pos)

        # Pattern matching for the variable
        self.current_position += 1  # Skip the open brace token
        match_cases = []

        while True:
            # Skip any newline tokens
            while self.tokens[self.current_position].type == 'NEWLINE':
                self.current_position += 1

            # Break the loop if the next token is a closing brace
            if self.tokens[self.current_position].type == 'CLOSE_BRACE':
                break

            match_case = self.parse_pattern()
            match_cases.append(match_case)

            # Move to the next token and check if it's a comma, a closing brace, or the start of a new match case
            self.current_position += 1
            while self.tokens[self.current_position].type == 'NEWLINE':
                self.current_position += 1

            if self.tokens[self.current_position].type == 'COMMA':
                self.current_position += 1  # Skip the comma token
            elif self.tokens[self.current_position].type == 'CLOSE_BRACE':
                break  # End of the `when` block
            elif self.tokens[self.current_position].type in self.COMPARISON_OPERATORS:
                continue  # Start of a new MATCHCASEnode
            else:
                raise CASOSyntaxError(f"Expected comma, closing brace, or a pattern operator, got {self.tokens[self.current_position].type}", 
                                      self.tokens[self.current_position].line_num, 
                                      self.tokens[self.current_position].char_pos)

        self.current_position += 1  # Skip the close brace token
        append_node = WHENnode(variable_name, match_cases)
        self.nodes.append(append_node)

    def parse_pattern(self):
        # Skip any newlines or unexpected tokens at the beginning
        while self.tokens[self.current_position].type in ['NEWLINE']:
            self.current_position += 1

        # Now we are at the beginning of the pattern
        if self.tokens[self.current_position].type not in self.COMPARISON_OPERATORS:
            raise CASOSyntaxError(f"Expected pattern operator, got {self.tokens[self.current_position].type}", self.tokens[self.current_position].line_num, self.tokens[self.current_position].char_pos)
        match_type = self.tokens[self.current_position].type # Saving the match type

        # If the match type is UKN, then we don't need to check for value syntax
        match_value = None
        if match_type != 'UKN':
            # Checking for value syntax, here can go: variables, numbers, list values, false, true, unknown, but can't go: expressions or lists 
            self.current_position += 1 # Skip the comparison operator token
            if self.tokens[self.current_position].type == 'ID':
                # Checking if the variable is declared
                if self.tokens[self.current_position].value not in self.variables:
                    raise CASOSyntaxError(f"Variable {self.tokens[self.current_position].value} not declared", self.tokens[self.current_position].line_num, self.tokens[self.current_position].char_pos)
            match_value = self.tokens[self.current_position].value # Saving the match value

        # Checking for arrow syntax
        self.current_position += 1 # Skip the value token
        if self.tokens[self.current_position].type != 'ARROW':
            raise CASOSyntaxError(f"Expected arrow, got {self.tokens[self.current_position].type}", self.tokens[self.current_position].line_num, self.tokens[self.current_position].char_pos)

        # Checking for action 
        self.current_position += 1 # Skip the arrow token
        if self.tokens[self.current_position].type != 'OPEN_BRACE':
            raise CASOSyntaxError(f"Expected open brace, got {self.tokens[self.current_position].type}", self.tokens[self.current_position].line_num, self.tokens[self.current_position].char_pos)

        # Instantiating the match case node
        self.current_position += 1 # Skip the open brace token
        match_case_node = MATCHCASEnode(match_type, match_value)

        # Parsing the body of the match case
        while self.tokens[self.current_position].type != 'CLOSE_BRACE':
            action_node = self.parse_action()
            match_case_node.children.append(action_node)

        # Returning the match case node
        self.current_position += 1 # Skip the close brace token
        return match_case_node

    # Method that will parse the action statement
    def parse_action(self):
        # Inside actions can go any statement, whatever is valid
        # NOTE: FOR FUTURE REFERENCE, WE HAVE ALREADY SKIPPED THE OPEN BRACE TOKEN
        while self.tokens[self.current_position].type != 'CLOSE_BRACE':
            self.parse_statement()

        action_node = self.nodes.pop()
        return action_node

    # Method that will parse the function definition
    def parse_function_declaration(self):
        # Checking for correct syntax
        self.current_position += 1 # Skip the FNC token
        if self.tokens[self.current_position].type != 'ID':
            raise CASOSyntaxError(f"Expected function name, got {self.tokens[self.current_position].type}", self.tokens[self.current_position].line_num, self.tokens[self.current_position].char_pos)

        # Checking if the function name is already declared
        function_name = self.tokens[self.current_position].value # Saving the function name
        if function_name in self.functions:
            raise CASOSyntaxError(f"Function {function_name} already declared", self.tokens[self.current_position].line_num, self.tokens[self.current_position].char_pos)

        # Checking for correct syntax
        self.current_position += 1 # Skip the function name token
        if self.tokens[self.current_position].type != 'OPEN_PAREN':
            raise CASOSyntaxError(f"Expected open parenthesis, got {self.tokens[self.current_position].type}", self.tokens[self.current_position].line_num, self.tokens[self.current_position].char_pos)

        # Parsing the parameters
        self.current_position += 1 # Skip the open parenthesis token
        parameters = {} # Dictionary that will hold the parameters
        while self.tokens[self.current_position].type != 'CLOSE_PAREN':
            if self.tokens[self.current_position].type != 'ID':
                raise CASOSyntaxError(f"Expected parameter name, got {self.tokens[self.current_position].type}", self.tokens[self.current_position].line_num, self.tokens[self.current_position].char_pos)
            parameter_name = self.tokens[self.current_position].value # Saving the parameter name
            # Adding the parameter to the dictionary
            if parameter_name in parameters:
                raise CASOSyntaxError(f"Parameter {parameter_name} already declared", self.tokens[self.current_position].line_num, self.tokens[self.current_position].char_pos)
            # Adding the parameter to the variables (so that it can be used inside the function)
            self.variables[parameter_name] = None
            
            # Assigning type to the parameter
            self.current_position += 1 # Skip the parameter name token
            if self.tokens[self.current_position].type != 'TYPE_ASSIGN':
                raise CASOSyntaxError(f"Expected type assignment, got {self.tokens[self.current_position].type}", self.tokens[self.current_position].line_num, self.tokens[self.current_position].char_pos)
            self.current_position += 1 # Skip the type assignment token
            if self.tokens[self.current_position].type not in self.TYPES:
                raise CASOSyntaxError(f"Expected type, got {self.tokens[self.current_position].type}", self.tokens[self.current_position].line_num, self.tokens[self.current_position].char_pos)
            parameter_type = self.tokens[self.current_position].type
            parameters[parameter_name] = parameter_type

            # Checking for comma or close parenthesis
            self.current_position += 1 # Skip the type token
            if self.tokens[self.current_position].type == 'COMMA':
                self.current_position += 1 # Skip the comma token
            elif self.tokens[self.current_position].type == 'CLOSE_PAREN':
                break
            else:
                raise CASOSyntaxError(f"Expected comma or close parenthesis, got {self.tokens[self.current_position].type}", self.tokens[self.current_position].line_num, self.tokens[self.current_position].char_pos)

        # Checking for correct syntax
        self.current_position += 1 # Skip the close parenthesis token
        if self.tokens[self.current_position].type != 'TYPE_ASSIGN':
            raise CASOSyntaxError(f"Expected type assignment, got {self.tokens[self.current_position].type}", self.tokens[self.current_position].line_num, self.tokens[self.current_position].char_pos)

        # Assigning type to the function
        self.current_position += 1 # Skip the type assignment token
        if self.tokens[self.current_position].type not in self.TYPES:
            raise CASOSyntaxError(f"Expected type, got {self.tokens[self.current_position].type}", self.tokens[self.current_position].line_num, self.tokens[self.current_position].char_pos)
        function_type = self.tokens[self.current_position].type
        
        # Checking for the function body
        self.current_position += 1 # Skip the type token
        if self.tokens[self.current_position].type != 'OPEN_BRACE':
            raise CASOSyntaxError(f"Expected open brace, got {self.tokens[self.current_position].type}", self.tokens[self.current_position].line_num, self.tokens[self.current_position].char_pos)

        # Parsing the body of the function
        self.current_position += 1 # Skip the open brace token
        function_body = []
        while self.tokens[self.current_position].type != 'CLOSE_BRACE':
            function_body.append(self.parse_statement())

        # Checking for correct syntax
        self.current_position += 1 # Skip the close brace token
        if self.tokens[self.current_position].type != 'NEWLINE':
            raise CASOSyntaxError(f"Expected new line, got {self.tokens[self.current_position].type}", self.tokens[self.current_position].line_num, self.tokens[self.current_position].char_pos)

        # Append the function definition to the functions dictionary
        self.functions[function_name] = (parameters, function_type, function_body)

        # Append the function definition to the AST
        function_definition_node = FUNCTIONDECLARATIONnode(function_name, parameters, function_type, function_body)
        self.nodes.append(function_definition_node)

        # Removing all the parameters from the variables dictionary
        for parameter in parameters:
            self.variables.pop(parameter)

    def parse_return(self):
        # Checking for correct syntax
        self.current_position += 1 # Skip the PIPE token
        if self.tokens[self.current_position].type == 'ID':
            return_value = self.parse_expression()
        else:
            raise CASOSyntaxError(f"Expected ID, got {self.tokens[self.current_position].type}", self.tokens[self.current_position].line_num, self.tokens[self.current_position].char_pos)

        # Append the return statement to the AST
        return_node = RETURNnode(return_value)
        self.nodes.append(return_node)
