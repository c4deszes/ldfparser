---
layout: page
title: LDF Parser Documentation
---

## About the parser

### Process

The complete parsing procedure has 3 phases.

1. The LDF is passed through lark-parser where it's converted into a syntax tree.

2. The tree is transformed into a Python dictionary.

3. The dictionary is converted into Python objects.

---

## Using the parser

### Parsing into dictionary

The library allows the conversion of LDF into a Python dictionary.
The dictionary's layout can be interpreted through the LDFTransformer class or
by exporting an LDF into JSON format. The field names and structure try
to be very similar to the ones in the LDF specification.

```python
ldf = parseLDFtoDict('network.ldf')

print(ldf['speed'])
>>> 19200
print(ldf['nodes']['slaves'])
>>> ['LSM', 'RSM']
```

If you're just looking to convert into JSON so that some other tool can interpret
it then have a look at `export` command in the [CLI](cli.md).

---

### Parsing into LIN objects

After converting the LDF into a dictionary the parser maps these values
into Python objects that can be used for easier data access as well as traversal
through the links between objects.

```python
ldf = parseLDF('network.ldf')
print(ldf.speed)
>>> 19200
for node in ldf.slaves:
  print(node.name)
>>> 'LSM'
>>> 'RSM'
```
