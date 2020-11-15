import os
import json
import ldfparser

if __name__ == "__main__":
	path = os.path.join(os.path.dirname(__file__), 'lin22.ldf')
	ldf = ldfparser.parseLDFtoDict(path)
	print(json.dumps(ldf))
