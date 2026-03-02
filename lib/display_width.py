#!/usr/bin/env python3
"""Calculate terminal display width of text, accounting for CJK wide characters.

Usage:
  echo "한글text" | python3 display_width.py          # outputs total display width
  printf "line1\nline2" | python3 display_width.py --per-line  # outputs width per line
"""
import sys
import unicodedata


def char_width(c):
    """Return display width of a single character."""
    eaw = unicodedata.east_asian_width(c)
    if eaw in ('W', 'F'):
        return 2
    return 1


def display_width(s):
    """Return total display width of string."""
    return sum(char_width(c) for c in s)


def main():
    per_line = '--per-line' in sys.argv
    text = sys.stdin.read()

    if per_line:
        lines = text.split('\n')
        # Remove trailing empty line from trailing newline
        if lines and lines[-1] == '':
            lines = lines[:-1]
        for line in lines:
            print(display_width(line))
    else:
        print(display_width(text))


if __name__ == '__main__':
    main()
