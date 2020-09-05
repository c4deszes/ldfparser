#
# MIT License
#
# Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the "Software"), to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
#
# Source: https://github.com/uCAN-LIN/LinUSBConverter/blob/29289c854a6cb63ea7191d9cf020526d4e4e48fc/python_lib/ucanlintools/LDF_parser.py
#

import os
from typing import Union

from lark import Lark, Transformer

from ldfparser.lin import LinFrame, LinSignal
from ldfparser.encoding import LinSignalType, LogicalValue, PhysicalValue

class LDF:
	def __init__(self, path: str):
		lark = os.path.join(os.path.dirname(__file__), 'ldf.lark')
		parser = Lark(grammar=open(lark), parser='lalr')
		ldf_file = open(path, "r").read()
		tree = parser.parse(ldf_file)
		json = LDFTransformer().transform(tree)
		ldf = {}
		for member in json:
			if member is not None:
				ldf.update(member)
		
		signalTypes = {}
		self.converters = {}
		if 'types' in ldf and 'representations' in ldf:
			for signalEncodingType in ldf['types']:
				signalType = LinSignalType(signalEncodingType[0], signalEncodingType[1:])
				signalTypes[signalType.name] = signalType
			
			for signalRepresentation in ldf['representations']:
				for signal in signalRepresentation[1:]:
					self.converters[signal] = signalTypes[signalRepresentation[0]]

		self.signals = []
		for signal in ldf['signals']:
			self.signals.append(
				LinSignal(
					signal['signal_name'],
					signal['size_bits'],
					signal['default_val']
				)
			)

		self.frames = []
		for frame in ldf['frames']:
			signalMapping = {}
			for signal in frame['frame_signals']:
				signalMapping[signal['bit_offset']] = self.signal(signal['name'])
			self.frames.append(
				LinFrame(
					frame['frame_id'],
					frame['frame_name'],
					frame['frame_len'],
					signalMapping
				)
			)

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

	def node(self, node_id):
		pass

#
# Source: https://github.com/uCAN-LIN/LinUSBConverter/blob/29289c854a6cb63ea7191d9cf020526d4e4e48fc/python_lib/ucanlintools/LDF_parser.py#L60
#
class LDFTransformer(Transformer):
	def parse_int(self, i:str):
		try:
			return int(i)
		except ValueError as e:
			return int(i, 16)

	def parse_real_or_integer(self, i:str):
		try:
			return float(i)
		except ValueError as e:
			return self.parse_int(i)

	def ldf_node_name(self,s):
		return s[0][0:]
	def signal_name(self, s):
		return s[0][0:]
	def signal_size(self, s):
		return self.parse_int(s[0])
	def signal_bit_offset(self, s):
		return self.parse_int(s[0])
	def ldf_node_master(self,s):
		return s[0][0:]
	def ldf_node_slaves(self,s):
		return s[0][0:]

	def ldf_nodes(self,s):
		return {'nodes': s}
	def ldf_signals(self,s):
		return {'signals': s}
	def ldf_frames(self,s):
		return {'frames': s}

	def ldf_container(self,s):
		return s

	def ldf_signal(self,s):
		return {'signal_name':s[0], 'size_bits':s[1], 'default_val': s[2], 'publisher': s[3], 'subscriber': s[4]}
	def ldf_frame(self,s):
		return {'frame_name':s[0], 'frame_id':s[1], 'publisher':s[2], 'frame_len':s[3], 'frame_signals':s[4:]}
	def ldf_frame_signal(self,s):
		return {'name':s[0],'bit_offset':s[1]}
	def ldf_frame_name(self,s):
		return s[0][0:] 
	def ldf_frame_id(self,s):
		return self.parse_int(s[0])
	def ldf_frame_len(self,s):
		return self.parse_int(s[0])
	def ldf_signal_size(self,s):
		return self.parse_int(s[0])
	def ldf_signal_bit_offset(self,s):
		return self.parse_int(s[0])
	def ldf_signal_name(self,s):
		return s[0][0:]
	def ldf_signal_default_value(self,s):
		s = s[0]
		s = s.replace('{','').replace('}','').split(',')
		o = []
		for x in s:
			o.append(self.parse_int(x))
		return o

	# start = dict 
	def start(self,s):
		return s[0]

	def ldf_node_atributes(self,s):
		return
		# return {"ldf_node_atributes" : "NOT_IMPLEMENTED"}
	def ldf_node_atributes_node(self,s):
		return
		# return {"ldf_node_atributes_node" : "NOT_IMPLEMENTED"}

	def ldf_schedule_table(self,s):
		return
		# return {"ldf_schedule_table" : "NOT_IMPLEMENTED"}
	def ldf_signal_representation(self,s):
		return {"representations" : s}
	def ldf_signal_representation_node(self,s):
		return s
	
	def ldf_signal_encoding_types(self, s):
		return {'types': s}
	def ldf_signal_encoding_type(self, s):
		return s

	def ldf_signal_encoding_type_name(self, s):
		return s[0][0:]

	def ldf_signal_encoding_logical_value(self, s):
		return LogicalValue(s[0], s[1] if len(s) > 1 else None)

	def ldf_encoding_logical_signal_value(self, s):
		return self.parse_int(s[0])

	def ldf_encoding_logical_signal_info(self, s):
		return s[0][1:-1]

	def ldf_signal_encoding_physical_value(self, s):
		return PhysicalValue(s[0], s[1], s[2], s[3], s[4] if len(s) > 4 else None)

	def ldf_encoding_phy_min(self, s):
		return self.parse_int(s[0])

	def ldf_encoding_phy_max(self, s):
		return self.parse_int(s[0])

	def ldf_encoding_phy_scale(self, s):
		return self.parse_real_or_integer(s[0])

	def ldf_encoding_phy_offset(self, s):
		return self.parse_real_or_integer(s[0])

	def ldf_encoding_phy_unit(self, s):
		return s[0][1:-1]

	def ldf_diagnostic(self,s):
		return
		# return {"ldf_diagnostic" : "NOT_IMPLEMENTED"}
	def ldf_diagnostic_frames(self,s):
		return
		# return {"ldf_diagnostic_frames" : "NOT_IMPLEMENTED"}
	def ldf_header(self,s):
		return
		# return {"ldf_header" : "NOT_IMPLEMENTED"}
	def ldf_header_lin(self,s):
		#print(s)
		return