JSON Export
===========

The parser creates an intermediate dictionary during parsing which can be exported as JSON.

The feature could be used to bring LDF parsing support to other languages, in some cases the
Python runtime could be included in different tool.

Script
------

.. code-block:: python

    from ldfparser import parse_ldf_to_dict
    import json

    with open('export.json', 'w+') as output:
        ldf = parse_ldf_to_dict('network.ldf')
        json.dump(ldf, output, indent=4)

Command-line
------------

The entrypoint registered by ldfparser includes a :ref:`subcommand <user/cli:Exporting to JSON>`
that can do this conversion.
