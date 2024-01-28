import caso_parser
import caso_lexer
import caso_transpiler

def main() -> None:
    # Reading the source code from the test file
    source_code = open('test\\test_3.caso', 'r').read()

    # ---------------------- LEXER ----------------------
    lexer = caso_lexer.CASOLexer(source_code)
    tokens = lexer.tokenize()
    print(tokens)

    print() # Separation

    # ---------------------- PARSER ----------------------
    parser = caso_parser.CASOParser(tokens)
    nodes = parser.parse()
    print(nodes)  

    print() # Separation

    # ------------------ TRANSPILER ----------------------
    transpiler = caso_transpiler.CASOTranspiler(nodes, file_path='build\\build_3.java')
    source = transpiler.transpile()
    print(source)

if __name__ == "__main__":
    main()
