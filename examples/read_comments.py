import os
import ldfparser

if __name__ == "__main__":
    path = os.path.join(os.path.dirname(__file__), 'lin22.ldf')
    ldf = ldfparser.parseLDF(path, captureComments=True)
    print(ldf.comments)
