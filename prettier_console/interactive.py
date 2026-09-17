"""
dedicated tools to create interactive UI in command line window
"""

import subprocess
import os
import sys
import keyboard
from .ascii_art import ascii_art as ascii_art

from typing import Any, Callable, Sequence, NoReturn
Prompt = str | Callable[[], str] # prompt is text or a builder function return text
Option = dict[str, Any] # one entry of a selection list

line_counter: int = 0

# ----------------------------------------------------------------------------------------------------------------------------------
# INPUT

def safe_input(prompt: str = "") -> str:
    """
    input with preventions of previous input buffer overflow

    :param prompt:          string,     text displayed before asking for input
    """
    if prompt: default_colored_output.print(prompt, color='white', end='', flush=True)

    result: list[str] = []

    while True:
        try:
            event = keyboard.read_event(suppress=True)
            
            if event.event_type == keyboard.KEY_DOWN:
                if event.name == 'enter':
                    default_colored_output.print()
                    return ''.join(result)
                elif event.name == 'backspace':
                    if result:
                        result.pop()
                        print('\b \b', end='', flush=True)
                elif event.name == 'space':
                    result.append(' ')
                    default_colored_output.print(' ', end='', flush=True)
                elif len(event.name) == 1:
                    result.append(event.name)
                    default_colored_output.print(event.name, color='white', end='', flush=True)
        except:
            return input()

#----------------------------------------------------------------------------------------------------------------------------------
# OUTPUT GADGETS

class colored_output:
    """
    Colors: black, red, green, yellow, blue, magenta, cyan, white.
    """

    _NORMAL_FG: dict[str, int] = {
        'BLACK': 30, 'RED': 31, 'GREEN': 32, 'YELLOW': 33,
        'BLUE': 34, 'MAGENTA': 35, 'CYAN': 36, 'WHITE': 37
    }
    _NORMAL_BG: dict[str, int] = {
        'BLACK': 40, 'RED': 41, 'GREEN': 42, 'YELLOW': 43,
        'BLUE': 44, 'MAGENTA': 45, 'CYAN': 46, 'WHITE': 47
    }

    _BRIGHT_FG: dict[str, int] = {
        'BLACK': 90, 'RED': 91, 'GREEN': 92, 'YELLOW': 93,
        'BLUE': 94, 'MAGENTA': 95, 'CYAN': 96, 'WHITE': 97
    }
    _BRIGHT_BG: dict[str, int] = {
        'BLACK': 100, 'RED': 101, 'GREEN': 102, 'YELLOW': 103,
        'BLUE': 104, 'MAGENTA': 105, 'CYAN': 106, 'WHITE': 107
    }

    def __init__(self, bright: bool = False) -> None:
        """
        :param bright:      boolean,    True = bright text
        """
        self._bright: bool = bright
        if bright:
            self._fg_map: dict[str, int] = self._BRIGHT_FG
            self._bg_map: dict[str, int] = self._BRIGHT_BG
        else:
            self._fg_map = self._NORMAL_FG
            self._bg_map = self._NORMAL_BG

        self._RESET: str = "\033[0m"

    def _get_escape(self, fg_color: str | None = None, bg_color: str | None = None) -> str:
        """
        return ANSI color code
        """
        codes: list[str] = []
        if fg_color and fg_color.upper() in self._fg_map:
            codes.append(str(self._fg_map[fg_color.upper()]))
        if bg_color and bg_color.upper() in self._bg_map:
            codes.append(str(self._bg_map[bg_color.upper()]))

        if not codes: return ""
        return f"\033[{';'.join(codes)}m"

    def print(self, *objects: Any, color: str = "white", background: str | None = None, sep: str = ' ', end: str = '\n', file = None, flush: bool = False) -> None:
        """
        print out colored content

        :param color:       string, text color
        :param objects:     any,        printing objects
        :param background:  string,     background color
        :param sep:         string,     delimintor between printing objects
        :param end:         string,     ending style
        :param file:        any,        output stream
        :param flush:       boolean,    flush buffer zone
        """
        text = sep.join(str(obj) for obj in objects)
        colored_text = f"{self._get_escape(color, background)}{text}{self._RESET}"
        print(colored_text, end=end, file=file, flush=flush)
        global line_counter
        if file is None or file is sys.stdout: line_counter += (text + end).count('\n')

    def get_print_string_text(self, *objects: Any, sep: str = ' ', color: str | None = None, background: str | None = None) -> str:
        """
        return colored text string for print

        :param color:       string,     text color
        :param objects:     any,        printing objects
        :param background:  string,     background color
        :param sep:         string,     delimintor between printing objects
        """
        text = sep.join(str(obj) for obj in objects)
        escape = self._get_escape(color, background)
        return f"{escape}{text}{self._RESET}"
    
default_colored_output = colored_output(bright=False) # shared instance used for every output of this module

def display_width(text: Any) -> int:
    """
    get consistent displayed width for latin + chinese characters string

    :param text:            string,     the text for getting length of display
    """
    width: int = 0
    for ch in str(text):
        if '\u4e00' <= ch <= '\u9fff' or '\u3000' <= ch <= '\u303f' or '\uff00' <= ch <= '\uffef':
            width += 2
        else:
            width += 1
    return width
        
def clear_screen() -> None:
    """
    flush content on the console
    """
    global line_counter
    command = 'cls' if os.name == 'nt' else 'clear'
    subprocess.run(command, shell=True, check=False)
    line_counter = 0

def clear_lines(line_num: int) -> None:
    """
    flush content between the line of the latest print (inclusive) to a given number of previous print line

    :param line_num:        int,        the number of lines to be flushed
    """
    global line_counter
    if line_num <= 0: return
    print(f"\033[{line_num}A\033[0J", end="", flush=True)
    line_counter = max(0, line_counter - line_num)

def print_header(input_string: str, color: str = 'white') -> None:
    """
    print a text rendered in the header ascii-art style.

    :param input_string:    string,     the text to render, '\\n' splits it into rows
    :param color:           string,     text color (default: white)
    """

    default_colored_output.print(ascii_art.default_header(input_string), color=color, background=None)

def print_banner(input_string: str, color: str = 'white') -> None:
    """
    print a text rendered in the banner ascii-art style.

    :param input_string:    string,     the text to render, '\\n' splits it into rows
    :param color:           string,     text color (default: white)
    """

    default_colored_output.print(ascii_art.default_banner(input_string), color=color, background=None)

def print_yesorno(prompt: Prompt) -> str:
    """
    print yes or no choice to let user select.

    :param prompt:          string/func,    the prompt displayed before asking.

    :return:                string,         'y' or 'n'
    """
    options: list[Option] = [
        {
            'text': 'Yes',
            'color': 'green',
            'id': 'y'
        },
        {
            'text': 'No',
            'color': 'red',
            'id': 'n'
        }
    ]
    return print_selections(prompt, options)

def print_selections(prompt: Prompt, options: Sequence[Option]) -> str:

    """
    print menu options could be operated by up and down arrow to select. returns the id of the option.

    :param prompt:          string/func,    the prompt string or prompt builder function(need to return string)
    :param options:         dict,           the options for choose
                            {
                                text:   string,     the option text displayed
                                color:  string,     color of the option displayed(default: white)
                                id: string,         unique identifier for each option
                            }
    """
    def hide_cursor() -> None: print('\033[?25l', end='', flush=True)
    def show_cursor() -> None: print('\033[?25h', end='', flush=True)

    active_index: int = 0

    # Calculate max length once for lining up entries
    target_w: int = max(display_width(str(option['text'])) for option in options)
    target_w = 10 if target_w < 10 else target_w

    if not callable(prompt): default_colored_output.print(prompt, color='white')
    else: default_colored_output.print(prompt(), color='white')

    def print_options() -> None:
        for idx, option in enumerate(options):
            lead_cursor: str = ">·" if idx == active_index else " "
            lag_cursor: str = "·<" if idx == active_index else " "

            text: str = option['text']
            color: str = option.get('color') or 'white'

            current_w = display_width(text)
            filler: str = ('·' if active_index == idx else " ") * (max((target_w - current_w), 0) + 4 - display_width(lead_cursor))

            default_colored_output.print(' '*(4 - display_width(lead_cursor)), color='white', end='', flush=True)
            default_colored_output.print(f"{lead_cursor}", color='white', end='', flush=True)
            default_colored_output.print(f"{idx+1}.{text}", color=color, end='', flush=True)
            default_colored_output.print(f"{filler}{lag_cursor}", color='white', flush=True)

    hide_cursor()
    # Print menu
    print_options()

    # Main loop for arrow key navigation
    while True:
        # Get key press
        key = keyboard.read_event(suppress=True)

        if key.event_type == keyboard.KEY_DOWN:
            if key.name == 'up':
                active_index = (active_index - 1) % len(options)
            elif key.name == 'down':
                active_index = (active_index + 1) % len(options)
            elif key.name == 'enter':
                show_cursor()
                clear_lines(len(options) + 1)   # the options plus the prompt printed above them
                return options[active_index]['id']
            else: continue

            # only the option lines are redrawn, the prompt above them stays where it is
            clear_lines(len(options))
            print_options()

# ----------------------------------------------------------------------------------------------------------------------------------
# OUTPUT BUNDLES

def leaf(name: str, body: Callable[..., Any], params: Sequence[Any] | None = None) -> Any:
    """
    open up a leaf panel with a linear procedure

    :param name:            string,         the name of the panel
    :param body:            func,           the things needs to be executed.
    :param params:          list,           the parameters for body, have to be positional argument.
    :return:                any,            whatever body returned, so a leaf can feed a value back to its caller
    """
    clear_screen()
    print_header(name)
    result: Any = body(*params) if params is not None else body()
    safe_input("Press Enter to return.")
    return result

def menu(name: str, prompt: Prompt, options: Sequence[Option] | None = None, home: bool = False) -> str:
    """
    open up a menu with single selection toward other menu

    :param name:            string,         the name of the panel
    :param prompt:          string/func,    the prompt pr a prompt builder function(need to return string)
    :param options:         [dict],         the options informations
                            [
                                {
                                text:   string, 
                                color:  string, 
                                id:     string, 
                                func: {
                                    body:   function, 
                                    param:  [any...],
                                    }
                                }
                                ...
                            ]
    """
    # gather the necessary information for print_selections(options)
    if options is None: options = []
    menu_options = [{'text': option['text'], 'color': option.get('color', None), 'id': option['id']} for option in options]

    # add back option to allow to return to previous menu
    if home: menu_options.append({'text': 'quit program', 'color': '', 'id': '__quit'})
    else: menu_options.append({'text': 'return to previous', 'color': '', 'id': '__back'})
    # check for any duplicated id to prevent ambiguation in searching the options
    if len([d.get('id') for d in menu_options]) != len(set([d.get('id') for d in menu_options])):
        raise Exception('duplicated id for options')

    while True:
        clear_screen()
        if not home:
            print_header(name)
        else:
            print_banner(name)
        if not callable(prompt): default_colored_output.print(prompt, color='white')
        else: default_colored_output.print(prompt(), color='white')
        default_colored_output.print()

        chosen_id = print_selections(
            f'Choose from the following {len(menu_options)} options:', 
            menu_options
        )
    
        if chosen_id in ['__back', '__quit']:
            return chosen_id

        selected: Option | None = None
        for opt in options:
            if opt['id'] == chosen_id:
                selected = opt
                break
            
        if not selected: raise Exception(f'no defined action for an option: {selected}.')

        # If there's a 'func', execute it
        if 'func' in selected:
            # either the callable itself, or {'body': callable, 'param': [args...]}
            func: Callable[..., Any] | dict[str, Any] = selected['func']
            if callable(func):
                result: Any = func()
            elif isinstance(func, dict) and 'body' in func:
                body: Callable[..., Any] = func['body']
                params: Sequence[Any] = func.get('param', [])
                result = body(*params)
            else: raise Exception(f'action provided for an option: {selected} is not callable.')
            if result == '__quit':
                return '__quit'

def home_menu(name: str, prompt: Prompt, options: Sequence[Option] | None = None) -> None:
    """
    open a root menu with single selection toward other menu

    :param name:            string,     the name of the panel
    :param prompt:          string,     the prompt
    :param options:         [dict...],  the options informations
                            [
                                {
                                text:   string, 
                                color:  string, 
                                id:     string, 
                                func: {
                                    body:   function, 
                                    param:  [any...],
                                    }
                                }
                                ...
                            ]
    """
    result = menu(name, prompt, options, home=True)
    if result == '__quit': quit_program(0)

# ----------------------------------------------------------------------------------------------------------------------------------
# PROGRAM EXIT

def quit_program(code: int = 0) -> NoReturn:
    clear_screen()
    default_colored_output.print("Exiting program.", color='white')
    default_colored_output.print('='*30, color='white')
    
    try: keyboard.unhook_all()
    except: pass
    finally: sys.exit(code)

# ----------------------------------------------------------------------------------------------------------------------------------
# FILE SYSTEM

def select_files_window(file_types: str | Sequence[str] | None) -> tuple[str, ...] | None:
    """
    opens file selection dialog.

    :param file_types:      [string...],    list of wanted types, eg. ['jpg', 'pdf', 'txt]

    :return:                the selected file location, if not selected return None
    """
    from tkinter import Tk
    import tkinter.filedialog

    root = Tk()
    root.withdraw()

    filetypes: list[tuple[str, str]] = []
    if file_types is None: filetypes.append(('All Files', '*.*'))
    else:
        if isinstance(file_types, str): file_types = [file_types]

        for file_type in file_types:
            ext = str(file_type).lstrip('*').lstrip('.').lower()
            # tkinter only matches a pattern, so a bare 'jpg' has to become '*.jpg'
            if ext in ('', '*'): filetypes.append(('All Files', '*.*'))
            else: filetypes.append((ext + ' file', '*.' + ext))

    files = tkinter.filedialog.askopenfilenames(
        title='File selection',
        filetypes=filetypes
    )

    root.destroy()
    return files if files else None

def select_folder_window() -> str | None:
    """
    opens file selection dialog.

    :return:                the selected folder path, if not selected return None
    """
    from tkinter import Tk
    import tkinter.filedialog 

    root = Tk()
    root.withdraw()
    folder = tkinter.filedialog.askdirectory(title='Folder selection')
    root.destroy()
    return folder if folder else None;

def select_folder(prompt: str = "select folder") -> str | None:
    """
    create input, verification, and provide reselect for folder selection.

    :param prompt:          string,         format is provided, no need for semicolon etc.
    :return:                the selected folder path, if not selected return None
    """

    global line_counter
    MAX_FNAME_LEN = 30
    while True:
        line_counter = 0
        default_colored_output.print(prompt, color="white", end=": ", flush=True)
        folder = select_folder_window()
        if folder is not None:
            # a folder is a single path string, joining it would split it into characters
            default_colored_output.print((folder[:MAX_FNAME_LEN] + "...") if len(folder) > MAX_FNAME_LEN else folder, color="white", flush=True)
            answer = print_yesorno("Is this correct?")
            if answer == 'y':
                return folder
            else:
                clear_lines(line_counter)
        else:
            default_colored_output.print("Selection aborted.", color="white")
            return None


def select_files(prompt: str = "Select file(s)", file_types: str | Sequence[str] | None = None) -> tuple[str, ...] | None:
    """
    create input, verification, and provide reselect for folder selection.

    :param prompt:          string,         format is provided, no need for semicolon etc.
    :param file_types:      [string]        the types of files wanted, passing None or leaving as blank is any file types
    :return:                the selected folder path, if not selected return None
    """

    global line_counter
    MAX_FNAME_LEN = 20
    while True:
        line_counter = 0
        default_colored_output.print(prompt, color="white", end=": ", flush=True)
        files = select_files_window(file_types)
        if files is not None:
            from pathlib import Path
            preview = ", ".join(
                [Path(f).name[:MAX_FNAME_LEN] + "..." if len(Path(f).name) > MAX_FNAME_LEN else Path(f).name 
                for f in files]
                )
            default_colored_output.print(preview, color="white", flush=True)
            answer = print_yesorno("Is this correct?")
            if answer == 'y':
                return files
            else:
                clear_lines(line_counter)
        else:
            default_colored_output.print("Selection aborted.")
            return None