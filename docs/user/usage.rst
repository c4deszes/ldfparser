Basic usage
===========

Parsing into objects
--------------------

The library has an object model of the LDF specification, this helps with the field types and it
includes additional methods to use the objects to for example encode/decode frames. See
:py:class:`ldfparser.ldf.LDF` for the attributes accessible after parsing.

.. code-block:: python

    import ldfparser

    ldf = ldfparser.parse_ldf('network.ldf')
    print(ldf.get_baudrate())
    >>> 19200
    for node in ldf.get_slaves():
    print(node.name)
    >>> 'LSM'
    >>> 'RSM'

Parsing into dictionary
-----------------------

The library allows the conversion of LDF into a Python dictionary, the exact field names and
structure can be seen in the source code of :py:class:`ldfparser.grammar.LdfTransformer` or the
:download:`JSON Schema <../../schemas/ldf.json>`.

.. code-block:: python

    import ldfparser

    ldf = ldfparser.parse_ldf_to_dict('network.ldf')

    print(ldf['speed'])
    >>> 19200
    print(ldf['nodes']['slaves'])
    >>> ['LSM', 'RSM']
