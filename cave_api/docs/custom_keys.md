### Top-level custom keys
In addition to the standard CAVE [top-level keys](all_keys/top_level_keys.md), API designers can add custom top-level keys that allow them to persist data that is computed as a result of a user-side action. This emulates (on the back-end side) a pattern widely used in front-end development, called [state management](https://en.wikipedia.org/wiki/State_management).

A fairly common use case for this approach is to persist data that may need to be invisible to users based on other user selections. For example, an app that has options that toggle other options might want to store any choices users have made when those options are not currently presented to the user. While designers could explore other solutions for data persistence, we believe that top-level custom keys provide an easy escape hatch for organizing and accessing a persistent data state in the CAVE API structure.

All top-level keys mentioned below are reserved for the use described in their respective docs and should not be used as custom keys as this may break functionality. Additionally the following top-level keys are reserved and should not be used as custom keys:

- `ignore`
- `associated`

A CAVE API structure with top-level custom keys looks as follows:
```py
{
    "settings": {...},
    "categories": {...},
    "appBar": {...},
    "arcs": {...},
    "nodes": {...},
    "geos": {...},
    "map": {...},
    "stats": {...},
    "kpis": {...},
    "kwargs":{...},
    "customTopLevelKey1": {
        "sendToClient": False,
        "customPersistedDataKey1": 10,
        "customPersistedDataKey2": [-1, 3],
        "customPersistedDataKey3": {...},
        # As many persisted data chunks as needed
    },
    "customTopLevelKey2": {...},
    # As many custom top level keys as needed
}
```

It is worth noting that the client will ignore any keys not in the aforementioned sections. If you plan to use additional top-level keys, it is advised that `sendToClient=False` to prevent unnecessary data overhead. Also note: in order to access these for persistent state, you should set `sendToApi=True`.
