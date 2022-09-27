# CAVE API Design
This document describes the data structure scheme used by a CAVE application to render custom user interfaces that accommodate to the use cases and preferences of an API designer. For the purposes of this documentation, an API designer is any person using the CAVE API code to create a CAVE App user experience.

## CAVE API Structure
The CAVE API Structure is the core data structure required for user interface design of the CAVE App. Its primary purpose is to place, rearrange, style, and specify the behavior of most of the UI elements in a CAVE application.

At first glance, the top-level keys in the data structure look like this:
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
    'kwargs':{...}
}
```
Throughout this documentation, we refer to the keys in the data structure above as _top-level keys_ (or _top-level groups_ to point out that these keys contain other key-value pairs).

Each top-level group might include unique elements or sub-keys that are specific to that group ([special keys](#special-keys)). However, other keys like `send_to_api` are meant to attach functionality that is more generic and therefore can be used in different top-level groups. To save time and [not repeat ourselves](https://en.wikipedia.org/wiki/Don%27t_repeat_yourself) throughout this documentation, we provide a "[Common keys](#common-keys)" section, and any such keys found in the documentation are referred back to their definition.

There is a third type of keys ([custom keys](#custom-keys)), which depend on the data and, therefore, their names vary according to the use case. The API designer can name these keys in the data structure at their convenience. Let's take a look at the following example where custom keys are used:
```py
{
    'categories': {
        'data':{
            'custom_location': {
                'data': {
                    'custom_loc_us_mi': {
                        'custom_region': 'North America',
                        'custom_country': 'USA',
                        'custom_state': 'Michigan'
                    },
                    'custom_loc_us_ma': {
                        'custom_region': 'North America',
                        'custom_country': 'USA',
                        'custom_state': 'Massachusetts'
                    },
                ...
                },
            }
        }
    }
}
```

Here, `custom_location`, `custom_loc_us_mi`, `custom_loc_us_ma`, `custom_region`, `custom_country`, and `custom_state` are all custom keys. These key names are not restricted and can be tied to the problem or use case data. These also do not need to be preceded by `custom_`, but this tag is used to indicate that they are custom keys for example purposes. (Throughout these docs, if not explicitly mentioned, all custom keys are preceded by the `custom_` tag whenever they are found in an example.)

Custom keys are always included as a direct child of common keys such as `data`, `props`, `types`, and `category`, but they also appear as a direct child of less frequent keys such as `nestedStructure`, or even within another custom key, as shown in the structure above.

### [Common keys](docs/common_keys/common_keys.md)

- #### [`props`](docs/common_keys/props.md)

- #### [`layout`](docs/common_keys/layout.md)

- #### [`numberFormat`](docs/common_keys/numberFormat.md)

- #### [`timeObject`](docs/common_keys/timeObject.md)


### [Top-Level keys](docs/all_keys/top_level_keys.md)

- #### [`settings`](docs/all_keys/settings.md)

- #### [`categories`](docs/all_keys/categories.md)

- #### [`appBar`](docs/all_keys/app_bar.md)

- #### [`arcs`](docs/all_keys/arcs.md)

- #### [`nodes`](docs/all_keys/nodes.md)

- #### [`geos`](docs/all_keys/geos.md)

- #### [`map`](docs/all_keys/map.md)

- #### [`stats`](docs/all_keys/stats.md)

- #### [`kpis`](docs/all_keys/kpis.md)

- #### [`kwargs`](docs/all_keys/kwargs.md)


### [Top-level custom keys](docs/custom_keys.md)
