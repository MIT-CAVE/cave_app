from django.core.files.storage import FileSystemStorage
from django.contrib.staticfiles.storage import StaticFilesStorage

PrivateMediaStorage = FileSystemStorage
PublicMediaStorage = FileSystemStorage
StaticStorage = StaticFilesStorage
