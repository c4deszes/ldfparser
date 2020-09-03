import ldfparser
import binascii

if __name__ == "__main__":
	ldf = ldfparser.LDF("network.ldf")
	content = ldf.frame('Backlight').data(
		{
			"backlight_level": 10
		}
	)
	print(binascii.hexlify(content))