# `timeObject`
`timeObject`s can be used to replace numerical values displayed on the map or used as prop [`values`](#value) in [`arcs`](../all_keys/arcs.md), [`nodes`](#../all_keys/nodes.md) or [`geos`](../all_keys/geos.md). These objects contain a list of values that correspond to a specfic timestep. The user can step through these in order or select a specific timestep from a list. In order to use `timeObject`, a [`timeLength`](../all_keys/settings.md#timeLength) must be specified equal to the length of all `value` lists given. Optionally, [`timeUnits`](../all_keys/settings.md#timeUnits) can be given to display the real world representation of each timestep.

Below is an example of a `timeObject` with a `timeLength` of 5:
```py
{
    "timeObject": True,
    "value": [1, 1, 2, 3, 5],
}
```
- The `timeObject` key being set to `True` is required for all `timeObject`s.
- All `value` lists must have lengths equal to the set [`timeLength`](../all_keys/settings.md#timeLength). If the length is updated it must happen to all `value` lists and the `timeLength` at the same time.
