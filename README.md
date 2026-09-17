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
        "id": "hello",
        "func": {"body": say_hello},  # plain callable, no arguments
    },
    {
        "text": "hello, Ada",
        "color": "cyan",
        "id": "hello_ada",
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

Pressing Enter on "hello world" calls hello_world() with no arguments; pressing Enter on "hello, Ada" calls hello_name("Ada"). Either way, once the handler returns, you're back at this menu — selecting "quit program" is what actually exits (via quit_program()). The options return and quit program is built into the menu(quit program for home_menu(), and return for menu()), so do not add them in the customized choice.

## Usage

### Colored output

```python
from prettier_console import default_colored_output, colored_output

default_colored_output.print("Build succeeded", color="green")
default_colored_output.print("Warning: low disk space", color="yellow", background="black")

# Or make your own instance (e.g. bright variant)
bright = colored_output(bright=True)
bright.print("Critical error", color="red")

# Get a colored string without printing it (e.g. to embed in another message)
tag = default_colored_output.get_print_string_text("[OK]", color="green")
print(f"{tag} All tests passed")
```

### Banners and headers (ASCII art)

```python
pc.print_banner("prettier_console")
pc.print_header("v1.0 released", color="cyan")
```

Multi-line input is supported — `\n` starts a new row of large text:

```python
pc.print_banner("quick brown fox\njumps over the\nlazy dog")
```

### Yes/no and custom menus

```python
answer = pc.print_yesorno("Delete this file?")   # returns 'y' or 'n'

choice = pc.print_selections(
    "Pick an environment:",
    [
        {"text": "Development", "color": "green", "id": "dev"},
        {"text": "Staging",     "color": "yellow", "id": "staging"},
        {"text": "Production",  "color": "red",    "id": "prod"},
    ],
)  # returns the chosen id (so requires being unique), navigable with the up/down arrow keys
```

### Full navigable menus

`menu()` builds a single screen; `home_menu()` is the entry point of your app (it adds a "quit" option instead of "back", and calls `quit_program()` when chosen).

```python
def say_hello():
    return pc.menu(name="hello world", prompt="hello!", options=None)

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

A menu branches; a *leaf* is where the branching stops. `leaf()` wraps a one-shot procedure in its own screen: it clears the terminal, prints the panel name as a header, runs your callable, then waits for Enter before handing control back to the menu that opened it — so whatever the procedure printed stays readable instead of being wiped by the next redraw.

```python
def pick_file():
    return pc.select_files(prompt="Select any file here")

def show_report(rows, title):
    print(title)
    for row in rows:
        print(" -", row)

options = [
    {
        "text": "open file selection",
        "color": "blue",
        "id": "file",
        # leaf() takes the body and its positional arguments, so wrap the call itself
        "func": {"body": pc.leaf, "param": ["file select", pick_file, []]},
    },
    {
        "text": "show report",
        "color": "cyan",
        "id": "report",
        "func": {"body": pc.leaf, "param": ["report", show_report, [["alpha", "beta"], "Results:"]]},
    },
]

pc.home_menu(name="HOME", prompt="Welcome!", options=options)
```

`leaf(name, body, params=None)` returns whatever `body(*params)` returned, so a leaf can feed a value back to the caller. `params` is a list of positional arguments — omit it (or pass an empty list) when the body takes none — and returning `"__quit"` from `body` still exits the whole menu stack.

### Safe input

```python
name = pc.safe_input("What's your name? ")
```

A drop-in replacement for `input()` that guards against stray keypresses left over in the input buffer (falls back to normal `input()` if the `keyboard` backend isn't available, e.g. on some restricted environments).

### File and folder pickers

```python
files = pc.select_files(prompt="Select an image", filetypes=["jpg", "png"])   # opens a native file dialog, returns a tuple of paths or None
folder = pc.select_folder(prompt="Select a folder")               # prompt is provided by default. Opens a native folder dialog, returns a path or None

files = pc.select_files_window(["jpg", "png"])  # opens purely the file selection dialog, no prompt, echo or reselections, same return as select_files()
folder = pc.select_folder_window()  # opens purely the folder selection dialog, same return as select_folder()
```

### Misc utilities

```python
pc.clear_screen()                 # cross-platform 'cls'/'clear'
width = pc.display_width("你好 world")   # display width accounting for full-width CJK characters
pc.quit_program(0)                # clears the screen, prints a goodbye message, exits
```

## Command line

Installing the package puts a `prettier_console` command on your PATH. Every command is also reachable through the module, which is handy inside a virtualenv where the script isn't on PATH:

```bash
prettier_console --help
python -m prettier_console.manage --help
```

| Command | Description |
|---|---|
| `updatefont <path> --sep <char> [--style NAME \| --banner \| --header]` | Add or replace an ASCII-art font style from a text file. |
| `upgrade` | Upgrade the installed package via pip. |

### `updatefont` — adding custom ASCII-art fonts

The banner/header glyphs are stored as JSON under `prettier_console/ascii_art_font/font/`. You can add or replace a style from a plain-text font file: one row per line, with the glyph segments for `A-Z` + space on each row separated by the character you pass to `--sep`.

```bash
prettier_console updatefont my_font.txt --sep /                 # style name defaults to the file name -> "my_font"
prettier_console updatefont my_font.txt --sep / --style retro   # save under a style name of your choice
prettier_console updatefont my_font.txt --sep / --banner        # overwrite the default banner style
prettier_console updatefont my_font.txt --sep / --header        # overwrite the default header style
```

- `--sep` is required and must be a single character.
- `--style` accepts alphanumeric names only, and is mutually exclusive with `--banner` and `--header`.
- The previous version of a style is automatically zipped into `font/legacy_fonts/` before being overwritten.

### `upgrade` — updating the package

```bash
prettier_console upgrade
```

Runs `pip install --upgrade prettier_console` with the current interpreter and exits with pip's exit code. Note that this reinstalls the package directory, so **custom fonts are reset to the defaults** — keep your font source files if you want to reapply them with `updatefont` afterwards.

## API reference

| Function | Description |
|---|---|
| `colored_output(bright=False)` | Class for producing ANSI-colored output. |
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

## Instances comes with the module

| Instance | Description |
|---|---|
| `default_colored_output` | Shared `colored_output` instance, for using the functions without having to instantiate `colored_output`. |
| `line_counter` | Built-in line counter that `default_colored_output` can mutate automatically to track how many lines are printed (notice: normal print does not count) |

## Worth noticing

When running, do not resize the window of powershell. Otherwise the formatting would break.

Avoid having wrapped text. The line_counter does not work well with wrapped text.