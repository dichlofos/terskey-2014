#!/usr/bin/env python
# coding: utf-8

"""
    Track splitter
    Written by Mikhail Veltishchev <dichlofos-mv@yandex.ru>
"""

import os


def _read_lines(file_name):
    """ Read file by lines. """
    lines = []
    with open(file_name) as track_file:
        for line in track_file:
            lines.append(line)
    return lines


def filter_by_day(lines, day, output_file_name):
    """ Filter track items by day and fix dates. """
    started = False
    cur_point = None
    some_points = False
    mask = '2014-08-{}'.format(day)
    print "Using mask", mask

    output_file = open(output_file_name, 'w')

    for line in lines:
        tr_line = line.strip()
        if tr_line.startswith('<trkpt'):
            started = True
            cur_point = []

        if tr_line.startswith('</trkpt'):
            cur_point.append(line)
            started = False
            # process point
            good = False
            good = any(mask in l for l in cur_point)

            if good:
                some_points = True
                for point_line in cur_point:
                    output_file.write(point_line)
            continue

        if started:
            cur_point.append(line)
            continue

        # else just output line
        output_file.write(line)

    output_file.close()

    if not some_points:
        print "Removing", output_file_name, "as no points written"
        os.unlink(output_file_name)


def main():
    """ Gravicappa. """
    file_name = 'track.gpx'
    lines = _read_lines(file_name)

    for day in xrange(1, 30):
        sday = str(day)
        if len(sday) < 2:
            sday = '0' + sday

        output_file_name = file_name.replace('.gpx', '-{}.gpx'.format(sday))
        print "Output", sday, "to", output_file_name
        filter_by_day(lines, sday, output_file_name)


if __name__ == '__main__':
    main()
