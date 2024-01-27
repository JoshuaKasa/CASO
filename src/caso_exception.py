class CASOException(Exception):
    def __init__(self, message):
        super().__init__(message)

class CASOIllegalTokenError(CASOException):
    def __init__(self, message, line_num, char_pos):
        super().__init__(f"{message} at line {line_num}, character {char_pos}")

class CASOSyntaxError(CASOException):
    def __init__(self, message, line_num, char_pos):
        super().__init__(f"{message} at line {line_num}, character {char_pos}")

class CASOTranspilerError(CASOException):
    def __init__(self, message):
        super().__init__(f"{message}")
