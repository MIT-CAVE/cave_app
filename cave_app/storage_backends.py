from django.conf import settings
from django.core.files.base import ContentFile
from django.core.files.storage import FileSystemStorage
from django.contrib.staticfiles.storage import StaticFilesStorage
import json



class PersistentCache(FileSystemStorage):
    location = 'persistent_cache'

    def get(self, name:str):
        if self.exists(name):
            with self.open(name) as f:
                data = json.load(f)
            return data
    
    def set(self, name:str, data:dict):
        self.delete(name)
        self.save(name, ContentFile(json.dumps(data)))

    def delete(self, name:str):
        if self.exists(name):
            super().delete(name)



PrivateMediaStorage = FileSystemStorage
PublicMediaStorage = FileSystemStorage
StaticStorage = StaticFilesStorage
