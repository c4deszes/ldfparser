Frames & Signals
================

One of the powerful features of this library is the ability to encode and decode frame contents
sent on the LIN bus. This could be used to implement a controller similar to what Vector Canoe
can do with the right hardware.

Signal parameters
-----------------

Signals are loaded and linked to their owners, the standard includes array signals ranging from
1 to 8 bytes in length both in the source LDF and the parsed object these signals are distinguished
by their initial values.

.. code-block:: python

    from ldfparser import parse_ldf

    ldf = parse_ldf("network.ldf")
    signal = ldf.get_signal('LeftIntLightsSwitch')
    print(signal.width)
    >>> 2
    print(signal.init_value)
    >>> 0

Frame information
-----------------

Frames are loaded under different types:

* Unconditional frames
* Event triggered frames
* Sporadic frames
* Diagnostic frames

Most use cases revolve around unconditional frames, they can be encoded, decoded given signal
values.

.. code-block:: python

    from ldfparser import parse_ldf

    ldf = parse_ldf("network.ldf")
    frame = ldf.get_unconditional_frame('LeftIntLightsSwitch')
    print(frame.frame_id)
    >>> 23

Encoding & decoding frames
--------------------------

Frame encoding let's users pick the signal values and then combine them into a valid LIN frame.

When a signal is missing from the dictionary it will be set to it's initial value.

.. code-block:: python

    from ldfparser import parse_ldf

    ldf = parse_ldf("network.ldf")
    data = ldf.get_unconditional_frame('LSM_Frame1').encode({
        'LeftIntLightsSwitch': 'Off'
    })

.. note:: The passed signal values are first encoded through their encoding types in the following order:

    #. Custom encoding type passed to the function
    #. Encoding types associated with the signal
    #. Signals with no encoding types but passed as integer values will be encoded raw

Encoding raw Signals
~~~~~~~~~~~~~~~~~~~~

The :py:meth:`ldfparser.frame.LinUnconditionalFrame.encode_raw` allows the same operation but
without the usage of encoding types, the values need to be integers in the range of their signal's
width.

.. code-block:: python

    from ldfparser import parse_ldf

    ldf = parse_ldf("network.ldf")
    data = ldf.get_unconditional_frame('LSM_Frame1').encode_raw({
        'LeftIntLightsSwitch': 0
    })
