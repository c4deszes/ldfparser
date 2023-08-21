Frames & Signals
================

One of the powerful features of this library is the ability to encode and decode frame contents
sent on the LIN bus. This could be used to implement a controller similar to Vector Canoe.

Signal parameters
-----------------

Frame information
-----------------

Encoding & decoding frames
--------------------------

Frame encoding let's users pick the signal values and then combine them into a valid LIN frame.

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
without the usage of encoding types.

.. code-block:: python

    from ldfparser import parse_ldf

    ldf = parse_ldf("network.ldf")
    data = ldf.get_unconditional_frame('LSM_Frame1').encode_raw({
        'LeftIntLightsSwitch': 0
    })
