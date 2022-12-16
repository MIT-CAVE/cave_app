# `numberFormat`
The `numberFormat` key is used to define a custom format for numeric values based on attributes such as: the specific [locale](https://en.wikipedia.org/wiki/Locale_(computer_software)), the nature of the accompanying unit (if present), the number of decimal places, and the handling of trailing zeros. Additionally, it allows you to configure auto-formatting behavior when in a [numeric input field](props.md#num).

A `numberFormat` specification can be added to the top level [`settings`](../all_keys/settings.md) to affect the displaying format of all the numeric data in the CAVE app. Also, it is possible to override its attributes by adding more `numberFormat` definitions at specific places within the CAVE API structure. Allowed locations for `numberFormat` are the [`settings.data`](../all_keys/settings.md) group, within a [`'num'` prop](props.md#num), within a [stat](../all_keys/stats.md) element or within a [KPI](../all_keys/kpis.md) element.

The `numberFormat` structure with all its keys looks as follows:
```py
"numberFormat": {
    "precision": 2,
    "unit": "%",
    "unitSpace": False,
    "currency": False,
    "trailingZeros": True,
    "nilValue": "N/A",
    "locale": "en-US",
}
```

## Nested inside the `numberFormat` group
Key | Default | Description
--- | ------- | -----------
<a name="currency">`currency`</a> | `False` | If `True`, the specified unit is treated as a currency and placed before the number. Additionally, if the [`unitSpace`](#unit-space) key is not specified, there will be no space between the unit and the number when `currency` is `True`, or a space will be placed otherwise.
<a name="precision">`precision`</a> | `2` | The number of fraction digits to use. Possible values are `0` to `20`. By setting the `precision` to `0`, you can attach an integer constraint on the element.
<a name="unit">`unit`</a> | | A unit of measurement displayed according to the unit formatting. (See [`unitSpace`](#unit-space) and [`currency`](#currency).) When used along a [`'num'` prop](props.md#num), the unit is rendered as an [adornment](https://mui.com/material-ui/react-text-field/#input-adornments) at the beginning or end of the input field.
<a name="unit-space">`unitSpace`</a> | | If `True`, a space will be placed between the unit and the number. If this key is not specified, the unit space will be determined by [`currency`](#currency).
<a name="trailing-zeros">`trailingZeros`</a> | `True` | If `True`, trailing zeros are displayed based on the [`precision`](#precision) value.
<a name="locale">`locale`</a> | `'en-US'` | A [locale identifier](https://en.wikipedia.org/wiki/IETF_language_tag).
<a name="nil-value">`nilValue`</a> | `'N/A'` | A default output for undefined or invalid values.
