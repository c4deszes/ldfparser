import os
import binascii

import ldfparser

if __name__ == "__main__":
	path = os.path.join(os.path.dirname(__file__), "network.ldf")
	ldf = ldfparser.LDF(path)
	print(ldf.baudrate)
	print(ldf.protocol_version)
	print(ldf.language_version)
	#print 