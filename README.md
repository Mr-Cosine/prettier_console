# prettier_console

Interactive, colorized command-line UI toolkit for Python — arrow-key menus, ASCII-art banners, colored text, and simple file/folder pickers.

## Installation

```bash
pip install prettier-console
```

**Requirements:** Python 3.10+, and the [`keyboard`](https://pypi.org/project/keyboard/) package (used for arrow-key navigation and `safe_input`, will be installed with the package). On Linux, reading keyboard events usually requires running with `sudo` or granting input-group permissions.

## Quickstart

```python
import prettier_console as pc

def say_hello():
    print("Hello, world!")

def say_hello_to(name):
    print(f"Hello, {name}!")

options = [
    {
        "text": "hello world",
        "color": "green",
        "id": "world",
        "func": {"body": say_hello},  # plain callable, no arguments
    },
    {
        "text": "hello, Ada",
        "color": "cyan",
        "id": "ada",
        "func": {"body": say_hello_to, "param": ["Ada"]},   # positional argument(s)
    },
]

pc.home_menu("HOME", "Welcome!", options)
```

```
██╗  ██╗  ██████╗  ███╗   ███╗ ███████╗
██║  ██║ ██╔═══██╗ ████╗ ████║ ██╔════╝
███████║ ██║   ██║ ██╔████╔██║ █████╗  
██╔══██║ ██║   ██║ ██║╚██╔╝██║ ██╔══╝  
██║  ██║ ╚██████╔╝ ██║ ╚═╝ ██║ ███████╗
╚═╝  ╚═╝  ╚═════╝  ╚═╝     ╚═╝ ╚══════╝
=======================================
Welcome!

Choose from the following 3 options:
    >·1.hello world····<
      2.hello, Ada
      3.quit program
```

Pressing Enter on "hello world" calls say_hello() with no arguments; pressing Enter on "hello, Ada" calls say_hello_to("Ada"). Either way, once the handler returns, you're back at this menu — selecting "quit program" is what actually exits (via quit_program()). The options return and quit program is built into the menu(quit program for home_menu(), and return for menu()), so do not add them in the customized choice.

## Usage

### Colored output

```python
from prettier_console import default_colored_output, Colored_output

default_colored_output.print("Build succeeded", color="green")
default_colored_output.print("Warning: low disk space", color="yellow", background="black")

# Or make your own instance (e.g. bright variant)
bright_output = Colored_output(bright=True)
bright_output.print("Critical error in bright red", color="red")

# Get a colored string without printing it (e.g. to embed in another message)
tag = default_colored_output.get_print_string_text("[OK]", color="green")
```

### Customizing the print of ascii art banners and headers

```python
import prettier_console as pc
pc.print_banner("prettier")
pc.print_header("console ready", color="cyan", background="red")
```

```
██████╗  ██████╗  ███████╗ ████████╗ ████████╗ ████╗ ███████╗ ██████╗ 
██╔══██╗ ██╔══██╗ ██╔════╝ ╚══██╔══╝ ╚══██╔══╝ ╚██╔╝ ██╔════╝ ██╔══██╗
██████╔╝ ██████╔╝ █████╗      ██║       ██║     ██║  █████╗   ██████╔╝
██╔═══╝  ██╔══██╗ ██╔══╝      ██║       ██║     ██║  ██╔══╝   ██╔══██╗
██║      ██║  ██║ ███████╗    ██║       ██║    ████╗ ███████╗ ██║  ██║
╚═╝      ╚═╝  ╚═╝ ╚══════╝    ╚═╝       ╚═╝    ╚═══╝ ╚══════╝ ╚═╝  ╚═╝
======================================================================
┏━┓ ┏━┓ ┳━┓ ┏━┓ ┏━┓ ┓   ┏━┓    ┳━┓ ┏━┓ ┏━┓ ┳━┓ ┓ ┏
┃   ┃ ┃ ┃ ┃ ┗━┓ ┃ ┃ ┃   ┣━     ┣┳┛ ┣━  ┣━┫ ┃ ┃ ┗━┫
┗━┛ ┗━┛ ┛ ┗ ┗━┛ ┗━┛ ┗━┛ ┗━┛    ┛┗┛ ┗━┛ ┛ ┗ ┻━┛ ┗━┛
==================================================
```

> **The bundled fonts only cover `A-Z` and space.** Digits, punctuation and `_` are not in the set, and would not be added when importing custom font. Lowercase is upper-cased automatically.

Multi-line input is supported — `\n` starts a new row of large text, the = separator's length is determined by the longest row:

```python
import prettier_console as pc
pc.print_header("quick brown fox\njumps over the\nlazy dog")
```

```
┏━┓ ┳ ┳  ┳  ┏━┓ ┓┏┓    ┳━┓ ┳━┓ ┏━┓ ┓ ┏ ┳━┓    ┏━┓ ┏━┓ ┏┓┏━
┃ ┃ ┃ ┃  ┃  ┃   ┣┫     ┣━┫ ┣┳┛ ┃ ┃ ┃┃┃ ┃ ┃    ┣━  ┃ ┃  ┣┫ 
┗━┻ ┗━┛  ┻  ┗━┛ ┛┗┛    ┻━┛ ┛┗┛ ┗━┛ ┗┻┛ ┛ ┗    ┻   ┗━┛ ━┛┗┛
 ┏┳ ┳ ┳ ┳┓┓ ┳━┓ ┏━┓    ┏━┓ ┓ ┏ ┏━┓ ┳━┓    ┏┳┓ ┓ ┏ ┏━┓
  ┃ ┃ ┃ ┃┃┃ ┣━┛ ┗━┓    ┃ ┃ ┃┏┛ ┣━  ┣┳┛     ┃  ┣━┫ ┣━ 
┗━┛ ┗━┛ ┛ ┗ ┻   ┗━┛    ┗━┛ ┗┛  ┗━┛ ┛┗┛     ┻  ┛ ┗ ┗━┛
┓   ┏━┓ ━━┓ ┓ ┏    ┳━┓ ┏━┓ ┏━┓
┃   ┣━┫ ┏┛  ┗━┫    ┃ ┃ ┃ ┃ ┃┏┓
┗━┛ ┛ ┗ ┗━┛ ┗━┛    ┻━┛ ┗━┛ ┗━┛
==========================================================
```

Any other style — including one added with `updatefont` — renders through `any_style`, which returns the string instead of printing it:

```python
from prettier_console import ascii_art
from prettier_console import default_colored_output

# assume added a font named custom_font1
text = ascii_art.any_style(input_string="hello world", style="custom_font1")
default_colored_output.print(text)
```

### Printing navigable selections

```python
answer = pc.print_yesorno("Delete this file?")   # pre-built yes-and-no, returns 'y' or 'n'

choice = pc.print_selections(
    "Pick an environment:",
    [
        {"text": "Development", "color": "green", "id": "dev"},
        {"text": "Staging",     "color": "yellow", "id": "staging"},
        {"text": "Production",  "color": "red",    "id": "prod"},
    ],
)  # returns the chosen id (so requires being unique), navigable with the up/down arrow keys
```

### Fully navigable menus

`menu()` builds a single screen; `home_menu()` is the entry point of your app (it adds a "quit" option instead of "back", and calls `quit_program()` when chosen).

```python
# this creates a menu page that has only one option which is returning to the parent panel.
# although it works, still not recommended for the sake of clarity.
def say_hello():
    return pc.menu(name="hello world", prompt="hello!", options=None)

# you can assign any function to an option, not necessarily to menu.
# When function finishes executing it will return to the parent panel.
# However, official method is to use leaf() when not needing to direct to other child panels.
def say_hello_to(name):
    print(f"Hello, {name}!")    

options = [
    {
        "text": "Say hello",
        "color": "red",
        "id": "hello",
        "func": {"body": say_hello},
    },
    {
        "text": "Say hello to someone",
        "color": "blue",
        "id": "hello_name",
        "func": {"body": say_hello_to, "param": ["Ada"]},
    },
]

pc.home_menu(name="HOME", prompt="Welcome!", options=options)
```

Each option's `func` is called when selected — either a plain callable, or a `{"body": fn, "param": [...]}` dict for passing positional arguments. Returning `"__quit"` from a handler exits the whole menu stack (this is what a nested `menu()` propagates upward when the user quits from the home menu).

`"__back"` and `"__quit"` are reserved ids used by the built-in "return to previous" / "quit program" entries — don't use them as your own option ids.

In order to build dynamic prompt that refreshes when the menu is redrawn, pass a function callback that returns a string.

```python
hw_counter = 0

def say_hello():
    return pc.menu(name="hello world", prompt="hello!", options=None)

def prompt_builder():
    global hw_counter
    hw_counter += 1
    return f"hello world for {hw_counter} times!"

options = [
    {
        "text": "Say hello",
        "color": "red",
        "id": "hello",
        "func": {"body": say_hello},
    },
]

pc.home_menu(name="HOME", prompt=prompt_builder, options=options)
```

### Leaf panels

A *menu* branches; a *leaf* is where the branching stops. `leaf()` wraps a one-shot procedure in its own screen: it clears the terminal, prints the panel name as a header, runs your callable, then waits for Enter before handing control back to the menu that opened it — so whatever the procedure printed stays readable instead of being wiped by the next redraw.

In simplest format, leaf() is just your custom function with a header printer and return management. So, start constructing leaf from writing what you need in your desired procedures, wrap it in a function, and finally pass into leaf()'s parameter.

```python
import prettier_console as pc

def show_report(rows, title):
    # your custom procedures, wrapped around a function.
    def print_report(rows, title):
        print(title)
        for row in rows:
            print(" -", row)
    
    # put that into the 
    return pc.leaf("report", print_report, params=[rows, title])

def pick_file():
    # if just one single procedure, you can directly put the function in the parameter without a function wrapper
    # pass the callable itself — no parentheses, leaf() calls it for you with params
    return pc.leaf("file select", pc.default_colored_output.print, params=["Select any file here"])

options = [
    {
        "text": "open file selection",
        "color": "blue",
        "id": "file",
        # leaf() takes the body and its positional arguments, so wrap the call itself
        "func": {"body": pick_file, "param": None},
    },
    {
        "text": "show report",
        "color": "cyan",
        "id": "report",
        "func": {"body": show_report, "param": [["alpha", "beta"], "Results:"]},
    },
]

pc.home_menu(name="HOME", prompt="Welcome!", options=options)
```

`leaf(name, body, params=None)` returns whatever `body(*params)` returned, so a leaf can feed a value back to the caller. `params` is a list of positional arguments — omit it (or pass an empty list) when the body takes none — and returning `"__quit"` from `body` still exits the whole menu stack.

### Safe input

```python
import prettier_console as pc
name = pc.safe_input("What's your name? ")
```

A drop-in replacement for `input()` that guards against stray keypresses left over in the input buffer (falls back to normal `input()` if the `keyboard` backend isn't available, e.g. on some restricted environments).

### File and folder pickers

```python
import prettier_console as pc

files = pc.select_files(prompt="Select an image", file_types=["jpg", "png"])   # opens a native file dialog, returns a tuple of paths or None
folder = pc.select_folder(prompt="Select a folder")               # prompt is provided by default. Opens a native folder dialog, returns a path or None

files = pc.select_files_window(["jpg", "png"])  # opens purely the file selection dialog, no prompt, echo or reselections, same return as select_files()
folder = pc.select_folder_window()  # opens purely the folder selection dialog, same return as select_folder()
```

### ASCII art library

The rendering functions live in the `ascii_art` subpackage. Import it alongside the main package:

```python
from prettier_console import ascii_art

text = ascii_art.any_style(input_string="hello", style="banner")   # returns the rendered string
glyph = ascii_art.get_character("A", "header")                     # one character's rows
```

Unlike `print_banner()` / `print_header()`, these return the rendered string instead of printing it, so you can colorize, pad or embed the result yourself. See the [API reference](#api-reference-for-prettier_consoleascii_art) below for the full list.

### Misc utilities

```python
pc.clear_screen()                 # cross-platform 'cls'/'clear'
width = pc.display_width("你好 world")   # display width accounting for full-width CJK characters
pc.quit_program(code=1)                # clears the screen, prints a goodbye message, exits
```

## Command line

Installing the package puts a `prettier_console` command on your PATH. Every command is also reachable through the module, which is handy inside a virtualenv where the script isn't on PATH:

```bash
prettier_console --help
python -m prettier_console.manage --help
```

| Command | Description |
|---|---|
| `updatefont <path> --delim <char> [--style NAME \| --banner \| --header]` | Add or replace an ASCII-art font style from a text file. |
| `upgrade` | Upgrade the installed package via pip. |

### `updatefont` — adding custom ASCII-art fonts

The banner/header glyphs are stored as JSON under `prettier_console/ascii_art/font/`. You can add or replace a style from a plain-text font file: one row per line, with the glyph segments for `A-Z` + space on each row separated by the character you pass to `--delim`.

```bash
prettier_console updatefont my_font.txt --delim /                 # style name defaults to the file name -> "my_font"
prettier_console updatefont my_font.txt --delim / --style retro   # save under a style name of your choice
prettier_console updatefont my_font.txt --delim / --banner        # overwrite the default banner style
prettier_console updatefont my_font.txt --delim / --header        # overwrite the default header style
```

- `--delim` is required and must be a single character.
- `--style` accepts alphanumeric names only, and is mutually exclusive with `--banner` and `--header`.
- The previous version of a style is automatically zipped into `font/legacy_fonts/` before being overwritten.

### `upgrade` — updating the package

```bash
prettier_console upgrade
```

Runs `pip install --upgrade prettier_console` with the current interpreter and exits with pip's exit code. Note that this reinstalls the package directory, so **custom fonts are reset to the defaults** — keep your font source files if you want to reapply them with `updatefont` afterwards.

## API references

### prettier_console

```python
import prettier_console as pc
```

| Function | Description |
|---|---|
| `Colored_output(bright=False)` | Class for producing ANSI-colored output. |
| `Line_counter()` | Class tracking how many lines have been printed. You rarely need your own — use the shared `line_counter` instance below. |
| `display_width(text)` | Display width of a string, counting CJK characters as 2. |
| `safe_input(prompt="")` | `input()` replacement resilient to buffered keypresses. |
| `clear_screen()` | Clears the terminal, cross-platform. |
| `clear_lines(line_num)` | Clears a given numbers of the latest printed lines. |
| `select_files(prompt="Select file(s)", file_types=None)` | Native file-open dialog with prompt, result echoing, and reselection; returns selected paths or `None`. |
| `select_folder(prompt="Select folder")` | Native folder-select dialog with prompt, result echoing, and reselection; returns a path or `None`. |
| `select_files_window(file_types)` | Opens native file-open dialog; returns selected paths or `None`. |
| `select_folder_window()` | Opens native folder-select dialog; returns a path or `None`. |
| `print_yesorno(prompt)` | Arrow-key Yes/No prompt; returns `'y'` or `'n'`. |
| `print_selections(prompt, options)` | Arrow-key single-select prompt; returns the chosen option's `id`. |
| `print_banner(text, color="white")` | Prints large ASCII-art banner text. |
| `print_header(text, color="white")` | Prints smaller ASCII-art header text. |
| `leaf(name, body, params=None)` | Runs `body(*params)` on its own headed screen, then waits for Enter; returns the body's result. |
| `menu(name, prompt, options=None, home=False)` | Renders one navigable menu screen. |
| `home_menu(name, prompt, options=None)` | Entry-point menu; quits the program via `quit_program()`. |
| `quit_program(code=0)` | Clears the screen, prints a goodbye message, exits. |

### prettier_console.ascii_art

```python
from prettier_console import ascii_art as ascii
```

| Function | Description |
|---|---|
| `any_style(input_string, style)` | Renders `input_string` in any installed style and underlines it with `=` as wide as the widest row; returns the string. `\n` starts a new row of large text. |
| `default_banner(input_string)` | `any_style(input_string, "banner")`. What `print_banner` renders before coloring. |
| `default_header(input_string)` | `any_style(input_string, "header")`. What `print_header` renders before coloring. |
| `build_display(input_string, style, delim="")` | Lower-level renderer for a **single** row of text: returns `(rendered_string, width)` with no underline. `delim` is inserted between glyphs on every row. |
| `get_character(char, style)` | Glyph for one character as `{row_number: row_text}`, keyed by row number as a string. Upper-cases `char`; raises if the style lacks it. |
| `get_cset(style)` | Loads a whole style from `ascii_art/font/<style>.json` as `{character: glyph}`; raises `Invalid style …` if the style is not installed. |
| `set_cset(style, font_path, delim)` | Parses a plain-text font file and writes it to `ascii_art/font/<style>.json`, adding or replacing that style. The programmatic form of [`updatefont`](#updatefont--adding-custom-ascii-art-fonts); unlike the CLI it does **not** archive the previous version. |

All of them raise a plain `Exception` on a missing style or a character the style does not define.

### Instances with prettier_console

```python
from prettier_console import <instance1>, <instance2>...
```

| Instance | Description |
|---|---|
| `default_colored_output` | Shared `Colored_output` instance, for using the functions without having to instantiate `Colored_output`. |
| `line_counter` | Shared `Line_counter` instance. `default_colored_output` updates it automatically, so it always holds the number of lines printed since the last reset (notice: normal `print()` does not count). |

**`default_colored_output` methods**

| Method | Description |
|---|---|
| `default_colored_output.print(*objects, color="white", background=None, sep=" ", end="\n", file=None, flush=False)` | Prints the objects in color. `*objects`, `sep`, `end`, `file` and `flush` behave exactly like the built-in `print()`; `color` and `background` add the ANSI codes. Returns `None`. |
| `default_colored_output.get_print_string_text(*objects, sep=" ", color=None, background=None)` | Same rendering, but returns the escaped string instead of printing it — for embedding a colored fragment inside a larger message. Note `color` defaults to `None` here, not `"white"`, so the default output carries no color code. |

Valid `color` and `background` values are `black`, `red`, `green`, `yellow`, `blue`, `magenta`, `cyan` and `white`; an unrecognized name is ignored rather than raising. Build your own instance with `Colored_output(bright=True)` for the bright variants of the same eight.

Only `print()` touches the shared `line_counter`, and only when `file` is `None` or `sys.stdout` — redirecting to another stream leaves the count alone. `get_print_string_text()` never counts, since it prints nothing.

**`line_counter` methods:** 

| Method | Description |
|---|---|
| `line_counter.printed_lines()` | Returns the current count as an `int`. |
| `line_counter.reset()` | Sets the count back to `0`. Called for you by `clear_screen()`. |
| `line_counter.record_line(line_num=1)` | Adds to the count. Raises `ValueError` on a negative argument. |
| `line_counter.set(line_num)` | Overwrites the count. Raises `ValueError` on a negative argument. |

Because it is a shared object, `from prettier_console import line_counter` gives you a name that keeps tracking the live count.

## Worth noticing

When running, do not resize the window of powershell. Otherwise the formatting would break.

Avoid having wrapped text. The line_counter does not work well with wrapped text. You may manually control text wrapping using "\n" in print.