from django.conf import settings
from django.core.cache import cache
from django.core.files.base import ContentFile
from cave_app.storage_backends import CacheStorage

import json, time, os
from pamda import pamda


@pamda.thunkify
def persist_cache_background_service(persistent_cache, id_regex:str):
    """
    Persists the data in the cache to the persistent storage

    persistent_cache: Cache
        The persistent cache object to use
    id_regex: str
        The regex to use to find the keys in the cache

    Notes:
        - This function is designed to be run in a separate thread
        - This function will only work for Redis based caches
    """
    print('Starting the cache persistence background service...')
    lowLevelCache = persistent_cache.cache._cache.get_client()
    while True:
        try:
            # Interruptable sleep
            for i in range(settings.CACHE_BACKUP_INTERVAL):
                time.sleep(1)
            # Load the meta data
            # This is used to prevent multiple backups from happening at the same time
            meta = persistent_cache.get('meta')
            if meta is None:
                meta = {'last_update':0}
            now = time.time()
            # Assume multiple servers are running - only run this if the last update was long enough ago
            if meta['last_update']+settings.CACHE_BACKUP_INTERVAL<now:
                meta['last_update'] = now
                persistent_cache.set('meta', meta)
                # Note: This will only work for Redis based caches
                for full_key in lowLevelCache.keys(id_regex):
                    # Remove the prefix from the key to get the actual key (EG: '01:data:1' -> 'data:1')
                    key = ":".join(full_key.decode().split(':')[2:])
                    data = persistent_cache.cache.get(key)
                    if data is not None:
                        persistent_cache.persist_set(key, data)
        except Exception as e:
            print('Error: The persist_cache function failed with the following error:')
            print(e)
            print('Restarting the cache persistence background service...')

class Cache(CacheStorage):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.cache = cache

        # Run the persistence background tasks if CACHE_BACKUP_INTERVAL is greater than 0
        # Checking if RUN_MAIN is true ensures that the background tasks are only run once on initial server start
        if os.environ.get('RUN_MAIN', None) == 'true' and settings.CACHE_BACKUP_INTERVAL > 0:
            service = persist_cache_background_service(persistent_cache=self, id_regex='*data:*')
            service.asyncRun()

    def get(self, name:str):
        """
        Gets the data from the cache if it exists, otherwise from the persistent storage and caches it
        """
        data = self.cache.get(name)
        if data != None:
            return data
        if self.exists(name):
            with self.open(name) as f:
                data = json.load(f)
            self.cache.set(name, data)
            return data
        return None
    
    def set(self, name:str, data:dict):
        """
        Sets the data in the cache but not in the persistent storage
        """
        self.cache.set(name, data)

    def delete(self, name:str):
        """
        Deletes the data in the cache and the persistent storage
        """
        self.cache.delete(name)
        self.persist_delete(name)

    def persist_delete(self, name:str):
        """
        Deletes the data in the persistent storage but not in the cache
        """
        if self.exists(name):
            super().delete(name)

    def persist_set(self, name:str, data:dict):
        """
        Sets the data in the persistent storage but not in the cache
        """
        self.persist_delete(name)
        self.save(name, ContentFile(json.dumps(data)))