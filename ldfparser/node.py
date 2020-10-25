from typing import List

from .lin import LinSignal

class LinProductId:
	def __init__(self, supplier_id: int, function_id: int, variant: int = None) -> None:
		self.supplier_id: int = supplier_id
		self.function_id: int = function_id
		self.variant: int = variant

class LinNode:

	def __init__(self, name: str):
		self.name = name
		self.subscribed_to: List[LinSignal] = []
		self.publishes: List[LinSignal] = []

class LinMaster(LinNode):

	def __init__(self, name: str, timebase: float, jitter: float):
		super().__init__(name)
		self.timebase: float = timebase
		self.jitter: float = jitter

class LinSlave(LinNode):

	def __init__(self, name: str):
		super().__init__(name)
		self.lin_protocol: float = None

class LinSlave20(LinSlave):
	def __init__(self, name: str) -> None:
		super().__init__(name)
		self.configured_nad: int = None
		self.product_id: LinProductId = None
		self.response_error: LinSignal = None
		self.p2_min: float = 0.05
		self.st_min: float = 0
		self.configurable_frames = []

class LinSlave21(LinSlave20):
	def __init__(self) -> None:
		self.initial_nad: int = None
		self.fault_state_signals: List[LinSignal] = []
		self.n_as_timeout: float = 1
		self.n_cr_timeout: float = 1
		
class LinNodeCompositionConfiguration:

	def __init__(self, name: str) -> None:
		self.name: str = name
		self.compositions: List[LinNodeComposition] = []

class LinNodeComposition:

	def __init__(self, name: str) -> None:
		self.name: str = name
		self.nodes: List[LinSlave] = []