from rest_framework.exceptions import ValidationError
from utils import constants


def validate_image_size(file):
    if file.size > constants.MAX_FILE_SIZE:
        raise ValidationError('maximum size of file can be {}MB'.format(
            constants.MAX_FILE_SIZE/(1024*1024)))
