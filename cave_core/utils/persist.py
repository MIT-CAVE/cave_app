from django.conf import settings

import time
from pamda import pamda

@pamda.thunkify
def persist_cache(persistent_cache, cache):
    """
    Persists the data for the current session to the persistent storage
    """
    lowLevelCache = cache._cache.get_client()
    while True:
        try:
            # Interruptable sleep
            for i in range(settings.CACHE_BACKUP_INTERVAL):
                time.sleep(1)
            # Load the meta data from the persistent storage
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
                for key in lowLevelCache.keys('*data:*'):
                    key = key.decode()[3:]
                    data = cache.get(key)
                    if data is not None:
                        persistent_cache.set(key, data)
        except Exception as e:
            print('Error: The persist_cache function failed with the following error:')
            print(e)