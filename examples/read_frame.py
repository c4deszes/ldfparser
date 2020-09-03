import ldfparser
import binascii

if __name__ == "__main__":
	ldf = ldfparser.LDF("network.ldf")
	message = bytearray([0xFA, 0xA0])
	content = ldf.frame('Buttons_Status').parse(message)
	print(content)