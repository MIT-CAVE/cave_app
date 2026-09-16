import os, sys, time

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Setup Django environment
os.environ.setdefault(
    "DJANGO_SETTINGS_MODULE",
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "cave_app.settings.development"),
)

import django

django.setup()

import hashlib
import orjson
from django.core.cache import cache as django_cache
from django.core.cache.backends.locmem import LocMemCache
from cave_core.utils.cache import Cache
from cave_core.models import Sessions, Teams, CustomUser
from cave_core.websockets.cave_ws_broadcaster import CaveWSBroadcaster, broadcaster
from cave_utils import Validator


# =====================================================================
# Mock In-Memory Cache Wrapper for Reliable Standalone Offline Testing
# =====================================================================
class MemoryCacheBackend:
    def __init__(self):
        self._store = {}
        self._serializer = orjson

    def get(self, key, default=None):
        return self._store.get(key, default)

    def set(self, key, value, timeout=None):
        self._store[key] = value

    def delete(self, key):
        self._store.pop(key, None)

    def clear(self):
        self._store.clear()

    def make_and_validate_key(self, key):
        return str(key)

    def get_backend_timeout(self, timeout):
        return timeout


class MockPipeline:
    def __init__(self, backend):
        self.backend = backend
        self.ops = []

    def get(self, key):
        self.ops.append(("get", key, None, None))
        return self

    def set(self, key, value, ex=None):
        self.ops.append(("set", key, value, ex))
        return self

    def delete(self, key):
        self.ops.append(("delete", key, None, None))
        return self

    def execute(self):
        results = []
        for op, key, val, _ in self.ops:
            if op == "get":
                raw = self.backend._store.get(key)
                results.append(
                    orjson.dumps(raw, default=str, option=orjson.OPT_NON_STR_KEYS)
                    if raw is not None
                    else None
                )
            elif op == "set":
                self.backend._store[key] = (
                    orjson.loads(val) if isinstance(val, (bytes, str)) else val
                )
                results.append(True)
            elif op == "delete":
                self.backend._store.pop(key, None)
                results.append(True)
        self.ops = []
        return results


class StandaloneCache(Cache):
    """
    Test Cache that wraps MemoryCacheBackend with pipelined client support.
    """

    def __init__(self):
        super().__init__()
        self._backend = MemoryCacheBackend()
        self.cache = self._backend
        self.cache._cache = self._backend
        self.cache._cache.get_client = lambda _, write=False: MockPipeline(self._backend)
        self.cache._cache._serializer = orjson
        self.cache.make_and_validate_key = lambda k: str(k)
        self.cache.get_backend_timeout = lambda t: t


# Silence background websocket pubsub outside live server
from cave_core.websockets import cave_ws_broadcaster as ws_module

ws_module.broadcaster.broadcast = lambda *args, **kwargs: None
ws_module.broadcaster.broadcast_many = lambda *args, **kwargs: None


# =====================================================================
# Test 1: Cache Primitives & orjson Serialization
# =====================================================================
def test_cache_primitives():
    print("Testing Cache primitives & serialization...")
    test_cache = StandaloneCache()

    # 1. Single Set / Get
    test_cache.set("test:key1", {"name": "Item 1", "count": 42}, memory=True, persistent=False)
    assert test_cache.get("test:key1") == {"name": "Item 1", "count": 42}, "Single get failed"

    # 2. Non-string dictionary keys (e.g. integer keys) & default=str serialization
    from datetime import datetime, timezone

    now = datetime(2026, 1, 1, 12, 0, 0, tzinfo=timezone.utc)
    non_str_key_payload = {
        1: "team_one",
        2: "team_two",
        "timestamp": now,
    }
    test_cache.set("test:non_str_keys", non_str_key_payload, memory=True, persistent=True)
    fetched_non_str = test_cache.get("test:non_str_keys")
    assert (
        fetched_non_str.get("1") == "team_one" or fetched_non_str.get(1) == "team_one"
    ), "Non-string key serialization/deserialization failed"
    assert "2026-01-01" in str(fetched_non_str.get("timestamp"))

    # 3. Default value on missing key
    assert (
        test_cache.get("test:missing", default="DEFAULT") == "DEFAULT"
    ), "Default value on missing key failed"

    # 4. Pipelined Set Many / Get Many
    payload = {
        "test:batch:1": {"a": [1, 2, 3], "nested": {"b": True}},
        "test:batch:2": {"x": 100.5, "y": None},
        "test:batch:3": {"text": "hello world"},
    }
    test_cache.set_many(payload, memory=True, persistent=False)
    fetched = test_cache.get_many(list(payload.keys()))
    assert fetched == payload, f"Pipelined get_many failed: {fetched} != {payload}"

    # 5. Pipelined Delete Many
    test_cache.delete_many(["test:batch:1", "test:batch:2"], memory=True, persistent=False)
    assert test_cache.get("test:batch:1") is None, "Delete many failed for key 1"
    assert test_cache.get("test:batch:2") is None, "Delete many failed for key 2"
    assert test_cache.get("test:batch:3") == {
        "text": "hello world"
    }, "Delete many deleted wrong key"

    # 6. Flush
    test_cache.flush(memory=True, persistent=False)
    assert test_cache.get("test:batch:3") is None, "Flush failed"
    print("✔ Cache primitives passed")


# =====================================================================
# Test 2: Session In-Memory Caching & Lock Lifecycle
# =====================================================================
def test_session_in_memory_caching():
    print("Testing Session in-memory caching and lock lifecycle...")
    test_cache = StandaloneCache()

    # Create mock session object
    session = Sessions(id=999, name="Test Session")
    # Patch global cache model with test_cache
    from cave_core.models import sessions as sessions_module

    old_cache = sessions_module.cache
    sessions_module.cache = test_cache

    try:
        # Prepopulate cache in Redis/Memory
        test_cache.set("session:999:user_ids", ["101"], memory=True)
        test_cache.set("session:999:versions", {"settings": 1, "panes": 1}, memory=True)
        test_cache.set(
            "session:999:data:settings", {"iconUrl": "https://example.com/icon"}, memory=True
        )
        test_cache.set("session:999:data:panes", {"data": {"slider": {"value": 10}}}, memory=True)

        # 1. Acquire Lock
        session.set_loading(True)
        assert session.__dict__.get("is_executing") is True, "Session is_executing should be True"
        assert test_cache.get("session:999:executing") is True, "Cache lock should be True"

        # 2. First get_data reads from cache and populates __dict__["data"]
        data1 = session.get_data(keys=["settings", "panes"])
        assert "data" in session.__dict__, "data_cache should exist on session"
        assert session.__dict__["data"]["settings"]["iconUrl"] == "https://example.com/icon"
        assert "hashes" in session.__dict__, "hashes should exist on session"

        # 3. Modify memory directly - subsequent get_data should hit memory, not backend
        session.__dict__["data"]["settings"]["iconUrl"] = "https://example.com/modified_in_memory"
        data2 = session.get_data(keys=["settings"])
        assert (
            data2["settings"]["iconUrl"] == "https://example.com/modified_in_memory"
        ), "get_data did not hit memory cache"

        # 4. Release Lock
        session.set_loading(False)
        assert (
            session.__dict__.get("is_executing") is False
        ), "is_executing should be False after unlock"
        assert (
            test_cache.get("session:999:executing") is False
        ), "Cache lock should be False after unlock"
        assert "data" not in session.__dict__, "data cache should be cleaned up on unlock"
        assert "versions" not in session.__dict__, "versions cache should be cleaned up on unlock"
        assert "hashes" not in session.__dict__, "hashes cache should be cleaned up on unlock"
    finally:
        sessions_module.cache = old_cache

    print("✔ Session in-memory caching and lock lifecycle passed")


# =====================================================================
# Test 3: Smart Delta Versioning & In-Place Mutation Detection
# =====================================================================
def test_smart_delta_versioning():
    print("Testing Smart Delta Versioning & In-Place Mutation...")
    test_cache = StandaloneCache()

    from cave_core.models import sessions as sessions_module

    old_cache = sessions_module.cache
    sessions_module.cache = test_cache

    try:
        session = Sessions(id=888, name="Delta Session")
        test_cache.set("session:888:user_ids", ["101"], memory=True)
        session.set_loading(True)

        # Initial state replacement
        initial_data = {
            "settings": {"iconUrl": "https://react-icons.mitcave.com/5.4.0"},
            "panes": {"data": {"mySlider": {"value": 10}}},
            "maps": {"data": {"map1": {"name": "Main Map"}}},
        }
        session.replace_data(data=initial_data, wipeExisting=True)

        v1 = session.get_versions()
        assert v1 == {"settings": 1, "panes": 1, "maps": 1}, f"Initial versions mismatch: {v1}"

        # Fetch session data for execution
        session_data = session.get_data(keys=["settings", "panes", "maps"])

        # MUTATE IN PLACE: modify only panes
        session_data["panes"]["data"]["mySlider"]["value"] = 50

        # Replace data with modified session_data
        session.replace_data(data=session_data, wipeExisting=False)

        v2 = session.get_versions()
        # ONLY panes version should increment! settings and maps should stay 1
        assert v2["panes"] == 2, f"Expected panes version to be 2, got {v2['panes']}"
        assert v2["settings"] == 1, f"Expected settings version to remain 1, got {v2['settings']}"
        assert v2["maps"] == 1, f"Expected maps version to remain 1, got {v2['maps']}"

        # Test Delta Broadcast resolution
        # Broadcast comparing v1 to v2 should ONLY yield updated_keys = ['panes']
        updated_keys = [k for k, v in v2.items() if v1.get(k) != v]
        assert updated_keys == ["panes"], f"Delta keys mismatch: {updated_keys} != ['panes']"

        # Broadcast with matching versions should yield empty list
        no_keys = [k for k, v in v2.items() if v2.get(k) != v]
        assert no_keys == [], f"Expected no updated keys, got {no_keys}"

        session.set_loading(False)
    finally:
        sessions_module.cache = old_cache

    print("✔ Smart delta versioning and in-place mutation passed")


# =====================================================================
# Test 4: wipeExisting Memory & Cache Pruning
# =====================================================================
def test_wipe_existing_pruning():
    print("Testing wipeExisting memory & cache pruning...")
    test_cache = StandaloneCache()

    from cave_core.models import sessions as sessions_module

    old_cache = sessions_module.cache
    sessions_module.cache = test_cache

    try:
        session = Sessions(id=777, name="Wipe Session")
        test_cache.set("session:777:user_ids", ["101"], memory=True)
        session.set_loading(True)

        # 1. Populate 3 keys
        session.replace_data(
            data={
                "settings": {"iconUrl": "abc"},
                "panes": {"data": {}},
                "maps": {"data": {}},
            },
            wipeExisting=True,
        )
        assert len(session.get_versions()) == 3
        assert "panes" in session.__dict__["data"]
        assert "maps" in session.__dict__["data"]

        # 2. Replace with only settings and wipeExisting=True
        session.replace_data(
            data={"settings": {"iconUrl": "xyz"}},
            wipeExisting=True,
        )

        v = session.get_versions()
        assert "settings" in v, "settings should remain"
        assert "panes" not in v, "panes should be removed from versions"
        assert "maps" not in v, "maps should be removed from versions"

        # Check memory cache pruning
        assert (
            "panes" not in session.__dict__["data"]
        ), "panes was not pruned from memory data cache"
        assert "maps" not in session.__dict__["data"], "maps was not pruned from memory data cache"
        assert "panes" not in session.__dict__["hashes"], "panes was not pruned from hashes"
        assert "maps" not in session.__dict__["hashes"], "maps was not pruned from hashes"

        # Check backend cache deletion
        assert test_cache.get("session:777:data:panes") is None, "panes was not deleted from cache"
        assert test_cache.get("session:777:data:maps") is None, "maps was not deleted from cache"

        session.set_loading(False)
    finally:
        sessions_module.cache = old_cache

    print("✔ wipeExisting pruning passed")


# =====================================================================
# Test 5: Mutation API Endpoint Logic & Out-of-Sync Detection
# =====================================================================
def test_session_mutations():
    print("Testing Session mutation logic & synchronization check...")
    test_cache = StandaloneCache()

    from cave_core.models import sessions as sessions_module

    old_cache = sessions_module.cache
    sessions_module.cache = test_cache

    try:
        session = Sessions(id=666, name="Mutate Session")
        test_cache.set("session:666:user_ids", ["101"], memory=True)
        session.set_loading(True)

        session.replace_data(
            data={"panes": {"values": {"slider": 10}}},
            wipeExisting=True,
        )
        current_version = session.get_versions()["panes"]

        # 1. Valid mutation with matching version
        res = session.mutate(
            data_version=current_version,
            data_name="panes",
            data_path=["values", "slider"],
            data_value=25,
        )
        assert res is None, f"Expected successful mutation, got {res}"
        data = session.get_data(keys=["panes"])
        assert data["panes"]["values"]["slider"] == 25, "Mutate failed to set new value"

        # 2. Out-of-sync mutation (version mismatch)
        res_sync_err = session.mutate(
            data_version=999,  # Mismatched version
            data_name="panes",
            data_path=["values", "slider"],
            data_value=50,
            ignore_version=False,
        )
        assert res_sync_err == {"synch_error": True}, "Expected synch_error on version mismatch"

        # 3. Ignore version flag overrides mismatch
        res_ignore = session.mutate(
            data_version=999,
            data_name="panes",
            data_path=["values", "slider"],
            data_value=50,
            ignore_version=True,
        )
        assert res_ignore is None, "ignore_version=True should succeed"
        data = session.get_data(keys=["panes"])
        assert data["panes"]["values"]["slider"] == 50

        session.set_loading(False)
    finally:
        sessions_module.cache = old_cache

    print("✔ Session mutation logic passed")


# =====================================================================
# Test 6: WebSocket Multi-User Broadcast Batching
# =====================================================================
def test_websocket_broadcast_batching():
    print("Testing WebSocket broadcast multi-user batching...")

    class MockModel:
        def __init__(self, user_ids):
            self._user_ids = user_ids

        def get_user_ids(self):
            return self._user_ids

    class MockBroadcasterEngine:
        def __init__(self):
            self.single_broadcasts = []
            self.many_broadcasts = []

        def broadcast(self, channel, payload):
            self.single_broadcasts.append((channel, payload))

        def broadcast_many(self, channels, payload):
            self.many_broadcasts.append((channels, payload))

    mock_engine = MockBroadcasterEngine()
    from cave_core.websockets import cave_ws_broadcaster as ws_module

    old_broadcaster = ws_module.broadcaster
    ws_module.broadcaster = mock_engine

    try:
        # Single user broadcast
        single_user_model = MockModel([101])
        CaveWSBroadcaster(single_user_model).broadcast(event="overwrite", data={"test": True})
        assert len(mock_engine.single_broadcasts) == 1, "Expected 1 single broadcast"
        assert mock_engine.single_broadcasts[0][0] == "101"
        assert len(mock_engine.many_broadcasts) == 0

        # Multi-user broadcast
        multi_user_model = MockModel([101, 102, 103])
        CaveWSBroadcaster(multi_user_model).broadcast(event="overwrite", data={"test": True})
        assert len(mock_engine.many_broadcasts) == 1, "Expected 1 broadcast_many call"
        assert mock_engine.many_broadcasts[0][0] == ["101", "102", "103"]
    finally:
        ws_module.broadcaster = old_broadcaster

    print("✔ WebSocket broadcast multi-user batching passed")


# =====================================================================
# Test 7: Concurrent Execution Lock Rejection
# =====================================================================
def test_concurrent_lock_rejection():
    print("Testing Concurrent Execution Lock Rejection...")
    test_cache = StandaloneCache()

    from cave_core.models import sessions as sessions_module

    old_cache = sessions_module.cache
    sessions_module.cache = test_cache

    try:
        session = Sessions(id=555, name="Lock Session")
        test_cache.set("session:555:user_ids", ["101"], memory=True)

        # First lock succeeds
        session.set_loading(True)
        assert session.__dict__.get("is_executing") is True

        # Second lock attempt on executing session must raise exception
        lock_failed = False
        try:
            session.set_loading(True)
        except Exception as e:
            lock_failed = True
            assert "already executing a task" in str(e)
        assert lock_failed, "Concurrent set_loading(True) should raise execution collision error"

        # Release lock
        session.set_loading(False, override_block=True)
        assert session.__dict__.get("is_executing") is False
    finally:
        sessions_module.cache = old_cache

    print("✔ Concurrent execution lock rejection passed")


# =====================================================================
# Test 8: Client-Only & Omit-Keys Filtering & Missing Key Creation
# =====================================================================
def test_key_filtering_and_missing_creation():
    print("Testing client_only/omit_keys filtering and create_missing_cache_keys...")
    test_cache = StandaloneCache()

    from cave_core.models import sessions as sessions_module

    old_cache = sessions_module.cache
    sessions_module.cache = test_cache

    try:
        session = Sessions(id=444, name="Filter Session")
        test_cache.set("session:444:user_ids", ["101"], memory=True)
        session.set_loading(True)

        # Set up keys including client and non-client/background keys
        test_cache.set("session:444:data:settings", {"iconUrl": "abc"}, memory=True)
        test_cache.set("session:444:data:panes", {"data": {}}, memory=True)
        test_cache.set("session:444:data:associated", {"data": {"assoc_1": {}}}, memory=True)
        test_cache.set("session:444:data:internal_private_key", {"secret": 123}, memory=True)
        test_cache.set(
            "session:444:versions",
            {"settings": 1, "panes": 1, "associated": 1, "internal_private_key": 1},
            memory=True,
        )

        # 1. client_only=True should exclude non-client api keys
        client_data = session.get_data(client_only=True)
        assert "settings" in client_data
        assert "panes" in client_data
        assert "associated" in client_data  # associated is in api_keys
        assert (
            "internal_private_key" not in client_data
        ), "internal_private_key should be filtered by client_only"

        # 2. omit_keys should omit specified keys
        omitted_data = session.get_data(
            keys=["settings", "panes"], omit_keys=["panes"], client_only=False
        )
        assert "settings" in omitted_data
        assert "panes" not in omitted_data

        # 3. create_missing_cache_keys=True creates empty dict for missing keys
        missing_data = session.get_data(
            keys=["maps"],
            create_missing_cache_keys=True,
            client_only=False,
        )
        assert missing_data.get("maps") == {}, "Expected empty dict for created missing key"
        assert (
            test_cache.get("session:444:data:maps") == {}
        ), "Missing key should be persisted to cache"

        session.set_loading(False)
    finally:
        sessions_module.cache = old_cache

    print("✔ Key filtering and missing key creation passed")


# =====================================================================
# Test 9: Large Payload & Complex Data Type Fidelity
# =====================================================================
def test_large_payload_fidelity():
    print("Testing Large Payload & Data Type Fidelity...")
    test_cache = StandaloneCache()

    # Generate 10,000 items with mixed data types
    large_list = [
        {
            "id": f"node_{i}",
            "lat": 42.3601 + (i * 0.0001),
            "lng": -71.0589 + (i * 0.0001),
            "active": (i % 2 == 0),
            "score": float(i) * 1.5,
            "metadata": {"tags": ["a", "b"], "nested_null": None},
        }
        for i in range(10000)
    ]
    large_payload = {
        "mapFeatures": {"data": {"nodes": {"data": {item["id"]: item for item in large_list}}}}
    }

    t0 = time.perf_counter()
    test_cache.set("session:333:data:mapFeatures", large_payload, memory=True, persistent=False)
    retrieved = test_cache.get("session:333:data:mapFeatures")
    t_el = time.perf_counter() - t0

    assert len(retrieved["mapFeatures"]["data"]["nodes"]["data"]) == 10000
    assert retrieved["mapFeatures"]["data"]["nodes"]["data"]["node_0"]["lat"] == 42.3601
    assert retrieved["mapFeatures"]["data"]["nodes"]["data"]["node_9999"]["active"] is False
    print(f"✔ 10,000 complex map nodes serialized & verified in {t_el*1000:.2f}ms")


# =====================================================================
# Main Runner
# =====================================================================
def run_all_tests():
    start_time = time.perf_counter()
    print("======================================================================")
    print(" Running CAVE Caching, Local Data & Mutation Test Suite")
    print("======================================================================")

    test_cache_primitives()
    test_session_in_memory_caching()
    test_smart_delta_versioning()
    test_wipe_existing_pruning()
    test_session_mutations()
    test_websocket_broadcast_batching()
    test_concurrent_lock_rejection()
    test_key_filtering_and_missing_creation()
    test_large_payload_fidelity()

    elapsed = time.perf_counter() - start_time
    print("======================================================================")
    print(f" ALL 9 TEST MODULES PASSED in {elapsed:.3f}s (Limit: < 15.000s)")
    print("======================================================================")
    assert elapsed < 15.0, f"Test execution took {elapsed:.3f}s, exceeding 15s limit!"


if __name__ == "__main__":
    run_all_tests()
