def string_to_int(cls, the_string):
    """Convert the string value to an int value, or return None."""
    for num, string in cls.choices:
        if string == the_string:
            return num
    return None

FULL_BULAN = {1:"Januari", 2:"Februari", 3:"Maret", 4:"April", 5:"Mei", 6:"Juni", 7:"Juli", 8:"Agustus", 9:"September", 10:"Oktober", 11:"November", 12:"Desember"}
