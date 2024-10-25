from enum import Enum


class AsciiEscapeCode(str, Enum):
    """
    Enumerates ASCII escape codes that allow to change the shell output colors.
    """

    CYAN = '\033[96m'
    END = '\033[0m'
