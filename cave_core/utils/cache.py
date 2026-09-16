from django.conf import settings
from django.core.cache import cache
from django.core.files.base import ContentFile
from cave_app.storage_backends import CacheStorage

import orjson


class Cache(CacheStorage):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.cache = cache

    def get(self, data_id: str, default=None):
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
        if settings.CACHE_BACKUP_INTERVAL is not None:
            try:
                with self.open(data_id) as f:
                    data = orjson.loads(f.read())
                self.set(data_id, data)
                return data
            except:
                pass
        return default

    def get_many(self, data_ids: list, default=None):
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

        # Fill any missing keys from persistent storage fallback or default
        missing = [d_id for d_id in data_ids if d_id not in results]
        if missing:
            for data_id in missing:
                results[data_id] = self.get(data_id, default)
        return results

    def set(
        self,
        data_id: str,
        data: dict,
        memory: bool = True,
        persistent: bool = False,
        timeout: int | None = settings.CACHE_TIMEOUT,
    ):
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
            self.save(
                data_id,
                ContentFile(orjson.dumps(data, default=str, option=orjson.OPT_NON_STR_KEYS)),
            )

    def set_many(
        self,
        data: dict,
        memory: bool = True,
        persistent: bool = False,
        timeout: int | None = settings.CACHE_TIMEOUT,
    ):
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
        if memory:
            # Pipelined batch write: sends all SET commands in a single network round-trip.
            # Compatible with AWS ElastiCache Serverless / Redis Cluster (no CROSSSLOT errors).
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
        if persistent:
            for data_id, val in data.items():
                self.save(
                    data_id,
                    ContentFile(orjson.dumps(val, default=str, option=orjson.OPT_NON_STR_KEYS)),
                )

    def persist(self, data_id: str):
        """
        Persists the data in the cache to the persistent storage

        data_id: str
            The data_id of the data to be persisted
        """
        data = self.cache.get(data_id, "__NONE__")
        if data != "__NONE__":
            self.set(data_id, data, memory=False, persistent=True)

    def persist_many(self, data_ids: list):
        """
        Persists the data in the cache to the persistent storage

        data_ids: list
            The data_ids of the data to be persisted
        """
        cached_data = self.get_many(data_ids)
        for data_id, val in cached_data.items():
            if val is not None:
                self.save(
                    data_id,
                    ContentFile(orjson.dumps(val, default=str, option=orjson.OPT_NON_STR_KEYS)),
                )

    def delete(self, data_id: str, memory: bool = False, persistent: bool = False):
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
        assert memory or persistent, "Cache.delete(): `memory` or `persistent` must be True"
        if memory:
            self.cache.delete(data_id)
        if persistent:
            try:
                super().delete(data_id)
            except:
                pass

    def delete_many(self, data_ids: list, memory: bool = False, persistent: bool = False):
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
        assert memory or persistent, "Cache.delete_many(): `memory` or `persistent` must be True"
        if memory:
            try:
                client = self.cache._cache.get_client(None, write=True)
                pipe = client.pipeline()
                for data_id in data_ids:
                    pipe.delete(self.cache.make_and_validate_key(data_id))
                pipe.execute()
            except Exception:
                for data_id in data_ids:
                    self.cache.delete(data_id)
        if persistent:
            for data_id in data_ids:
                try:
                    super().delete(data_id)
                except Exception:
                    pass

    def flush(self, memory: bool = False, persistent: bool = False):
        """
        Flushes the cache and/or the persistent storage

        memory: bool
            Whether to flush the cache
            Default: False
        persistent: bool
            Whether to flush the persistent storage
            Default: False
        """
        # print(f'Cache -> Flushing')
        if memory:
            self.cache.clear()
        if persistent:
            files = self.listdir("")[1]
            self.delete_many(files, persistent=True)
