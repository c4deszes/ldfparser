---
layout: default
title: LDF Parser - Command Line Interface
---

## Commons

### Information

The `info` subcommand will print general information about the LDF, such as language
version, baudrate, node and frame counts. When the `details` option is added it will
print a list of node names, frames, etc. instead of counts.

`ldfparser --ldf <file> info [--details]`

### Exporting to JSON

The `export` subcommand can be used to export the LDF as a JSON file to be used by
other tools. When the `output` option is not specified it will print the contents to `stdout`.

`ldfparser --ldf <file> export [--output <output>]`

---

## Nodes

The `node` subcommand can be used to access information about the LIN nodes in the LDF.

### List of nodes

`ldfparser --ldf <file> node --list`

### Node information per role

These commands print information about LIN nodes.

`ldfparser --ldf <file> node --master`

`ldfparser --ldf <file> node --slave <name>`

---

## Frames

The `frame` subcommand can be used to access information about the LIN frames in the LDF.

### List of frames

`ldfparser --ldf <file> frame --list`

### Frame information

These commands print information about the LIN frames.

`ldfparser --ldf <file> frame --name <name>`

`ldfparser --ldf <file> frame --id <id>`

---

## Signals

The `signal` subcommand can be used to access information about the LIN frames in the LDF.

### List of signals

`ldfparser --ldf <file> signal --list`

### Signal information

`ldfparser --ldf <file> signal --name <name>`
