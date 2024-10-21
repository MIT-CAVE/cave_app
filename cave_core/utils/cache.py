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
                persistent_cache.set('meta', meta, timeout=None)
                for key in persistent_cache.keys(id_regex, memory=True):
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
            service = persist_cache_background_service(self, 'session:*')
            service.asyncRun(daemon=True)

    def __format_low_level_cache_key__(self, key: bytes):
        return ":".join(key.decode().split(':')[2:])
    
    def __low_level_cache__(self):
        return self.cache._cache.get_client()
    
    def __low_level_cache_keys__(self, pattern:str):
        return [self.__format_low_level_cache_key__(key) for key in self.__low_level_cache__().keys(pattern)]

    def keys(self, pattern:str, memory:bool=False, persistent:bool=False):
        """
        Gets the keys in the cache based on a pattern

        Note: This function will only work for Redis based caches

        pattern: str
            The pattern to use to find the keys
            Note: The pattern is a simple string pattern to indicate key starts with
            Note: A '*' can be used as a wildcard at the end of the pattern but not in the middle
        memory: bool
            Whether to get the keys from the memory based cache
            Default: False
            Note: Can not be True if persistent is True
        persistent: bool
            Whether to get the keys from the persistent storage cache
            Default: False
            Note: Can not be True if memory is True
        """
        assert memory ^ persistent, "Cache.keys(): Either memory or persistent must be True but not both"
        if memory:
            pattern = f"*{pattern}" if not pattern.startswith("*") else pattern
            return self.__low_level_cache_keys__(pattern)
        else:
            if pattern == '*':
                return [item for item in self.listdir('')[1] if item != '.gitignore']
            return [item for item in self.listdir('')[1] if item != '.gitignore' and pattern.replace('*', '') in item]


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
            try:
                with self.open(data_id) as f:
                    data = json.load(f)
                self.set(data_id, data)
                return data
            except:
                pass
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
                    try:
                        with self.open(data_id) as f:
                            missing_data[data_id] = json.load(f)
                        self.set(data_id, missing_data[data_id])
                    except:
                        missing_data[data_id] = default
                data.update(missing_data)
            else:
                for data_id in missing_ids:
                    data[data_id] = default
        return data
    
    def set(self, data_id:str, data:dict, memory:bool=True, persistent:bool=False, timeout:[int|None]=settings.CACHE_TIMEOUT):
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
        timeout: int
            The timeout to use for the cache
            Default: settings.CACHE_TIMEOUT
            Note: If None, the cache will not expire
        """
        if memory:
            self.cache.set(data_id, data, timeout=timeout)
        if persistent:
            self.save(data_id, ContentFile(json.dumps(data)))

    def set_many(self, data:dict, memory:bool=True, persistent:bool=False, timeout:[int|None]=settings.CACHE_TIMEOUT):
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
        timeout: int
            The timeout to use for the cache
            Default: settings.CACHE_TIMEOUT
            Note: If None, the cache will not expire        
        """
        # print(f'Cache -> Setting: {data.keys()}')
        if memory:
            self.cache.set_many(data, timeout=timeout)
        if persistent:
            for data_id, value in data.items():
                self.set(data_id, value, memory=False, persistent=True)

    def delete(self, data_id:str, memory:bool=False, persistent:bool=False):
        """
        Deletes the data in one or both of the cache and the persistent storage

        data_id: str
            The data_id of the data to be deleted
        memory: bool
            Whether to delete the data from the cache
            Default: False
        persistent: bool
            Whether to delete the data from the persistent storage
            Default: False
        """
        # print(f'Cache -> Deleting: {data_id}')
        assert memory or persistent, "Either memory or persistent must be True"
        if memory:
            self.cache.delete(data_id)
        if persistent:
            try:
                super().delete(data_id)
            except:
                pass

    def delete_many(self, data_ids:list, memory:bool=False, persistent:bool=False):
        """
        Deletes the data in one or both of the cache and the persistent storage

        data_ids: list
            The data_ids of the data to be deleted
        memory: bool
            Whether to delete the data from the cache
            Default: False
        persistent: bool
            Whether to delete the data from the persistent storage
            Default: False
        """
        # print(f'Cache -> Deleting: {data_ids}')
        assert memory or persistent, "Cache.delete_many(): Either memory or persistent must be True"
        if memory:
            self.cache.delete_many(data_ids)
        if persistent:
            for data_id in data_ids:
                self.delete(data_id, persistent=True)

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
        assert memory or persistent, "Cache.delete_pattern(): Either memory or persistent must be True"
        if memory:
            self.delete_many(self.keys(pattern, memory=True), memory=True)
        if persistent:
            self.delete_many(self.keys(pattern, persistent=True), persistent=True)