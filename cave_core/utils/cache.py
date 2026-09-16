from django.conf import settings
from django.core.cache import cache


class Cache:
    """
    High-performance wrapper around Django's cache backend (Redis / Valkey / LocMem)
    with pipelined multi-key operations.
    """

    def __init__(self):
        self.cache = cache

    def get(self, data_id: str, default=None):
        """
        Gets the data from the cache.

        data_id: str
            The data_id of the data to be retrieved
        default: any
            The default value to return if the data does not exist
            Default: None

        Returns: any
        """
        return self.cache.get(data_id, default)

    def get_many(self, data_ids: list, default=None):
        """
        Gets multiple keys from the cache in a single pipelined network round-trip.

        data_ids: list
            The data_ids of the data to be retrieved
        default: any
            The default value to return if a key does not exist
            Default: None

        Returns: dict
        """
        results = {}
        # Pipelined retrieval: sends all GET commands in a single network round-trip.
        # Uses individual pipeline.get() which avoids CROSSSLOT errors in Redis Cluster / ElastiCache Serverless.
        try:
            client = self.cache._cache.get_client(None)
            pipe = client.pipeline()
            for data_id in data_ids:
                pipe.get(self.cache.make_and_validate_key(data_id))
            raw_values = pipe.execute()
            for data_id, raw_val in zip(data_ids, raw_values):
                if raw_val is not None:
                    results[data_id] = self.cache._cache._serializer.loads(raw_val)
        except Exception:
            results = {}

        # Fill any missing keys using standard cache get or default
        if len(results) != len(data_ids):
            for data_id in data_ids:
                if data_id not in results:
                    val = self.get(data_id, default)
                    if val is not None:
                        results[data_id] = val
        return results

    def set(
        self,
        data_id: str,
        data: dict,
        timeout: int | None = settings.CACHE_TIMEOUT,
    ):
        """
        Sets the data in the cache.

        data_id: str
            The data_id of the data to be stored
        data: any
            The data to be stored
        timeout: int | None
            The timeout to use for the cache
            Default: settings.CACHE_TIMEOUT
            Note: If None, the cache will not expire
        """
        self.cache.set(data_id, data, timeout=timeout)

    def set_many(
        self,
        data: dict,
        timeout: int | None = settings.CACHE_TIMEOUT,
    ):
        """
        Sets multiple keys in the cache in a single pipelined network round-trip.

        data: dict
            A dictionary of keys and values to be stored
        timeout: int | None
            The timeout to use for the cache
            Default: settings.CACHE_TIMEOUT
            Note: If None, the cache will not expire
        """
        try:
            client = self.cache._cache.get_client(None, write=True)
            pipe = client.pipeline()
            backend_timeout = self.cache.get_backend_timeout(timeout)
            for data_id, val in data.items():
                cache_key = self.cache.make_and_validate_key(data_id)
                serialized = self.cache._cache._serializer.dumps(val)
                if backend_timeout is not None:
                    pipe.set(cache_key, serialized, ex=backend_timeout)
                else:
                    pipe.set(cache_key, serialized)
            pipe.execute()
        except Exception:
            for data_id, val in data.items():
                self.cache.set(data_id, val, timeout=timeout)

    def delete(self, data_id: str):
        """
        Deletes the data from the cache.

        data_id: str
            The data_id of the data to be deleted
        """
        self.cache.delete(data_id)

    def delete_many(self, data_ids: list):
        """
        Deletes multiple keys from the cache in a single pipelined network round-trip.

        data_ids: list
            The data_ids of the data to be deleted
        """
        try:
            client = self.cache._cache.get_client(None, write=True)
            pipe = client.pipeline()
            for data_id in data_ids:
                pipe.delete(self.cache.make_and_validate_key(data_id))
            pipe.execute()
        except Exception:
            for data_id in data_ids:
                self.cache.delete(data_id)

    def flush(self):
        """
        Flushes all keys from the cache.
        """
        self.cache.clear()
