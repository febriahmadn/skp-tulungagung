def string_to_int(cls, the_string):
    """Convert the string value to an int value, or return None."""
    for num, string in cls.choices:
        if string == the_string:
            return num
    return None
