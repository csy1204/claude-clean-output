#!/usr/bin/env python3
"""Extract tables and diagrams from Claude Code transcript, format them.

Usage:
  python3 extract.py <transcript.jsonl>
  python3 extract.py <transcript.jsonl> --json              # output as JSON array
  python3 extract.py <transcript.jsonl> --normalize-chars   # convert ASCII box chars to unicode
"""
import json
import sys
import re
import os

# Import sibling modules
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from format_table import format_table
from format_diagram import format_diagram


def get_last_assistant_text(transcript_path):
    """Read JSONL transcript and return last assistant message text."""
    last_text = None
    with open(transcript_path, 'r', encoding='utf-8') as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            try:
                entry = json.loads(line)
            except json.JSONDecodeError:
                continue

            if entry.get('type') == 'assistant':
                content = entry.get('message', {}).get('content', [])
                for block in content:
                    if block.get('type') == 'text':
                        last_text = block.get('text', '')
    return last_text or ''


def extract_tables(text):
    """Extract markdown table blocks from text."""
    tables = []
    lines = text.split('\n')
    current_table = []
    in_table = False

    for line in lines:
        stripped = line.strip()
        if stripped.startswith('|') and stripped.endswith('|'):
            in_table = True
            current_table.append(stripped)
        else:
            if in_table and current_table:
                tables.append('\n'.join(current_table))
                current_table = []
            in_table = False

    if current_table:
        tables.append('\n'.join(current_table))

    return tables


def extract_diagrams(text):
    """Extract code-fenced diagram blocks containing box-drawing characters."""
    diagrams = []
    box_chars = set('┌┐└┘─│├┤┬┴┼╔╗╚╝═║╠╣╦╩╬+')

    # Find fenced code blocks
    pattern = r'```[^\n]*\n(.*?)```'
    for match in re.finditer(pattern, text, re.DOTALL):
        block = match.group(1)
        if any(c in box_chars for c in block):
            diagrams.append(block.rstrip('\n'))

    return diagrams


def main():
    if len(sys.argv) < 2:
        print("Usage: extract.py <transcript.jsonl> [--json] [--normalize-chars]", file=sys.stderr)
        sys.exit(1)

    transcript_path = sys.argv[1]
    as_json = '--json' in sys.argv
    do_normalize = '--normalize-chars' in sys.argv

    text = get_last_assistant_text(transcript_path)
    if not text:
        sys.exit(0)

    tables = extract_tables(text)
    diagrams = extract_diagrams(text)

    if not tables and not diagrams:
        sys.exit(0)

    results = []

    for table in tables:
        formatted = format_table(table)
        results.append({'type': 'table', 'formatted': formatted})

    for diagram in diagrams:
        formatted = format_diagram(diagram, do_normalize_chars=do_normalize)
        results.append({'type': 'diagram', 'formatted': formatted})

    if as_json:
        print(json.dumps(results, ensure_ascii=False, indent=2))
    else:
        for item in results:
            if item['type'] == 'table':
                print(item['formatted'])
            else:
                print('```')
                print(item['formatted'])
                print('```')
            print()


if __name__ == '__main__':
    main()
