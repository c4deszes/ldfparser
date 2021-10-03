---
layout: default
title: LDF Parser - Signals
---

## Using signals

### Retrieving signal information

After parsing the LDF into objects the properties of signals defined in the LDF
will be accessible.

```python
ldf = parseLDF('network.ldf')

light_switch_signal = ldf.get_signal('LeftIntLightsSwitch')
print(light_switch_signal.name)
>>> 'LeftIntLightsSwitch'
print(light_switch_signal.width)
>>> 8
print(light_switch_signal.init_value)
>>> 0
```
