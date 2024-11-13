from django.conf import settings
import os, time
from pamda import pamda

@pamda.thunkify
def __session_persistence_service_task__(Sessions, cache):
    """
    Persists the data in the cache to the persistent storage

    Sessions: Sessions
        The Sessions object to be used for the cache

    Notes:
        - This function is designed to be run in a separate thread
    """
    # Run the persistence background tasks
    # Checking if RUN_MAIN is true ensures that the background tasks are only run once on initial server start
    print('Starting the cache persistence background service...')
    while True:
        try:
            # Interruptable sleep
            for i in range(settings.CACHE_BACKUP_INTERVAL):
                time.sleep(1)
            # Load the meta data
            # This is used to prevent multiple backups from happening at the same time
            meta = cache.get('meta')
            if meta is None:
                meta = {'last_update':0}
            now = time.time()
            # Assume multiple servers are running - only run this if the last update was long enough ago
            if meta['last_update']+settings.CACHE_BACKUP_INTERVAL<now:
                meta['last_update'] = now
                cache.set('meta', meta, timeout=None)
                for obj in Sessions.objects.all():
                    obj.persist_cache_data()
        except Exception as e:
            print('Error: The persist_cache function failed with the following error:')
            print(e)
            print('Restarting the cache persistence background service...')

def session_persistence_service(Sessions, cache):
    if os.environ.get('RUN_MAIN', None) == 'true' and settings.CACHE_BACKUP_INTERVAL is not None:
        service = __session_persistence_service_task__(Sessions, cache)
        service.asyncRun(daemon=True)