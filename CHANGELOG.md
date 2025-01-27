# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

## [0.26.0] - 2025-01-27

### Changed

- Empty signal encoders are now allowed
- Signals can now be associated with multiple frames, accessible under `signal.frames`
- Physical values are now rounded to the nearest integer, rather than down

### Migration guide for 0.26.0

- Newly written should be using `signal.frames` to determine the owners of a signal, for
  compatibility reasons `signal.frame` is still set, but only when a signal is associated with one
  frame
- Physical values might be rounded the wrong way depending on the user's intention. This type of
rounding should generally work better in values ranging from `0-X`, for example `49.9` is no longer
rounded down to `49`. If this is undesired the user can in most cases offset the input by `0.5` and
it should work as previously as `-0.5` rounds to `0`, check
[Python's round function](https://docs.python.org/3/library/functions.html#round) for more.

## [0.25.0] - 2024-04-28

### Changed

- Signals overlapping error message now includes relevant information

## [0.24.0] - 2024-02-22

### Changed

- scientific/engineeering notation values can now have upper case E

## [0.23.0] - 2024-02-05

### Changed

- Padding in a frame can now be changed from zeros to padding with ones

## [0.22.0] - 2024-01-30

### Added

- Support for J2602 slave node attributes:
  - `wakeup_time`, `poweron_time`

## [0.21.0] - 2023-09-13

### Fixes

- Add support for encode/decode frame with byte array signals

## [0.20.0] - 2023-06-12

### Added

- Support for SAE J2602 legacy version
- Grammar support for the following J2602 fields:
  - `max_header_length`, `response_tolerance` for the master node
  - `response_tolerance` for slave node attributes

## [0.19.0] - 2023-03-12

### Added

- ISO17987 version support
- Grammar support for the following ISO17987 fields:
  - `LDF_file_revision`
  - Endianness

### Changed

- `LDF::get_frame` can now return diagnostic frames

### Fixes

- `LinSlave` protocol version property is now the correct type
- `LinUnconditionalFrame::decode` no longer calls the deprecated `parse_raw` function

## [0.18.0] - 2022-12-13

### Changed

- Remove `tests` folder from python package
- Close all files which are opened by the ldfparser

## [0.17.0] - 2022-10-17

### Added

- Diagnostic addresses section in LIN 1.3 description files are now parsed correctly,
  the `initial_nad` and `configured_nad` attributes will be set according to the address

## [0.16.0] - 2022-10-02

### Added

- Sporadic frames are parsed into Python objects

### Changed

- Path to the grammar and LDF template are now resolved absolute to allow using them in `pyinstaller`
- `LDF::get_frame` can also return sporadic frames

### Fixed

- The loaded diagnostic frames' lengths are now correctly set

## [0.15.0] - 2022-08-20

### Added

- BCD values are now checked when decoding physical values

### Changes

- Master and slaves declarations are now optional
- Channel name can now be any string, including an empty string instead of requiring a valid C
  identifier.

## [0.14.0] - 2022-02-26

### Added

- `LDF` objects can now be saved as `.ldf` files (experimental)
- Encoding types now have references to the Signals it represents
- `LDF` object now has functions to lookup encoding types
- `LinSignal` now reference the `LinUnconditionalFrame` they're in

### Changed

- Bumped `lark-parser` dependency to first major version, see
[Lark release notes](https://github.com/lark-parser/lark/releases/tag/1.0.0)
- `LdfTransformer` has been moved to a separate module

### Migration guide for 0.14.0

- The breaking change in `lark` that impacts `ldfparser` is the change in the dependency's name.
Since the module name is still `lark` it causes two dependencies to refer to the same package
files. If you now install `lark` or `ldfparser==0.14.0` and then you uninstall `lark-parser`
you will have to reinstall the `lark` dependency.

## [0.13.1] - 2022-02-12

### Fixed

- `P2_min`, `ST_min` and `N_As` and `N_Cr` timeout default values are now set correctly

## [0.13.0] - 2022-02-05

### Added

- Schedule tables are now parsed into Python objects

### Changed

- The delay of schedule entries in the dictionary now have a floating point type and their unit
has been normalized to seconds

### Fixed

- Added missing `UnassignFrameId` command to JSON schema

### Migration guide for 0.13.0

- Any reference to `ldf['schedule_tables'][id]['schedule'][entry]['delay']` that assumes that
milliseconds are used as the unit has to be updated to either multiply the current value by `1000`
or somehow change the assumption about the unit to seconds.
All numeric values that have an associated unit have their SI prefix removed during parsing, for
example `kbps` is converted into `bps`. The schedule entry delay was one case where it wasn't
handled accordingly.

## [0.12.0] - 2021-11-21

### Added

- Diagnostic frames and signals are now parsed
- Standard diagnostic commands can be encoded and decoded

### Changed

- `LinUnconditionalFrame` can be encoded using a `List` of signal values
- Comment capturing has been reworked to use the Lexer callback feature of the Lark parser

## [0.11.1] - 2021-11-02

### Added

- Scientific notation is now allowed when providing floating point values

## [0.11.0] - 2021-10-17

### Added

- Units of Physical values can now be preserved when decoding frames
- `LinSignal` now has a reference to it's signal representation
- New encoding and decoding functions have been added, these allow conversions without passing
`ldf.converters`, instead it will try to use the default encoders but still allow users to override
the encoding type locally.

### Fixed

- The new encoding allows frames to be encoded/decoded even when encoding types are missing (issue #72 )

### Deprecated

- `LinUnconditionalFrame`'s `parse`, `parse_raw`, `data` and `raw` functions were deprecated in
favor of the new encoding functions

## [0.10.0] - 2021-10-02

### Added

- `LinVersion` class was added that allows better version handling than the previous floating point
values
- Event Triggered Frames are now parsed correctly and stored in `LinEventTriggeredFrame` objects
- Pylint has been introduced into the CI pipeline

### Changed

- Tabs have been replaced with spaces in order to conform with [PEP8](https://www.python.org/dev/peps/pep-0008/)
- Frame, Signal and LDF classes were moved into their on modules
- Unconditional frame handling has been moved from `LinFrame` class into `LinUnconditionalFrame`
- Language and protocol version is now parsed as strings, see migration guide for more information
- LDF class has been completely replaced, see migration guide on how to update

### Fixed

- Fixed configurable frames being resolved with `None` when event triggered frames were referenced

### Deprecated

- `parseLDF`, `parseLDFtoDict`, `parseComments` were deprecated in favor of the same methods with a
snake case signature

- `LDF::frame(x)`, `LDF::signal(x)`, `LDF::slave(x)` were deprecated, they were replaced with proper
getters but those contracts are slightly different

It's recommended to replace the deprecated functions as they will be removed in `1.0.0`, most of
them have drop in replacements.

### Migration guide for 0.10.0

#### Imports and classes

- A few modules were reorganized, this might cause certain `import` statements to be broken, imports
that only use the `ldfparser` package are backwards compatible

- Previously `LinFrame` represented unconditional frames and was used to encode and decode frames,
this was changed in order to support the other frame types later. `LinFrame` now only contains
the most basic properties, name and identifier, while the rest has been transferred out into
`LinUnconditionalFrame` and `LinEventTriggeredFrame`. This change should only affect scripts that
directly reference the `LinFrame` class, when using queries through the `LDF` objects the behavior
is identical.

#### Dictionary object

- `protocol_version` and `language_version` were changed to be of string type, the previous floating
point values were good for comparing versions but it's overall problematic due to precision issues,
if you still need floating point values then you must convert them in your scripts

#### LDF object

- Previously the LDF class contained only a few methods that allowed searching in the collections,
but everything else had to be accessed through the member fields. This is changed in `0.10.0` in
order to allow a better deprecation process in the future.
  - All fields have been prefixed with `_` to mark them as internal, they should not be accessed
  directly
  - Getters were added, they are direct replacements of the old member fields, e.g.: `ldf.signals`
  was replaced with `ldf.get_signals()`
  - Lookup methods in the LDF are now more performant because they don't rely on linear search, however
  the behavior was changed, instead of returning `None` the new methods will raise a `LookupError`
  - Properties are used to keep compatibility with older versions where these fields are referenced,
  in the future there may be warnings enabled and possibly removed in later releases

#### Parsing

- Replace `ldf.parseLDF(x)` with `ldf.parse_ldf(x)`, signatures are slightly different but functionally identical
- Replace `ldf.parseLDFtoDict(x)` with `ldf.parse_ldf_to_dict(x)`

## [0.9.1] - 2021-09-11

### Added

- Missing node attributes: Response Error, Fault State Signals and Configurable frames are now
linked to the `LinSlave` object ( #66 )

## [0.9.0] - 2021-07-31

### Fixed

- Fixed ASCII and BCD encoding types missing from the syntax ( #56 )
- Fixed `subscribed_to` variable on `LinSlave` containing the wrong objects ( #59 )
- Fixed whitespace not being allowed in the `Nodes` section before the colons ( #61 )
- Fixed parsing initial values of array type signals ( #62 )

## [0.8.0] - 2021-06-01

## Added

- Standard JSON schema for parsed LDFs

### Fixed

- Missing encoders causing `KeyError` instead of `ValueError`

## [0.7.1] - 2021-04-21

### Fixed

- Frame encoder incorrectly encoding zero valued signals into their initial values ( #40 )

## [0.7.0] - 2021-01-04

### Added

- CLI interface for basic LDF tasks (#33), entrypoint is added, documentation available in
the docs folder
- Frames are now linked to the publishing node

### Changed

- Variant value now defaults to 0 instead of None

### Fixed

- Signals incorrectly being appended to the published frame list

## [0.6.0] - 2020-11-28

### Added

- Signal and LIN node objects are now linked when subscribers and publishers are specified
- The following node attributes are now parsed into the LDF objects
  - P2_min
  - ST_min
  - N_As_timeout
  - N_Cr_timeout
- UnassignFrameId command which is in LIN 2.0 spec
- Schedule table commands are now parsed

### Changed

- Signals with no subscribers are now allowed, while this is not to spec. OEMs use it ( @kayoub5 )
- Node attributes section can now be empty ( @kayoub5 )
- AssignFrameIdRange now accepts either 0 or 4 PID values

## [0.5.2] - 2020-11-13

### Added

- Allows specifying the file encoding when parsing LDF files ( #19 )

### Fixed

- AssignFrameIdRange command syntax in schedule tables ( #18 )

### Reworked

- Updated comment syntax to the one used in lark commons ( #17 ) this requires lark-parser >= 0.10.0

## [0.5.1] - 2020-11-09

### Added

- Support for parsing comments in LDF

### Fixed

- Empty block comments not being allowed

## [0.5.0] - 2020-11-03

### Added

- Support for reading node attributes
- Support for array type signals
- Support for BCD and ASCII values
- Factory method for parsing LDF files, this breaks scripts still using 0.4.1 and below
- Method for converting LDF into dictionary

### Changed

- Reworked Lark parser to better support different LDF versions, 1.3 to 2.2 should be supported

## [0.4.1] - 2020-10-15

### Fixed

- Multiple slaves not being allowed in the LDF, specified in the LIN standard

## [0.4.0] - 2020-10-06

### Added

- Support for different comment syntaxes

## [0.3.2] - 2020-09-28

### Fixed

- Signal encoding/decoding using MSB instead of LSB order specified in the LIN 2.1 standard

## [0.3.1] - 2020-09-07

### Fixed

- Negative values are now supported in physical value's scale and offset fields

## [0.3.0] - 2020-09-06

### Added

- Support for reading LDF metainformation (version, baudrate)

## [0.2.0] - 2020-09-05

### Added

- Signal encoding support

## [0.1.0] - 2020-09-03

### Added

- Initial LDF Parser package
- Frame encoding and decoding support
