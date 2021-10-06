import os
import zipfile
from shutil import copy2 as cp
from pdf_compressor.utils import sizeof_fmt, load_dotenv, del_or_keep_compressed
from os.path import dirname, isfile

pdf_path = "assets/dummy.pdf"


def file_test_creator(filename: str, content: str):
    f = open(filename, 'a')
    f.write(content)
    f.close()


def test_sizeof_fmt():
    assert sizeof_fmt(123456) == "120.6 KB"

    assert sizeof_fmt(123456789, 3) == sizeof_fmt(123456789, prec=3) == "117.738 MB"


def test_load_env():
    test_file = f"{dirname(__file__)}/.env.test"

    file_test_creator(test_file, "APP_TEST=test")

    load_dotenv(filepath=test_file)

    os.remove(test_file)

    assert os.getenv('APP_TEST') == 'test'


def test_load_commented_env():
    test_file = f"{dirname(__file__)}/.env.test_commented"

    file_test_creator(test_file, "#APP_TEST=test")

    load_dotenv(filepath=test_file)

    os.remove(test_file)

    assert os.getenv('COMMENT') is None


def test_load_empty_env():
    test_file = f"{dirname(__file__)}/.env.empty"

    file_test_creator(test_file, "")

    load_dotenv(filepath=test_file)

    os.remove(test_file)

    assert os.getenv('APP_EMPTY') is None


def test_del_or_keep_compressed_without_diff_compression():
    dummy_1 = "assets/dummy-1.pdf"
    dummy_2 = "assets/dummy-2.pdf"
    archive = "assets/compressed.zip"

    cp(pdf_path, dummy_1)
    cp(pdf_path, dummy_2)

    with zipfile.ZipFile(archive, mode='w') as z:
        z.write(dummy_1)
        z.write(dummy_2)

    try:
        del_or_keep_compressed([dummy_1, dummy_2], archive, inplace=False, suffix='test')
    finally:
        assert isfile(archive) is False


def test_del_or_keep_compressed_with_diff_compression():
    dummy_1 = "assets/dummy-1.pdf"
    archive = "assets/compressed.zip"
    keep_with_suffix = "assets/dummy-1_compressed.pdf"

    empty_file = 'assets/empty_file.pdf'
    open(empty_file, 'a')

    cp(pdf_path, dummy_1)

    with zipfile.ZipFile(archive, mode='w') as z:
        z.write(empty_file)

    try:
        del_or_keep_compressed([dummy_1], archive, inplace=False, suffix='_compressed')

        assert isfile(archive) is False
        assert isfile(dummy_1) is True
        assert isfile(empty_file) is True
        assert isfile(keep_with_suffix) is True

    finally:
        os.remove(dummy_1)
        os.remove(empty_file)
        os.remove(keep_with_suffix)

