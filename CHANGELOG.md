# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

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
