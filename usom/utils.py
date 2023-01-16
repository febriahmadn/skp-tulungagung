import os
from uuid import uuid4

from django.core.exceptions import ValidationError
from django.utils.deconstruct import deconstructible


@deconstructible
class PathForFileModel(object):
    def __init__(self, sub_path):
        self.path = sub_path

    def __call__(self, instance, filename):
        ext = filename.split(".")[-1]
        # set filename as random string
        filename = "{}.{}".format(uuid4().hex, ext)
        # return the whole path to the file
        return os.path.join(self.path, filename)


def image_validation(value):
    filesize = value.size
    if filesize > 204800:
        raise ValidationError("Anda Tidak Bisa Mengunggah foto lebih dari 200kb")
    else:
        return value


roman_numeral = ("M", "CM", "D", "CD", "C", "XC", "L", "XL", "X", "IX", "V", "IV", "I")
numeral_map = tuple(
    zip((1000, 900, 500, 400, 100, 90, 50, 40, 10, 9, 5, 4, 1), roman_numeral)
)


def int_to_roman(i):
    result = []
    for integer, numeral in numeral_map:
        count = i // integer
        result.append(numeral * count)
        i -= integer * count
    return "".join(result)


def roman_to_int(n):
    i = result = 0
    for integer, numeral in numeral_map:
        while n[i: i + len(numeral)] == numeral:
            result += integer
            i += len(numeral)
    return result


def angka_golongan(value):
    if value == "a":
        return 1
    elif value == "b":
        return 2
    elif value == "c":
        return 3
    elif value == "d":
        return 4
    elif value == "e":
        return 5
    else:
        None
