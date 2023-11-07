import argparse
import logging
import os
import sys

from linkedin_parser.config import config
from linkedin_parser.save_html import save_html
from linkedin_parser.urls_generator import generate_search_urls
from linkedin_parser.info_extractor import extract_info


logger = logging.getLogger('linkedin_parser')
logger.setLevel(logging.DEBUG)
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
ch = logging.StreamHandler()
ch.setLevel(logging.DEBUG)
ch.setFormatter(formatter)
logger.addHandler(ch)


def build_parser():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        '-c', '--config', dest='config_file', action='store', type=str,
        help='path to custom config file', default=''
    )
    parser.add_argument(
        '-d', '--data', dest='data_path', action='store', type=str,
        help='path to data directory', default=""
    )
    subparsers = parser.add_subparsers(
        dest="action", help='actions'
    )

    gen_urls_parser = subparsers.add_parser(
        'gen_urls', help='generate search URLs'
    )
    gen_urls_parser.add_argument(
        '-o', '--output', dest='output_file', action='store', type=str,
        help='output file to store URLs',
        default=None
    )
    gen_urls_parser.add_argument(
        '-i', '--input', dest='input_file', action='store', type=str,
        help='input file with database results',
        required=True
    )
    save_html_parser = subparsers.add_parser(
        'save_html', help='save html pager for stdin entries'
    )
    save_html_parser.add_argument(
        '-i', '--input', dest='input_file', action='store', type=str,
        help='input file with URLs',
        required=True
    )
    save_html_parser.add_argument(
        '-o', '--output', dest='output_path', action='store', type=str,
        help='output directory for HTML dump',
        default=None
    )
    extract_parser = subparsers.add_parser(
        'extract', help='extract info from linkedin HTML dump'
    )
    extract_parser.add_argument(
        '-i', '--html', dest='html_path', action='store', type=str,
        help='directory with HTML files to parse',
        default=None
    )
    extract_parser.add_argument(
        '-o', '--output', dest='output_file', action='store', type=str,
        help='output file to store extracted info',
        default=None
    )
    return parser


def main():
    parser = build_parser()
    params, other_params = parser.parse_known_args()
    if params.config_file:
        config.update_from_file(params.config_file)
    if params.data_path:
        config.DATA["path"] = params.data_path

    if params.action == "gen_urls":
        if params.output_file is None:
            print("snake")
            params.output_file = os.path.join(config.DATA["path"], 'linkedin_urls.csv')
            print(config.DATA["path"])
        with open(params.input_file, "r") as f:
            generate_search_urls(f, params.output_file)
    elif params.action == "save_html":
        if params.output_path is None:
            params.output_path = os.path.join(config.DATA["path"])
        with open(params.input_file, "r") as f:
            save_html(f, params.output_path)
    elif params.action == "extract":
        if params.output_file is None:
            params.output_file = os.path.join(config.DATA["path"], 'linkedin_analysis.csv')
        if params.html_path is None:
            params.html_path = config.DATA["path"]

        extract_info(params.html_path, params.output_file)
    else:
        parser.print_help()
