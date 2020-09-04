import os
import binascii

import ldfparser

if __name__ == "__main__":
	path = os.path.join(os.path.dirname(__file__), "network.ldf")
	ldf = ldfparser.LDF(path)
	content = ldf.frame('Backlight').data(
		{
			"backlight_level": "50%"
		},
		ldf.converters
	)
	print(binascii.hexlify(content))