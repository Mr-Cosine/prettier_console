import json
import string
import os

def _get_cset(style):
    script_dir = os.path.dirname(os.path.abspath(__file__))
    try:
        cset = json.load(open(os.path.join(script_dir, 'font', f'{style}.json'), 'r', encoding='utf-8'))
    except FileNotFoundError:
        raise Exception(f"Invalid style {style}: not supported by the font library")
    except Exception as e:
        raise Exception(f"Error loading style {style}: {str(e)}")
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
        
def parse_font_file(path):
    """
    parse a text file into a character set dictionary for a font style.

    each line is one row of the glyphs: the 26 letters (A-Z) followed by the
    space character, each segment separated by '/'.

    :param path:            string,     path to the font text file

    :return:                dict,       {char: {'1': string, '2': string, ...}}
    """
    with open(path, 'r', encoding='utf-8') as f:
        lines = f.read().splitlines()

    if len(lines) == 0:
        raise Exception('Font file error: file is empty')

    characters = list(string.ascii_uppercase) + [' ']
    cset = {character: {} for character in characters}

    for i, line in enumerate(lines):
        segments = line.split('/')
        if len(segments) != len(characters):
            raise Exception(
                f"Font file error: line {i + 1} has {len(segments)} '/'-separated segments, "
                f'expected {len(characters)} (A-Z + space).'
            )
        for character, segment in zip(characters, segments):
            cset[character][str(i + 1)] = segment

    return cset

def set_cset(style, font_path):
    """
    parse a font text file and add or replace a style under ascii_art_font/font/.

    :param style:           string,     the style key to save the parsed font under
    :param font_path:       string,     path to the font text file
    """
    script_dir = os.path.dirname(os.path.abspath(__file__))
    font_dir = os.path.join(script_dir, 'font')
    os.makedirs(font_dir, exist_ok=True)
    json_path = os.path.join(font_dir, f'{style}.json')

    data = parse_font_file(font_path)

    with open(json_path, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=4)

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