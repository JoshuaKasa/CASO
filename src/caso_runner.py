import time
import os
import sys

from caso_lexer import CASOLexer
from caso_parser import CASOParser
from caso_transpiler import CASOTranspiler

def main(input_path: str, output_path: str) -> None:
    """
    Main function to read source code, tokenize, parse, and transpile it.

    Args:
    input_path (str): The path to the input source file.
    output_path (str): The path to the output file.
    """

    # Constructing file paths
    script_dir = os.path.dirname(os.path.abspath(__file__))

    input_file_path = os.path.join(input_path)
    output_file_path = os.path.join(output_path)

    try:
        # Reading the source code from the test file
        with open(input_file_path, 'r') as file:
            source_code = file.read()

        # Starting milliseconds
        start_time = int(round(time.time() * 1000))

        # ---------------------- LEXER ----------------------
        # Tokenization of the source code
        lexer = CASOLexer(source_code)
        tokens = lexer.tokenize()
        print("Tokens:", tokens)

        print("\n")  # Separation

        # ---------------------- PARSER ----------------------
        # Parsing the tokens into an AST
        parser = CASOParser(tokens)
        nodes = parser.parse()
        print("Parsed Nodes:", nodes)

        print("\n")  # Separation

        # ------------------ TRANSPILER ----------------------
        transpiler = CASOTranspiler(nodes, file_path=output_file_path)
        source = transpiler.transpile()
        print("Transpiled Source Code:\n", source)

        # Ending milliseconds
        end_time = int(round(time.time() * 1000))
        print(f"\nExecution time: {end_time - start_time}ms")

    except FileNotFoundError:
        print(f"File not found: {input_file_path}")
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Usage: python caso_runner.py <input_file> <output_file>")
    else:
        main(sys.argv[1], sys.argv[2])

