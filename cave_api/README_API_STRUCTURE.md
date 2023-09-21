# CAVE API Design
This document describes the data structure scheme used by a CAVE application to render custom user interfaces that accommodate to the use cases and preferences of an API designer. For the purposes of this documentation, an API designer is any person using the CAVE API code to create a CAVE App user experience.

## CAVE API Structure
The CAVE API Structure is the core data structure required for user interface design of the CAVE App. Its primary purpose is to place, rearrange, style, and specify the behavior of most of the UI elements in a CAVE application.

At first glance, the top-level keys in the data structure look like this:
```py
{
    'appBar': {...},
    'arcs': {...},
    'categories': {...},
    'pages': {...},
    'geos': {...},
    'kpis': {...},
    'kwargs':{...},
    'maps': {...},
    'modals': {...},
    'nodes': {...},
    'panes': {...},
    'settings': {...},
    'stats': {...}
}
```
Throughout this documentation, we refer to the keys in the data structure above as _top-level keys_ (or _top-level groups_ to point out that these keys contain other key-value pairs).

Each top-level group might include unique elements or sub-keys that are specific to that group (**special keys**). However, other keys like `sendToApi` are meant to attach functionality that is more generic and therefore can be used in different top-level groups. To save time and [not repeat ourselves](https://en.wikipedia.org/wiki/Don%27t_repeat_yourself) throughout this documentation, we provide a "[Common keys](#common-keys)" section, and any such keys found in the documentation are referred back to their definition.

There is a third type of keys (**custom keys**), which depend on the data and, therefore, their names vary according to the use case. The API designer can name these keys in the data structure at their convenience. Let's take a look at the following example where custom keys are used:
```py
{
    'categories': {
        'data':{
            'customLocation': {
                'data': {
                    'customLocUsMi': {
                        'customRegion': 'North America',
                        'customCountry': 'USA',
                        'customState': 'Michigan'
                    },
                    'customLocUsMa': {
                        'customRegion': 'North America',
                        'customCountry': 'USA',
                        'customState': 'Massachusetts'
                    },
                ...
                },
            }
        }
    }
}
```

Here, `customLocation`, `customLocUsMi`, `customLocUsMa`, `customRegion`, `customCountry`, and `customState` are all custom keys. These key names are not restricted and can be tied to the problem or use case data. These also do not need to be preceded by `custom_`, but this tag is used to indicate that they are custom keys for example purposes. (Throughout these docs, if not explicitly mentioned, all custom keys are preceded by the `custom` tag whenever they are found in an example.)

Custom keys are always included as a direct child of common keys such as `data`, `props`, `types`, and `category`, but they also appear as a direct child of less frequent keys such as `nestedStructure`, or even within another custom key, as shown in the structure above.

### [Common keys](docs/common_keys/common_keys.md)

- #### [`layout`](docs/common_keys/layout.md)

- #### [`props`](docs/common_keys/props.md)

- #### [`timeValues`](docs/common_keys/time_value.md)


### [Top-Level keys](docs/all_keys/top_level_keys.md)

- #### [`appBar`](docs/all_keys/app_bar.md)

- #### [`arcs`](docs/all_keys/arcs.md)

- #### [`categories`](docs/all_keys/categories.md)

- #### [`pages`](docs/all_keys/pages.md)

- #### [`geos`](docs/all_keys/geos.md)

- #### [`kpis`](docs/all_keys/kpis.md)

- #### [`kwargs`](docs/all_keys/kwargs.md)

- #### [`maps`](docs/all_keys/maps.md)

- #### [`modals`](docs/all_keys/modals.md)

- #### [`nodes`](docs/all_keys/nodes.md)

- #### [`panes`](docs/all_keys/panes.md)

- #### [`settings`](docs/all_keys/settings.md)

- #### [`stats`](docs/all_keys/stats.md)


### [Top-level custom keys](docs/custom_keys.md)
