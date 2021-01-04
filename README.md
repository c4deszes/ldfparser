# LDF Parser

[![Workflow](https://github.com/c4deszes/ldfparser/workflows/CI/badge.svg?branch=master)](https://github.com/c4deszes/ldfparser/actions)
[![PyPI version](https://badge.fury.io/py/ldfparser.svg)](https://pypi.org/project/ldfparser/)
[![PyPI - Python Version](https://img.shields.io/pypi/pyversions/ldfparser.svg)](https://pypi.org/project/ldfparser/)
[![codecov.io](https://codecov.io/github/c4deszes/ldfparser/coverage.svg?branch=master)](https://codecov.io/github/c4deszes/ldfparser?branch=master)
[![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)](https://opensource.org/licenses/MIT)

> This tool is able parse LIN Description Files, retrieve signal names and frames from them, as well as encoding messages using frame definitions and decoding them.

---

## Disclaimer

The tool has been written according the LIN standards 1.3, 2.0, 2.1 and 2.2A, but due to errors in the documentation there's no guarantee that the library will be able to parse your LDF. In such cases if possible first verify the LDF with a commercial tool
such as Vector LDF Explorer or the tool that was used to create the LDF.  If the LDF seems to be correct then open a new issue. I also recommend trying the LDF to JSON conversion mechanism, see if that succeeds.

Since the LDF usually contains sensitive information try to provide either an anonymized version with signals and frames obfuscated or just the relevant segments in an example LDF.

---

## Example

```python
import ldfparser

# Load LDF
ldf = ldfparser.LDF(path = "network.ldf")
frame = ldf.frame('Frame_1')

# Get baudrate from LDF
print(ldf.baudrate)

# Encode signal values into frame
message = frame.raw({"Signal_1": 123, "Signal_2": 0})
print(binascii.hexlify(message))
# >> 0x7B00

# Decode message into dictionary of signal names and values
received = bytearray([0x7B, 0x00])
print(frame.parse(received))
# >> {"Signal_1": 123, "Signal_2": 0}

# Encode signal values through converters
message = frame.data({"MotorRPM": 100, "FanState": "ON"}, ldf.converters)
print(binascii.hexlify(message))
# >> 0xFE01

```

---

## Features

+ Semantic validation of LDF files

+ Retrieve header information (version, baudrate)

+ Retrieve Signal and Frame information

+ Retrieve Signal encoding types and use them to convert values

+ Retrieve Node attributes

+ Command Line Interface

+ Capturing comments

### Currently not supported

+ Scheduling table

+ Diagnostics

---

## Installation

Install via `pip install ldfparser`

---

## Contributors

@c4deszes (Author)

---

## Credits

Inspired by [uCAN-LIN LinUSBConverter](https://github.com/uCAN-LIN/LinUSBConverter), specifically the LDF parsing mechanism via [Lark](https://github.com/lark-parser/lark). Previously the library included most of the lark file, parsing code and examples, since 0.5.0 they've been completely rewritten to better accomodate the different LIN standards.

---

## License

[![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)](https://opensource.org/licenses/MIT)
