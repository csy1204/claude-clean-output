#!/usr/bin/env python3
"""Config loader/saver for claude-clean-output plugin.

Config file: ~/.claude/plugins/claude-clean-output/config.json

Usage:
  python3 config.py --get <key>                      # print value
  python3 config.py --set <key>=<value>               # set value
  python3 config.py --dump                             # print full config JSON
  python3 config.py --config-dir <dir> --get <key>    # custom config dir (testing)
"""
import json
import os
import sys

DEFAULT_CONFIG = {
    "autoFormat": True,
    "clipboard": True,
    "savePath": "~/.claude/clean-output/latest.md",
    "unicodeDiagrams": False,
    "promptRules": True,
    "promptStrength": "standard",
}

def get_config_path(config_dir=None):
    if config_dir:
        return os.path.join(config_dir, "config.json")
    return os.path.expanduser("~/.claude/plugins/claude-clean-output/config.json")


def load_config(config_dir=None):
    path = get_config_path(config_dir)
    config = dict(DEFAULT_CONFIG)
    if os.path.exists(path):
        with open(path, 'r', encoding='utf-8') as f:
            user_config = json.load(f)
        config.update(user_config)
    return config


def save_config(config, config_dir=None):
    path = get_config_path(config_dir)
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, 'w', encoding='utf-8') as f:
        json.dump(config, f, ensure_ascii=False, indent=2)
        f.write('\n')


def parse_value(val):
    """Parse string value to appropriate Python type."""
    if val.lower() == 'true':
        return True
    if val.lower() == 'false':
        return False
    try:
        return int(val)
    except ValueError:
        return val


def main():
    args = sys.argv[1:]
    config_dir = None

    # Parse --config-dir
    if '--config-dir' in args:
        idx = args.index('--config-dir')
        config_dir = args[idx + 1]
        args = args[:idx] + args[idx + 2:]

    config = load_config(config_dir)

    if '--get' in args:
        key = args[args.index('--get') + 1]
        value = config.get(key, '')
        print(str(value).lower() if isinstance(value, bool) else value)
    elif '--set' in args:
        pair = args[args.index('--set') + 1]
        key, val = pair.split('=', 1)
        config[key] = parse_value(val)
        save_config(config, config_dir)
    elif '--dump' in args:
        print(json.dumps(config, ensure_ascii=False, indent=2))
    else:
        print("Usage: config.py [--config-dir DIR] --get KEY | --set KEY=VAL | --dump", file=sys.stderr)
        sys.exit(1)


if __name__ == '__main__':
    main()
