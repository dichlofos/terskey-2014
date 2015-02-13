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
        for line in track_file:
            lines.append(line)
    return lines


def filter_by_day(lines, day, output_file_name):
    """Filter track items by day and fix dates."""
    started = False
    cur_point = None
    mask = '2014-08-{}'.format(day)
    print mask

    output_file = open(output_file_name, 'w')

    for line in lines:
        tr_line = line.strip()
        if tr_line.startswith('<trkpt'):
            started = True
            cur_point = []

        if started:
            cur_point.append(line)

        if tr_line.startswith('</trkpt'):
            started = False
            # process point
            good = False
            for l in cur_point:
                #print l, mask
                if mask in l:
                    print 'good', l
                    # matching cur point to day mask
                    good = True

            if good:
                for l in cur_point:
                    output_file.write(l)
            continue

        # else just output line
        output_file.write(line)



    print day
    return


def main():
    """Gravicappa"""
    file_name = 'track.gpx'
    lines = read_lines(file_name)

    for day in xrange(4, 5):
        sday = str(day)
        if len(sday) < 2:
            sday = '0' + sday

        output_file_name = file_name.replace('.gpx', '-{}.gpx'.format(sday))
        print "Output", sday, "to", output_file_name
        filter_by_day(lines, sday, output_file_name)


if __name__ == '__main__':
    main()
