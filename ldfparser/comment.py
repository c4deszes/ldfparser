import os
from typing import List

from lark import Lark, Transformer

def parseComments(content: str) -> List[str]:
	comment = os.path.join(os.path.dirname(__file__), 'comment.lark')
	parser = Lark(grammar=open(comment), parser='lalr')
	tree = parser.parse(content)
	return CommentCollector().transform(tree)

class CommentCollector(Transformer):
	def start(self, tree):
		return tree[0:]

	def comment(self, tree):
		return tree[0]

	def line_comment(self, tree):
		return tree[0][0:]

	def block_comment(self, tree):
		return tree[0][0:]