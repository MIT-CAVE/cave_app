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
                        persistent_cache.set(key, data, memory=False, persistent=True)
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
            service = persist_cache_background_service(persistent_cache=self, id_regex='*session:*')
            service.asyncRun()

    def get(self, data_id:str, default=None):
        """
        Gets the data from the cache if it exists, otherwise from the persistent storage and caches it

        If the data does not exist in either the cache or the persistent storage, None is returned

        data_id: str
            The data_id of the data to be retrieved
        default: any
            The default value to return if the data does not exist
            Default: None

        Returns: dict
        """
        # print(f'Cache -> Getting: {data_id}')
        data = self.cache.get(data_id, "__NONE__")
        if data != "__NONE__":
            return data
        # Only pull from the persistent storage if the CACHE_BACKUP_INTERVAL is greater than 0
        if settings.CACHE_BACKUP_INTERVAL > 0:
            if self.exists(data_id):
                with self.open(data_id) as f:
                    data = json.load(f)
                self.cache.set(data_id, data)
                return data
        return default
    
    def get_many(self, data_ids:list, default=None):
        """
        Gets the data from the cache if it exists, otherwise from the persistent storage and caches it

        If the data does not exist in either the cache or the persistent storage, None is returned

        data_ids: list
            The data_ids of the data to be retrieved
        default: any
            The default value to return if the data does not exist
            Default: None

        Returns: dict
        """
        # print(f'Cache -> Getting: {data_ids}')
        data = self.cache.get_many(data_ids)
        missing_ids = [data_id for data_id in data_ids if data_id not in data]
        if len(missing_ids) > 0:
            # Only pull from the persistent storage if the CACHE_BACKUP_INTERVAL is greater than 0
            if settings.CACHE_BACKUP_INTERVAL > 0:
                missing_data = {}
                for data_id in missing_ids:
                    if self.exists(data_id):
                        with self.open(data_id) as f:
                            missing_data[data_id] = json.load(f)
                        self.cache.set(data_id, missing_data[data_id])
                    else:
                        missing_data[data_id] = default
                data.update(missing_data)
            else:
                for data_id in missing_ids:
                    data[data_id] = default
        return data
    
    def set(self, data_id:str, data:dict, memory:bool=True, persistent:bool=False):
        """
        Sets the data in one or both of the cache and the persistent storage

        data_id: str
            The data_id of the data to be stored
        data: dict
            The data to be stored
            Note: Must be JSON serializable
        memory: bool
            Whether to store the data in the cache
            Default: True
        persistent: bool
            Whether to store the data in the persistent storage
            Default: False
        """
        # print(f'Cache -> Setting: {data_id}')
        if memory:
            self.cache.set(data_id, data)
        if persistent:
            self.delete(data_id, memory=False, persistent=True)
            self.save(data_id, ContentFile(json.dumps(data)))

    def set_many(self, data:dict, memory:bool=True, persistent:bool=False):
        """
        Sets the data in one or both of the cache and the persistent storage

        data: dict
            A set of keys and values to be stored
            Note: Each value Must be JSON serializable
        memory: bool
            Whether to store the data in the cache
            Default: True
        persistent: bool
            Whether to store the data in the persistent storage
            Default: False
        """
        # print(f'Cache -> Setting: {data.keys()}')
        if memory:
            self.cache.set_many(data)
        if persistent:
            for data_id, value in data.items():
                self.set(data_id, value, memory=False, persistent=True)

    def delete(self, data_id:str, memory:bool=True, persistent:bool=True):
        """
        Deletes the data in one or both of the cache and the persistent storage

        data_id: str
            The data_id of the data to be deleted
        memory: bool
            Whether to delete the data from the cache
            Default: True
        persistent: bool
            Whether to delete the data from the persistent storage
            Default: True
        """
        # print(f'Cache -> Deleting: {data_id}')
        if memory:
            self.cache.delete(data_id)
        if persistent:
            if self.exists(data_id):
                super().delete(data_id)

    def delete_many(self, data_ids:list, memory:bool=True, persistent:bool=True):
        """
        Deletes the data in one or both of the cache and the persistent storage

        data_ids: list
            The data_ids of the data to be deleted
        memory: bool
            Whether to delete the data from the cache
            Default: True
        persistent: bool
            Whether to delete the data from the persistent storage
            Default: True
        """
        # print(f'Cache -> Deleting: {data_ids}')
        if memory:
            self.cache.delete_many(data_ids)
        if persistent:
            for data_id in data_ids:
                self.delete(data_id, memory=False, persistent=True)

    def delete_pattern(self, pattern:str, memory:bool=True, persistent:bool=True):
        """
        Deletes the data in one or both of the cache and the persistent storage based on a pattern

        pattern: str
            The pattern to use to find the data to be deleted
            Note: The pattern is a simple string pattern to indicate key starts with
            Note: A '*' can be used as a wildcard at the end of the pattern but not in the middle
        memory: bool
            Whether to delete the data from the cache
            Default: True
        persistent: bool
            Whether to delete the data from the persistent storage
            Default: True
        """
        # print(f'Cache -> Deleting: {pattern}')
        if memory:
            keys = [":".join(full_key.decode().split(':')[2:]) for full_key in self.cache._cache.get_client().keys(f"*{pattern}")]
            self.delete_many(keys, memory=True)
        if persistent:
            persistent_pattern = pattern.replace('*', '')
            keys = [item for item in self.listdir('')[1] if item != '.gitignore' and item.startswith(persistent_pattern)]
            self.delete_many(keys, memory=False, persistent=True)