from django.core.files.storage import FileSystemStorage
from django.contrib.staticfiles.storage import StaticFilesStorage

class PrivateMediaStorage(FileSystemStorage):
    pass

class PublicMediaStorage(FileSystemStorage):
    pass

class StaticStorage(StaticFilesStorage):
    pass

class CacheStorage(FileSystemStorage):
    location = 'persistent_cache'