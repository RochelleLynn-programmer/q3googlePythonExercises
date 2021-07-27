"""Copyspecial Assignment"""

# Copyright 2010 Google Inc.
# Licensed under the Apache License, Version 2.0
# http://www.apache.org/licenses/LICENSE-2.0

import re
import os
import sys
import shutil
import subprocess
import argparse


__author__ = """Rochelle Edwards (rochellelynn-programmer)"""


def get_special_paths(dirname):
    """Given a dirname, returns a list of all its special files."""
    dirs_list = os.listdir(dirname)
    special_list = []
    for item in dirs_list:
        is_special = re.search(r'_{2}\w+_{2}', item)
        if is_special:
            special_item_path = os.path.abspath(os.path.join(dirname, item))
            special_list.append(special_item_path)
    return special_list


def copy_to(path_list, dest_dir):
    """given a list of file paths, copies those files into the given dir"""
    dest_path = os.path.join(os.getcwd(), dest_dir)
    if not os.path.isdir(dest_path):
        os.makedirs(dest_path)
    for item in path_list:
        shutil.copy(item, dest_path)


def zip_to(path_list, dest_zip):
    """given a list of file paths, zip the files up into the given zip path"""
    run_list = ["zip", "-j", dest_zip]
    run_list.extend(path_list)
    try:
        zipped_file = subprocess.run(run_list)
        print(f'Command I am going to do: {" ".join(run_list)}')
    except zipped_file.returncode != 0:
        print(zipped_file.stderr)


def create_parser():
    """Create a command line parser with 3 definitions"""
    parser = argparse.ArgumentParser()
    parser.add_argument('--todir', help='dest dir for special files')
    parser.add_argument('--tozip', help='dest zipfile for special files')
    parser.add_argument('from_dir', help='returns list of special files')
    return parser


def main(args):
    """Main driver code for copyspecial."""
    parser = create_parser()

    ns = parser.parse_args(args)

    if not ns:
        parser.print_usage()
        sys.exit(1)

    dir_list = ns.from_dir
    todir = ns.todir
    tozip = ns.tozip

    special_list = get_special_paths(dir_list)

    if todir:
        copy_to(special_list, todir)
    elif tozip:
        zip_to(special_list, tozip)
    else:
        for item in special_list:
            print(item)


if __name__ == "__main__":
    main(sys.argv[1:])
