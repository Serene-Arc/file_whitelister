#!/usr/bin/env python3
# encoding=utf-8

import pathlib

import pytest

import filewhitelist.__main__ as filewhitelist


@pytest.mark.parametrize(('whitelist', 'test_str'), ((['test.txt'], 'test.txt'),
                                                     (['test1.txt', 'test2.txt'], 'test1.txt')))
def test_file_normal_test_good(whitelist: list[str], test_str: str):
    test_file = pathlib.Path(test_str)
    result = filewhitelist.test_file_regular(whitelist, test_file)
    assert result is True


@pytest.mark.parametrize(('whitelist', 'test_str'), ((['test.txt'], 'random.txt'),
                                                     (['test1.txt', 'test2.txt'], 'random.txt')))
def test_file_normal_test_bad(whitelist: list[str], test_str: str):
    test_file = pathlib.Path(test_str)
    result = filewhitelist.test_file_regular(whitelist, test_file)
    assert result is False


@pytest.mark.parametrize(('whitelist', 'test_str', 'distance'), ((['test.txt'], 'tes.txt', 1),
                                                                 (['test1.txt', 'test2.txt'], 'test3.txt', 1),
                                                                 (['test.txt'], 'test00.txt', 2),
                                                                 (['test.txt'], 'test.txt', 2),
                                                                 (['test.txt', 'random.mp3'], 'test00.txt', 2)))
def test_file_levenshtein_test_good(whitelist: list[str], test_str: str, distance: int):
    test_file = pathlib.Path(test_str)
    result = filewhitelist.test_file_levenshtein(whitelist, test_file, distance)
    assert result is True


@pytest.mark.parametrize(('whitelist', 'test_str', 'distance'), ((['test.txt'], 'random.txt', 0),
                                                                 (['test.txt'], 'random', 1)))
def test_file_levenshtein_test_bad(whitelist: list[str], test_str: str, distance: int):
    test_file = pathlib.Path(test_str)
    result = filewhitelist.test_file_levenshtein(whitelist, test_file, distance)
    assert result is False
