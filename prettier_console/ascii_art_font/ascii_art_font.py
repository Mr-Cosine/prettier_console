import json
import string
import os

Glyph = dict[str, str]  # one glyph: {row number as a string: that row's text}
CharacterSet = dict[str, Glyph] # a whole font style: {uppercase character: glyph}

# ----------------------------------------------------------------------------------------------------------------------------------
# CHAR SET GETTERS

def _get_cset(style: str) -> CharacterSet:
    """
    extract the character set and store in a dictionary

    :param style:           string,     the desired style
    """
    script_dir = os.path.dirname(os.path.abspath(__file__))
    try:
        cset: dict = json.load(open(os.path.join(script_dir, 'font', f'{style}.json'), 'r', encoding='utf-8'))
    except FileNotFoundError:
        raise Exception(f"Invalid style {style}: not supported by the font library")
    except Exception as e:
        raise Exception(f"Error loading style {style}: {str(e)}")
    return cset

def get_character(char: str, style: str) -> Glyph:
    """
    get the ascii art content for any character

    :param char:            string,     any single character from A-Z
    :param style:           string,     the desired style for ascii art
    
    :return:                dict        the ascii art in row number -> content per row
    """
    if len(char) > 1 or not isinstance(char, str): raise Exception("Chracter invalid: must be a character")
    char = char.upper()

    cset = _get_cset(style)
    output_char = cset.get(char, None)
    if output_char is None:
        missing = 'whitespace' if char == ' ' else char
        raise Exception(f'File error: incomplete ascii character library. Missing character: {missing}')

    return output_char

# ----------------------------------------------------------------------------------------------------------------------------------
# CHAR SET SETTER
        
def parse_font_file(path: str, sep: str) -> CharacterSet:
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

    characters = [c for c in string.ascii_uppercase] + [' ']
    cset = {character: {} for character in characters}

    for i, line in enumerate(lines):
        segments = line.split(sep=sep)
        if len(segments) != len(characters):
            raise Exception(
                f"Font file error: line {i + 1} has {len(segments)} {sep}-separated segments, "
                f'expected {len(characters)} (A-Z + space).'
            )
        for character, segment in zip(characters, segments):
            cset[character][str(i + 1)] = segment

    return cset

def set_cset(style: str, font_path: str, sep: str) -> None:
    """
    parse a font text file and add or replace a style under ascii_art_font/font/.

    :param style:           string,     the style key to save the parsed font under
    :param font_path:       string,     path to the font text file
    """
    script_dir = os.path.dirname(os.path.abspath(__file__))
    font_dir = os.path.join(script_dir, 'font')
    os.makedirs(font_dir, exist_ok=True)
    json_path = os.path.join(font_dir, f'{style}.json')

    data = parse_font_file(font_path, sep)

    with open(json_path, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=4)

# ----------------------------------------------------------------------------------------------------------------------------------
# DISPLAY BUILDERS

def build_display(input_string: str, style: str, delim: str = '') -> tuple[str, int]:
    """
    get the output text in the ascii art given style, with the width of a single character

    :param input_string:    string,     the content want to get ascii art from
    :param style:           string,     the style desired
    :param delim:           stirng,     the thing put in between each aschii art character, one on each row
    """
    if len(input_string) < 1: input_string = ' '

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

def _build_default_display(input_string: str, style: str) -> str:
    """
    build the rendered content of a default style, underlined by a separator.

    :param input_string:    string,     the text to render, '\\n' splits it into rows
    :param style:           string,     the font style to render with

    :return:                string,     the rendered content, rows joined by '\\n'
    """
    lines = []
    length = 0
    for line in input_string.split('\n'):
        display_content, length = build_display(line, style, delim=' ')
        lines.append(display_content)
    lines.append('='*length)
    return '\n'.join(lines)

def default_banner(input_string: str) -> str:
    """
    build the banner content.

    :param input_string:    string,     the text to render

    :return:                string,     the rendered banner content
    """
    return _build_default_display(input_string, 'banner')

def default_header(input_string: str) -> str:
    """
    build the header content.

    :param input_string:    string,     the text to render

    :return:                string,     the rendered header content
    """
    return _build_default_display(input_string, 'header')