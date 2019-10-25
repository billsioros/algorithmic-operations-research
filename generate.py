
# MIT License
#
# Copyright (c) 2019 Vasileios Sioros
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.

import re

import os

import time

import locale

import json

import argparse

from tika import parser


config_path = os.path.join(os.getcwd(), "config.json")

config_template = {
    "title": {
    },
    "authors": [
    ],
    "packages": [
    ],
    "commands": {
    },
    "environments": {
    }
}

tex_project_template = \
"""
\\documentclass[12pt]{{article}}

\\usepackage[utf8]{{inputenc}}
\\usepackage[greek, english]{{babel}}
\\usepackage{{{packages}}}

{commands}

{environments}

\\setlength{{\\parindent}}{{0in}}
\\setlength{{\\oddsidemargin}}{{0in}}
\\setlength{{\\textwidth}}{{6.5in}}
\\setlength{{\\textheight}}{{10in}}
\\setlength{{\\topmargin}}{{-1.0in}}
\\setlength{{\\headheight}}{{18pt}}

\\titlespacing*{{\\subsection}}
{{0pt}}{{5.5ex plus 1ex minus .2ex}}{{4.3ex plus .2ex}}

\\title{{\\huge{primary_title}\\\\{secondary_title}}}
\\author{{{authors}}}
\\date{{{date}}}

\\begin{{document}}

\\maketitle

\\thispagestyle{{empty}}

\\pagebreak

\\pagenumbering{{arabic}}

{subsections}

\\end{{document}}
"""


def parse_command(command, args_count_rgx=r"#[1-9][0-9]*"):

    signature, body = command

    args_count = len(re.findall(args_count_rgx, body, flags=re.UNICODE))

    args_str = f"[{args_count}]" if args_count > 0 else ""

    return f"\\newcommand{{{signature}}}{args_str}{{{body}}}"


def parse_environment(environment):

    signature, body = environment

    begin, end = body["begin"], body["end"]

    return f"\\newenvironment{{{signature}}}\n\t{{{begin}}}\n\t{{{end}}}"


def parse_section(section):

    section = section.strip()

    section = re.sub(r"\n\n+", "\n", section, flags=re.UNICODE)

    section = re.sub(r"[^\S\n]+", " ", section, flags=re.UNICODE)

    return f"\n\n\\subsection*{{{section}}}\n\n\\vspace{{2in}}\n\n\\pagebreak"


def parse_seed(seed, section_rgx=r"([1-9][0-9]*\.[^\S\n]*?.+?[\?\.]\n+)(?=([1-9][0-9]*\.[^\S\n]*?.+?[\?\.]\n+)|($)|(.*))"):

    sections = parser.from_file(seed)['content']

    sections = sections.encode('utf8', 'strict').decode('ascii', 'ignore')

    sections = re.findall(section_rgx, sections, flags=re.UNICODE | re.DOTALL)

    sections = map(lambda section: section[0], sections)

    return map(parse_section, sections)


if __name__ == '__main__':

    argparser = argparse.ArgumentParser(description="LaTeX Project Base Generation")

    argparser.add_argument("-l", "--load",      help="specify the input file")
    argparser.add_argument("-s", "--save",      help="specify the output file",           required=True)
    argparser.add_argument("-d", "--directory", help="make parent directories as needed", action="store_true")
    argparser.add_argument("-o", "--overwrite", help="enable overwriting",                action="store_true")

    args = argparser.parse_args()


    if os.path.exists(args.save):

        if not args.overwrite:

            raise ValueError(f"Permission to overwrite '{args.save}' has not been granted")

    else:

        if args.directory:

            os.makedirs(os.path.dirname(args.save))


    if not os.path.exists(config_path):

        with open(config_path, "w", encoding="utf8") as config_file:

            json.dump(config_template, config_file, indent=4, sort_keys=True)

            config = config_template

    else:

        with open(config_path, "r", encoding="utf8") as config_file:

            config = json.load(config_file)


    with open(args.save, "w", encoding="utf8") as tex_file:

        locale.setlocale(locale.LC_ALL, "el")

        tex_file.write(
            tex_project_template.format(
                packages=", ".join(sorted(config["packages"])),
                commands='\n'.join(map(parse_command, config["commands"].items())),
                environments='\n'.join(map(parse_environment, config["environments"].items())),
                primary_title=config["title"].get("primary", ""),
                secondary_title=config["title"].get("secondary", ""),
                authors="\\\\".join(config["authors"]),
                date=time.strftime("%B %Y"),
                subsections='\n'.join(parse_seed(args.load)) if args.load else ""
            )
        )
