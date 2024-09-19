"""uploading.py: Backend management of uploaded files.
    Copyright (C) 2023, 2024  cserver45, cseven
    License info can be viewed in main.py or the LICENSE file.
"""
import os
import uuid
# import pyclamd

# application = pyclamd.ClamdNetworkSocket('localhost', 3310)

allowed_extensions = {'png', 'jpg', 'jpeg', 'gif'}


def allowed_file(filename):
    """Checks if the file format is allowed."""
    return '.' in filename and filename.rsplit(
        '.', 1)[1].lower() in allowed_extensions


def scan_for_virus(_file_path):
    """Scans for Viruses."""
    return False  # application.scan(file_path)


def replace_old_file(old):  # this will grow bigger later
    """Replaces the old file."""
    if os.path.exists(old.lstrip("/")):
        os.remove(old.lstrip("/"))


def rename_file(file_path):
    """Renames a file."""
    return file_path.split('.')[0].rstrip('/') if os.path.exists(file_path.lstrip('/'))\
    else uuid.uuid4()


def upload_file(file, old, location):
    """Adds the file to the static/profiles dir."""
    if not allowed_file(file.filename):
        return 0
    file_path = f"static/images/{location}/{uuid.uuid4()}.{file.filename.rsplit('.', 1)[1].lower()}"
    file.save(file_path)  # saves the file at the location
    if scan_for_virus(file_path):
        os.remove(file_path)  # Remove the file if a virus is detected
        return 1
    replace_old_file(old)
    return f"/{file_path}"
