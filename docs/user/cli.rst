Command-line interface (CLI)
============================

A command line interface is available after installation of the package, it allows simple operations
to be done without writing a script.

Below are the list of subcommands, or you can use the following command to get help:

.. code-block:: bash

    ldfparser --help

Subcommands
-----------

Information
~~~~~~~~~~~

The `info` subcommand will print general information about the LDF, such as language
version, baudrate, node and frame counts. When the `details` option is added it will
print a list of node names, frames, etc. instead of counts.

.. code-block:: bash

    ldfparser --ldf <file> info [--details]`

Exporting to JSON
~~~~~~~~~~~~~~~~~

The `export` subcommand can be used to export the LDF as a JSON file to be used by
other tools. When the `output` option is not specified it will print the contents to the standard
output.

.. code-block:: bash

    ldfparser --ldf <file> export [--output <output>]

Node information
~~~~~~~~~~~~~~~~

The `node` subcommand can be used to access information about the LIN nodes in the LDF. The default
behavior will list all nodes.

.. code-block:: bash

    ldfparser --ldf <file> node --list

With the ``--master`` and ``--slave`` options it prints information about the specific LIN node.

.. code-block:: bash

    ldfparser --ldf <file> node --master

    ldfparser --ldf <file> node --slave <name>

Frame information
~~~~~~~~~~~~~~~~~

The `frame` subcommand can be used to access information about the LIN frames in the LDF.

.. code-block:: bash

    ldfparser --ldf <file> frame --list

These commands print information about the LIN frames.

.. code-block:: bash

    ldfparser --ldf <file> frame --name <name>

    ldfparser --ldf <file> frame --id <id>

Signal information
~~~~~~~~~~~~~~~~~~

The `signal` subcommand can be used to access information about the LIN signals in the LDF.

.. code-block:: bash

    ldfparser --ldf <file> signal --list

.. code-block:: bash

    ldfparser --ldf <file> signal --name <name>
