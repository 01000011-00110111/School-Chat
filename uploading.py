import os
import uuid
# import pyclamd

import database

allowed_extensions = {'png', 'jpg', 'jpeg', 'gif'}


def allowed_file(filename):
    return '.' in filename and filename.rsplit(
        '.', 1)[1].lower() in allowed_extensions


def scan_for_virus(file_path):
    return False
    # broken SAY "PLZ NO VIRUS"


def replace_old_file(old):  # this will grow bigger later
    if os.path.exists(old.lstrip("/")):
        os.remove(old.lstrip("/"))


def rename_file(file_path):
    return file_path.split('.')[0].rstrip('/') if os.path.exists(file_path.lstrip('/'))\
    else uuid.uuid4()


def upload_file(file, old):
    old_file = old.lstrip('/')
    # print(old, ":", file)
    if not allowed_file(file.filename):
        return 0
    replace_old_file(old)
    new_filename = f"static/profiles/{rename_file(old_file)}.{file.filename.rsplit('.', 1)[1].lower()}"
    file_path = f"{new_filename.split('.')[0]}.png"
    file.save(file_path)  # saves the file at the location

    virus_scan_result = scan_for_virus(file_path)

    if virus_scan_result:
        os.remove(file_path)  # Remove the file if a virus is detected
        print(virus_scan_result)
        return 1
        # flash(virus_scan_result, 'error')
        # return virus_scan_result

    return_path = f"/{file_path}"
    return return_path
