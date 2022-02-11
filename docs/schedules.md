---
layout: default
title: LDF Parser - Schedules
---

## Accessing schedules

### Retrieving schedule information

After parsing the LDF into objects the schedule tables defined in the LDF will
be accessible.

```python
ldf = parse_ldf('network.ldf')

configuration_schedule = ldf.get_schedule_table('Configuration_Schedule')
print(configuration_schedule.name)
>>> 'Configuration_Schedule'
for entry in configuration_schedule.schedule:
    print(f"{type(entry).__name__} - {entry.delay * 1000} ms")
>>> 'AssignNadEntry - 15 ms'
>>> 'AssignFrameIdRangeEntry - 15 ms'
>>> 'AssignFrameIdEntry - 15 ms'
>>> 'AssignFrameIdEntry - 15 ms'
>>> 'AssignFrameIdEntry - 15 ms'
```

The objects referenced in the table entries are also linked.

```python
print(configuration_schedule.schedule[0].node.name)
>>> 'LSM'
```
