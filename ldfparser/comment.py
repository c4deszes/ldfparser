"""
Utilities for parsing comments from Lark files
"""
import os
import warnings
from typing import List
from lark import Lark, Transformer

def parse_comments(content: str) -> List[str]:
    """Parses comments in LDF files

    :param content: LDF file content as string
    :type content: str
    :returns: a list of all comments in the LDF file
    :rtype: List[str]
    """
    comment = os.path.join(os.path.dirname(__file__), 'lark', 'comment.lark')
    parser = Lark(grammar=open(comment), parser='lalr')
    tree = parser.parse(content)
    return CommentCollector().transform(tree)

def parseComments(content: str) -> List[str]:
    # pylint: disable=invalid-name
    """Deprecated, use `parse_comments` instead

    This method will be removed in 1.0.0
    """
    warnings.warn("'parseComments' is deprecated, use 'parse_comments' instead", DeprecationWarning)
    return parse_comments(content)

class CommentCollector(Transformer):
    # pylint: disable=C0116,R0201
    """
    Transforms grammar tree into dictionary containing the comments
    """

    def start(self, tree):
        return tree[0:]

    def comment(self, tree):
        return tree[0]

    def line_comment(self, tree):
        return tree[0][0:]

    def block_comment(self, tree):
        return tree[0][0:]
