Diagnostics
===========

Diagnostic data availability is subject to the diagnostic signals and frames described in the parsed
LDF.

The standard specifies two frames reserved for standard diagnostic operations, the master request
frame (0x3C) and the slave response frame (0x3D). These have custom objects associated with them
that allows the user to encode and decode them according to the services described in the standard.

Encoding master requests
------------------------

.. code-block:: python

    ldf = parse_ldf('network.ldf')

    ldf.master_request_frame...

Decoding slave responses
------------------------

.. code-block:: python
