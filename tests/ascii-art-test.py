import prettier_console as pc

pc.print_banner('quick brown fox\njumps over the\nlazy dog', color="white")
pc.print_header('quick brown fox jumps over the lazy dog', color=pc.default_colored_output.colors.white())

pc.print_banner('quick brown fox\njumps over the\nlazy dog', color="red")
pc.print_header('quick brown fox jumps over the lazy dog', color=pc.default_colored_output.colors.blue())
