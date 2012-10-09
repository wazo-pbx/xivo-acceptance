# -*- coding: UTF-8 -*-

import re
import datetime


def _rec_update_dict(base_dict, overlay_dict):
    for k, v in overlay_dict.iteritems():
        if isinstance(v, dict):
            old_v = base_dict.get(k)
            if isinstance(old_v, dict):
                _rec_update_dict(old_v, v)
            else:
                base_dict[k] = {}
                _rec_update_dict(base_dict[k], v)
        elif isinstance(v, list):
            if k in base_dict:
                base_dict[k].extend(v)
            else:
                base_dict[k] = v
        else:
            base_dict[k].append(v)


def extract_number_and_context_from_extension(extension, default_context='default'):
    if re.search('@', extension):
        exten = extension.split('@')
        number = exten[0]
        context = exten[1]
        ret = (number, context)
    else:
        ret = (extension, default_context)
    return ret


def read_last_log_lines(logs,
                        min_timestamp,
                        date_format="%b %d %H:%M:%S",
                        date_pattern="^[\w]{3} [\d ]{2} [\d]{2}:[\d]{2}:[\d]{2}"):
    now = datetime.datetime.now()
    current_year = now.year
    date_match = re.compile(date_pattern, re.I)

    lines = []
    for line in logs:
        if line == '' or not date_match.match(line):
            continue
        datetext = line[0:15]
        timestamp = datetime.datetime.strptime(datetext, date_format)
        #Needed so that the timestamp has the right year
        timestamp = datetime.datetime(
            year=current_year,
            month=timestamp.month,
            day=timestamp.day,
            hour=timestamp.hour,
            minute=timestamp.minute,
            second=timestamp.second)

        if timestamp >= min_timestamp:
            lines.append(line)

    return lines
