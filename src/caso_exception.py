class CASOException(Exception):
    def __init__(self, message):
        super().__init__(message)

class CASOIllegalTokenError(CASOException):
    def __init__(self, message, line_num, char_pos):
        super().__init__(f"{message} at line {line_num}, character {char_pos}")

class CASOSyntaxError(CASOException):
    def __init__(self, message, line_num, char_pos):
        super().__init__(f"{message} at line {line_num}, character {char_pos}")

class CASONotDeclaredError(CASOSyntaxError):
    def __init__(self, message, line_num, char_pos):
        super().__init__(f"{message}", line_num, char_pos)

class CASOTypeError(CASOSyntaxError):
    def __init__(self, message, line_num, char_pos):
        super().__init__(f"{message}", line_num, char_pos)

class CASOIndexError(CASOSyntaxError):
    def __init__(self, message, line_num, char_pos):
        super().__init__(f"{message}", line_num, char_pos)

class CASOValueError(CASOSyntaxError):
    def __init__(self, message, line_num, char_pos):
        super().__init__(f"{message}", line_num, char_pos)

class CASONameError(CASOSyntaxError):
    def __init__(self, message, line_num, char_pos):
        super().__init__(f"{message}", line_num, char_pos)

class CASOAttributeError(CASOSyntaxError):
    def __init__(self, message, line_num, char_pos):
        super().__init__(f"{message}", line_num, char_pos)

class CASOTranspilerError(CASOException):
    def __init__(self, message):
        super().__init__(f"{message}")

class CASOWarning():
    def __init__(self, message, line_num, char_pos):
        print(f"Warning: {message} at line {line_num}, character {char_pos}")
