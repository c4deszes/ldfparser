from parso import parse
import pytest
import glob
import json
import os

from ldfparser import parse_ldf, save_ldf

ldf_directory = os.path.join(os.path.dirname(__file__), 'ldf')
snapshot_directory = os.path.join(os.path.dirname(__file__), 'snapshot')
ldf_files = glob.glob(ldf_directory + '/*.ldf')

class TestSave:

    @pytest.mark.unit
    @pytest.mark.parametrize(('ldf_path'), ldf_files)
    def test_resave(self, ldf_path):
        """
        Tests whether the loaded LDFs can be saved as is, and then reloaded without any errors
        """
        ldf = parse_ldf(ldf_path)
        output_path = os.path.join(os.path.dirname(__file__), 'tmp', 'test_resave_' + os.path.basename(ldf_path))
        save_ldf(ldf, output_path)

        new_ldf = parse_ldf(output_path)
