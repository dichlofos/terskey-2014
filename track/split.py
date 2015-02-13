#!/usr/bin/env python
# coding: utf-8

"""
    Track splitter
"""

#import os
#import sys


def read_lines(file_name):
    """ Read file by lines"""
    lines = []
    with open(file_name) as track_file:
        lines.append(track_file.readline())
    return lines


def filter_by_day(lines, day, output_file_name):
    """Filter track items by day and fix dates."""
    print day
    return


def main():
    """Gravicappa"""
    file_name = 'track.gpx'
    lines = read_lines(file_name)
    print lines
    for day in xrange(1, 20):
        sday = str(day)
        if len(sday) < 2:
            sday = '0' + sday

        output_file_name = file_name.replace('.gpx', '-{}.gpx'.format(sday))
        filter_by_day(lines, day, output_file_name)

