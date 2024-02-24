# TODO: Finish implementing list parsing. (DONE)

# TODO: Implement function calling, we already got function declaration done. (DONE)
#   - I made the basic function call node and parsing but I have yet to implement the actual parsing of it, the main problems are:
#   1. When using a if statement inside a function call, the parser throws a 'Unable to pop from an empty list' error. (DONE): This happened, not because of the function call, but because of the 'parse_action' function, it was popping even when the list was empty, throwing an error, I simply added a if check.
#   2. The function call node is not being parsed correctly, as I have to determine whether what I'm parsing is a function call or a variable assignment. (DONE)
#   3. Making it so that the transpiler, transpiles the function declarations outside of the main function. (DONE)

# TODO: Finishing if, elsif and else statements. (DONE)
#   - If statements are done. (DONE)
#   - Else statements are yet to do. (DONE)
#   - Elsif are throwing some kind of error: `An error occurred: 'NoneType' object has no attribute 'type'` (DONE)

# TODO: Adding new type of loop, for loops are boring. (DONE)
# TODO: Making it so that the elsif statement checks if the previous VALID node was an if statement or an elsif statement. (IN PROGRESS - MOMENTARILY PAUSED - I've tried doing it but my version doesn't work with nested structures, maybe I'll ask ChatGPT to help me idk :) )

# TODO: Fix local variable error:
#   - The error consists on the fact that the parser puts all variables inside the same list and doesn't track the scope of the variables, so if you declare a variable inside a function, even if inside the Java code the variable is transpiled as local, the parser doesn't understand that and throws an error. (DONE)

# TODO: Converting variable types into Java types directly from the parser. (IN PROGRESS - MOMENTARILY PAUSED)
# TODO: Converting variable types into Java types directly from the parser. (DONE)

# TODO: Implement the 'use' keyword for importing modules. (DONE)

# TODO: Implement the 'object' keyword for object declaration (classes in Java):
#   - I gotta implement a OBJECTnode and then make the syntax and all. (DONE)
#   - I need another stack for the object attributes and methods, as they are not the same as the global variables and functions. (DONE)
#   - Implement full inheritance. (IN PROGRESS - ALMOST DONE)

# TODO: Add libraries function and variable calls, for future me, here's a example: (IN PROGRESS - MOMENTARILY PAUSED)
#   - `use standard`
#   - `standard::print_line("Hello, World!")`

# TODO: Add being able to use `self` `super` and the dot operator for object attributes and methods. (IN PROGRESS)
#   - Gotta check for errors and existing objects and shit, for now I've only made the general AST node
#   - Future me, don't forget to add objects as types for variables (basically object declaration you stupid bastard)

# TODO: Implement scoping for ALL the possible cases, this means: obejcts, functions, attributes, constructors, etc...
#   - I can't do it all today, so for future me, remember this pseudocode:
#       First thing that comes to my mind is to make it so that declared variables can actually be seen as objects, this means that I'll need to make a new parameter
#       for the variable infos stating if it's a object or not, in case it is a object then we can access it, else, we can't. How do we know if the var is a object?
#       We will simply check if it's been declared after the name of a object (remember we add objects as types whenever we declare one).

# TODO: Add 'at' notation (me, remember to look at your notes)
# TODO: Add 'at' notation (me, remember to look at your notes). (DONE)
#   - I should also add the 'at' notation for functions, idk :/

from enum import Enum

from caso_exception import CASOSyntaxError, CASOAttributeError, CASOValueError, CASONameError, CASOIndexError, CASOIllegalTokenError, CASONotDeclaredError, CASOWarning, CASOInvalidClassMemberError, CASOInvalidTypeError, CASOClassNotFoundError, CASOImportError, CASOUnexpectedTokenError
from caso_exception import CASOSyntaxError, CASOAttributeError, CASOValueError, CASONameError, CASOIndexError, CASOIllegalTokenError, CASONotDeclaredError, CASOWarning, CASOInvalidClassMemberError, CASOInvalidTypeError, CASOClassNotFoundError, CASOImportError, CASOUnexpectedTokenError, CASOClassAlreadyDeclaredError, CASOMismatchedTypeError
from caso_lexer import CASOLexer
from caso_types import conversion_table 

import os

class NodeType(Enum):
    VARIABLE_DECLARATION = 1
    VARIABLE_ASSIGNMENT = 2
    EXPRESSION = 3
    WHEN = 4
    MATCHCASE = 5
    FUNCTION_DECLARATION = 6
    FUNCTION_CALL = 7
    RETURN = 8
    IF = 9
    ELSE = 10
    ELSIF = 11
    LOOP = 12
    JAVA_SOURCE = 13
    USE = 14
    OBJECT = 15
    ATTRIBUTE_ACCESS = 16
    LOAN = 17

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
        self.variable_type = conversion_table[variable_type]
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
    def __init__(self, function_name, function_args, return_type):
        super().__init__(NodeType.FUNCTION_DECLARATION)
        self.function_name = function_name
        self.function_args = function_args
        self.return_type = conversion_table[return_type]
        self.function_body = [] # Body of the function

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

class IFnode(ASTnode):
    def __init__(self, condition):
        super().__init__(NodeType.IF)
        self.condition = condition
        self.if_body = [] # Body of the if statement

    def __repr__(self):
        return f"IFnode({repr(self.condition)}, {repr(self.if_body)})"

class ELSEnode(ASTnode):
    def __init__(self):
        super().__init__(NodeType.ELSE)
        self.else_body = [] # Body of the else statement

    def __repr__(self):
        return f"ELSEnode({repr(self.else_body)})"

class ELSIFnode(ASTnode):
    def __init__(self, condition):
        super().__init__(NodeType.ELSIF)
        self.condition = condition
        self.elsif_body = [] # Body of the elsif statement

    def __repr__(self):
        return f"ELSIFnode({repr(self.condition)}, {repr(self.elsif_body)})"

class LOOPnode(ASTnode):
    def __init__(self, loop_variable, loop_start, loop_end, loop_guard=None):
        super().__init__(NodeType.LOOP)
        self.loop_variable = loop_variable
        self.loop_start = loop_start
        self.loop_end = loop_end
        self.loop_guard = loop_guard
        self.loop_body = [] # Body of the loop

    def __repr__(self):
        return f"LOOPnode({repr(self.loop_variable)}, {repr(self.loop_start)}, {repr(self.loop_end)}, {repr(self.loop_guard)}, {repr(self.loop_body)})"

class JAVASOURCEnode(ASTnode):
    def __init__(self, java_code):
        super().__init__(NodeType.JAVA_SOURCE)
        self.java_code = java_code

    def __repr__(self):
        return f"JAVASOURCEnode({repr(self.java_code)})"

class OBJECTnode(ASTnode):
    def __init__(self, object_name, object_attributes, object_methods=None, parent_class=None, parent_class_attributes=None, parent_class_methods=None):
        super().__init__(NodeType.OBJECT)
        self.object_name = object_name
        self.object_attributes = object_attributes
        self.object_methods = object_methods
        self.parent_class = parent_class
        self.parent_class_attributes = parent_class_attributes
        self.parent_class_methods = parent_class_methods

    def __repr__(self):
        return f"OBJECTnode({repr(self.object_name)}, {repr(self.object_attributes)}, {repr(self.object_methods)}, {repr(self.parent_class)}, {repr(self.parent_class_attributes)}, {repr(self.parent_class_methods)})"

class USEnode(ASTnode):
    def __init__(self, module_name, imports):
        super().__init__(NodeType.USE)
        self.module_name = module_name
        self.imports = imports

    def __repr__(self):
        return f"USEnode({repr(self.module_name)}, {repr(self.imports)})"

class ATTRIBUTEACCESSnode(ASTnode):
    def __init__(self, object_name, attribute_name):
        super().__init__(NodeType.ATTRIBUTE_ACCESS)
        self.object_name = object_name
        self.attribute_name = attribute_name

    def __repr__(self):
        return f"ATTRIBUTEACCESSnode({repr(self.object_name)}, {repr(self.attribute_name)})"

class LOANnode(ASTnode):
    def __init__(self, loan_variable):
        super().__init__(NodeType.LOAN)
        self.loan_variable = loan_variable
        self.loan_body = [] # Body of the loan

    def __repr__(self):
        return f"LOANnode({repr(self.loan_variable)}, {repr(self.loan_body)})"

class CASOParser:
    def __init__(self, tokens):
        self.tokens = tokens
        self.current_position = 0
        self.nodes = [] # This will be the list of nodes that will be returned by the parse() method
        self.functions = {} # This will be the dictionary of functions that will be returned by the parse() method    
        self.scope_stack = [{}] # Keeping track of the scope of the variables
        self.object_stack = [] # Inside here we will put the full object declaration node, with its attributes and methods
        self.imported_modules = [] # List of imported modules

    # Useful constants
    TYPES = ['LIST', 'STRING', 'INT', 'FLOAT', 'BOOL', 'EMPTY']
    ARITHMETIC_OPERATORS = ['PLUS', 'MINUS', 'MUL', 'DIV', 'MOD']
    COMPARISON_OPERATORS = ['EQ', 'NEQ', 'LT', 'LE', 'GT', 'GE', 'UKN', 'OR', 'AND', 'TRUE', 'FALSE'] + ARITHMETIC_OPERATORS

    # Scoping variables
    current_node = None # This will be the current node

    def parse(self):
        while self.current_position < len(self.tokens):
            self.nodes.append(self.parse_statement())

        # Debug scope stack printing
        print('Scope stack:')
        print(self.scope_stack, end='\n\n')

        print('Object stack:')
        print(self.object_stack, end='\n\n')

        return self.nodes

    def parse_statement(self):
        current_token = self.tokens[self.current_position]

        if current_token.type == "LET":
            self.parse_declaration()
        elif current_token.type == "ID":
            if self.tokens[self.current_position + 1].type == "REASSIGN":
                self.parse_assignment()
            elif self.tokens[self.current_position + 1].type == "LPAREN":
                self.parse_function_call()
            elif self.tokens[self.current_position + 1].type == "DOT":
                self.parse_object_attribute_access()
            else:
                raise Exception(f"Invalid token {current_token.value} at position {current_token.position}")

        elif current_token.type == "WHEN":
            self.parse_when()
        elif current_token.type == "FUNCTION":
            self.parse_function_declaration()
        elif current_token.type == "PIPE":
            self.parse_return()
        elif current_token.type == "IF":
            self.parse_if()
        elif current_token.type == 'ELSIF':
            self.parse_elsif()
        elif current_token.type == 'ELSE':
            self.parse_else()
            # TODO: Implement else parsing (DONE)
        elif current_token.type == 'LOOP':
            self.parse_loop()
        # This is a very important part of the parser, as it will allow us to include Java code in our CASO code
        elif current_token.type == 'GENERAL_JAVA_TOKEN':
            self.parse_java_source() 
        elif current_token.type == 'OBJECT':
            self.parse_object()
        elif current_token.type == 'INIT':
            self.parse_constructor()
        elif current_token.type == 'USE':
            self.parse_use()
        else:
            if current_token.type == "NEWLINE":
                self.current_position += 1
            else:
                raise CASOIllegalTokenError(f"Unexpected token {current_token.type}", current_token.line_num, current_token.char_pos)

    def expect_token(self, *expected_types):
        """Checks if the current token matches one of the expected types. Raises an error if not."""
        current_token = self.tokens[self.current_position]
        
        # Prepare the error message in advance, assuming a mismatch will occur
        error_message = f"Expected token of type {', '.join(expected_types)}, but got {current_token.type}"
        
        # Check if the current token's type is among the expected types
        if current_token.type not in expected_types:
            raise CASOSyntaxError(error_message, current_token.line_num, current_token.char_pos)
        
        # If the check passes, return the current token
        return current_token

    def advance_token(self):
        '''This method will advance the current token position by one and return the new current token'''
        self.current_position += 1
        return self.tokens[self.current_position]

    def current_token(self):
        '''This method will return the current token'''
        return self.tokens[self.current_position]

    def current_token_type(self):
        '''This method will return the current token type'''
        return self.current_token().type

    def current_token_value(self):
        '''This method will return the current token value'''
        return self.current_token().value

    def register_variable(self, variable_name, variable_type, initial_value=None, used=False, at=False):
        '''Updated to register a variable with its type, an initial value, and additional info'''
        if self.lookup_variable(variable_name) is not None:
            raise CASOSyntaxError(f"Variable {variable_name} already declared in this scope", self.current_token().line_num, self.current_token().char_pos)
        
        variable_info = {
            'type': variable_type,
            'value': initial_value,
            'used': used,
            'at': at # Check if the variable follows 'at' notation
        }

        self.add_variable_to_current_scope(variable_name, variable_info)

    def is_registered_variable(self, variable_name):
        '''This method will check if a variable is already registered'''
        return False if self.lookup_variable(variable_name) is None else True

    def is_not_registered_variable_exception(self, variable_name):
        '''This method will check if a variable is not registered and raise an exception if it is'''
        if not self.is_registered_variable(variable_name):
            raise CASOSyntaxError(f"Variable {variable_name} not declared", self.current_token().line_num, self.current_token().char_pos)

    def is_registered_variable_exception(self, variable_name):
        '''This method will check if a variable is already registered and raise an exception if it is'''
        if self.is_registered_variable(variable_name):
            raise CASOSyntaxError(f"Variable {variable_name} already declared", self.current_token().line_num, self.current_token().char_pos)

    def is_valid_type(self, variable_type):
        '''This method will check if a variable type is valid'''
        return variable_type in self.TYPES

    def is_valid_type_exception(self, variable_type):
        '''This method will check if a variable type is valid and raise an exception if it is not'''
        if not self.is_valid_type(variable_type):
            raise CASOSyntaxError(f"Invalid variable type {variable_type}", self.current_token().line_num, self.current_token().char_pos)
        return True

    def is_registered_function(self, function_name):
        '''This method will check if a function is already registered'''
        return function_name in self.functions

    def is_not_registered_function_exception(self, function_name):
        '''This method will check if a function is not registered and raise an exception if it is'''
        if not self.is_registered_function(function_name):
            raise CASOSyntaxError(f"Function {function_name} not declared", self.current_token().line_num, self.current_token().char_pos)

    def is_registered_function_exception(self, function_name):
        '''This method will check if a function is already registered and raise an exception if it is'''
        if self.is_registered_function(function_name):
            raise CASOSyntaxError(f"Function {function_name} already declared", self.current_token().line_num, self.current_token().char_pos)

    def push_scope(self):
        '''This method will push a new scope to the scope stack'''
        self.scope_stack.append({})

    def pop_scope(self):
        '''This method will pop the current scope from the scope stack'''
        if len(self.scope_stack) > 1:
            self.scope_stack.pop()
        else:
            raise CASOSyntaxError("No scope to pop", self.current_token().line_num, self.current_token().char_pos)

    def add_variable_to_current_scope(self, variable_name, variable_info):
        '''Modifies the scope to store a dictionary with variable information instead of just the type'''
        if variable_name in self.scope_stack[-1]:
            raise CASONotDeclaredError(f"Variable {variable_name} already declared in this scope", self.current_token().line_num, self.current_token().char_pos)
        self.scope_stack[-1][variable_name] = variable_info

    def lookup_variable(self, variable_name):
        for scope in reversed(self.scope_stack):
            if variable_name in scope:
                return scope[variable_name]
        return None  # Variable not found

    def modify_variable_value(self, variable_name, new_value):
        '''This method will modify the value of a variable'''
        variable_info = self.lookup_variable(variable_name)
        if variable_info is None:
            raise CASONotDeclaredError(self.current_token().line_num, self.current_token().char_pos, self.current_token_type()) 
        variable_info['value'] = new_value

    def current_line_num(self):
        '''This method will return the current line number'''
        return self.current_token().line_num

    def current_char_pos(self):
        '''This method will return the current character position'''
        return self.current_token().char_pos

    def library_exists(self, library_name):
        '''This method will check if a library exists inside the /libraries directory'''
        return os.path.exists(f"test/libraries/{library_name}.caso")

    def get_library_source_code(self, library_name):
        '''This method will return the source code of a library'''
        with open(f"test/libraries/{library_name}.caso", "r") as file:
            return file.read()

    # List of the methods that will parse the different types of statements
    def parse_declaration(self):
        self.advance_token() # Skip the LET token
        
        # Checking for 'at' notation
        at_notation = False
        if self.current_token_type() == 'AT':
            at_notation = True
            self.advance_token() # Skip the AT token

        # The next token should be the variable name
        variable_name_token = self.expect_token("ID")
        variable_name_token = self.expect_token('ID')
        variable_name = variable_name_token.value # Save the variable name

        # Check if the variable name is already in the dictionary of variables
        self.is_registered_variable_exception(variable_name)

        # Now should come the type assignment operator
        self.advance_token() # Skip the variable name token
        self.expect_token("TYPE_ASSIGN")
        self.expect_token('TYPE_ASSIGN')

        # Now should come the variable type
        self.advance_token() # Skip the type assignment token
        variable_type_token = self.tokens[self.current_position]
        self.is_valid_type(variable_type_token.value) # Check if the variable type is valid
        
        # Check if the variable type is a list
        is_list = False
        if variable_type_token.type == "LIST": # This means that the variable type is a list
            variable_type = self.parse_list()
            is_list = True # Set the is_list flag to True
        else:
            variable_type = variable_type_token.value
            self.current_position += 1 # Skip the variable type token

        # Now should come the assignment operator
        self.expect_token("ASSIGN")
        self.expect_token('ASSIGN')

        # Now should come the variable value, which can be either an expression or a list
        self.current_position += 1 # Skip the assignment token
        if is_list:
        self.advance_token() # Skip the assignment token
        if is_list: # If the variable type is a list, then the variable value should be a list expression
            variable_value = self.parse_list_expression()
        else:
            variable_value = self.parse_expression()
            # Here 2 things could happen, loan functions or an expression
            if self.current_token_type() == 'FROM':
                # If the current token is a FROM token, then we should parse the loan function
                # For doing this, we will set the current variable value to 'None' and then parse the loan function first
                # so that we can get the variable value from the loan function later
                self.parse_loan() # For later, here we should get the variable value from the loan function
                variable_value = self.nodes[-1].loan_variable # Get the variable value from the loan function
            else:
                variable_value = self.parse_expression()

        # We can now add the variable to the current scope
        self.register_variable(variable_name, variable_type, variable_value, False, at_notation)

        # After all the above, we can add the declaration node to the list of nodes
        append_node = DECLARATIONnode(variable_name, variable_type, variable_value)
        self.nodes.append(append_node)

    # This function will be used to parse the assignment statement
    def parse_assignment(self):
        # The first token should be the variable name
        variable_name_token = self.current_token() # Save the variable name token
        variable_name = variable_name_token.value

        # Check if the variable name is in the dictionary of variables
        self.is_not_registered_variable_exception(variable_name)

        # Adding one to number of times the variable has been used
        for scope in reversed(self.scope_stack): # Loop through the scope stack
            if variable_name in scope:
                variable_info = scope[variable_name] # Get the variable info
                variable_info['used'] = True # Adding one to the number of times the variable has been used
                break # Break the loop after the variable has been found

        # Now should come the assignment operator
        self.advance_token() # Skip the variable name token
        assignment_token = self.expect_token('REASSIGN')

        # Now should come the variable value, which is an expression
        self.advance_token() # Skip the assignment token
        variable_value = self.parse_expression()
        if variable_value == '':
            raise CASOSyntaxError(f"Expected expression, got {variable_value}", assignment_token.line_num, assignment_token.char_pos)

        # Modify the variable value in the dictionary of variables
        self.modify_variable_value(variable_name, variable_value)
   
        # After all the above, we can add the assignment node to the list of nodes
        append_node = ASSIGNMENTnode(variable_name, variable_value)
        self.nodes.append(append_node)

    # This is the method that will parse ALL expressions
    def parse_expression(self) -> str:
        return self.parse_until('NEWLINE')

    # This method will parse a list expression
    def parse_until(self, *token_types: str) -> str:
        ''' 
        This method will parse an expression until one of the specified token types is found, skipping the final token.

        Parameters:
        - token_types (str): The types of tokens to parse until (variable number of arguments)

        Returns:
        - expression_string (str): The parsed expression as a string
        '''
        expression_tokens = []

        # Collect all the tokens until one of the specified token types is found, I gotta check for this fucking new lines every time, I gotta fix this shit
        while self.current_position < len(self.tokens) and self.current_token_type() not in token_types and self.current_token_type() != 'NEWLINE':
            token = self.current_token()
            if token.type in self.COMPARISON_OPERATORS:
                expression_tokens.append(token)
            elif token.type == 'ID':
                # User is trying to call a variable (never in my life will I implement recursion)
                if self.is_registered_variable(token.value) == True:
                    expression_tokens.append(token)
                    # Adding 1 to the number of times the variable has been used
                    for scope in reversed(self.scope_stack):
                        if token.value in scope:
                            variable_info = scope[token.value]
                            variable_info['used'] = True
                            break
                else:
                    raise CASOSyntaxError(f"Expression variable {self.tokens[self.current_position].value} not declared", self.current_line_num(), self.current_char_pos())
            elif token.type == 'NUMBER':
                expression_tokens.append(token)
            elif token.type == 'STRING_LITERAL':
                expression_tokens.append(token)
            else:
                raise CASOSyntaxError(f"Unexpected token {token.type}", token.line_num, token.char_pos)
            self.current_position += 1

        # Skip the token if it matches one of the specified token types
        if self.current_position < len(self.tokens) and self.tokens[self.current_position].type in token_types:
            self.current_position += 1 # Skip the token

        # Convert to raw string (ensuring all values are strings)
        expression_string = ' '.join(str(token.value) for token in expression_tokens)
        return expression_string

    def parse_list_expression(self):
        # Checking for correct syntax
        self.current_position += 1 # Skip the open bracket token

        # Parsing the list
        list_values = []
        while self.current_token_type() != 'CLOSE_BRACKET':
            list_values.append(self.current_token_value())
            self.advance_token()

            # Checking for correct syntax
            if self.current_token_type() == 'COMMA':
                self.advance_token() # Skip the comma token

        # Checking for correct syntax
        self.expect_token('CLOSE_BRACKET')

        # Finally finish parsing the list
        self.advance_token() # Skip the close bracket token
        return list_values

    # This is the method that will parse lists
    def parse_list(self):
        # Checking for correct syntax
        self.advance_token() # Skip the list token
        self.expect_token('OPEN_BRACKET')
        list_content_type = 'List['

        # Recursively parse the list
        self.advance_token() # Skip the open bracket token
        list_content_type += str(self.parse_list_content())

        # Checking for correct syntax
        self.expect_token('CLOSE_BRACKET')

        # Finally finish parsing the list
        self.advance_token() # Skip the close bracket token
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
        self.is_not_registered_variable_exception(variable_name)
        
        # Correct syntax check
        self.current_position += 1 # Skip the variable name token
        if self.tokens[self.current_position].type != 'OPEN_BRACE':
            raise CASOSyntaxError(f"Expected open bracket, got {self.tokens[self.current_position].type}", self.tokens[self.current_position].line_num, self.tokens[self.current_position].char_pos)

        # Pattern matching for the variable
        self.current_position += 1  # Skip the open brace token
        match_cases = []

        while True:

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

        self.advance_token()  # Skip the closing brace token
        append_node = WHENnode(variable_name, match_cases)
        self.nodes.append(append_node)

    def parse_pattern(self):
        # Skip any newlines or unexpected tokens at the beginning
        while self.tokens[self.current_position].type in ['NEWLINE']:
            self.advance_token()

        # Now we are at the beginning of the pattern
        if self.tokens[self.current_position].type not in self.COMPARISON_OPERATORS:
            raise CASOSyntaxError(f"Expected pattern operator, got {self.tokens[self.current_position].type}", self.tokens[self.current_position].line_num, self.tokens[self.current_position].char_pos)
        match_type = self.current_token_type()

        # If the match type is UKN, then we don't need to check for value syntax
        match_value = None
        if match_type != 'UKN':
            # Checking for value syntax, here can go: variables, numbers, list values, false, true, unknown, but can't go: expressions or lists 
            self.advance_token() # Skip the match type token
            if self.tokens[self.current_position].type == 'ID':
                # Checking if the variable is declared
                self.is_registered_variable(self.current_token_value())
            match_value = self.current_token_value()

        # Checking for arrow syntax
        self.advance_token() # Skip the arrow token
        self.expect_token('ARROW') # Checking for correct syntax

        self.advance_token() # Skip the arrow token
        match_case_node = MATCHCASEnode(match_type, match_value)

        # Ensure we have an opening brace for the case body
        self.expect_token('OPEN_BRACE')

        self.advance_token() # Skip the open brace token
        match_case_body = self.parse_action()
        match_case_node.children = match_case_body

        return match_case_node

    # Method that will parse bodys of actions
    def parse_action(self):
        # NOTE: THIS WILL BE USED FOR HANDLING EVERYTHING UNTIL THE END OF THE BODY OF SOMETHING (WHEN, FUNCTIONS, ETC)
        # Skip any newlines or unexpected tokens at the beginning 
        # NOTE: ASSUME WE ALREADY SKIPPED THE OPEN BRACE TOKEN
        while self.current_token_type() in ['NEWLINE']:
            self.advance_token()

        # Now we are at the beginning of the body
        full_body = []
        while self.current_token_type()  != 'CLOSE_BRACE':
            self.parse_statement()
            if not self.nodes: # Check if the nodes are empty
                continue # If they are, continue to the next token

            parsed_statement = self.nodes.pop() # Saving the parsed statement
            full_body.append(parsed_statement)

        self.advance_token() # Skip the close brace token
        return full_body

    # Method that will parse the function definition
    def parse_function_declaration(self):
        # Entering a new scope
        self.push_scope()

        # Checking for correct syntax
        self.advance_token() # Skip the FUNCTION token
        self.expect_token('ID') # Expecting a function name token

        # Checking if the function name is already declared
        function_name = self.current_token_value() # Saving the function name
        self.is_registered_function(function_name) # Checking if the function is already declared)

        # Checking for correct syntax
        self.advance_token() # Skip the function name token
        self.expect_token('OPEN_PAREN') # Expecting an open parenthesis token

        # Parsing the parameters
        self.advance_token() # Skip the open parenthesis token
        parameters = {} # Dictionary that will hold the parameters
        while self.tokens[self.current_position].type != 'CLOSE_PAREN':
            self.expect_token('ID') # Expecting a parameter name
            parameter_name = self.current_token_value() 

            # Adding the parameter to the dictionary
            if parameter_name in parameters:
                raise CASOSyntaxError(f"Parameter {parameter_name} already declared", self.tokens[self.current_position].line_num, self.tokens[self.current_position].char_pos)
            # Adding the parameter to the current scope
            self.register_variable(parameter_name, 'UKN')
            
            # Assigning type to the parameter
            self.advance_token() # Skip the parameter name token
            self.expect_token('TYPE_ASSIGN')

            self.advance_token() # Skip the type assignment token
            if self.tokens[self.current_position].type not in self.TYPES: raise CASOSyntaxError(f"Expected type, got {self.tokens[self.current_position].type}", self.tokens[self.current_position].line_num, self.tokens[self.current_position].char_pos)
            parameter_type = self.current_token_type()
            parameters[parameter_name] = parameter_type

            # Checking for comma or close parenthesis
            self.advance_token() # Skip the type token
            if self.current_token_type() == 'COMMA':
                self.current_position += 1 # Skip the comma token
            elif self.current_token_type()  == 'CLOSE_PAREN':
                break
            else:
                raise CASOSyntaxError(f"Expected comma or close parenthesis, got {self.tokens[self.current_position].type}", self.tokens[self.current_position].line_num, self.tokens[self.current_position].char_pos)

        # Checking for correct syntax
        self.advance_token() # Skip the close parenthesis token
        self.expect_token('TYPE_ASSIGN')

        # Assigning type to the function
        self.current_position += 1 # Skip the type assignment token
        if self.tokens[self.current_position].type not in self.TYPES: # Check if the type is valid
            raise CASOSyntaxError(f"Expected type, got {self.tokens[self.current_position].type}", self.tokens[self.current_position].line_num, self.tokens[self.current_position].char_pos)
        function_type = self.tokens[self.current_position].type
        
        # Checking for the function body
        self.advance_token() # Skip the type token
        self.expect_token('OPEN_BRACE')

        # Parsing the body of the function
        self.current_position += 1 # Skip the open brace token
        function_definition_node = FUNCTIONDECLARATIONnode(function_name, parameters, function_type)
        function_body = self.parse_action() # Parsing the body of the function
        function_definition_node.function_body = function_body # No need to skip the close brace token, it is already skipped in the parse_action method

        # Exiting the scope
        self.pop_scope()

        # Checking for correct syntax
        self.expect_token('NEWLINE')

        # Append the function definition to the functions dictionary
        self.functions[function_name] = (parameters, function_type)

        # Append the function definition to the AST
        self.nodes.append(function_definition_node)

    def parse_return(self):
        # Checking for correct syntax
        self.advance_token() # Skip the RETURN token
        return_value = self.parse_until('NEWLINE') # We already skipped the new line token

        # Append the return statement to the AST
        return_node = RETURNnode(return_value)
        self.nodes.append(return_node)

    # If, else, elsif
    def parse_if(self):
        # Checking for correct syntax
        self.advance_token() # Skip the IF token
        self.expect_token('OPEN_PAREN')

        # Parsing the condition
        self.advance_token()
        condition = self.parse_until('CLOSE_PAREN') # We already skipped the close parenthesis token

        # Checking for correct syntax
        self.expect_token('OPEN_BRACE')

        # Parsing the body
        self.advance_token()
        if_node = IFnode(condition)
        body = self.parse_action() # We already skipped the close brace token
        if_node.if_body = body

        # Adding the if statement to the AST
        self.nodes.append(if_node)
    
    def parse_elsif(self):       
        # Entering a new scope
        self.push_scope()

        # Checking if the first VALID node before the elsif is an if or an elsif
        # first_valid_node = None
        # # How this works is basically: we iterate through the nodes in reverse order, and we stop when we find the first valid node (which is any node that is not None (empty or newline)), then we check if first valid node we found is  of type ELSIF or if, and if it is we set the first_valid_node variable to that, else we throw an error, for now this only works with non nested structures
        # for node in reversed(self.nodes):
        #     if node != None: # If the node is an if or an elsif (and it's not None (empty or newline))
        #         if node.node_type in [NodeType.IF, NodeType.ELSIF]: # If the node is an if or an elsif
        #             first_valid_node = node
        #         break

        # if first_valid_node is None:
        #     raise CASOUnexpectedTokenError(self.current_line_num(), self.current_char_pos(), self.current_token_type(), 'Expected a IF or ELSIF before ELSIF')

        # Checking for correct syntax
        self.advance_token()
        self.expect_token('OPEN_PAREN')

        # Parsing the condition
        self.advance_token()
        condition = self.parse_until('CLOSE_PAREN') # We already skipped the close parenthesis token

        # Checking for correct syntax   
        self.expect_token('OPEN_BRACE')

        # Parsing the body
        self.advance_token()
        elsif_node = ELSIFnode(condition)
        body = self.parse_action()
        elsif_node.elsif_body = body

        # Exiting the scope
        self.pop_scope()

        # Adding the elsif statement to the AST
        self.nodes.append(elsif_node)

    def parse_else(self):
        # Entering a new scope
        self.push_scope()

        # Checking for correct syntax
        self.advance_token()
        self.expect_token('OPEN_BRACE')

        # Parsing the body
        self.current_position += 1 # Skip the open brace token
        else_node = ELSEnode()
        body = self.parse_action()
        else_node.else_body = body

        # Exiting the scope
        self.pop_scope()

        # Adding the else statement to the AST
        self.nodes.append(else_node)

    def parse_function_call(self):
        # Checking for correct syntax
        function_name = self.current_token_value()
        self.advance_token()

        # Checking if the function exists
        self.is_not_registered_function_exception(function_name)
        self.expect_token('OPEN_PAREN')

        # Parsing the parameters (parameters can also be expressions)
        self.advance_token() # Skip the open parenthesis token
        parameters = []
        while True: # Since we already skip the close parenthesis token, we don't need to check for it
            parameter = self.parse_until('COMMA', 'CLOSE_PAREN') # The method already skips the comma or close parenthesis token
            parameters.append(parameter)
            if parameter == '':
                break
        if parameters[-1] == '':
            parameters.pop(-1)

        # We've already skipped the close parenthesis token
        # Adding the function call to the AST
        function_call_node = FUNCTIONCALLnode(function_name, parameters)
        self.nodes.append(function_call_node)   

    def parse_loop(self):
        # Entering a new scope
        self.push_scope()

        # Checking for correct syntax
        self.advance_token() # Skip the LOOP token
        self.expect_token('OPEN_PAREN')

        # Syntax here should be (variable, expression to_keyword expression)
        # Parsing the variable
        self.advance_token() # Skip the variable token
        variable = self.current_token_value()
        # Checking if the variable is already defined
        self.is_registered_variable_exception(variable)
        self.register_variable(variable, 'INT')
        self.advance_token() # Skip the variable token

        self.expect_token('COMMA')
        self.current_position += 1 # Skip the comma token

        # Now should come the expression to_keyword expression
        expression1 = self.parse_until('TO')
        expression2 = self.parse_until('CLOSE_PAREN') # We already skipped the close parenthesis token

        # Checking for correct syntax
        # Here could come 2 things, 1 is a brace, the other is a guard clause
        guard_clause = None
        if self.current_token_type() == 'OPEN_BRACE':
            self.advance_token() # Skip the open brace token
        elif self.current_token_type() == 'PIPE':
            self.advance_token() # Skip the pipe token
            guard_clause = self.parse_until('PIPE') # We already skipped the pipe token

            self.expect_token('OPEN_BRACE')
            self.advance_token() # Skip the open brace token
        else:
            raise CASOSyntaxError(f"Expected open brace or guard clause, got {self.tokens[self.current_position].type}", self.tokens[self.current_position].line_num, self.tokens[self.current_position].char_pos)

        # Parsing the body
        loop_node = LOOPnode(variable, expression1, expression2, guard_clause)
        body = self.parse_action()
        loop_node.loop_body = body

        # Exiting the scope
        self.pop_scope()

        # Adding the loop statement to the AST
        self.nodes.append(loop_node)

    def parse_java_source(self):
        # We don't need to parse each line, as the parser is built for CASO and we're well... parsing Java, we just gotta append each line to the node
        java_source = self.tokens[self.current_position].value
        self.current_position += 1 # Skip the JAVA_SOURCE token

        # Adding the java source to the AST
        java_source_node = JAVASOURCEnode(java_source)
        self.nodes.append(java_source_node)

    # Function for making parameter parsing easier
    def parse_parameters_declaration_until(self, *end_tokens):
        # ASSUMING WE ALREADY SKIPPED THE OPEN PARENTHESIS TOKEN
        parameters = {}
        while self.current_token_type() not in end_tokens:
            self.expect_token('ID') # Expecting a parameter name
            parameter_name = self.current_token_value()

            # Getting parameter type
            self.advance_token() # Skip the parameter name token
            self.expect_token('TYPE_ASSIGN') # Expecting a type assignment token
            self.advance_token() # Skip the type assignment token
            parameter_type = self.current_token_type() # Getting the parameter type
            if parameter_type not in self.TYPES: 
                raise CASOInvalidTypeError(self.current_line_num(), self.current_char_pos(), self.current_token_value()) # Checking if the type is valid

            # If the parameter is a list, we need to parse it
            if parameter_type == 'LIST':
                self.advance_token() # Skip the list token
                parameter_type = self.parse_list_expression() # Parsing the list expression

            # Adding the parameter to the dictionary
            if parameter_name in parameters:
                raise CASOSyntaxError(f"Parameter {parameter_name} already declared", self.current_line_num(), self.current_char_pos())
            else:
                self.is_registered_variable_exception(parameter_name) # Checking if the variable is already defined
            parameters[parameter_name] = parameter_type # Adding the parameter to the dictionary
            self.register_variable(parameter_name, parameter_type) # Adding the parameter to the current scope

            # Skipping the parameter type token
            if parameter_type != 'LIST':
                self.advance_token()

            self.expect_token('COMMA', 'CLOSE_PAREN') # Expecting a comma or close parenthesis token

            if self.current_token_type() == 'COMMA':
                self.advance_token()
            elif self.current_token_type() == 'CLOSE_PAREN':
                break
            else:
                raise CASOSyntaxError(f"Expected comma or close parenthesis, got {self.current_token_type()}", self.current_line_num(), self.current_char_pos())

        # Skipping the close parenthesis token and returning
        self.advance_token()
        return parameters

    # Parser function for a class definition
    def parse_object(self):
        # Entering a new scope
        self.push_scope()

        self.advance_token() # Skip the OBJECT token
        object_name = self.expect_token('ID').value # The object name should be an identifier
        self.advance_token() # Skip the object name token

        # We can know parse the parameters
        self.expect_token('OPEN_PAREN')
        self.advance_token() # Skip the open parenthesis token
        
        # The function we're about to use, assumes the open parenthesis token has already been skipped
        parameters = self.parse_parameters_declaration_until('CLOSE_PAREN') # This also adds them to the current scope abd skips the close parenthesis token

        self.expect_token('OPEN_BRACE', 'INHERIT') # Expecting an open brace or inherit

        # Checking if the class has a parent class
        inherited_class = None
        inherited_attributes = {}
        inherited_methods = []

        if self.current_token_type() == 'INHERIT':
            self.advance_token() # Skip the inherit token

            # Getting the inherited class
            self.expect_token('ID') # Expecting an identifier

            inherited_class_name = self.current_token_value()
            for object in self.object_stack: # Check if the inherited class is defined
                if object.object_name == inherited_class_name: # The OBJECTnode has a attribute called object_name, we will check if it's equal to the inherited class
                    inherited_class = object # We set the inherited class to the object
                    break

            if inherited_class == None: # If the class is not defined, we raise an error
                raise CASOClassNotFoundError(self.current_line_num(), self.current_char_pos(), inherited_class_name) # If the class is not defined, we raise an error

            # Inheriting all the methods and attributes from the inherited class
            for attribute_name, attribute_type in inherited_class.object_attributes.items():
                inherited_attributes[attribute_name] = attribute_type
                # Adding the attribute to the current scope
                self.register_variable(attribute_name, attribute_type)

            for method in inherited_class.object_methods:
                inherited_methods.append(method)

            self.advance_token() # Skip the inherited class token

            # Setting the inherited class as the inherited class name
            inherited_class = inherited_class_name

        # Object methods (this could also be empty)
        self.advance_token() # Skip the open brace token

        # Parsing the methods
        methods = []
        while self.current_token_type() != 'CLOSE_BRACE':
            # Checking for newline
            if self.current_token_type() == 'NEWLINE': # If the token is a new line
                self.advance_token() # Skipping until the next token is not a new line
                continue # Skipping the rest of the loop

            # Checking for function declaration
            if self.current_token_type() == 'FUNCTION': # If the token is a function declaration
                self.parse_function_declaration()
                self.advance_token() # Skip the new line token
                method= self.nodes.pop()
                methods.append(method)
            else:
                raise CASOInvalidClassMemberError(self.current_line_num(), self.current_char_pos(), self.current_token_type())

        # Exiting the scope
        self.pop_scope()
        self.advance_token() # Skip the close brace token

        # Adding the object to the AST
        object_node = OBJECTnode(object_name, parameters, methods, inherited_class, inherited_attributes, inherited_methods)
        self.nodes.append(object_node)
        self.object_stack.append(self.nodes[-1]) # Adding the object to the object stack (this is for inheritance purposes and is done by getting the last element of the nodes list)
        # Fast pseudo-code for future me: when inheritance is implemented, check if the inherited class is in the object stack, if it is, fine, if it isn't, raise an error
        # then get the inherited class methods and add them to the object methods

    def parse_constructor(self):
        # Entering a new scope
        self.push_scope()

        self.advance_token() # Skip the CONSTRUCTOR token

    # Parsing imports, this is done using the USE token
    def parse_use(self):
        self.advance_token() # Skip the USE token
        self.expect_token('ID') # Expecting an identifier

        # Getting the import name
        import_name = self.current_token_value()
        if self.library_exists(import_name) == False:
            raise CASOImportError(self.current_line_num(), self.current_char_pos(), import_name)

        # Parsing the library
        library_source_code = self.get_library_source_code(import_name)

        tokenizer = CASOLexer(library_source_code)
        tokens = tokenizer.tokenize()

        parser = CASOParser(tokens)
        nodes = parser.parse()

        # Getting all the imports from the import name
        import_list = []
        self.advance_token() # Skip the import name token

        if self.current_token_type() == 'IMPORT': # Checking if the user wants to import everything
            self.advance_token() # Skip the import token
            while self.current_token_type() != 'NEWLINE':
                self.expect_token('ID') # Expecting an identifier
                import_list.append(self.current_token_value())
                self.advance_token() # Skip the import token
        else:
            self.advance_token() # Skip the import token

        # Adding the imported funcions/objects/variables to the current scope
        for node in nodes:
            # Checking if the node is a function declration and if it is in the import list
            if node != None and node.node_type == NodeType.FUNCTION_DECLARATION: # If the token isn't a new line and is a function declaration
                if node.function_name in import_list:
                    if self.is_registered_function(node.function_name) == False:
                        self.functions[node.function_name] = node.return_type

        # Adding the import to the AST
        use_node = USEnode(import_name, import_list)
        self.nodes.append(use_node)

    # Parsing object attribute access
    def parse_object_attribute_access(self):
        object_name = self.current_token_value() # Getting the object name
        self.advance_token() # Skip the object name token
        self.advance_token() # Skip the DOT token
        self.expect_token('ID') # Expecting an identifier
        attribute_name = self.current_token_value() # Getting the attribute name
        self.advance_token() # Skip the attribute name token

        # Adding the attribute access to the AST
        attribute_access_node = ATTRIBUTEACCESSnode(object_name, attribute_name)
        self.nodes.append(attribute_access_node)

    # Parse 'loan' functions
    def parse_loan(self):
        self.advance_token() # Skip the FROM token
        self.expect_token('OPEN_PAREN')
        self.advance_token()

        # Entering a new scope
        self.push_scope()

        # Parse the body of the loan
        loan_body = self.parse_action('CLOSE_PAREN')
        print('Loan body:', loan_body)
        
        # After parsing the body, we get the variable we want to take the loan from
        self.expect_token('TAKE')
        self.advance_token()
        self.expect_token('ID') # Expecting an identifier (the variable name)
        variable_name = self.current_token_value()
        self.advance_token()

        # Checking if the variable is inside the loan body
        self.is_not_registered_variable_exception(variable_name)

        # Adding the loan to the AST
        loan_node = LOANnode(variable_name)
        loan_node.loan_body = loan_body
        self.nodes.append(loan_node)

        # Exiting the scope
        self.pop_scope()
