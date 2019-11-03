import os
import uuid


def unique_path(instance, filename):
    # file will be uploaded to MEDIA_ROOT/images/<filename>
    _, ext = os.path.splitext(filename)
    return 'images/{}{}'.format(uuid.uuid4(), ext)