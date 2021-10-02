import glob
import json
import os

import ldfparser

if __name__ == "__main__":
    ldf_directory = os.path.join(os.path.dirname(__file__), 'ldf')
    snapshot_directory = os.path.join(os.path.dirname(__file__), 'snapshot')
    ldf_files = glob.glob(ldf_directory + '/*.ldf')

    if not os.path.exists(snapshot_directory):
        os.mkdir(snapshot_directory)

    for ldf in ldf_files:
        data = ldfparser.parse_ldf_to_dict(ldf)
        output_path = os.path.join(snapshot_directory, os.path.basename(ldf)) + '.json'
        with open(output_path, 'w+') as output:
            json.dump(data, output)
