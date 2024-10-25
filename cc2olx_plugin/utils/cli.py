def is_command_line_argument_name(string: str) -> bool:
    """
    Decide whether the string is a command line argument.
    """
    return string.rstrip('\'"').startswith('-')
