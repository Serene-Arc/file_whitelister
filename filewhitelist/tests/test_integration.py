#!/usr/bin/env python3
# coding=utf-8

import argparse
from pathlib import Path

import pytest

import filewhitelist.__main__ as filewhitelist


@pytest.fixture()
def args():
    args = argparse.Namespace()
    args.whitelist = Path('whitelist_test.txt')
    args.output = Path('.')
    args.directory = Path('.').resolve()
    args.stdout = False
    args.verbosity = 0
    args.levenshtein = None
    return args


def test_basic_stdout_output(capsys: pytest.CaptureFixture, args: argparse.Namespace):
    args.stdout = True
    filewhitelist.main(args)
    captured = capsys.readouterr()
    assert 'Whitelist file loaded' not in captured.out
    assert 'Writing to output' not in captured.out
    assert all([t in captured.out.split('\n') for t in ('whitelist_test.txt', 'test_integration.py', '__init__.py')])
    assert 'test_main.py' not in captured.out.split('\n')


def test_basic_file_output(capsys: pytest.CaptureFixture, args: argparse.Namespace, tmp_path: Path):
    args.output = tmp_path / Path('results.txt')
    filewhitelist.main(args)
    captured = capsys.readouterr()
    assert args.output.exists()
    assert 'Whitelist file loaded' in captured.out
    assert 'Writing to output' in captured.out
    assert '3 files not in whitelist found' in captured.out
