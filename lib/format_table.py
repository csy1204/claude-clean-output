#!/usr/bin/env python3
"""Normalize markdown pipe tables with CJK display width alignment.

Reads a markdown table from stdin, outputs the aligned version to stdout.
"""
import sys
import unicodedata
import re


def char_width(c):
    eaw = unicodedata.east_asian_width(c)
    return 2 if eaw in ('W', 'F') else 1


def display_width(s):
    return sum(char_width(c) for c in s)


def pad_to_width(s, target_width):
    """Pad string with spaces to reach target display width."""
    current = display_width(s)
    return s + ' ' * (target_width - current)


def parse_row(line):
    """Parse a pipe table row into list of cell contents (stripped)."""
    line = line.strip()
    if line.startswith('|'):
        line = line[1:]
    if line.endswith('|'):
        line = line[:-1]
    return [cell.strip() for cell in line.split('|')]


def is_separator_row(cells):
    """Check if row is a separator (---) row."""
    return all(re.match(r'^:?-+:?$', cell.strip()) for cell in cells if cell.strip())


def format_table(text):
    lines = text.strip().split('\n')
    if not lines:
        return text

    # Parse all rows
    rows = [parse_row(line) for line in lines]

    # Normalize column count to max
    max_cols = max(len(row) for row in rows)
    for row in rows:
        while len(row) < max_cols:
            row.append('')

    # Calculate max display width per column
    col_widths = [0] * max_cols
    for i, row in enumerate(rows):
        if is_separator_row(row):
            continue
        for j, cell in enumerate(row):
            w = display_width(cell)
            if w > col_widths[j]:
                col_widths[j] = w

    # Ensure minimum width of 3 for separator dashes
    col_widths = [max(w, 3) for w in col_widths]

    # Format each row
    output_lines = []
    for row in rows:
        if is_separator_row(row):
            # Separator dashes fill the full cell width + 2 (for the spaces around content)
            # Format: |------|------|  (no spaces around dashes)
            cells = ['-' * (col_widths[j] + 2) for j in range(max_cols)]
            output_lines.append('|' + '|'.join(cells) + '|')
        else:
            cells = [pad_to_width(cell, col_widths[j]) for j, cell in enumerate(row)]
            output_lines.append('| ' + ' | '.join(cells) + ' |')

    return '\n'.join(output_lines)


def main():
    text = sys.stdin.read()
    print(format_table(text))


if __name__ == '__main__':
    main()
