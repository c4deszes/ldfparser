Comments
========

The LIN standard allows C/C++ style comments in the LDF files.

Capturing comments
------------------

In the grammar single and multiline comments are put on an ignore list, meaning lark won't
create tokens for them in the syntax tree. Lark has a feature to invoke a callback function
whenever a comment is encountered, this is used by the parser to capture the comments in a list.

Capturing has to be explicitly enabled during parsing, otherwise the comment list will be empty.

.. code-block:: python

    from ldfparser import parse_ldf

    ldf = parse_ldf('network.ldf', capture_comments=True)

    for comment in ldf.comments:
        print(comment)
