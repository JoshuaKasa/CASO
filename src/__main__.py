import caso_parser
import caso_lexer

def main() -> None:
    source_code = """
    let x: Int = 10
    let y: Int = 20
    let z: Int = x + y
    """
    lexer = caso_lexer.MapleLexer(source_code)
    tokens = lexer.tokenize()
    print(tokens)

    print() # Separation

    parser = caso_parser.CASOParser(tokens)
    nodes = parser.parse()
    print(nodes)

if __name__ == "__main__":
    main()
