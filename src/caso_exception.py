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

class CASOInvalidTypeError(CASOException):
    def __init__(self, line_num, char_pos, current_token):
        super().__init__(f'Invalid variable type: {current_token} at line {line_num}, character {char_pos}')

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

class CASOInvalidClassMemberError(CASOException):
    def __init__(self, line_num, char_pos, current_token):
        super().__init__(f'Invalid class member: {current_token} at line {line_num}, character {char_pos}, expected a method or attribute')

class CASOClassNotFoundError(CASOException):
    def __init__(self, line_num, char_pos, current_token):
        super().__init__(f'Class {current_token} not found at line {line_num}, character {char_pos}')

class CASOWarning():
    def __init__(self, message, line_num, char_pos):
        print(f"Warning: {message} at line {line_num}, character {char_pos}")
