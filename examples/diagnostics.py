import os

import ldfparser

class LinMaster:

    def send_frame(self, baudrate: int, frame_id: int, data: bytearray):
        # LIN Tool specific functionality
        pass

if __name__ == "__main__":
    path = os.path.join(os.path.dirname(__file__), 'lin22.ldf')
    ldf = ldfparser.parse_ldf(path)
    lin_master = LinMaster()
    requestFrame = ldf.master_request_frame
    requestData = requestFrame.encode_data_dump(nad=0x01, data=[0x01, 0xFF, 0xFF, 0xFF, 0xFF])

    lin_master.send_frame(ldf.baudrate, requestFrame.frame_id, requestData)
