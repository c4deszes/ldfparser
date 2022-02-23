import os
import sys
import jinja2
import argparse

from ldfparser.ldf import LDF
from ldfparser.parser import parse_ldf

def save_ldf(ldf: LDF, path: str, template_path: str = None) -> None:
    if template_path is None:
        template_path = os.path.join(os.path.dirname(__file__), 'templates', 'ldf.jinja2')

    with open(template_path, 'r') as file:
        template = jinja2.Template(file.read())
        ldf_content = template.render(ldf=ldf)

    with open(path, 'w+') as ldf_file:
        ldf_file.writelines(ldf_content)

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('-f', '--ldf', required=True)
    parser.add_argument('-o', '--output', required=True)
    args = parser.parse_args(sys.argv[1:])

    ldf = parse_ldf(args.ldf)
    save_ldf(ldf, args.output)
