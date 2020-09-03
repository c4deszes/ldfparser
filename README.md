# LDF Parser

![Workflow](https://github.com/c4deszes/ldfparser/workflows/CI/badge.svg) [![License](http://img.shields.io/:license-mit-blue.svg?style=flat-square)](http://badges.mit-license.org)

> This tool is able parse LIN Description Files, retrieve signal names and frames from them, as well as encoding messages using frame definitions and decoding them.

---

## Example

```python
import ldfparser

# Load LDF
ldf = ldfparser.LDF(path = "network.ldf")
frame = ldf.frame('Frame_1')

# Encode signal values into frame
message = frame.data({"Signal_1": 123, "Signal_2": 0})
print(binascii.hexlify(message))
# >> 0x7B00

# Decode message into dictionary of signal names and values
received = bytearray([0x7B, 0x00])
print(frame.parse(received))
# >> {"Signal_1": 123, "Signal_2": 0}

```

---

## Installation

Install via `pip install ldfparser`

---

## Credits

Inspired by [uCAN-LIN LinUSBConverter](https://github.com/uCAN-LIN/LinUSBConverter), specifically the LDF parsing mechanism via [Lark](https://github.com/lark-parser/lark)

---

## License

[![License](http://img.shields.io/:license-mit-blue.svg?style=flat-square)](http://badges.mit-license.org)