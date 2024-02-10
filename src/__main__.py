import caso_parser
import caso_lexer
import caso_transpiler

import sys
import os
import time
import traceback  

def main(input_path: str) -> None:
    """
    Main function to read source code, tokenize, parse, and transpile it.

    Args:
    input_path (str): The path to the input source file.
    """

    # Constructing file paths
    script_dir = os.path.dirname(os.path.abspath(__file__))

    input_file_path = os.path.join('test', input_path)
    output_file_name = input_path.replace('.caso', '')
    output_file_path = os.path.join(script_dir, 'build', output_file_name)

    try:
        # Reading the source code from the test file
        with open(input_file_path, 'r') as file:
            source_code = file.read()

        # Starting milliseconds
        start_time = int(round(time.time() * 1000))

        # ---------------------- LEXER ----------------------
        # Tokenization of the source code
        from caso_lexer import CASOLexer
        lexer = CASOLexer(source_code)
        tokens = lexer.tokenize()
        print("Tokens:", tokens)

        print("\n")  # Separation

        # ---------------------- PARSER ----------------------
        # Parsing the tokens into an AST
        from caso_parser import CASOParser
        parser = CASOParser(tokens)
        nodes = parser.parse()
        print("Parsed Nodes:", nodes)

        print("\n")  # Separation

        # ------------------ TRANSPILER ----------------------
        # Transpiling the AST to target language
        from caso_transpiler import CASOTranspiler
        transpiler = CASOTranspiler(nodes, file_path=output_file_path)
        source = transpiler.transpile()
        print("Transpiled Source Code:\n", source)

        # Ending milliseconds
        end_time = int(round(time.time() * 1000))
        print(f"\nExecution time: {end_time - start_time}ms")

    except Exception as e:
        print(f"Error: {e}")
        traceback.print_exc()

# Example of calling the main function
if __name__ == "__main__":
    main(sys.argv[1])
