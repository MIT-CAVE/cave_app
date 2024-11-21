from django.core.files.storage import FileSystemStorage
from django.contrib.staticfiles.storage import StaticFilesStorage

class PrivateMediaStorage(FileSystemStorage):
    pass

class PublicMediaStorage(FileSystemStorage):
    pass

class StaticStorage(StaticFilesStorage):
    pass

class CacheStorage(FileSystemStorage):
    location = '__cache__'
    # Special code to always overwrite the file on a save
    def get_available_name(self, name: str, max_length: int | None = None) -> str:
        if self.exists(name):
            self.delete(name, persistent=True)
        return name