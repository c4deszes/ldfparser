Command-line interface (CLI)
============================

Usage & help
------------

.. code-block:: text

    ldfparser --help

Subcommands
-----------

Information
~~~~~~~~~~~

The `info` subcommand will print general information about the LDF, such as language
version, baudrate, node and frame counts. When the `details` option is added it will
print a list of node names, frames, etc. instead of counts.

.. code-block:: text

    ldfparser --ldf <file> info [--details]`

.. code-block:: text

Exporting to JSON
~~~~~~~~~~~~~~~~~

The `export` subcommand can be used to export the LDF as a JSON file to be used by
other tools. When the `output` option is not specified it will print the contents to `stdout`.

.. code-block:: text

    ldfparser --ldf <file> export [--output <output>]

Node information
~~~~~~~~~~~~~~~~

The `node` subcommand can be used to access information about the LIN nodes in the LDF.

.. code-block:: text

    ldfparser --ldf <file> node --list

These commands print information about LIN nodes.

.. code-block:: text

    ldfparser --ldf <file> node --master

    ldfparser --ldf <file> node --slave <name>

Frame information
~~~~~~~~~~~~~~~~~

The `frame` subcommand can be used to access information about the LIN frames in the LDF.

.. code-block:: text

    ldfparser --ldf <file> frame --list

These commands print information about the LIN frames.

.. code-block:: text

    ldfparser --ldf <file> frame --name <name>

    ldfparser --ldf <file> frame --id <id>

Signal information
~~~~~~~~~~~~~~~~~~

The `signal` subcommand can be used to access information about the LIN signals in the LDF.

.. code-block:: text

    ldfparser --ldf <file> signal --list

.. code-block:: text

    ldfparser --ldf <file> signal --name <name>
