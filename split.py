#!/usr/bin/env python
# coding: utf-8
"""
Track splitter.

Written by Mikhail Veltishchev <dichlofos-mv@yandex.ru>
"""

import os
import sys
import dateutil.parser
import datetime
import argparse


def _read_lines(file_name):
    """ Read file by lines. """
    lines = []
    with open(file_name) as track_file:
        for line in track_file:
            lines.append(line)
    return lines


def _fix_time(point_line, time_offset=6):
    """ Fix time offset. """
    if not '<time' in point_line:
        return point_line

    # kyrgyzstan time offset GMT+6
    time = point_line.replace('<time>', '').replace('</time>', '')

    line_datetime = dateutil.parser.parse(time) + datetime.timedelta(hours=time_offset)
    return '<time>' + line_datetime.isoformat() + '</time>\n'


def filter_by_day(lines, day, output_file_name, time_offset):
    """ Filter track items by day and fix dates. """
    started = False
    cur_point = None
    some_points = False
    mask = '2014-08-{}'.format(day)
    #print "Using mask", mask

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
            good = any(mask in l for l in cur_point)

            if good:
                some_points = True
                for point_line in cur_point:
                    point_line = _fix_time(
                        point_line=point_line,
                        time_offset=time_offset,
                    )
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

    parser = argparse.ArgumentParser()
    parser.add_argument(
        "-t", "--time-offset",
        type=int,
        help="Time offset")

    parser.add_argument(
        "-i", "--track",
        type=str,
        required=True,
        help="Input track name"
    )

    parser.add_argument(
        "-w", "--waypoints",
        type=str,
        help="Input waypoints name"
    )

    args = parser.parse_args()

    time_offset = 6
    if args.time_offset is not None:
        time_offset = args.time_offset
    print "Using time offset", time_offset

    file_name = args.track
    if not file_name.endswith('.gpx'):
        print "I cannot handle non-GPX-tracks"
        sys.exit(1)

    lines = _read_lines(file_name)

    for day in xrange(1, 30):
        sday = str(day)
        if len(sday) < 2:
            sday = '0' + sday

        output_file_name = file_name.replace('.gpx', '-{}.gpx'.format(sday))
        print "Output", sday, "to", output_file_name
        filter_by_day(
            lines=lines,
            day=sday,
            output_file_name=output_file_name,
            time_offset=time_offset,
        )

    if args.waypoints:
        output_wpt_file_name = args.waypoints.replace('.gpx', '-fixed-local-time.gpx')
        output_wpt_file = open(output_wpt_file_name, 'w')

        wpt_lines = _read_lines(args.waypoints)
        for line in wpt_lines:
            line = _fix_time(
                point_line=line,
                time_offset=time_offset,
            )
            output_wpt_file.write(line)

        print "Waypoints with fixed time written to", output_wpt_file_name


if __name__ == '__main__':
    main()
