# prettier_console

Interactive, colorized command-line UI toolkit for Python — arrow-key menus, ASCII-art banners, colored text, and simple file/folder pickers.

## Installation

```bash
pip install prettier-console
```

**Requirements:** Python 3.8+, and the [`keyboard`](https://pypi.org/project/keyboard/) package (used for arrow-key navigation and `safe_input`, will be installed with the package). On Linux, reading keyboard events usually requires running with `sudo` or granting input-group permissions.

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
)  # returns the chosen id, navigable with the up/down arrow keys
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

Each option's `func` is called when selected — either a plain callable, or a `{"body": fn, "param": [...]}` dict for passing positional arguments. Returning `"quit"` from a handler exits the whole menu stack.

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

### Safe input

```python
name = pc.safe_input("What's your name? ")
```

A drop-in replacement for `input()` that guards against stray keypresses left over in the input buffer (falls back to normal `input()` if the `keyboard` backend isn't available, e.g. on some restricted environments).

### File and folder pickers

```python
files = pc.select_files(["jpg", "png"])   # opens a native file dialog, returns a tuple of paths or None
folder = pc.select_folder()               # opens a native folder dialog, returns a path or None
```

### Misc utilities

```python
pc.clear_screen()                 # cross-platform 'cls'/'clear'
width = pc.display_width("你好 world")   # display width accounting for full-width CJK characters
pc.quit_program(0)                # clears the screen, prints a goodbye message, exits
```

## CLI: adding custom ASCII-art fonts

The banner/header glyphs are stored as JSON under `prettier_console/ascii_art_font/font/`. You can add or replace a style from a plain-text font file (one row per line, glyph segments for `A-Z` + space separated by `/`):

```bash
python -m prettier_console.manage updatefont my_font.txt --style retro
python -m prettier_console.manage updatefont my_font.txt --banner   # overwrite the default banner style
python -m prettier_console.manage updatefont my_font.txt --header   # overwrite the default header style
```

The previous version of a style is automatically zipped into `font/legacy_fonts/` before being overwritten.

## API reference

| Function | Description |
|---|---|
| `colored_output(bright=False)` | Class for producing ANSI-colored output. |
| `default_colored_output` | Shared `colored_output` instance used throughout the module. |
| `display_width(text)` | Display width of a string, counting CJK characters as 2. |
| `safe_input(prompt="")` | `input()` replacement resilient to buffered keypresses. |
| `clear_screen()` | Clears the terminal, cross-platform. |
| `select_files(file_types)` | Native file-open dialog; returns selected paths or `None`. |
| `select_folder()` | Native folder-select dialog; returns a path or `None`. |
| `print_yesorno(prompt)` | Arrow-key Yes/No prompt; returns `'y'` or `'n'`. |
| `print_selections(prompt, options)` | Arrow-key single-select prompt; returns the chosen option's `id`. |
| `print_banner(text, color="white")` | Prints large ASCII-art banner text. |
| `print_header(text, color="white")` | Prints smaller ASCII-art header text. |
| `menu(name, prompt, options=None, home=False)` | Renders one navigable menu screen. |
| `home_menu(name, prompt, options=None)` | Entry-point menu; quits the program via `quit_program()`. |
| `quit_program(code=0)` | Clears the screen, prints a goodbye message, exits. |

## Worth noticing

When running, do not resize the window of powershell. Otherwise the formatting would break