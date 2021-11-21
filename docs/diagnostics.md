---
layout: default
title: LDF Parser - Diagnostics
---

## Diagnostics

### Encoding diagnostic requests

The `LinDiagnosticRequest` contains methods that allow encoding and decoding of the standard
node configuration commands.

```python
ldf = parse_ldf('network.ldf')

ldf.master_request_frame.encode_assign_nad(inital_nad=0,
                                           supplier_id=0x7FFF,
                                           function_id=0xFFFF,
                                           new_nad=0x13)
>>> b'\x00\x06\xB0\xFF\x7F\xFF\xFF\x13'
```

### Decoding diagnostic responses

```python
ldf = parse_ldf('network.ldf')

ldf.slave_response_frame.decode_response(b'\x00\x01\xF0\xFF\xFF\xFF\xFF\xFF')
>>> { 'NAD': 0x00,'PCI': 0x01, 'RSID': 0xF0,
      'D1': 0xFF, 'D2': 0xFF, 'D3': 0xFF, 'D4': 0xFF, 'D5': 0xFF}
```
