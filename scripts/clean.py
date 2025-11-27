#!/usr/bin/env python3
"""
Cross-platform project cleanup script.

Usage:
    python scripts/clean.py [--dry-run] [--remove-venv] [--venv-name <name>] [--root <path>]

Behaviors:
- Removes: build/, dist/, *.egg-info, __pycache__/, *.pyc, .pytest_cache/, .coverage, htmlcov/
- Optionally removes project virtualenvs: .venv/ and venv/ (or custom name provided)
- Safety checks: only removes directories under repository root by default.
- --yes bypasses confirmation prompts.

This script is intended to run on any OS with Python installed and can be used in "any terminal".
"""

from __future__ import annotations

import argparse
import os
import shutil
import sys
from glob import glob
from pathlib import Path


def confirm(prompt: str) -> bool:
    try:
        resp = input(f"{prompt} [y/N]: ")
    except EOFError:
        return False
    return resp.lower() in ("y", "yes")


def safe_rmtree(p: Path, dry_run: bool = False) -> None:
    if not p.exists():
        print(f"Skipping (not found): {p}")
        return
    if not p.resolve().is_relative_to(Path.cwd().resolve()):
        print(f"Refusing to remove outside cwd: {p}")
        return
    if dry_run:
        print(f"(dry-run) Would remove: {p}")
        return
    try:
        print(f"Removing: {p}")
        shutil.rmtree(p)
    except Exception as e:
        print(f"Failed to remove {p}: {e}")


def remove_pyc_files(root: Path, dry_run: bool = False) -> None:
    for dirpath, dirnames, filenames in os.walk(root):
        # skip .venv/ and venv/ by default
        if ".venv" in dirpath.split(os.sep) or "venv" in dirpath.split(os.sep):
            continue
        for filename in filenames:
            if filename.endswith('.pyc'):
                p = Path(dirpath) / filename
                if dry_run:
                    print(f"(dry-run) Would remove file: {p}")
                else:
                    try:
                        p.unlink()
                        print(f"Removed file: {p}")
                    except Exception as e:
                        print(f"Failed to remove file {p}: {e}")


def remove_pycache_dirs(root: Path, dry_run: bool = False) -> None:
    for dirpath, dirnames, filenames in os.walk(root):
        for d in list(dirnames):
            if d == "__pycache__":
                p = Path(dirpath) / d
                if dry_run:
                    print(f"(dry-run) Would remove pfolder: {p}")
                else:
                    safe_rmtree(p, dry_run=False)


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Clean Python project build and cache artifacts.")
    parser.add_argument("--dry-run", action="store_true", help="Print actions without removing files")
    parser.add_argument("--remove-venv", action="store_true", help="Remove virtual environment directories (venv/.venv) if present")
    parser.add_argument("--venv-name", type=str, default=None, help="Additional venv directory name to remove")
    parser.add_argument("--venv-dir", type=str, default=None, help="Specific path to a virtual environment to remove")
    parser.add_argument("--yes", action="store_true", help="Proceed without interactive confirmation (dangerous)")
    parser.add_argument("--root", type=str, default='.', help="Project root path (defaults to current cwd)")
    args = parser.parse_args(argv)

    root = Path(args.root).resolve()
    os.chdir(root)

    patterns_dirs = [
        root / 'build',
        root / 'dist',
    ]

    # Add egg-info directories
    egg_infos = list(root.glob('*.egg-info'))
    patterns_dirs.extend(egg_infos)

    # Additional caches and artifacts
    extra_dirs = [root / '.pytest_cache', root / 'htmlcov']
    patterns_dirs.extend(extra_dirs)

    # coverage file
    coverage_file = root / '.coverage'

    print(f"Cleaning project root: {root}")
    print("-- Dry run mode --") if args.dry_run else None

    # Show what we'll remove
    print("Planned directory removals:")
    for p in patterns_dirs:
        print(" - ", p)
    print("Planned file removals:")
    print(" - .coverage")
    print(" - all .pyc files and __pycache__ directories under project (excluding venv/.venv)")

    if args.remove_venv:
        venv_paths = [root / '.venv', root / 'venv']
        if args.venv_name:
            venv_paths.append(root / args.venv_name)
        if args.venv_dir:
            venv_paths.append(Path(args.venv_dir).resolve())
        print("Virtual environments planned for removal:")
        for p in venv_paths:
            print(" - ", p)

    if not args.yes and not args.dry_run:
        proceed = confirm("Proceed with the removal of the listed items? THIS CANNOT BE UNDONE")
        if not proceed:
            print("Aborting.")
            return 0

    # Remove directories
    for p in patterns_dirs:
        safe_rmtree(Path(p), dry_run=args.dry_run)

    # Remove coverage file
    if coverage_file.exists():
        if args.dry_run:
            print(f"(dry-run) Would remove file: {coverage_file}")
        else:
            try:
                coverage_file.unlink()
                print(f"Removed file: {coverage_file}")
            except Exception as e:
                print(f"Failed to remove {coverage_file}: {e}")

    # Remove __pycache__ and .pyc
    remove_pycache_dirs(root, dry_run=args.dry_run)
    remove_pyc_files(root, dry_run=args.dry_run)

    # Remove pytest caches and htmlcov - already covered in patterns

    # Remove venv(s) optionally
    if args.remove_venv:
        venv_paths = [root / '.venv', root / 'venv']
        if args.venv_name:
            venv_paths.append(root / args.venv_name)
        if args.venv_dir:
            venv_paths.append(Path(args.venv_dir).resolve())

        for v in venv_paths:
            if v.exists():
                # Avoid removing activated environment
                # On Windows we can't detect activation simply, but we can warn
                if args.dry_run:
                    print(f"(dry-run) Would remove venv: {v}")
                else:
                    if not args.yes:
                        warn = confirm(f"Remove virtual environment {v}? This may be in use.")
                        if not warn:
                            print(f"Skipping removal: {v}")
                            continue
                    safe_rmtree(v, dry_run=False)

    print("Cleanup complete.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
