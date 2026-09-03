import json
import string
import os

def _get_cset(style):
    script_dir = os.path.dirname(os.path.abspath(__file__))
    data = json.load(open(os.path.join(script_dir, 'ascii_font.json'), 'r', encoding='utf-8'))
    cset = data.get(style, None)
    if cset is None:
        raise Exception(f"Invalid style {style}: not supported by the font library")
    return cset

def get_character(char, style):
    if len(char) > 1 or not isinstance(char, str): raise Exception("Chracter invalid: must be a character")
    char = char.upper()

    cset = _get_cset(style)
    output_char = cset.get(char, None)
    if output_char is None:
        missing = 'space' if char == ' ' else char
        raise Exception(f'File error: incomplete ascii character library. Missing character: {missing}')

    return output_char

def list_styles():
    script_dir = os.path.dirname(os.path.abspath(__file__))
    with open(os.path.join(script_dir, 'ascii_font.json'), 'r', encoding='utf-8') as f:
        print(json.load(f).keys())

def build_display(input_string, style, delim=None):
    if len(input_string) < 1: return
    if delim is None: delim = ''

    all_characters = set(input_string.upper())
    cset = {}
    for c in all_characters: cset.update({c: get_character(c, style)})

    print_string = [c.upper() for c in input_string]
    lines = []
    line = 1
    while all(cset.get(c).get(str(line), None) is not None for c in cset):
        lines.append(delim.join(cset.get(char).get(str(line)) for char in print_string))
        line += 1

    width = len(lines[0]) if lines else 0
    return '\n'.join(lines), width
        
def default_print_banner(input_string):
    parsed = input_string.split('\n')
    for line in parsed:
        display_content, length = build_display(line, 'banner', delim=' ')
        print(display_content)
    print('='*length)

def default_print_header(input_string):
    parsed = input_string.split('\n')
    for line in parsed:
        display_content, length = build_display(line, 'header', delim=' ')
        print(display_content)
    print('='*length)