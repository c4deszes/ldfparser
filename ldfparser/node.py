
class LinNode:

	def __init__(self, name: str):
		self.name = name
		self.subscribed_to = []
		self.publishes = []

class LinMaster:

	def __init__(self):
		self.name = ""
		self.timebase = 0.005
		self.jitter = 0.0001
		self.subscribed_to

class LinSlave:

	def __init__(self):
		self.name = ""
		self.lin_protocol = ""
		self.configured_nad = 0x01
		