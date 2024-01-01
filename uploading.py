import os
import uuid
from pyclamd import ClamdUnixSocket

import database

allowed_extensions = {'png', 'jpg', 'jpeg', 'gif'}


def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in allowed_extensions

def scan_for_virus(file_path):
    try:
        cd = ClamdUnixSocket()
        scan_result = cd.scan_file(file_path)
        if scan_result:
            return f"Virus detected: {scan_result['stream']}"
        else:
            return None
    except Exception as e:
        return f"Error during virus scan: {str(e)}"
    

def upload_file(file):
    if not allowed_file(file.filename):
        return 0

    file_name = uuid.uuid4() # Creates a uuid for a filename
    new_filename = f"{file_name}.{file.filename.rsplit('.', 1)[1].lower()}" # renames the file and adds back the original extension
    file_path = os.path.join('static/profiles', new_filename) # Tells where the file will be put
    file.save(file_path) # saves the file at the location 

    virus_scan_result = scan_for_virus(file_path)

    if virus_scan_result:
        os.remove(file_path)  # Remove the file if a virus is detected
        print(virus_scan_result)
        return 1
        # flash(virus_scan_result, 'error')
        return 'NO VIRUS PLZ'

    return file_path