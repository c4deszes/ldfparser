"""
Module contains functions for saving LDF objects
"""
import os
import sys
import jinja2
import argparse
from typing import Union

from ldfparser.ldf import LDF
from ldfparser.parser import parse_ldf

def save_ldf(ldf: LDF,
             output_path: Union[str, bytes, os.PathLike],
             template_path: Union[str, bytes, os.PathLike] = None) -> None:
    """
    Saves an LDF object as an `.ldf` file

    :param ldf: LDF object
    :type ldf: LDF
    :param output_path: Path where the file will be saved
    :type output_path: PathLike
    :param template_path: Path where the template is located, if not specified then an internal
                          template will be used
    :type template_path: PathLike
    """
    if template_path is None:
        template_path = os.path.abspath(os.path.join(os.path.dirname(__file__), 'templates', 'ldf.jinja2'))

    with open(template_path, 'r') as file:
        template = jinja2.Template(file.read())
        ldf_content = template.render(ldf=ldf)

    with open(output_path, 'w+') as ldf_file:
        ldf_file.writelines(ldf_content)

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('-f', '--ldf', required=True)
    parser.add_argument('-o', '--output', required=True)
    parser.add_argument('-t', '--template', required=False)
    args = parser.parse_args(sys.argv[1:])

    ldf = parse_ldf(args.ldf)
    save_ldf(ldf, args.output, args.template)

if __name__ == '__main__':
    main()
