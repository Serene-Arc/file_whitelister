#!/usr/bin/env python3

import argparse
import os
import pathlib

parser = argparse.ArgumentParser()

if __name__ == "__main__":
    parser.add_argument('file', help='text file with list of files')
    parser.add_argument('directory', help='directory to scan')

    args = parser.parse_args()
    args.file = pathlib.Path(args.file).resolve()
    args.directory = pathlib.Path(args.directory).resolve()

    master_list = []
    with open(args.file, 'r') as file:
        for line in file:
            master_list.append(line.strip())

    for file in os.listdir(args.directory):
        if file not in master_list:
            print(file)
