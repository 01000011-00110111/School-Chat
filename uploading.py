"""uploading.py: Backend management of uploaded files.
    Copyright (C) 2023, 2024  cserver45, cseven
    License info can be viewed in main.py or the LICENSE file.
"""
import os
import uuid

# import pyclamd

allowed_extensions = {'png', 'jpg', 'jpeg', 'gif'}


def allowed_file(filename):
    """Checks if the file format is allowed."""
    return '.' in filename and filename.rsplit(
        '.', 1)[1].lower() in allowed_extensions


def scan_for_virus(_file_path):
    """Scans for Viruses (needs to be added)."""
    return False
    # broken SAY "PLZ NO VIRUS"


def replace_old_file(old):  # this will grow bigger later
    """Replaces the old file"""
    if os.path.exists(old.lstrip("/")):
        os.remove(old.lstrip("/"))


def rename_file(file_path):
    """Renames a file."""
    return file_path.split('.')[0].rstrip('/') if os.path.exists(file_path.lstrip('/'))\
    else uuid.uuid4()


def upload_file(file, old):
    """Adds the file to the static/profiles dir."""
    if not allowed_file(file.filename):
        return 0
    old_file = old.lstrip('/')
    replace_old_file(old)
    new_filename = \
    f"static/profiles/{rename_file(old_file)}.{file.filename.rsplit('.', 1)[1].lower()}"
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
