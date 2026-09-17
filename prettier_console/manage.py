"""
command line interface for prettier_console
"""

import zipfile
import hashlib
from datetime import datetime
import argparse
import os
import sys
import string
import subprocess

from .ascii_art_font import ascii_art_font

def _cmd_upgrade(args):
    r = subprocess.run([sys.executable, "-m", "pip", "install", "--upgrade", "prettier_console"])
    if r.returncode != 0:
        print("Upgrade failed — see pip output above.", file=sys.stderr)
    sys.exit(r.returncode)


def _cmd_updatefont(args):
    if args.banner: style = 'banner'
    elif args.header: style = 'header'
    else: style = args.style if args.style else os.path.splitext(os.path.basename(args.path))[0]
    if args.sep: sep = args.sep
    else: raise argparse.ArgumentError("must specify separator for the font.")

    try:
        font_folder_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'ascii_art_font', 'font')
        target_path = os.path.join(font_folder_path, f'{style}.json')

        if os.path.exists(target_path):
            randID = hashlib.md5(f'{datetime.now().timestamp()}'.encode()).hexdigest()
            zip_name = f'{style}-{randID}.zip'
            os.makedirs(os.path.join(font_folder_path, "legacy_fonts"), exist_ok=True)
            zip_path = os.path.join(font_folder_path, "legacy_fonts", zip_name)

            with zipfile.ZipFile(zip_path, 'w', zipfile.ZIP_DEFLATED) as zipf:
                zipf.write(target_path, arcname=f'{style}.json')

        ascii_art_font.set_cset(style, font_path=args.path, sep=sep)
        print(f'Font updated.')
    except Exception as e:
        print(f'Error: {e}', file=sys.stderr)
        sys.exit(1)


def single_char(value):
    if len(value) != 1:
        raise argparse.ArgumentTypeError("Value must be a single character.")
    return value

def style_name(value):
    if any(c not in string.ascii_letters and c not in '1234567890' for c in value):
        raise argparse.ArgumentTypeError("Cannot include non alphanumerical character in style name")
    return value

def main():
    parser = argparse.ArgumentParser(prog='prettier_console')
    subparsers = parser.add_subparsers(dest='command', required=True)

    updatefont = subparsers.add_parser(
        'updatefont',
        help='add or replace an ascii-art font style from a text file'
    )
    updatefont.add_argument(
        'path',
        help="path to a text file with A-Z + space glyphs, one row per line, each character separated by '/'"
    )
    updatefont.add_argument(
        '--sep', 
        type=single_char, 
        required=True,
        help='separator between characters'
    )
    target = updatefont.add_mutually_exclusive_group()
    target.add_argument('--banner', action='store_true', help='save as the banner style')
    target.add_argument('--header', action='store_true', help='save as the header style')
    target.add_argument('--style', type=style_name, help='style name to save as (default: the file name without extension)')
    updatefont.set_defaults(func=_cmd_updatefont)

    upgrade = subparsers.add_parser(
        'upgrade',
        help="update the module to the newest, will reset fonts"
    )
    upgrade.set_defaults(func=_cmd_upgrade)

    args = parser.parse_args()
    args.func(args)

if __name__ == '__main__':
    main()
