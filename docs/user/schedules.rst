Schedules
=========

Schedules describe which frames the LIN master requests from nodes and how frequently they're
requested.

Schedule information
--------------------

The schedules can be accessed by name, the entries in the schedule can be iterated through.

The delay is stored as a floating point number in seconds.

The nodes, frames referenced in schedule entries are linked to objects in the LDF.

.. code-block:: python

    from ldfparser import parse_ldf

    ldf = parse_ldf('network.ldf')
    schedule = ldf.get_schedule_table('NormalSchedule')
    print(schedule.name)
    >>> 'NormalSchedule'
    for entry in configuration_schedule.schedule:
        print(f"{type(entry).__name__} - {entry.delay * 1000} ms")
    >>> 'AssignNadEntry - 15 ms'
    >>> 'AssignFrameIdRangeEntry - 15 ms'
    >>> 'AssignFrameIdEntry - 15 ms'
    >>> 'AssignFrameIdEntry - 15 ms'
    >>> 'AssignFrameIdEntry - 15 ms'
