ldfparser
=========

.. toctree::
    :hidden:

    user/index
    dev/index
    api/index
    contributions

The `ldfparser` library allows extracting information out of LIN descriptor files
that are used to describe automotive networks.

Installation
------------

Releases are automatically published to PyPI, so you can install it using pip.

.. code-block:: bash

    pip install ldfparser

Project status
--------------

The library is in a *pre-release* state, some of the functionalities are effectively
final such as the intermediate output of the parser. Interfaces, functions, variable
names may change any time with the plan being to first deprecate the function in a
release then remove it later.

In productive systems always pin the library version to a known working release.

License
-------

Distributed under the terms of `MIT license <https://opensource.org/licenses/MITs>`_,
ldfparser is free to use and modify.
