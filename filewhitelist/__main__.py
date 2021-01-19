#!/usr/bin/env python3

import argparse
import logging
import pathlib
import sys
from typing import Optional

import Levenshtein

parser = argparse.ArgumentParser()
logger = logging.getLogger()


def load_whitelist(file_location: pathlib.Path) -> list[str]:
    file_list = []
    with open(file_location, 'r') as file:
        for line in file:
            file_list.append(line.strip())
    return file_list


def _create_parser_options():
    parser.add_argument('whitelist', help='text file with list of files')
    parser.add_argument('directory', help='directory to scan')
    parser.add_argument('-l', '--levenshtein', nargs='?', type=int, const=1, default=None)
    parser.add_argument('-v', '--verbose', action='count', default=0)

    output_group = parser.add_mutually_exclusive_group()
    output_group.add_argument('-o', '--output', type=str, default='results.txt')
    output_group.add_argument('-s', '--stdout', action='store_true')


def _setup_logging(stdout_enabled: bool, verbosity: int):
    logger.setLevel(1)
    formatter = logging.Formatter('[%(asctime)s - %(name)s - %(levelname)s] - %(message)s')
    if verbosity <= 0:
        logger_level = logging.INFO
    else:
        logger_level = logging.DEBUG
    if not stdout_enabled:
        stream = logging.StreamHandler(sys.stdout)
        stream.setFormatter(formatter)
        stream.setLevel(logger_level)
        logger.addHandler(stream)


def test_file_levenshtein(white_list: list[str], test_file: pathlib.Path, levenshtein_distance: int) -> bool:
    for white_listed_file in white_list:
        if Levenshtein.distance(white_listed_file, test_file.name) <= levenshtein_distance:
            return True
    return False


def test_file_regular(whitelist: list[str], test_file: pathlib.Path) -> bool:
    return test_file.name in whitelist


def search_directory(directory: pathlib.Path, white_list: list[str], levenshtein: Optional[int]) -> list[pathlib.Path]:
    found_files = []
    for existing_file in directory.iterdir():
        if levenshtein is not None:
            if not test_file_levenshtein(white_list, existing_file, levenshtein):
                found_files.append(existing_file)
        else:
            if not test_file_regular(white_list, existing_file):
                found_files.append(existing_file)
    return found_files


def write_results(output_file: pathlib.Path, file_list):
    with open(output_file, 'w') as result_file:
        for ff in file_list:
            result_file.write(ff.name + '\n')


def main(args: argparse.Namespace):
    _setup_logging(args.stdout, args.verbosity)

    args.output = pathlib.Path(args.output).resolve()
    args.whitelist = pathlib.Path(args.whitelist).resolve()
    args.directory = pathlib.Path(args.directory).resolve()

    if not args.whitelist.is_file():
        raise Exception('file argument must be a file')
    if not args.directory.is_dir():
        raise Exception('directory argument must be a directory')

    white_list = load_whitelist(args.whitelist)
    logger.info('Whitelist file loaded')

    found_files = search_directory(args.directory, white_list, args.levenshtein)
    logger.info('{} files not in whitelist found'.format(len(found_files)))

    logger.info('Writing to output')
    if args.stdout is False:
        write_results(args.output, found_files)
    else:
        for result in found_files:
            print(result.name)


if __name__ == "__main__":
    _create_parser_options()
    main(parser.parse_args())
