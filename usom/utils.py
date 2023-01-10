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
