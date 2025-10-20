#!/usr/bin/python3
#
# Copyright (C) 2023-2025 The Phosh developers
#
# SPDX-License-Identifier: GPL-3.0-or-later
#
# Author: Guido Günther <agx@sigxcpu.org>
#
# Create a phosh release in gitlab

import argparse
import gitlab
import os
import sys
import subprocess

NEWS_PATH = "./NEWS"


def parse_news(filename, version):
    news = ''
    ui_translations = ''

    with open(filename) as f:
        line = f.readline()
        if not line.strip().endswith(version):
            print("NEWS entry doesn't match tag")
            return 1

        in_header = True
        in_ui = False
        for line in f:
            # Skip until first bullet point
            if in_header and line[0] != '*':
                continue
            else:
                in_header = False

            if line.startswith("* UI translations"):
                in_ui = True

            if line.strip() == '':
                break

            if in_ui:
                ui_translations += line
            else:
                news += line

    return news, ui_translations


def get_since(version):
    """
    Get the previous release version

    >>> get_since("0.1.0")
    '0.0.0'
    >>> get_since("0.45.0")
    '0.44.0'
    >>> get_since("0.0.6")
    '0.0.5'
    >>> get_since("1.0.1")
    '1.0.0'
    """
    # For alpha, beta, etc we don't include any prior releases
    if '~' in version:
        return version
    (major, minor, micro) = [int(x) for x in version.split('.')]
    # Bug fix releases
    if (major != 0 or minor != 0) and micro != 0:
        micro -= 1
    # New "major releases
    elif major == 0 and minor == 0:
        micro -= 1
    elif major == 0 and micro == 0:
        minor -= 1
    elif minor == 0 and micro == 0:
        major -= 1
    return f"{major}.{minor}.{micro}"


def main(argv):
    parser = argparse.ArgumentParser(os.path.basename(argv[0]),
                                     description='''Make a release''')
    parser.add_argument('-i', '--project-id', dest='id',
                        help='The repo id',
                        type=int)
    parser.add_argument('--url', dest='url',
                        default="https://gitlab.gnome.org",
                        help='The repo id',
                        type=str)
    parser.add_argument('--tarballs', dest='tarballs',
                        help='Location of signed release tarballs',
                        type=str)
    parser.add_argument('--dry-run', action=argparse.BooleanOptionalAction,
                        help="Parse, don't publish")
    args = parser.parse_args(argv[1:])

    gitlab_token = os.getenv("GITLAB_TOKEN")
    if not gitlab_token:
        print("Need to set GITLAB_TOKEN in environment")
        return 1

    if not args.id:
        print("No project id")
        return 1

    ret, version = subprocess.getstatusoutput("dpkg-parsechangelog -SVersion")
    if ret:
        print("Failed to get version from changelog", file=sys.stderr)
        return 1
    if version is None:
        return 1

    since = get_since(version)
    ret, changes = subprocess.getstatusoutput(f"dpkg-parsechangelog -SChanges --since {since}")
    if ret:
        print("Failed to get debian/changelog changes", file=sys.stderr)
        return 1
    ret, source = subprocess.getstatusoutput("dpkg-parsechangelog -SSource")
    if ret:
        print("Failed to get source package ", file=sys.stderr)
        return 1
    ret, tag = subprocess.getstatusoutput("git describe HEAD")
    if ret:
        print("Failed to describe HEAD", file=sys.stderr)
        return 1
    if not tag or ' ' in tag:
        print(f"Can't get tag: {tag}")
        return 1

    version = tag.replace('_', '~')
    if version.startswith('v'):
        version = version[1:]

    print(f"Releasing {tag}, version: {version} on {args.url}")

    news = ''
    translations = ''
    if os.path.exists(NEWS_PATH):
        news, translations = parse_news(NEWS_PATH, version)

    if translations:
        translations = f"""
i18n updates
============
{translations}
"""
    notes = ''
    if os.path.exists(".git/notes"):
        with open(".git/notes") as f:
            notes = f.read()

    name = f"{source} {version}"
    message = f"""Summary of changes
==================
{news}{translations}
Detailed changes
================

```{changes}
```
{notes}
"""

    if args.dry_run:
        print(message)
        return

    gl = gitlab.Gitlab(args.url, private_token=gitlab_token)
    project = gl.projects.get(args.id)
    release = project.releases.create(
        {
            'name': name,
            'tag_name': tag,
            'description': message,
        })

    if args.tarballs and len(args.tarballs):
        release.links.create({"url": args.tarballs, "name": "Signed release tarballs"})

    return 0


if __name__ == '__main__':
    sys.exit(main(sys.argv))
