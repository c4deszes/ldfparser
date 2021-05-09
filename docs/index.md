---
layout: default
title: LDF Parser Documentation
---

The `ldfparser` library allows extracting information out of LIN descriptor files
that are used to describe automotive networks.

## Project status

The library is in a *pre-release* state, some of the functionalities are effectively
final such as the intermediate output of the parser. Interfaces, functions, variable
names may change any time with the plan being to first deprecate the function in a
release then remove it later.

## Setup

Releases are automatically published to PyPI, so you can install it using pip.

```bash
pip install ldfparser
```

Since the library is still in a pre-release state it's recommended that in
production use cases you pin the version to a minor release in your requirements.txt

## Documentation

[Parsing LDF files](parser.md)

[Using the command line interface](commandline.md)

## License

Distributed under the terms of
[MIT license](https://opensource.org/licenses/MITs),
ldfparser is free to use and modify.
