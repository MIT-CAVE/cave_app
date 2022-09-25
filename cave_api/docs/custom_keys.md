### Top-level custom keys
In addition to the standard CAVE top-level keys described in this document, designers can add custom top-level keys that allow them to persist data that is computed as a result of a user-side action. This emulates (on the back-end side) a pattern widely used in front-end development, called [state management](#https://en.wikipedia.org/wiki/State_management).

A fairly common use case for this approach is to persist data that may need to be invisible to users based on other user selections. For example, an app that has options that toggle other options might want to store any choices users have made when those options are not currently presented to the user. While designers could explore other solutions for data persistence, we believe that top-level custom keys provide an easy escape hatch for organizing and accessing a persistent data state in the CAVE API structure.

All top-level keys mentioned above are reserved for the use described above and should not be used as custom keys as this may break functionality. Additionally the following top-level keys are reserved and should not be used as custom keys:

- `ignore`
- `associated`

A CAVE API structure with top-level custom keys looks as follows:
```py
{
    'settings': {...},
    'categories': {...},
    'appBar': {...},
    'arcs': {...},
    'nodes': {...},
    'geos': {...},
    'map': {...},
    'stats': {...},
    'kpis': {...},
    'kwargs':{...},
    'custom_top_level_key_1': {
        'send_to_client': False,
        'custom_persisted_data_key_1': 10,
        'custom_persisted_data_key_2': [-1, 3],
        'custom_persisted_data_key_3': {...},
        # As many persisted data chunks as needed
    },
    'custom_top_level_key_2': {...},
    # As many custom top level keys as needed
}
```

It is worth noting that the client will ignore any keys not in the aforementioned sections. If you plan to use additional top-level keys, it is advised that `send_to_client=False` to prevent unnecessary data overhead. Also note: in order to access these for persistent state, you should set `send_to_api=True`.