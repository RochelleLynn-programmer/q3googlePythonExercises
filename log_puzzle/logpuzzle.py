# Log Puzzle exercise

# Copyright 2010 Google Inc.
# Licensed under the Apache License, Version 2.0
# http://www.apache.org/licenses/LICENSE-2.0

import os
import re
import sys
import urllib.request
import argparse

__author__ = """Rochelle Edwards (rochellelynn-programmer)"""


def sort_urls(url_list):
    """Takes in a list of unique links and sorts them based off the string
    after the final dash if regex is true, sorts regularly otherwise"""
    reg_pattern_determine_sort = r"\w+-\w+-\w+.jpg$"
    sort_on_last = re.search(reg_pattern_determine_sort, url_list[1])
    if not sort_on_last:
        sorted_urls = sorted(url_list)
    else:
        url_list.sort(key=lambda x: x.split('-')[-1])
        sorted_urls = url_list
    return sorted_urls


def read_urls(filename):
    """Returns a list of the puzzle URLs from the given log file,
    extracting the hostname from the filename itself, sorting
    alphabetically in increasing order, and screening out duplicates.
    """
    reg_pattern_link = r'GET\s(\S+puzzle\S+)\s'
    reg_pattern_filename = r"\S_(\S+)"
    with open(filename, "r") as f:
        contents = f.read()
    matched_links = re.findall(reg_pattern_link, contents)
    add_to_link = re.findall(reg_pattern_filename, filename)
    formated_links = []
    matched_links = list(set(matched_links))
    sorted_links = sort_urls(matched_links)
    for link in sorted_links:
        formated_links.append(f"http://{add_to_link[0]}{link}")
    return formated_links


def download_images(img_urls, dest_dir):
    """Given the URLs already in the correct order, downloads
    each image into the given directory.
    Gives the images local filenames img0, img1, and so on.
    Creates an index.html in the directory with an <img> tag
    to show each local image file.
    Creates the directory if necessary.
    """
    img_link_list = ["<html><body>"]
    dest_path = os.path.join(os.getcwd(), dest_dir)
    if not os.path.isdir(dest_path):
        os.makedirs(dest_path)
    for i, url in enumerate(img_urls):
        full_file_name = os.path.join(dest_path, f"img{i}")
        img_link_list.append(f"<img src='img{i}' alt ='an image'>")
        urllib.request.urlretrieve(url, full_file_name)
        print(f"Retrieving {url}")
    img_link_list.append("</body></html>")
    write_to_index_file = "".join(img_link_list)
    with open(f'{dest_dir}/index.html', "w") as f:
        f.write(write_to_index_file)


def create_parser():
    """Creates an argument parser object."""
    parser = argparse.ArgumentParser()
    parser.add_argument('-d', '--todir',
                        help='destination directory for downloaded images')
    parser.add_argument('logfile', help='apache logfile to extract urls from')

    return parser


def main(args):
    """Parses args, scans for URLs, gets images from URLs."""
    parser = create_parser()
    ns = parser.parse_args(args)

    if not ns:
        parser.print_usage()
        sys.exit(1)

    todir = ns.todir
    logfile = ns.logfile

    img_urls = read_urls(logfile)

    if todir:
        download_images(img_urls, todir)
    else:
        print('\n'.join(img_urls))


if __name__ == '__main__':
    main(sys.argv[1:])
