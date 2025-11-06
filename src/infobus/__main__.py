"""Module entry point for running `infobus` as `python -m infobus`.

This simply delegates to the CLI's main() function.
"""

from .cli import main

if __name__ == "__main__":
    main()
