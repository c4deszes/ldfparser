import os
import warnings
from typing import Any, Dict, List
from lark import Lark

from .diagnostics import LIN_MASTER_REQUEST_FRAME_ID, LIN_SLAVE_RESPONSE_FRAME_ID, LinDiagnosticFrame, LinDiagnosticRequest, LinDiagnosticResponse
from .schedule import AssignFrameIdEntry, AssignFrameIdRangeEntry, AssignNadEntry, ConditionalChangeNadEntry, DataDumpEntry, FreeFormatEntry, MasterRequestEntry, SaveConfigurationEntry, ScheduleTable, SlaveResponseEntry, UnassignFrameIdEntry, LinFrameEntry

from .frame import LinEventTriggeredFrame, LinUnconditionalFrame
from .signal import LinSignal
from .encoding import ASCIIValue, BCDValue, LinSignalEncodingType, LogicalValue, PhysicalValue, ValueConverter
from .lin import LIN_VERSION_2_0, LIN_VERSION_2_1, LinVersion
from .node import LinMaster, LinProductId, LinSlave
from .ldf import LDF
from .grammar import LdfTransformer

def parse_ldf_to_dict(path: str, capture_comments: bool = False, encoding: str = None) -> Dict:
    """
    Parses an LDF file into a Python dictionary.

    :param path: Path to the LDF file
    :type path: str
    :param encoding: File encoding, for example 'UTF-8'
    :type encoding: str
    """
    comments = []
    lark = os.path.join(os.path.dirname(__file__), 'grammars', 'ldf.lark')
    parser = Lark(grammar=open(lark), parser='lalr', lexer_callbacks={
        'C_COMMENT': comments.append,
        'CPP_COMMENT': comments.append
    }, propagate_positions=True)
    ldf_file = open(path, "r", encoding=encoding).read()
    tree = parser.parse(ldf_file)
    json = LdfTransformer().transform(tree)

    if capture_comments:
        json['comments'] = [comment.value for comment in comments]
    return json

def parseLDFtoDict(path: str, captureComments: bool = False, encoding: str = None) -> Dict:
    # pylint: disable=invalid-name
    """
    Deprecated, use `parse_ldf_to_dict` instead

    This method will be removed in 1.0.0
    """
    warnings.warn("'parseLDFtoDict' is deprecated, use 'parse_ldf_to_dict' instead", DeprecationWarning)
    return parse_ldf_to_dict(path, captureComments, encoding)

def parse_ldf(path: str, capture_comments: bool = False, encoding: str = None) -> LDF:
    """
    Parses an LDF file into an object

    :param path: Path to the LDF file
    :type path: str
    :param encoding: File encoding, for example 'UTF-8'
    :type encoding: str
    """
    json = parse_ldf_to_dict(path, capture_comments, encoding)
    ldf = LDF()
    ldf._source = json

    _populate_ldf_header(json, ldf)
    _populate_ldf_signals(json, ldf)
    _populate_ldf_frames(json, ldf)
    _populate_ldf_event_triggered_frames(json, ldf)
    _populate_diagnostic_signals(json, ldf)
    _populate_diagnostic_frames(json, ldf)
    _populate_ldf_nodes(json, ldf)
    _populate_ldf_encoding_types(json, ldf)
    _populate_schedule_tables(json, ldf)

    _link_ldf_signals(json, ldf)
    _link_ldf_frames(json, ldf)
    _link_ldf_schedule_table(json, ldf)

    if capture_comments:
        ldf._comments = json['comments']

    return ldf

def parseLDF(path: str, captureComments: bool = False, encoding: str = None) -> LDF:
    # pylint: disable=invalid-name
    """
    Deprecated, use `parse_ldf` instead, this method will be removed in 1.0.0
    """
    warnings.warn("'parseLDF' is deprecated, use 'parse_ldf' instead", DeprecationWarning)
    return parse_ldf(path, captureComments, encoding)

def _populate_ldf_header(json: dict, ldf: LDF):
    ldf._protocol_version = LinVersion.from_string(_require_key(json, 'protocol_version', 'LDF missing protocol version.'))
    ldf._language_version = LinVersion.from_string(_require_key(json, 'language_version', 'LDF missing language version.'))
    ldf._baudrate = _require_key(json, 'speed', 'LDF missing speed definition.')
    ldf._channel = json.get('channel_name')

def _populate_ldf_signals(json: dict, ldf: LDF):
    for signal in _require_key(json, 'signals', 'LDF missing Signals section.'):
        ldf._signals[signal['name']] = LinSignal.create(signal['name'], signal['width'], signal['init_value'])

def _populate_ldf_frames(json: dict, ldf: LDF):
    for frame in _require_key(json, 'frames', 'LDF missing Frames section.'):
        signals = {}

        for signal in frame['signals']:
            s = ldf.get_signal(signal['signal'])
            if s is None:
                raise ValueError(f"{frame['name']} references non existing signal {signal['signal']}")
            signals[signal['offset']] = s

        length = frame['length']
        if length is None and ldf.get_language_version() > LIN_VERSION_2_0:
            raise ValueError(f"Frame({frame['frame_id']}, {frame['name']}) has no length specified, only allowed in LIN 2.0 and below.")
        if length is None:
            if 0 <= frame['frame_id'] <= 31:
                length = 2
            elif 32 <= frame['frame_id'] <= 47:
                length = 4
            elif 48 <= frame['frame_id'] <= 63:
                length = 8

        ldf._unconditional_frames[frame['name']] = LinUnconditionalFrame(frame['frame_id'], frame['name'], length, signals)

def _populate_ldf_event_triggered_frames(json: dict, ldf: LDF):
    if "event_triggered_frames" not in json:
        return
    for frame in json['event_triggered_frames']:
        frames = []
        for a in frame['frames']:
            frames.append(ldf.get_unconditional_frame(a))
        ldf._event_triggered_frames[frame['name']] = LinEventTriggeredFrame(frame['frame_id'], frame['name'], frames)

def _populate_ldf_nodes(json: dict, ldf: LDF):
    nodes = _require_key(json, 'nodes', 'Missing Nodes section.')
    master_node = nodes['master']
    ldf._master = LinMaster(master_node['name'], master_node['timebase'], master_node['jitter'])

    if ldf.get_language_version() >= LIN_VERSION_2_0:
        for node in _require_key(json, 'node_attributes', 'Missing Node_attributes section, required in LDF 2.0+'):
            if node['name'] not in nodes['slaves']:
                raise ValueError(f"Node {node['name']} is configured but not listed as a slave.")
            ldf._slaves[node['name']] = _create_ldf2x_node(node, ldf.get_language_version())
    else:
        for slave in nodes['slaves']:
            node = LinSlave(slave)
            node.lin_protocol = ldf.protocol_version
            ldf._slaves[node.name] = node

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
    elif language_version >= LIN_VERSION_2_1:
        raise ValueError(f"Node {name} has no product_id specified, required for LDF 2.1+")

    slave.p2_min = node.get('P2_min', 0.05)
    slave.st_min = node.get('ST_min', 0)
    slave.n_as_timeout = node.get('N_As_timeout', 1)
    slave.n_cr_timeout = node.get('N_Cr_timeout', 1)

    return slave

def _populate_diagnostic_signals(json: dict, ldf: LDF):
    if 'diagnostic_signals' in json:
        for signal in json['diagnostic_signals']:
            ldf._diagnostic_signals[signal['name']] = LinSignal.create(signal['name'], signal['width'], signal['init_value'])

def _populate_diagnostic_frames(json: dict, ldf: LDF):
    if 'diagnostic_frames' in json:
        for frame in json['diagnostic_frames']:
            signals = {}

            for signal in frame['signals']:
                s = ldf.get_diagnostic_signal(signal['signal'])
                if s is None:
                    raise ValueError(f"{frame['name']} references non existing signal {signal['signal']}")
                signals[signal['offset']] = s

            frame_obj = LinDiagnosticFrame(frame['frame_id'], frame['name'], 9, signals)
            ldf._diagnostic_frames[frame['name']] = frame_obj
            if frame['frame_id'] == LIN_MASTER_REQUEST_FRAME_ID:
                ldf._master_request_frame = LinDiagnosticRequest(frame_obj)
            if frame['frame_id'] == LIN_SLAVE_RESPONSE_FRAME_ID:
                ldf._slave_response_frame = LinDiagnosticResponse(frame_obj)

def _create_schedule_table_entry(json: dict, ldf: LDF):  # noqa: C901
    if json['command']['type'] == 'frame':
        entry = LinFrameEntry()
        entry.delay = json['delay']
        entry.frame = ldf.get_frame(json['command']['frame'])
        return entry
    if json['command']['type'] == 'master_request':
        entry = MasterRequestEntry()
        entry.delay = json['delay']
        return entry
    if json['command']['type'] == 'slave_response':
        entry = SlaveResponseEntry()
        entry.delay = json['delay']
        return entry
    if json['command']['type'] == 'assign_nad':
        entry = AssignNadEntry()
        entry.delay = json['delay']
        entry.node = ldf.get_slave(json['command']['node'])
        return entry
    if json['command']['type'] == 'conditional_change_nad':
        entry = ConditionalChangeNadEntry()
        entry.delay = json['delay']
        entry.nad = json['command']['nad']
        entry.id = json['command']['id']
        entry.byte = json['command']['byte']
        entry.mask = json['command']['mask']
        entry.inv = json['command']['inv']
        entry.new_nad = json['command']['new_nad']
        return entry
    if json['command']['type'] == 'data_dump':
        entry = DataDumpEntry()
        entry.delay = json['delay']
        entry.node = ldf.get_slave(json['command']['node'])
        entry.data = json['command']['data']
        return entry
    if json['command']['type'] == 'save_configuration':
        entry = SaveConfigurationEntry()
        entry.delay = json['delay']
        entry.node = ldf.get_slave(json['command']['node'])
        return entry
    if json['command']['type'] == 'assign_frame_id':
        entry = AssignFrameIdEntry()
        entry.delay = json['delay']
        entry.node = ldf.get_slave(json['command']['node'])
        entry.frame = ldf.get_frame(json['command']['frame'])
        return entry
    if json['command']['type'] == 'unassign_frame_id':
        entry = UnassignFrameIdEntry()
        entry.delay = json['delay']
        entry.node = ldf.get_slave(json['command']['node'])
        entry.frame = ldf.get_frame(json['command']['frame'])
        return entry
    if json['command']['type'] == 'assign_frame_id_range':
        entry = AssignFrameIdRangeEntry()
        entry.delay = json['delay']
        entry.node = ldf.get_slave(json['command']['node'])
        entry.frame_index = json['command']['frame_index']
        entry.pids = json['command']['pids']
        return entry
    if json['command']['type'] == 'free_format':
        entry = FreeFormatEntry()
        entry.delay = json['delay']
        entry.data = json['command']['data']
        return entry
    raise ValueError("Unknown schedule command type")

def _populate_schedule_tables(json: dict, ldf: LDF):
    if 'schedule_tables' in json:
        for table in json['schedule_tables']:
            schedule_table = ScheduleTable(table['name'])
            for item in table['schedule']:
                entry = _create_schedule_table_entry(item, ldf)
                schedule_table.schedule.append(entry)
            ldf._schedule_tables[schedule_table.name] = schedule_table

def _link_ldf_signals(json: dict, ldf: LDF):  # noqa: C901
    for signal in _require_key(json, 'signals', 'LDF missing Signals section.'):
        signal_obj = ldf.get_signal(signal['name'])
        if signal['publisher'] == ldf.master.name:
            ldf._master.publishes.append(signal_obj)
            signal_obj.publisher = ldf._master
        else:
            slave = ldf.slave(signal['publisher'])
            if slave is None:
                raise ValueError(f"Signal {signal_obj.name} references non existent node {signal['publisher']}")
            slave.publishes.append(signal_obj)
            signal_obj.publisher = slave

        if ldf._master.name in signal['subscribers']:
            ldf._master.subscribes_to.append(signal_obj)
            signal_obj.subscribers.append(ldf._master)
        for subscriber in signal['subscribers']:
            if subscriber != ldf.master.name:
                slave = ldf.slave(subscriber)
                if slave is None:
                    raise ValueError(f"Signal {signal_obj.name} references non existent node {subscriber}")
                slave.subscribes_to.append(signal_obj)
                signal_obj.subscribers.append(slave)
    if ldf.get_protocol_version() < LIN_VERSION_2_0:
        return
    for node in json['node_attributes']:
        slave = ldf.get_slave(node['name'])
        if node.get('response_error'):
            slave.response_error = ldf.get_signal(node['response_error'])
        if node.get('fault_state_signals'):
            for signal in node['fault_state_signals']:
                slave.fault_state_signals.append(ldf.get_signal(signal))
        if node.get('configurable_frames'):
            pass
            if isinstance(node['configurable_frames'], Dict):
                for (frame, pid) in node['configurable_frames'].items():
                    slave.configurable_frames[pid] = ldf.get_frame(frame)
            elif isinstance(node['configurable_frames'], List):
                for (idx, frame) in enumerate(node['configurable_frames']):
                    slave.configurable_frames[idx] = ldf.get_frame(frame)

def _link_ldf_frames(json: dict, ldf: LDF):
    for frame in _require_key(json, 'frames', 'LDF missing Frames sections.'):
        frame_obj = ldf.get_frame(frame['frame_id'])
        if frame['publisher'] == ldf._master.name:
            ldf._master.publishes_frames.append(frame_obj)
            frame_obj.publisher = ldf._master
        else:
            slave = ldf.get_slave(frame['publisher'])
            if slave is None:
                raise ValueError(f"Frame {frame_obj.name} references non existent node {frame['publisher']}")
            slave.publishes_frames.append(frame_obj)
            frame_obj.publisher = slave

def _link_ldf_schedule_table(json: dict, ldf: LDF):
    if "event_triggered_frames" not in json:
        return
    for frame in json['event_triggered_frames']:
        frame_obj = ldf.get_event_triggered_frame(frame['name'])
        frame_obj.collision_resolving_schedule_table = ldf.get_schedule_table(frame['collision_resolving_schedule_table'])

def _populate_ldf_encoding_types(json: dict, ldf: LDF):
    if json.get('signal_encoding_types') is None or json.get('signal_representations') is None:
        return
    for encoding_type in json['signal_encoding_types']:
        converters = []
        for encoding_value in encoding_type['values']:
            converters.append(_convert_encoding_value(encoding_value))
        ldf._signal_encoding_types[encoding_type['name']] = LinSignalEncodingType(encoding_type['name'], converters)
    for representations in json['signal_representations']:
        for signal in representations['signals']:
            signal_obj = ldf.get_signal(signal)
            signal_obj.encoding_type = ldf._signal_encoding_types[representations['encoding']]
            ldf._signal_representations[signal_obj] = ldf._signal_encoding_types[representations['encoding']]

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

def _require_key(value: dict, key: str, msg: str) -> Any:
    if value.get(key) is None:
        raise ValueError(msg)
    return value[key]
