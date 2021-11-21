import os

import ldfparser

class LinMaster:

    def send_frame(self, baudrate: int, frame_id: int, data: bytearray):
        # LIN Tool specific functionality
        pass

    def request_frame(self, baudrate: int, frame_id: int) -> bytearray:
        # LIN Tool specific functionality
        return bytearray()

if __name__ == "__main__":
    path = os.path.join(os.path.dirname(__file__), 'lin22.ldf')
    ldf = ldfparser.parse_ldf(path)
    lin_master = LinMaster()

    # Send Data dump
    requestData = ldf.master_request_frame.encode_data_dump(nad=0x01, data=[0x01, 0xFF, 0xFF, 0xFF, 0xFF])
    lin_master.send_frame(ldf.baudrate, ldf.master_request_frame.frame_id, requestData)

    # Receive data dump response
    responseData = lin_master.request_frame(ldf.baudrate, ldf.slave_response_frame.frame_id)
    print(ldf.slave_response_frame.decode_response(responseData))
