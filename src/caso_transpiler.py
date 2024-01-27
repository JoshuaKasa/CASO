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
