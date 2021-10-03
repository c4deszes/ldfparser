---
layout: default
title: LDF Parser - Frames
---

## Using frames

### Retrieving unconditional frame information

After parsing the LDF into objects the properties of frames defined in the LDF
will be accessible.

```python
ldf = parse_ldf('network.ldf')

lsm_frame1 = ldf.get_unconditional_frame('LSM_Frm1')
print(lsm_frame1.frame_id)
>>> 2
print(lsm_frame1.name)
>>> 'LSM_Frm1'
print(lsm_frame1.length)
>>> 2
print(lsm_frame1.publisher)
>>> LinSlave(..)
```

---

### Encoding frames

Encoding is the process of the converting the provided LIN Signals into a
complete frame.

When encoding there are two options, you can encode raw values
and pack them into a frame, or alternatively you can pass the logical values
through the signal encoders before packing.

```python
ldf = parse_ldf('network.ldf')

lsm_frame1 = ldf.get_unconditional_frame('LSM_Frm1')
encoded_frame = lsm_frame1.raw(
    {'LeftIntLightsSwitch': 100}
)
```

When encoding through signal encoders you have to pass a list of value converters,
you can either provide a custom map or pass the one provided by the LDF object.

```python
ldf = parse_ldf('network.ldf')

lsm_frame1 = ldf.get_unconditional_frame('LSM_Frm1')
encoded_frame = lsm_frame1.data(
    {'LeftIntLightsSwitch': 'Off'},
    ldf.converters
)
```

---

### Decoding frames

Decoding is the process of unpacking a LIN frame into the signal values.

Similarly to encoding, you can decode frames into raw signal values or decode
them through the signal encoders.

```python
ldf = parse_ldf('network.ldf')

lsm_frame1 = ldf.get_unconditional_frame('LSM_Frm1')
decoded_frame = lsm_frame1.parse_raw(bytearray([0x00]))
```

When decoding through signal encoders you have to pass a list of value converters,
you can either provide a custom map or pass the one provided by the LDF object.

```python
ldf = parse_ldf('network.ldf')

lsm_frame1 = ldf.get_unconditional_frame('LSM_Frm1')
decoded_frame = lsm_frame1.parse(bytearray([0x00]), ldf.converters)
```
