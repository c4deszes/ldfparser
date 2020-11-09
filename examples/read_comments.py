import os
import json
import ldfparser

if __name__ == "__main__":
	ldf = ldfparser.parseLDF(os.path.join(os.path.dirname(__file__), 'lin22.ldf'), captureComments=True)
	print(ldf.comments)