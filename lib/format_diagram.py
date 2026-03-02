#!/usr/bin/env python3
"""Normalize ASCII diagrams: strip whitespace, optionally convert ASCII box chars to unicode.

Usage:
  echo "diagram" | python3 format_diagram.py                 # normalize whitespace only
  echo "diagram" | python3 format_diagram.py --normalize-chars  # also convert +- to ┌─
"""
import sys
import re


# Mapping from ASCII box chars to unicode equivalents
ASCII_TO_UNICODE = {
    # Corners and intersections are context-dependent
    '-': '─',
    '|': '│',
}


def detect_corner(lines, row, col):
    """Detect what unicode corner/tee to use for a '+' at given position."""
    has_up = row > 0 and col < len(lines[row - 1]) and lines[row - 1][col] in '|│┃'
    has_down = row < len(lines) - 1 and col < len(lines[row + 1]) and lines[row + 1][col] in '|│┃'
    has_left = col > 0 and lines[row][col - 1] in '-─━'
    has_right = col < len(lines[row]) - 1 and lines[row][col + 1] in '-─━'

    if has_down and has_right and not has_up and not has_left:
        return '┌'
    if has_down and has_left and not has_up and not has_right:
        return '┐'
    if has_up and has_right and not has_down and not has_left:
        return '└'
    if has_up and has_left and not has_down and not has_right:
        return '┘'
    if has_up and has_down and has_right and not has_left:
        return '├'
    if has_up and has_down and has_left and not has_right:
        return '┤'
    if has_down and has_left and has_right and not has_up:
        return '┬'
    if has_up and has_left and has_right and not has_down:
        return '┴'
    if has_up and has_down and has_left and has_right:
        return '┼'
    # Fallback for ambiguous: top-left corner
    return '┌'


def normalize_chars(lines):
    """Convert ASCII box drawing to unicode."""
    result = []
    for row_idx, line in enumerate(lines):
        new_line = list(line)
        for col_idx, ch in enumerate(line):
            if ch == '+':
                new_line[col_idx] = detect_corner(lines, row_idx, col_idx)
            elif ch in ASCII_TO_UNICODE:
                new_line[col_idx] = ASCII_TO_UNICODE[ch]
        result.append(''.join(new_line))
    return result


def format_diagram(text, do_normalize_chars=False):
    lines = text.rstrip('\n').split('\n')

    # Strip trailing whitespace from each line
    lines = [line.rstrip() for line in lines]

    # Normalize leading whitespace: find minimum non-empty leading spaces, subtract from all
    min_indent = float('inf')
    for line in lines:
        if line.strip():  # skip empty lines
            indent = len(line) - len(line.lstrip())
            min_indent = min(min_indent, indent)

    if min_indent > 0 and min_indent != float('inf'):
        lines = [line[min_indent:] if len(line) >= min_indent else line for line in lines]

    # Optionally convert ASCII box chars to unicode
    if do_normalize_chars:
        lines = normalize_chars(lines)

    return '\n'.join(lines)


def main():
    do_normalize = '--normalize-chars' in sys.argv
    text = sys.stdin.read()
    print(format_diagram(text, do_normalize_chars=do_normalize))


if __name__ == '__main__':
    main()
