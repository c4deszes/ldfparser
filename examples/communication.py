import os
import ldfparser


class LinMaster:

	def send_frame(self, baudrate: int, frame_id: int, data: bytearray):
		# LIN Tool specific functionality
		pass


if __name__ == "__main__":
	path = os.path.join(os.path.dirname(__file__), 'lin22.ldf')
	ldf = ldfparser.parseLDF(path)
	lin_master = LinMaster()
	requestFrame = ldf.frame('CEM_Frm1')
	requestData = requestFrame.data({"InternalLightsRequest": 'on'}, ldf.converters)

	lin_master.send_frame(ldf.baudrate, requestFrame.frame_id, requestData)
