# LDF Parser

[![Workflow](https://github.com/c4deszes/ldfparser/workflows/CI/badge.svg?branch=master)](https://github.com/c4deszes/ldfparser/actions)
[![Github Pages](https://img.shields.io/static/v1?style=flat&logo=github&label=gh-pages&color=green&message=deployed)](https://c4deszes.github.io/ldfparser/)
[![PyPI version](https://badge.fury.io/py/ldfparser.svg)](https://pypi.org/project/ldfparser/)
[![PyPI - Python Version](https://img.shields.io/pypi/pyversions/ldfparser.svg)](https://pypi.org/project/ldfparser/)
[![codecov.io](https://codecov.io/github/c4deszes/ldfparser/coverage.svg?branch=master)](https://codecov.io/github/c4deszes/ldfparser?branch=master)
[![Total alerts](https://img.shields.io/lgtm/alerts/g/c4deszes/ldfparser.svg?logo=lgtm&logoWidth=18)](https://lgtm.com/projects/g/c4deszes/ldfparser/alerts/)
[![Language grade: Python](https://img.shields.io/lgtm/grade/python/g/c4deszes/ldfparser.svg?logo=lgtm&logoWidth=18)](https://lgtm.com/projects/g/c4deszes/ldfparser/context:python)
![GitHub last commit](https://img.shields.io/github/last-commit/c4deszes/ldfparser)
[![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)](https://opensource.org/licenses/MIT)

> This tool is able parse LIN Description Files, retrieve signal names and frames from them, as well as encoding messages using frame definitions and decoding them.

---

## Disclaimers

The library is still in a pre-release state, therefore features may break between minor versions.
For this reason it's recommended that productive environments pin to the exact version of the
library and do an integration test or review when updating the version. Breaking changes and how to
migrate to the new version will be documented in the
[changelog](https://github.com/c4deszes/ldfparser/blob/master/CHANGELOG.md) and on the
[Github releases page](https://github.com/c4deszes/ldfparser/releases).

The tool has been written according the LIN standards [1.3](docs/external/LIN_1.3.pdf),
[2.0](docs/external/LIN_2.0.pdf), [2.1](docs/external/LIN_2.1.pdf) and [2.2A](docs/external/LIN_2.2A.pdf),
but due to errors in the documentation there's no guarantee that the library will be able to parse your LDF.
In such cases if possible first verify the LDF with a commercial tool such as Vector LDF Explorer or the
tool that was used to create the LDF.  If the LDF seems to be correct then open a new issue.
I also recommend trying the LDF to JSON conversion mechanism, see if that succeeds.

The LIN standard is now known as [ISO 17987](https://www.iso.org/standard/61222.html) which
clears up some of the confusing parts in the 2.2A specification. Since this new standard is not
freely available **this library won't support the modifications present in ISO 17987 actively**.
As of `0.19.0` some parts are supported based on information in the public domain.

The SAE organization has their own variant of the LIN standard, known as
[SAE J2602](https://www.sae.org/standards/content/j2602-1_202110/). As of `0.20.0` some additional
fields are supported, but just like with ISO since the standard is not free it's support is limited
to external contributors and publicly available information.

The LDF usually contains sensitive information, if you need to open an issue related to the parser
then try to provide either an anonymized version with signals and frames obfuscated or just the
relevant segments in an example LDF when opening issues.

---

## Installation

You can install this library from PyPI using pip.

```bash
pip install ldfparser
```

---

## Examples

```python
import ldfparser
import binascii

# Load LDF
ldf = ldfparser.parse_ldf(path = "network.ldf")
frame = ldf.get_unconditional_frame('Frame_1')

# Get baudrate from LDF
print(ldf.get_baudrate())

# Encode signal values into frame
message = frame.encode_raw({"Signal_1": 123, "Signal_2": 0})
print(binascii.hexlify(message))
>>> 0x7B00

# Decode message into dictionary of signal names and values
received = bytearray([0x7B, 0x00])
print(frame.decode(received))
>>> {"Signal_1": 123, "Signal_2": 0}

# Encode signal values through converters
message = frame.encode({"MotorRPM": 100, "FanState": "ON"})
print(binascii.hexlify(message))
>>> 0xFE01
```

More examples can be found in the [examples directory](./examples).

---

## Documentation

Documentation is published to [Github Pages](https://c4deszes.github.io/ldfparser/).

---

## Features

+ Semantic validation of LDF files

+ Retrieve header information (version, baudrate)

+ Retrieve Signal and Frame information

+ Retrieve Signal encoding types and use them to convert values

+ Retrieve Node attributes

+ Retrieve schedule table information

+ Command Line Interface

+ Capturing comments

+ Encode and decode standard diagnostic frames

+ Saving LDF object as an `.ldf` file (experimental)

### Known issues / missing features

+ Certain parsing related errors are unintuitive

+ Checksum calculation for frames

+ Token information is not preserved

---

## Development

Install the library locally by running `pip install -e .[dev]`

[Pytest](https://pytest.org/) is used for testing, to execute all tests run `pytest -m 'not snapshot'`

[Flake8](https://flake8.pycqa.org/en/latest/) is used for linting, run `flake8` to print out all linting errors.

---

## Contributors

[@c4deszes](https://github.com/c4deszes) (Author)

---

## Credits

Inspired by [uCAN-LIN LinUSBConverter](https://github.com/uCAN-LIN/LinUSBConverter), specifically the LDF parsing mechanism via [Lark](https://github.com/lark-parser/lark). Previously the library included most of the lark file, parsing code and examples, since 0.5.0 they've been completely rewritten to better accomodate the different LIN standards.

---

## License

[![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)](https://opensource.org/licenses/MIT)
