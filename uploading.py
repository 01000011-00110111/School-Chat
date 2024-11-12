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
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in allowed_extensions

def scan_for_virus(_file_path):
    """Scans for Viruses."""
    return False  # application.scan(file_path)

def replace_old_file(old):  # this will grow bigger later
    """Replaces the old file."""
    if os.path.exists(old.lstrip("/")):
        os.remove(old.lstrip("/"))

# def rename_file(old, location):
#     """Renames a file."""
#     _, old_filename = os.path.split(old)
#     if old_filename == "":
#         old_filename = str(uuid.uuid4())
#     filename = os.path.splitext(old_filename)[0]
#     path = f"static/images/{location}/{filename}.png"
#     return path


# def upload_file(file, old, location):
#     """Adds the file to the static/profiles dir."""
#     if not allowed_file(file.filename):
#         return 0
#     if old:
#         # If old file path is provided, use it
#         file_path = old
#     else:
#         # If no old file path is provided, generate a new one
#         file_path = rename_file(old, location)
#     if file_path.startswith("/static"):
#         # Remove the leading / from the file path for os operations
#         file_path_no_slash = file_path[1:]
#     else:
#         file_path_no_slash = file_path
#     dir_path = os.path.dirname(file_path_no_slash)
#     file.filename = os.path.basename(file_path_no_slash)
#     if os.path.exists(file_path_no_slash):
#         os.remove(file_path_no_slash)
#     if not os.path.exists(dir_path):
#         os.makedirs(dir_path)
#     file.save(f"{dir_path}/{file.filename}")
#     if scan_for_virus(f"{dir_path}/{file.filename}"):
#         os.remove(f"{dir_path}/{file.filename}")  # Remove the file if a virus is detected
#         return 1
#     replace_old_file(old)
#     # Return the file path with the leading / for consistency
#     return f"/{file_path}"

def upload_file(file, old, location):
    """Adds the file to the static/profiles dir."""
    if not allowed_file(file.filename):
        return 0
    if scan_for_virus(file):
        return 1
    if old != "":
        file_path = old.lstrip("/")
    else:
        file_path = f"static/images/{location}/{str(uuid.uuid4())}.png"
    if old:
        replace_old_file(old)
    file.save(file_path)
    return f"/{file_path}"


def upload_file_theme(theme_id, file):
    """Adds the file to the static/images/themes dir."""
    if not hasattr(file, 'filename'):
        filename = f"{theme_id}.png"
    else:
        filename = file.filename

    if not allowed_file(filename):
        return 0
    if scan_for_virus(file):
        return 1
    file_path = f"static/images/themes/{theme_id}.png"
    with open(file_path, 'wb') as f:
        f.write(file.read())
    return f"/{file_path}"
