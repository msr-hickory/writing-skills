"""Shared utilities library for Hickory projects.

This directory contains reusable tools and utilities shared across multiple projects:
- sheet_formatter: Google Sheets formatting utility
- hickory_colors: Official Hickory brand color palette

Projects should add this directory to their sys.path to import from here:

    import sys
    sys.path.insert(0, 'C:/Users/mspit/AI/lib')

    from sheet_formatter import SheetFormatter
    from hickory_colors import DARK_GREEN

Or by setting PYTHONPATH environment variable:

    export PYTHONPATH="C:/Users/mspit/AI/lib:$PYTHONPATH"
    python script.py
"""
