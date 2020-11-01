import os
import json
import ldfparser

if __name__ == "__main__":
	ldf = ldfparser.parseLDFtoDict(os.path.join(os.path.dirname(__file__), 'lin22.ldf'))
	print(json.dumps(ldf))