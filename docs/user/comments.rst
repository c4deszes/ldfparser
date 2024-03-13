Comments
========

The LIN standard allows C/C++ style comments in the LDF files.

.. code-block:: c

    // Single line comment

    /*
     * Multiline comment
     */

Capturing comments
------------------

In the grammar single and multiline comments are put on an ignore list, meaning lark won't
create tokens for them in the syntax tree. Lark has a feature to invoke a callback function
whenever a comment is encountered, this is used by the parser to capture the comments in a list.

Capturing has to be explicitly enabled during parsing, otherwise the comment list will be empty.

.. note:: Both single and multiline comments are captured in their complete form, meaning that
          leading ``//`` and ``/*`` are included in the captures. The best way therefore to retrieve
          data from comments would be to use a regular expression and go through each match.

          When nesting single and multiline comments, the comment inside will not be a separate
          record. Multiline comments will include newline characters.

.. code-block:: python

    from ldfparser import parse_ldf

    ldf = parse_ldf('network.ldf', capture_comments=True)

    for comment in ldf.comments:
        print(comment)
