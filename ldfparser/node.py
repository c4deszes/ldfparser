
class LinNode:

	def __init__(self, name: str):
		self.name = name
		self.subscribed_to = []
		self.publishes = []

class LinMaster(LinNode):

	def __init__(self, name: str, timebase: float, jitter: float):
		super().__init__(name)
		self.timebase = timebase
		self.jitter = jitter

class LinSlave(LinNode):

	def __init__(self, name: str):
		super().__init__(name)
		self.lin_protocol = None
		self.configured_nad = None
		self.initial_nad = None
		self.response_error = None
		self.fault_state_signals = []
		self.p2_min = None
		self.st_min = None
		self.n_as_timeout = None
		self.n_cr_timeout = None
		self.configurable_frames = []
		