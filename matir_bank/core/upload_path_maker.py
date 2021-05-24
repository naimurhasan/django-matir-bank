import uuid
import os

def upload_path_maker(dir, instance, filename):
    fn, file_extension = os.path.splitext(filename)
    return '{}/user_{}_{}{}'.format(dir, instance.user.id, uuid.uuid4().hex, file_extension)
