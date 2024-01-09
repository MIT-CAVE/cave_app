from django.core.exceptions import ValidationError

def limit_upload_size(upload, max_size_mb:int):
    """
    Function:

    Validates the size of an upload

    Args:

    - `upload`: The upload to validate
        - An object with a `file.size` attribute referring to the size of the upload in bytes
    - `max_size_mb`: The maximum size in megabytes
    """
    if upload.file.size > max_size_mb * 1024 * 1024:
        raise ValidationError(f"Upload must be under {max_size_mb}MB")