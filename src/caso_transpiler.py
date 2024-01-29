import re
from caso_parser import NodeType
from caso_exception import CASOTranspilerError

class CASOTranspiler:
    def __init__(self, ast, file_path='caso_transpiled.java', create_file=True): 
        self.ast = ast
        self.file_name = file_path.split("\\")[-1].split(".")[0]
        self.transpiled_code = f'''
        // This is the general header template for the transpiled code
        import java.util.Scanner;
        import java.util.ArrayList;

        public class {self.file_name} {{
            public static void main(String[] args) {{

        ''' # This will be the transpiled code that will be returned by the transpile() method
        self.create_file = create_file # This will be used to determine whether or not to create a file
    OPERATORS = {
        'PLUS': '+',
        'MINUS': '-',
        'MUL': '*',
        'DIV': '/',
        'MOD': '%',
        'EQ': '==',
        'NEQ': '!=',
        'LT': '<',
        'LE': '<=',
        'GT': '>',
        'GE': '>=',
        'UKN': '?'
    }

    def transpile(self) -> str:
        for node in self.ast:
            self.transpile_node(node)

        # Before creating the file we need to close the main method and the class
        self.transpiled_code += '''
            }
        }
        '''

        # Creating the file
        if self.create_file:
            with open(f"{self.file_name}.java", "w") as file:
                file.write(self.transpiled_code)

        # Returning the transpiled code as a string
        return self.transpiled_code

    def transpile_node(self, node):
        if node != None: # This was either a blank line or a comment
            if node.node_type == NodeType.VARIABLE_DECLARATION:
                self.transpile_declaration(node)
            elif node.node_type == NodeType.VARIABLE_ASSIGNMENT:
                self.transpile_assignment(node)
            elif node.node_type == NodeType.WHEN:
                self.transpile_when(node)
            elif node.node_type == NodeType.MATCHCASE:
                self.transpile_matchcase(node)
            elif node.node_type == NodeType.FUNCTION_DECLARATION:
                self.transpile_function_declaration(node)
            elif node.node_type == NodeType.FUNCTION_CALL:
                pass
            elif node.node_type == NodeType.RETURN:
                self.transpile_return(node)
            else:
                raise CASOTranspilerError("Unknown node type '%s'" % node.node_type)

    def transpile_declaration(self, node):
        self.transpiled_code += f'''
        {node.variable_type.lower()} {node.variable_name} = {node.variable_value};
        '''

    def transpile_assignment(self, node):
        self.transpiled_code += f'''
        {node.variable_name} = {node.variable_value};
        '''

    def transpile_when(self, node):
        for i, matchcase in enumerate(node.match_cases):
            self.transpile_matchcase(matchcase, node.variable_name, i) 

    def transpile_matchcase(self, node, variable_name=None, case_number=0):
        if variable_name == None:
            variable_name = node.variable_name

        operator = self.OPERATORS[node.match_type]
        if operator == '?':
            self.transpiled_code += f'''
                else {{
                '''
            for statement in node.children:
                self.transpile_node(statement)
            self.transpiled_code += '''
            }
            '''
        else:
            if case_number == 0:
                self.transpiled_code += f'''
                if ({variable_name} {operator} {node.match_value}) {{
                '''
                for statement in node.children:
                    self.transpile_node(statement)
                self.transpiled_code += '''
                }
                '''
            else:
                self.transpiled_code += f'''
                else if ({variable_name} {operator} {node.match_value}) {{
                '''
                for statement in node.children:
                    self.transpile_node(statement)
                self.transpiled_code += '''
                }
                '''

    def transpile_function_declaration(self, node):
        self.transpiled_code += f'''
        public static {node.return_type.lower()} {node.function_name}(
        '''
        # Iterating over the dictionary of parameters
        for i, (param_name, param_type) in enumerate(node.function_args.items()):
            self.transpiled_code += f"{param_type.lower()} {param_name}"
            if i != len(node.function_args) - 1:
                self.transpiled_code += ", "
        self.transpiled_code += ") {\n"

        # Iterating over the function body
        for statement in node.function_body:
            self.transpile_node(statement)
        self.transpiled_code += '''
        }
        '''

    def transpile_return(self, node):
        self.transpiled_code += f'''
        return {node.return_value};
        '''
