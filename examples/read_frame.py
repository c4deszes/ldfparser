import os
import binascii

import ldfparser

if __name__ == "__main__":
	path = os.path.join(os.path.dirname(__file__), "network.ldf")
	ldf = ldfparser.LDF(path)
	message = bytearray([0xFA, 0xA0])
	content = ldf.frame('Buttons_Status').parse(message)
	print(content)