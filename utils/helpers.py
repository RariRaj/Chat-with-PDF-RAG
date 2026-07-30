import os

from config import UPLOAD_FOLDER


def save_uploaded_file(uploaded_file):
    """
    Saves uploaded PDF into uploaded_files folder.
    Returns the saved file path.
    """

    os.makedirs(UPLOAD_FOLDER, exist_ok=True)

    file_path = os.path.join(UPLOAD_FOLDER, uploaded_file.name)

    with open(file_path, "wb") as f:
        f.write(uploaded_file.getbuffer())

    return file_path
