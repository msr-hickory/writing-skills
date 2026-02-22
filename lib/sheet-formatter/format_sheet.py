#!/usr/bin/env python
"""CLI tool for applying consulting-grade formatting to Google Sheets.

Usage:
    python format_sheet.py --sheet-id <ID> --profile summary_tab --force
    python format_sheet.py --config custom_format.json
    python format_sheet.py --sheet-id <ID> --profile data_detail --tabs "Summary" "Detail" --force

Examples:
    # Format all tabs with a profile
    python format_sheet.py \
      --sheet-id 1glOaEsjg97KcF2yD20a40nJtXcLAKlnYqz8DPQLI8EQ \
      --profile summary_tab \
      --force

    # Format specific tabs with custom options
    python format_sheet.py \
      --sheet-id 1glOaEsjg97KcF2yD20a40nJtXcLAKlnYqz8DPQLI8EQ \
      --profile data_detail \
      --tabs "All Leads" "Summary" \
      --header-row 1 \
      --header-bold \
      --freeze-rows 1 \
      --force
"""

import sys
import argparse
import json
from pathlib import Path

from sheet_formatter import SheetFormatter, PROFILES


def main():
    parser = argparse.ArgumentParser(
        description="Apply consulting-grade formatting to Google Sheets",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Format with profile
  python format_sheet.py --sheet-id <ID> --profile summary_tab --force

  # Format specific tabs
  python format_sheet.py --sheet-id <ID> --profile data_detail --tabs "Summary" "Detail" --force

  # Format with config file
  python format_sheet.py --config format_config.json --force
        """,
    )

    # Required arguments
    parser.add_argument(
        "--sheet-id",
        help="Google Sheets ID",
    )

    # Profile and tabs
    parser.add_argument(
        "--profile",
        choices=list(PROFILES.keys()),
        help="Pre-built profile name (summary_tab, data_detail, kpi_dashboard)",
    )
    parser.add_argument(
        "--tabs",
        nargs="+",
        help="Tab names to format (space-separated). If not specified, formats all tabs.",
    )

    # Token and force
    parser.add_argument(
        "--token-path",
        help="Path to OAuth token file. Defaults to SHEETS_TOKEN_FILE env var.",
    )
    parser.add_argument(
        "--force",
        action="store_true",
        help="Skip confirmation prompt (for CI/CD environments)",
    )

    # Config file alternative
    parser.add_argument(
        "--config",
        help="JSON config file path (alternative to --profile)",
    )

    # Individual formatting options (overrides profile defaults)
    parser.add_argument(
        "--header-row",
        type=int,
        help="Header row number (1-based)",
    )
    parser.add_argument(
        "--header-bold",
        action="store_true",
        help="Make header bold",
    )
    parser.add_argument(
        "--freeze-rows",
        type=int,
        help="Number of rows to freeze",
    )
    parser.add_argument(
        "--freeze-columns",
        type=int,
        help="Number of columns to freeze",
    )

    args = parser.parse_args()

    try:
        # Validate: must specify either --config or --profile
        if not args.config and not args.sheet_id:
            print("[ERROR] Either --config or --sheet-id is required", file=sys.stderr)
            parser.print_help()
            sys.exit(1)

        if not args.config and not args.profile:
            print("[ERROR] Specify either --config or --profile", file=sys.stderr)
            sys.exit(1)

        # Initialize formatter
        fmt = SheetFormatter(
            args.sheet_id or "placeholder",  # sheet_id needed for config, but we use config path
            token_path=args.token_path,
        )

        # Load configuration
        if args.config:
            config_path = Path(args.config)
            if not config_path.exists():
                print(f"[ERROR] Config file not found: {args.config}", file=sys.stderr)
                sys.exit(1)

            with open(config_path) as f:
                config = json.load(f)

            # Validate config has sheet_id
            if "sheet_id" not in config:
                print("[ERROR] Config must include 'sheet_id'", file=sys.stderr)
                sys.exit(1)

            # Update formatter with config sheet_id
            fmt.sheet_id = config["sheet_id"]

            # Load profile from config if specified
            if "profile" in config:
                fmt.profile(config["profile"])

            # Apply config-specified overrides
            if "header_row" in config:
                hr = config["header_row"]
                fmt.header_row(
                    hr.get("row_num", 1),
                    bold=hr.get("bold", True),
                    bg_color=hr.get("bg_color"),
                    fg_color=hr.get("fg_color"),
                    font_size=hr.get("font_size"),
                    align=hr.get("align"),
                )

            if "columns" in config:
                for col_key, col_spec in config["columns"].items():
                    fmt.column(
                        col_key,
                        width=col_spec.get("width"),
                        align=col_spec.get("align"),
                        format=col_spec.get("format"),
                    )

            if "freeze" in config:
                freeze = config["freeze"]
                fmt.freeze(
                    freeze.get("rows", 0),
                    freeze.get("columns", 0),
                )

            # Override with CLI args if specified
            if args.header_row:
                fmt.header_row(args.header_row, bold=args.header_bold or False)
            if args.freeze_rows:
                fmt.freeze_rows(args.freeze_rows)
            if args.freeze_columns:
                fmt.freeze_columns(args.freeze_columns)

        else:
            # Use profile + CLI args (no config file)
            fmt.profile(args.profile)

            # Apply CLI option overrides
            if args.header_row:
                fmt.header_row(args.header_row, bold=args.header_bold or False)
            if args.freeze_rows:
                fmt.freeze_rows(args.freeze_rows)
            if args.freeze_columns:
                fmt.freeze_columns(args.freeze_columns)

        # Apply formatting
        try:
            fmt.apply(tabs=args.tabs, force=args.force)
            print("[OK] Formatting applied successfully")
            sys.exit(0)

        except EnvironmentError as e:
            print(f"[ERROR] {e}", file=sys.stderr)
            print(f"       Use --force to skip confirmation (for CI/CD)", file=sys.stderr)
            sys.exit(1)

    except FileNotFoundError as e:
        print(f"[ERROR] File not found: {e}", file=sys.stderr)
        sys.exit(1)

    except ValueError as e:
        print(f"[ERROR] Invalid input: {e}", file=sys.stderr)
        sys.exit(1)

    except RuntimeError as e:
        print(f"[ERROR] {e}", file=sys.stderr)
        sys.exit(1)

    except Exception as e:
        print(f"[ERROR] Unexpected error: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
