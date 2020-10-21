import os
from typing import Union

from lark import Lark, Transformer

from ldfparser.lin import LinFrame, LinSignal
from ldfparser.encoding import LinSignalType, LogicalValue, PhysicalValue

import json

class LDF:
	def __init__(self):
		self.protocol_version = None
		self.language_version = None
		self.baudrate = None
		self.channel_name = None
		self.master = None
		self.slaves = []
		self.signals = []
		self.frames = []
		self.converters = []

	def signal(self, name: str) -> LinSignal:
		"""
		Returns Signal with the given name
		"""
		return next((x for x in self.signals if x.name == name), None)

	def frame(self, frame_id:Union[int, str]) -> LinFrame:
		"""
		Returns a Frame with the given id, or the given name
		"""
		if isinstance(frame_id, int):
			return next((x for x in self.frames if x.frame_id == frame_id), None)
		elif isinstance(frame_id, str):
			return next((x for x in self.frames if x.name == frame_id), None)
		return None

def parseLDF(path: str) -> LDF:
	lark = os.path.join(os.path.dirname(__file__), 'ldf.lark')
	parser = Lark(grammar=open(lark), parser='lalr')
	ldf_file = open(path, "r").read()
	tree = parser.parse(ldf_file)
	transformed = LDFTransformer().transform(tree)
	print(json.dumps(transformed))
	pass

class LDFTransformer(Transformer):
	def parse_integer(self, i:str):
		try:
			return int(i)
		except ValueError as e:
			return int(i, 16)

	def parse_real_or_integer(self, i:str):
		try:
			return float(i)
		except ValueError as e:
			return self.parse_int(i)

	def ldf_identifier(self, tree):
		return tree[0][0:]

	def ldf_integer(self, tree):
		return self.parse_integer(tree[0])

	def ldf_float(self, tree):
		return self.parse_real_or_integer(tree[0])

	def start(self, tree):
		return tree[0]

	def ldf(self, tree):
		ldf = {}
		for k in tree[0:]:
			ldf[k[0]] = k[1]
		return ldf

	def header_lin_description_file(self, tree):
		return ("header", "lin_description_file")

	def header_protocol_version(self, tree):
		return ("protocol_version", str(tree[0]))

	def header_language_version(self, tree):
		return ("language_version", str(tree[0]))

	def header_speed(self, tree):
		return ("speed", float(tree[0]) * 1000)

	def header_channel(self, tree):
		return ("channel", tree[0])

	def nodes(self, tree):
		return ("nodes", {'master': tree[0], 'slaves': tree[1]})

	def nodes_master(self, tree):
		return {"name": tree[0], "timebase": tree[1] * 0.001, "jitter": tree[2] * 0.001}

	def nodes_slaves(self, tree):
		return tree

	def node_compositions(self, tree):
		return ("node_compositions", tree[0:])

	def node_compositions_configuration(self, tree):
		return {"name": tree[0], "compositions": tree[1]}

	def node_compositions_composite(self, tree):
		return {"name": tree[0], "nodes": tree[1:]}

	def signals(self, tree):
		return ("signals", tree)

	def signal_definition(self, tree):
		return {"name": tree[0], "width": int(tree[1]), "default_value": tree[2], "publisher": tree[3], "subscribers": tree[4:]}

	def signal_default_value(self, tree):
		return tree[0]

	def signal_default_value_single(self, tree):
		return int(tree[0])

	def signal_default_value_array(self, tree):
		return tree[0]

	def frames(self, tree):
		return ("frames", tree)

	def frame_definition(self, tree):
		return {"name": tree[0], "frame_id": int(tree[1]), "publisher": tree[2], "length": tree[3] if len(tree) > 4 else None, "signals": tree[4] if len(tree) > 4 else tree[3]}

	def frame_signals(self, tree):
		return tree[0:]

	def frame_signal(self, tree):
		return {"signal": tree[0], "offset": int(tree[1])}

	def sporadic_frames(self, tree):
		return ("sporadic_frames", tree[0:])

	def sporadic_frame_definition(self, tree):
		return {"name": tree[0], "frames": tree[1:]}

	def event_triggered_frames(self, tree):
		return ("event_triggered_frames", tree[0:])

	def event_triggered_frame_definition(self, tree):
		return {"name": tree[0]}

	def event_triggered_frame_definition_frames(self, tree):
		return tree[0:]

	def node_attributes(self, tree):
		return ("node_attributes", tree[0:])

	def node_definition(self, tree):
		node = {"name": tree[0]}
		for k in tree[1:]:
			node[k[0]] = k[1]
		return node

	def node_definition_protocol(self, tree):
		return ("lin_protocol", str(tree[0]))

	def node_definition_configured_nad(self, tree):
		return ("configured_nad", tree[0])

	def node_definition_initial_nad(self, tree):
		return ("initial_nad", tree[0])

	def node_definition_product_id(self, tree):
		return ("product_id", {"supplier_id": tree[0], "function_id": tree[1], "variant": tree[2] if len(tree) > 2 else None})

	def node_definition_response_error(self, tree):
		return ("response_error", tree[0])

	def node_definition_fault_state_signals(self, tree):
		return ("fault_state_signals", tree[0:])

	def node_definition_p2_min(self, tree):
		return ("P2_min", tree[0])

	def node_definition_st_min(self, tree):
		return ("ST_min", tree[0])

	def node_definition_n_as_timeout(self, tree):
		return ("N_As_timeout", tree[0])

	def node_definition_n_cr_min(self, tree):
		return ("N_Cr_timeout", tree[0])

	def node_definition_configurable_frames(self, tree):
		return tree[0]

	def node_definition_configurable_frames_20(self, tree):
		frames = {}
		a = iter(tree)
		for frame, msg_id in zip(a, a):
			frames[frame] = msg_id
		return ("configurable_frames", frames)

	def node_definition_configurable_frames_21(self, tree):
		return ("configurable_frames", tree[0:])

	def schedule_tables(self, tree):
		return ("schedule_tables", tree)

	def schedule_table_definition(self, tree):
		return {"name": tree[0], "schedule": tree[1:]}

	def schedule_table_entry(self, tree):
		return {"command": tree[0], "delay": tree[1]}
	
	def schedule_table_command(self, tree):
		return tree[0]

	def schedule_table_command_masterreq(self, tree):
		return {"type": "master_request"}

	def schedule_table_command_slaveresp(self, tree):
		return {"type": "slave_response"}

	def schedule_table_command_assignnad(self, tree):
		return {"type": "assign_nad", "node": tree[0]}

	def schedule_table_command_conditionalchangenad(self, tree):
		return {"type": "conditional_change_nad"} #TODO: add arguments

	def schedule_table_command_datadump(self, tree):
		return {"type": "data_dump", "node": tree[0], "data": tree[1:]}

	def schedule_table_command_saveconfiguration(self, tree):
		return {"type": "save_configuration", "node": tree[0]}

	def schedule_table_command_assignframeidrange(self, tree):
		return {"type": "assign_frame_id_range"} #TODO: add arguments

	def schedule_table_command_assignframeid(self, tree):
		return {"type": "assign_frame_id"} # TODO: add arguments

	def schedule_table_command_freeformat(self, tree):
		return {"type": "free_format", "data": tree[0:]}

	def schedule_table_command_frame(self, tree):
		return {"type": "frame", "frame": tree[0]}

	def signal_groups(self, tree):
		return ("signal_groups", tree)

	def signal_group(self, tree):
		signals = {}
		a = iter(tree[2:])
		for signal, offset in zip(a, a):
			signals[signal] = offset
		return {"name": tree[0], "size": tree[1], "signals": signals}

	def signal_encoding_types(self, tree):
		return ("signal_encoding_types", tree)

	def signal_encoding_type(self, tree):
		return {"name": tree[0], "values": tree[1:]}

	def signal_encoding_logical_value(self, tree):
		return {"type": "logical", "value": tree[0], "text": tree[1] if len(tree) > 1 else None}

	def signal_encoding_physical_value(self, tree):
		return {"type": "physical", "min": tree[0], "max": tree[1], "scale": tree[2], "offset": tree[3], "unit": tree[4] if len(tree) > 4 else None}

	def signal_encoding_bcd_value(self, tree):
		return {"type": "bcd"}

	def signal_encoding_ascii_value(self, tree):
		return {"type": "ascii"}

	def signal_representations(self, tree):
		return ("signal_representations", tree)

	def signal_representation_node(self, tree):
		return {"encoding": tree[0], "signals": tree[1:]}