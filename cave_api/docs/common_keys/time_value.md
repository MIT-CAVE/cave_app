# `timeValues`
`timeValues`s can be used to update base (non dictionary) values displayed on the map in [`arcs`](../all_keys/arcs.md), [`nodes`](#../all_keys/nodes.md) or [`geos`](../all_keys/geos.md). These objects contain a list of values that correspond to a specfic timestep. The user can step through these in order or select a specific timestep from a list. The object representing the current timestep is merged with the parent containing the `timeValue` key. In order to use `timeValues`, a [`timeLength`](../all_keys/settings.md#timeLength) must be specified equal to the length of all `timeValue` lists given. Optionally, [`timeUnits`](../all_keys/settings.md#timeUnits) can be given to display the real world representation of each timestep.

Below is an example of `timeValues` with a `timeLength` of 3:
```py
"timeValues": {
    0: { "value": 0 },
    1: { "value": 100 },
    2: { "value": 300 },
}
```
- All `timeValue` objects must have integer keys with lengths equal to the set [`timeLength`](../all_keys/settings.md#timeLength). If the length is updated it must happen to all `timeValue` lists and the `timeLength` at the same time.
