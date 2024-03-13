Parser
======

The parsing is done is 3 larger steps:

#. First the LDF file is passed through the lark parser library
#. The returned syntax tree is then traversed and is transformed into a dictionary
#. Lastly the dictionary is converted into Python objects

Grammar
-------

In this phase a grammar description is used to validate that the syntax of the read LDF is correct.
At the same time the parser creates a syntax tree under which the values of all the fields will be
available.

The grammar is created in a way to support all LIN standards, including the newer ones at ISO and
SAE. The advantage is that we don't need an additional phase or input to determine the LIN version
and it also cuts down on maintenance.

Tree transform
--------------

The returned syntax tree would be difficult to interpret on it's own, luckily lark provides
a transformer class that can be used to extract the named fields inside the grammar, this makes
it's nested nature easier to handle.

The output of the transformer in this case is a Python dictionary which maps field names like
the language version to the provided version value.

The transformer just like the grammar is LIN standard agnostic, so even at this point we don't
know if the LDF is semantically correct.

Conversion
----------

The keys in the dictionary are converted into Python objects. During this process values are
validated, including references.
