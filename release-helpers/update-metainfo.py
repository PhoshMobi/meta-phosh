#!/usr/bin/python3
#
# Copyright (C) 2026 Phosh.mobi e.V.
#
# SPDX-License-Identifier: GPL-3.0-or-later
#
# Author: Guido Günther <agx@sigxcpu.org>
#
# Update metainfo with notes

import argparse
import datetime
import glob
import os
import shutil
import sys

NEWS_PATH = "./NEWS"


def parse_news(filename):
    news = []

    with open(filename) as f:
        line = f.readline()

        version = line.split()
        if len(version) != 2:
            print(f"Failed to parse version, got {len(version)} parts")
            sys.exit(1)

        version = version[1]

        in_header = True
        in_ui = False
        in_contributors = False
        in_issues = False
        have_translations = True
        for line in f:
            # Skip until first bullet point
            if in_header and line[0] != "*":
                continue
            else:
                in_header = False

            if line.startswith("* UI translations"):
                in_ui = True
                in_contributors = in_issues = False
                have_translations = True
            elif line.startswith("* Contributors:"):
                in_contributors = True
                in_ui = in_issues = False
            elif line.startswith("* Issues fixed:"):
                in_issues = True
                in_ui = in_contributors = False

            if line.strip() == "":
                break

            if not in_ui and not in_contributors and not in_issues:
                # Multiline item
                if line.startswith("  "):
                    news[-1] += ' ' + line.strip()
                else:
                    if line.startswith("* "):
                        news.append(line[2:].strip())
                    else:
                        news.append(line)

        if have_translations:
            news.append("Translation updates")

    return version, news


def guess_metainfo():
    files = glob.glob("data/*.metainfo.xml*")
    if len(files) != 1:
        print("Found no or more than one metainfo file", file=sys.stderr)
        sys.exit(1)
    return files[0]


def build_xml(news, version, date):
    xml = f"""    <release version=\"{version}\" date=\"{date}\">
      <description translate="no">\n"""
    if len(news) == 1:
        xml += "        <p>{line[0]}</p>\n"
    else:
        xml += "        <ul>\n"
        for line in news:
            xml += f"          <li>{line}</li>\n"

        xml += "        </ul>\n"
    xml += """      </description>
    </release>\n\n"""
    return xml


def main(argv):
    parser = argparse.ArgumentParser(
        os.path.basename(argv[0]), description="""Update metainfo"""
    )
    parser.add_argument(
        "--metainfo",
        dest="metainfo",
        default=None,
        help="The metainfo file to to update",
        type=str,
    )
    parser.add_argument(
        "--dry-run", action=argparse.BooleanOptionalAction, help="Parse, don't publish"
    )
    args = parser.parse_args(argv[1:])

    if args.metainfo:
        metainfo = args.metainfo
    else:
        metainfo = guess_metainfo()

    dt = datetime.datetime.now()
    date = dt.date().isoformat()

    version, news = parse_news(NEWS_PATH)

    print(f"Updating {metainfo} with {version}")

    xml = build_xml(news, version, date)

    if args.dry_run:
        print(xml)
        return 0

    found_releases = False
    tmp_metainfo = f"{metainfo}.tmp"
    with open(metainfo) as infile:
        with open(tmp_metainfo, 'w') as outfile:

            for line in infile:
                outfile.write(line)
                if "<releases>" in line:
                    found_releases = True
                    outfile.write(xml)

    if found_releases:
        shutil.move(tmp_metainfo, metainfo)
    else:
        print("Didn't find release section, plesae insert xml manually")
        print(xml)
        return 1

    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
