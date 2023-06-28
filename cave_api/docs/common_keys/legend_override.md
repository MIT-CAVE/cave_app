# `legendOverride`
The `legendOverride` key is used to define how a `num` prop is displayed in the legend, such as in scientific notation, based on [`numberFormat`](number_format.md) or with fixed values.

The `legendOverride` structure with all its keys looks as follows:
```py
"legendOverride": {
    "useScientificFormat": False,
    "scientificPrecision": 5,
    "minLabel": "Lo",
    "maxLabel": "Hi",
}
```

## Nested inside the `numberFormat` group
Key | Default | Description
--- | ------- | -----------
<a name="useScientificFormat">`useScientificFormat`</a> | `True` | If `False`, the value will be formatted with [`numberFormat`](number_format.md)
<a name="scientificPrecision">`scientificPrecision`</a> | `3` | The number of digits to use. Only used if `useScientificFormat` is `True`
<a name="minLabel">`minLabel`</a> | | A string to set as the minimum label. Takes precedence over other formatting.
<a name="maxLabel">`maxLabel`</a> | | A string to set as the maximum label. Takes precedence over other formatting.
