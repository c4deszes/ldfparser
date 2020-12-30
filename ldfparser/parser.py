import os
from typing import Any, Union, Dict, List
from lark import Lark, Transformer

from .lin import LinFrame, LinSignal
from .encoding import ASCIIValue, BCDValue, LinSignalType, LogicalValue, PhysicalValue, ValueConverter
from .node import LinMaster, LinProductId, LinSlave
from .comment import parseComments


class LDF:
	def __init__(self):
		self._source = None
		self.protocol_version: float = None
		self.language_version: float = None
		self.baudrate: int = None
		self.channel: str = None
		self.master: LinMaster = None
		self.slaves: List[LinSlave] = []
		self.signals: List[LinSignal] = []
		self.frames: List[LinFrame] = []
		self.converters: Dict[str, LinSignalType] = {}
		self.comments: List[str] = []

	def signal(self, name: str) -> LinSignal:
		"""
		Returns Signal with the given name
		"""
		return next((x for x in self.signals if x.name == name), None)

	def frame(self, frame_id: Union[int, str]) -> LinFrame:
		"""
		Returns a Frame with the given id, or the given name
		"""
		if isinstance(frame_id, int):
			return next((x for x in self.frames if x.frame_id == frame_id), None)
		elif isinstance(frame_id, str):
			return next((x for x in self.frames if x.name == frame_id), None)
		return None

	def slave(self, name: str) -> LinSlave:
		"""
		Returns Lin Slave with the given name
		"""
		return next((x for x in self.slaves if x.name == name), None)


def parseLDFtoDict(path: str, captureComments: bool = False, encoding: str = None) -> Dict[str, Any]:
	lark = os.path.join(os.path.dirname(__file__), 'ldf.lark')
	parser = Lark(grammar=open(lark), parser='lalr')
	ldf_file = open(path, "r", encoding=encoding).read()
	tree = parser.parse(ldf_file)
	json = LDFTransformer().transform(tree)
	if captureComments:
		json['comments'] = parseComments(ldf_file)
	return json


def parseLDF(path: str, captureComments: bool = False, encoding: str = None) -> LDF:
	json = parseLDFtoDict(path, captureComments, encoding)
	ldf = LDF()
	ldf._source = json

	_populate_ldf_header(json, ldf)
	_populate_ldf_signals(json, ldf)
	_populate_ldf_frames(json, ldf)
	_populate_ldf_nodes(json, ldf)
	_populate_ldf_encoding_types(json, ldf)

	_link_ldf_signals(json, ldf)
	_link_ldf_frames(json, ldf)

	if captureComments:
		ldf.comments = json['comments']

	return ldf


def _populate_ldf_header(json: dict, ldf: LDF):
	ldf.protocol_version = _require_key(json, 'protocol_version', 'LDF missing protocol version.')
	ldf.language_version = _require_key(json, 'language_version', 'LDF missing language version.')
	ldf.baudrate = _require_key(json, 'speed', 'LDF missing speed definition.')
	ldf.channel = json.get('channel_name')


def _populate_ldf_signals(json: dict, ldf: LDF):
	for signal in _require_key(json, 'signals', 'LDF missing Signals section.'):
		ldf.signals.append(LinSignal.create(signal['name'], signal['width'], signal['init_value']))


def _populate_ldf_frames(json: dict, ldf: LDF):
	for frame in _require_key(json, 'frames', 'LDF missing Frames section.'):
		signals = {}

		for signal in frame['signals']:
			s = ldf.signal(signal['signal'])
			if s is None:
				raise ValueError(f"{frame['name']} references non existing signal {signal['signal']}")
			signals[signal['offset']] = s

		length = frame['length']
		if length is None and ldf.language_version > 2.0:
			raise ValueError(f"Frame({frame['frame_id']}, {frame['name']}) has no length specified, only allowed in LIN 2.0 and below.")
		if length is None:
			if 0 <= frame['frame_id'] <= 31:
				length = 2
			elif 32 <= frame['frame_id'] <= 47:
				length = 4
			elif 48 <= frame['frame_id'] <= 63:
				length = 8

		ldf.frames.append(LinFrame(frame['frame_id'], frame['name'], length, signals))


def _populate_ldf_nodes(json: dict, ldf: LDF):
	nodes = _require_key(json, 'nodes', 'Missing Nodes section.')
	master_node = nodes['master']
	ldf.master = LinMaster(master_node['name'], master_node['timebase'], master_node['jitter'])

	if ldf.language_version >= 2.0:
		for node in _require_key(json, 'node_attributes', 'Missing Node_attributes section, required in LDF 2.0+'):
			if node['name'] not in nodes['slaves']:
				raise ValueError(f"Node {node['name']} is configured but not listed as a slave.")
			ldf.slaves.append(_create_ldf2x_node(node, ldf.language_version))
	else:
		for slave in nodes['slaves']:
			node = LinSlave(slave)
			node.lin_protocol = ldf.protocol_version
			ldf.slaves.append(node)


def _create_ldf2x_node(node: dict, language_version: float):
	name = node['name']
	lin_protocol = _require_key(node, 'lin_protocol', f"Node {name} has no LIN protocol version specified.")
	slave = LinSlave(name)
	slave.lin_protocol = lin_protocol
	slave.configured_nad = _require_key(node, 'configured_nad', f"Node {name} has no configured NAD.")
	slave.initial_nad = slave.configured_nad if node.get('initial_nad') is None else node.get('initial_nad')

	if node.get('product_id') is not None:
		supplier = node['product_id']['supplier_id']
		function = node['product_id']['function_id']
		variant = node['product_id']['variant']
		product_id = LinProductId(supplier, function, variant)
		slave.product_id = product_id
	elif language_version >= 2.1:
		raise ValueError(f"Node {name} has no product_id specified, required for LDF 2.1+")

	if node.get('P2_min') is not None:
		slave.p2_min = node['P2_min']
	if node.get('ST_min') is not None:
		slave.st_min = node['ST_min']
	if node.get('N_As_timeout') is not None:
		slave.n_as_timeout = node['N_As_timeout']
	if node.get('N_Cr_timeout') is not None:
		slave.n_cr_timeout = node['N_Cr_timeout']

	return slave


def _link_ldf_signals(json: dict, ldf: LDF):
	for signal in _require_key(json, 'signals', 'LDF missing Signals section.'):
		signal_obj = ldf.signal(signal['name'])
		if signal['publisher'] == ldf.master.name:
			ldf.master.publishes.append(signal_obj)
			signal_obj.publisher = ldf.master
		else:
			slave = ldf.slave(signal['publisher'])
			if slave is None:
				raise ValueError(f"Signal {signal_obj.name} references non existent node {signal['publisher']}")
			slave.publishes.append(signal_obj)
			signal_obj.publisher = slave

		if ldf.master.name in signal['subscribers']:
			ldf.master.subscribes_to.append(signal_obj)
			signal_obj.subscribers.append(ldf.master)
		for subscriber in signal['subscribers']:
			if subscriber != ldf.master.name:
				slave = ldf.slave(subscriber)
				if slave is None:
					raise ValueError(f"Signal {signal_obj.name} references non existent node {subscriber}")
				slave.subscribes_to.append(signal)
				signal_obj.subscribers.append(slave)


def _link_ldf_frames(json: dict, ldf: LDF):
	for frame in _require_key(json, 'frames', 'LDF missing Frames sections.'):
		frame_obj = ldf.frame(frame['frame_id'])
		if frame['publisher'] == ldf.master.name:
			ldf.master.publishes_frames.append(frame_obj)
			frame_obj.publisher = ldf.master
		else:
			slave = ldf.slave(frame['publisher'])
			if slave is None:
				raise ValueError(f"Frame {frame_obj.name} references non existent node {frame['publisher']}")
			slave.publishes_frames.append(frame_obj)
			frame_obj.publisher = slave


def _populate_ldf_encoding_types(json: dict, ldf: LDF):
	if json.get('signal_encoding_types') is None or json.get('signal_representations') is None:
		return
	signalTypes = {}
	for encoding_type in json['signal_encoding_types']:
		converters = []
		for encoding_value in encoding_type['values']:
			converters.append(_convert_encoding_value(encoding_value))
		signalTypes[encoding_type['name']] = LinSignalType(encoding_type['name'], converters)
	for representations in json['signal_representations']:
		for signal in representations['signals']:
			ldf.converters[signal] = signalTypes[representations['encoding']]


def _convert_encoding_value(json: dict) -> ValueConverter:
	if json['type'] == 'logical':
		return LogicalValue(json['value'], json['text'])
	if json['type'] == 'physical':
		return PhysicalValue(json['min'], json['max'], json['scale'], json['offset'], json['unit'])
	if json['type'] == 'bcd':
		return BCDValue()
	if json['type'] == 'ascii':
		return ASCIIValue()
	raise ValueError(f"Unsupported value type {json['type']}")


def _require_key(a: dict, k: str, msg: str) -> Any:
	if a.get(k) is None:
		raise ValueError(msg)
	return a[k]


class LDFTransformer(Transformer):
	def parse_integer(self, i: str):
		try:
			return int(i)
		except ValueError:
			return int(i, 16)

	def parse_real_or_integer(self, i: str):
		try:
			return float(i)
		except ValueError:
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
		return ("protocol_version", tree[0])

	def header_language_version(self, tree):
		return ("language_version", tree[0])

	def header_speed(self, tree):
		return ("speed", int(float(tree[0]) * 1000))

	def header_channel(self, tree):
		return ("channel_name", tree[0])

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
		return {"name": tree[0], "width": int(tree[1]), "init_value": tree[2], "publisher": tree[3], "subscribers": tree[4:]}

	def signal_default_value(self, tree):
		return tree[0]

	def signal_default_value_single(self, tree):
		return int(tree[0])

	def signal_default_value_array(self, tree):
		return tree[0]

	def diagnostic_signals(self, tree):
		return ("diagnostic_signals", [])

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

	def diagnostic_frames(self, tree):
		return ("diagnostic_frames", [])

	def node_attributes(self, tree):
		return ("node_attributes", tree[0:])

	def node_definition(self, tree):
		node = {"name": tree[0]}
		for k in tree[1:]:
			node[k[0]] = k[1]
		return node

	def node_definition_protocol(self, tree):
		return ("lin_protocol", tree[0])

	def node_definition_configured_nad(self, tree):
		return ("configured_nad", tree[0])

	def node_definition_initial_nad(self, tree):
		return ("initial_nad", tree[0])

	def node_definition_product_id(self, tree):
		return ("product_id", {"supplier_id": tree[0], "function_id": tree[1], "variant": tree[2] if len(tree) > 2 else 0})

	def node_definition_response_error(self, tree):
		return ("response_error", tree[0])

	def node_definition_fault_state_signals(self, tree):
		return ("fault_state_signals", tree[0:])

	def node_definition_p2_min(self, tree):
		return ("P2_min", tree[0] * 0.001)

	def node_definition_st_min(self, tree):
		return ("ST_min", tree[0] * 0.001)

	def node_definition_n_as_timeout(self, tree):
		return ("N_As_timeout", tree[0] * 0.001)

	def node_definition_n_cr_timeout(self, tree):
		return ("N_Cr_timeout", tree[0] * 0.001)

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
		return {"type": "conditional_change_nad", "nad": tree[0], "id": tree[1], "byte": tree[2], "mask": tree[3], "inv": tree[4], "new_nad": tree[5]}

	def schedule_table_command_datadump(self, tree):
		return {"type": "data_dump", "node": tree[0], "data": tree[1:]}

	def schedule_table_command_saveconfiguration(self, tree):
		return {"type": "save_configuration", "node": tree[0]}

	def schedule_table_command_assignframeidrange(self, tree):
		return {"type": "assign_frame_id_range", "node": tree[0], "frame_index": tree[1], "pids": tree[2:]}

	def schedule_table_command_assignframeid(self, tree):
		return {"type": "assign_frame_id", "node": tree[0], "frame": tree[1]}

	def schedule_table_command_unassignframeid(self, tree):
		return {"type": "unassign_frame_id", "node": tree[0], "frame": tree[1]}

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

	def signal_encoding_text_value(self, tree):
		return tree[0][1:-1]

	def signal_representations(self, tree):
		return ("signal_representations", tree)

	def signal_representation_node(self, tree):
		return {"encoding": tree[0], "signals": tree[1:]}
