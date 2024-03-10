import re
import os

from caso_parser import NodeType
from caso_exception import CASOTranspilerError
from caso_types import conversion_table

class CASOTranspiler:
    def __init__(self, ast, scope_stack, file_path='caso_transpiled.java', create_file=True): 
        self.ast = ast
        self.scope_stack = scope_stack
        self.file_path = file_path
        self.file_name = file_path.split("\\")[-1].split(".")[0]
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
        'UKN': '?',
        'AND': '&&',
        'OR': '||'
    }

    def transpile(self) -> str:
        # Remove all the variable declarations that haven't been used and follow the 'at' notation
        # First we will collect the name of names of variables to be removed
        variables_to_remove = set()
        for scope in self.scope_stack:
            for variable_name, variable_info in scope.items():
                if variable_info['at'] == True and variable_info['used'] == False:
                    variables_to_remove.add(variable_name)

        # Then we will filter the AST using a single pass
        if variables_to_remove: # If there are variables to remove
            self.ast = [node for node in self.ast if not (
                node and node.node_type == NodeType.VARIABLE_DECLARATION and node.variable_name in variables_to_remove
            )]
        
        # We first transpile the general header of the file
        self.transpiled_code = f'''
        // This is the general header template for the transpiled code
        import java.util.Scanner;
        import java.util.ArrayList;
        '''

        # Transpiling the native java code
        for node in self.ast:
            if node == None:
                continue
            if node.node_type == NodeType.INCORPORATE:
                self.transpile_incorporate(node)
                self.ast.remove(node)

        # Adding the main file
        self.transpiled_code += f'''
        public class {self.file_name.split("/")[-1]} {{
        '''

        # Before transpiling the main method we must transpile all the function declarations
        '''
        For a better explanation of why we're using `reversed(self.ast)`:
            If we don't when the loop finds a function declaration node, it removes it from the list, because the node is removed,
            all subsequent nodes are shifted to the left, but meanwhile, the loop goes to the next index, skipping the node that was
            shifted to the left. 
        '''
        for node in reversed(self.ast): # We doing it in reverse so that even if we remove a node, we don't skip any
            if node is None:
                continue
            if node.node_type == NodeType.FUNCTION_DECLARATION:
                self.transpile_function_declaration(node, transpile_to_main=False)
                self.ast.remove(node)

        # Now we can transpile the main method
        self.transpiled_code += '''
            public static void main(String[] args) {

        ''' # This will be the transpiled code that will be returned by the transpile() method

        # Transpiling the main method
        for node in self.ast:
            self.transpile_node(node)

        # Before creating the file we need to close the main method and the class
        self.transpiled_code += '''
            }
        }
        '''

        # Creating the file
        if self.create_file:
            with open(f"{self.file_path}.java", "w") as file:
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
            elif node.node_type == NodeType.FUNCTION_CALL:
                self.transpile_function_call(node)
            elif node.node_type == NodeType.RETURN:
                self.transpile_return(node)
            elif node.node_type == NodeType.IF:
                self.transpile_if(node)
            elif node.node_type == NodeType.ELSIF:
                self.transpile_elsif(node)
            elif node.node_type == NodeType.ELSE:
                self.transpile_else(node)
            elif node.node_type == NodeType.LOOP:
                self.transpile_loop(node)
            elif node.node_type == NodeType.JAVA_SOURCE:
                self.transpile_native_java(node)
            elif node.node_type == NodeType.OBJECT:
                self.transpile_object(node) 
            elif node.node_type == NodeType.LOAN:
                self.transpile_loan(node)
            elif node.node_type == NodeType.ATTRIBUTE_ACCESS:
                self.transpile_attribute_access(node)
            elif node.node_type == NodeType.METHOD_ACCESS:
                self.transpile_method_access(node)
            else:
                raise CASOTranspilerError("Unknown node type '%s'" % node.node_type)

    def transpile_node_to_string(self, node):
        initial_transpiled = self.transpiled_code
        self.transpile_node(node)

        # Getting the difference between the initial transpiled code and the final transpiled code
        difference_transpiled = self.transpiled_code[len(initial_transpiled):]
        self.transpiled_code = initial_transpiled
        
        return difference_transpiled

    def transpile_declaration(self, node):
        if node.is_object:
            self.transpiled_code += f'''
            {node.variable_type} {node.variable_name} = new {node.variable_type}('''
            for i, property in enumerate(node.object_properties):
                self.transpiled_code += f'{property}'
                if i != len(node.object_properties) - 1:
                    self.transpiled_code += ', '
            self.transpiled_code += ');\n'
        else:
            self.transpiled_code += f'''
            {node.variable_type} {node.variable_name} = {node.variable_value};
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

    def transpile_function_declaration(self, node, transpile_to_main=True):
        static_code = 'static ' if node.is_shared else ''

        local_transpiled_code = f'''
        public {static_code} {node.return_type} {node.function_name}(
        '''
        # Iterating over the dictionary of parameters
        for i, (param_name, param_type) in enumerate(node.function_args.items()):
            local_transpiled_code += f"{param_type} {param_name}"
            if i != len(node.function_args) - 1:
                local_transpiled_code += ", "
        local_transpiled_code += ") {\n"

        # Iterating over the function body
        for statement in node.function_body:
            if transpile_to_main:
                self.transpile_node(statement)
            else:
                local_transpiled_code += self.transpile_node_to_string(statement)
        local_transpiled_code += '''
        }
        '''
        if transpile_to_main:
            self.transpiled_code += local_transpiled_code
        # This transpile function returns a value 'cause we need to use it inside the transpile object method
        return local_transpiled_code

    def transpile_return(self, node):
        self.transpiled_code += f'''
        return {node.return_value};
        '''

    def transpile_if(self, node):
        self.transpiled_code += f'''
        if ({node.condition}) {{
        '''
        for statement in node.if_body:
            self.transpile_node(statement)
        self.transpiled_code += '''
        }
        '''

    def transpile_elsif(self, node):
        self.transpiled_code += f'''
        else if ({node.condition}) {{
        '''
        for statement in node.elsif_body:
            self.transpile_node(statement)
        self.transpiled_code += '''
        }
        '''

    def transpile_else(self, node):
        self.transpiled_code += f'''
        else {{
        '''
        for statement in node.else_body:
            self.transpile_node(statement)
        self.transpiled_code += '''
        }
        '''

    def transpile_function_call(self, node):
        self.transpiled_code += f'''
            {node.function_name}(
        '''
        for i, arg in enumerate(node.function_args):
            self.transpiled_code += f'{arg}'
            if i != len(node.function_args) - 1:
                self.transpiled_code += ', '
        self.transpiled_code += ');'

    def transpile_loop(self, node):
        self.transpiled_code += f'''
        for (int {node.loop_variable} = {node.loop_start}; {node.loop_variable} <= {node.loop_end}; {node.loop_variable}++) {{
        '''
        
        if node.loop_guard != None:
            self.transpiled_code += f'''
            if ({node.loop_guard}) {{
            '''
            for statement in node.loop_body:
                self.transpile_node(statement)
            self.transpiled_code += '''
            }
            '''
        else:
            for statement in node.loop_body:
                self.transpile_node(statement)
        self.transpiled_code += '''
        }
        '''

    def transpile_native_java(self, node):
        self.transpiled_code += f'''
        {node.java_code}
        '''

    def transpile_object(self, node):
        # Ensure the libraries directory exists
        os.makedirs('build/libraries', exist_ok=True)
        
        # File path for the new file
        file_path = os.path.join('build/libraries', f'{node.object_name}.java')
        
        # Initialize transpiled_code
        transpiled_code = 'package libraries;' # The transpiled code for the object
        
        extends_clause = f" extends {node.parent_class}" if node.parent_class else ""
        transpiled_code += f'''
        public class {node.object_name}{extends_clause} {{
        '''

        for var_name, var_type in node.object_attributes.items():
            transpiled_code += f'''
            public {var_type} {var_name};
            '''

        # Transpiling the object constructor
        transpiled_code += f'''
        public {node.object_name} (
        '''

        for i, (param_name, param_type) in enumerate(node.object_attributes.items()):
            transpiled_code += f"{param_type} {param_name}"
            if i != len(node.object_attributes) - 1:
                transpiled_code += ", "
        transpiled_code += ") {\n"

        if node.parent_class:
            transpiled_code += f''' 
            super(
            '''
            for i, (attr_name, attr_type) in enumerate(node.parent_class_attributes.items()):
                transpiled_code += f"{attr_name}"
                if i != len(node.parent_class_attributes) - 1:
                    transpiled_code += ", "
            transpiled_code += ");\n"

        for var_name, var_type in node.object_attributes.items():
            transpiled_code += f'''
            this.{var_name} = {var_name};
            '''
        transpiled_code += '''
        }
        '''

        for method in node.object_methods:
            # Assuming transpile_function_declaration appends to transpiled_code
            transpiled_code += self.transpile_function_declaration(method, transpile_to_main=False)

        for var_name, var_type in node.object_attributes.items():
            transpiled_code += f'''
            public {var_type} get_{var_name}() {{
                return this.{var_name};
            }}

            public void set_{var_name}({var_type} {var_name}) {{
                this.{var_name} = {var_name};
            }}
        '''

        transpiled_code += f'''
        @Override
        public String toString() {{
            return "{node.object_name}(" +
        '''
        for i, (var_name, var_type) in enumerate(node.object_attributes.items()):
            transpiled_code += f'''
            "{var_name}=" + this.{var_name} +
            '''
        transpiled_code += '''
            ")";
        }}
        '''

        # Writing the transpiled code to the file
        with open(file_path, 'w') as file:
            file.write(transpiled_code)

    def transpile_incorporate(self, node):
        full_imports = list(node.module_attributes) + list(node.module_methods) + [] # Joining a empty list to avoid None in case nothing is imported
        for import_name in full_imports:
            import_name = f'{node.module_name}.{import_name}' if len(full_imports) > 1 else f'{node.module_name}'
            self.transpiled_code += f'''
            import libraries.{import_name}; 
            ''' # Using 'libraries' as the package name for the imported objects cause they're being transpiled to the 'libraries' directory

    def transpile_loan(self, node):
        # TODO: Make some kind of way of transpiling functions inside a loan
        # right now they're being parsed as a normal function, but you can't
        # have a function inside a function in Java
        for statement in node.loan_body:
            if statement.node_type == NodeType.FUNCTION_DECLARATION:
                self.transpile_function_declaration(statement)
            self.transpile_node(statement)

    def transpile_attribute_access(self, node):
        self.transpiled_code += f'''
        {node.object_name}.{node.attribute_name}
        '''

    def transpile_method_access(self, node):
        self.transpiled_code += f'''
        {node.object_name}.{node.method_name}(
        '''
        for i, arg in enumerate(node.method_args):
            self.transpiled_code += f'{arg}'
            if i != len(node.method_args) - 1:
                self.transpiled_code += ', '
        self.transpiled_code += ');'
