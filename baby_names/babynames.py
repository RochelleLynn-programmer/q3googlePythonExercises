# BabyNames python coding exercise.

# Copyright 2010 Google Inc.
# Licensed under the Apache License, Version 2.0
# http://www.apache.org/licenses/LICENSE-2.0

import sys
import re
import argparse

__author__ = """Rochelle Edwards (rochellelynn-programmer)"""


def extract_names(filename):
    """
    Given a single file name for babyXXXX.html, returns a
    single list starting with the year string followed by
    the name-rank strings in alphabetical order.
    ['2006', 'Aaliyah 91', 'Aaron 57', 'Abagail 895', ...]
    """
    names = []
    temp_dict = {}
    with open(filename) as f:
        scrape_names = f.read()
    year_pattern = re.compile(r'Popularity\sin\s(\d\d\d\d)')
    name_pattern = re.compile(r'<td>(\d+)</td><td>(\w+)</td><td>(\w+)</td>')
    year_result = year_pattern.findall(scrape_names)
    name_result = name_pattern.findall(scrape_names)
    names.extend(year_result)
    for name in name_result:
        (rank, male, female) = name
        if male not in temp_dict:
            temp_dict[male] = rank
        if female not in temp_dict:
            temp_dict[female] = rank
    for k, v in temp_dict.items():
        names.append(f'{k} {v}')
    names.sort()
    return names


def create_parser():
    """Create a command line parser object with 2 argument definitions."""
    parser = argparse.ArgumentParser(
        description="Extracts and alphabetizes baby names from html.")
    parser.add_argument(
        '--summaryfile', help='creates a summary file', action='store_true')
    parser.add_argument('files', help='filename(s) to parse', nargs='+')
    return parser


def main(args):
    """Main function, creates the command line parser object with parsing rules. When invokes, collects command line arguments into a namespace"""
    parser = create_parser()

    ns = parser.parse_args(args)

    if not ns:
        parser.print_usage()
        sys.exit(1)

    file_list = ns.files

    create_summary = ns.summaryfile

    for file_name in file_list:
        name_list = extract_names(file_name)
        names = '\n'.join(name_list)
        if create_summary:
            with open(f'{file_name}.summary', "w") as f:
                f.write(names)
        else:
            print(names)


if __name__ == '__main__':
    main(sys.argv[1:])