import hashlib


def get_file_hash(uploaded_file):
    """
    Generate SHA256 hash of uploaded PDF.
    """

    file_bytes = uploaded_file.getvalue()

    return hashlib.sha256(file_bytes).hexdigest()
