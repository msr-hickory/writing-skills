"""Google Sheets formatting utility with Hickory brand colors and consulting standards.

This module provides a Python API for applying consulting-grade formatting
(cell styles, borders, column sizing, number formats, freeze panes) to Google Sheets.
Enforces Hickory branding and CLAUDE.md Spreadsheet Standards automatically.

Usage:
    # Library mode
    from lib.sheet_formatter import SheetFormatter
    fmt = SheetFormatter("sheet_id", "token_path")
    fmt.profile("summary_tab").apply()

    # Or custom formatting
    fmt = SheetFormatter("sheet_id")
    fmt.header_row(1, bold=True, bg_color=DARK_GREEN).freeze_rows(1).apply()

Reference:
    - CLAUDE.md Spreadsheet Standards: 18 formatting rules for consulting layouts
    - Hickory-Brand-Theme-Guide.md: Official color palette and usage guidelines
    - hickory_colors.py: Color palette definitions
"""

import sys
import os
import time
from pathlib import Path
from copy import deepcopy
import json
from typing import Any, Optional

from hickory_colors import (
    DARK_GREEN_HEX,
    FOREST_GREEN_HEX,
    WARM_CREAM_HEX,
    WHITE_HEX,
    BLACK_HEX,
    CREAM_DARK_HEX,
    DARK_GREEN_SHEETS,
    FOREST_GREEN_SHEETS,
    WARM_CREAM_SHEETS,
    WHITE_SHEETS,
    BLACK_SHEETS,
    CREAM_DARK_SHEETS,
    hex_to_rgb_float,
)


# ============================================================================
# HICKORY COLOR PALETTE (Convenience Constants)
# ============================================================================

# Core palette
DARK_GREEN = DARK_GREEN_SHEETS
FOREST_GREEN = FOREST_GREEN_SHEETS
WARM_CREAM = WARM_CREAM_SHEETS
WHITE = WHITE_SHEETS
BLACK = BLACK_SHEETS
CREAM_DARK = CREAM_DARK_SHEETS


# ============================================================================
# PROFILE DEFINITIONS
# ============================================================================

PROFILES = {
    "summary_tab": {
        "description": "Executive summary style: bold dark green headers, centered, alternating rows",
        "header_row": {
            "bg_color": DARK_GREEN,
            "fg_color": WHITE,
            "bold": True,
            "font_size": 12,
            "align": "CENTER",
            "row_num": 1,
        },
        "section_header_rows": {
            "bg_color": FOREST_GREEN,
            "fg_color": WHITE,
            "bold": True,
            "font_size": 11,
            # Rows are typically at 4, 15, 24 but caller can override
        },
        "alternating_rows": {
            "bg_color_even": WHITE,
            "bg_color_odd": WARM_CREAM,
            "data_start_row": 2,
        },
        "columns": {
            "A": {"width": 2},  # Spacer column (IB convention)
            "B": {"width": 18, "align": "LEFT"},  # Labels
            "C-Z": {"width": 14, "align": "RIGHT"},  # Default numeric
        },
        "freeze": {"rows": 1, "columns": 0},
        "borders": {"style": "SOLID", "color": CREAM_DARK},
    },
    "data_detail": {
        "description": "Data table style: consistent widths, frozen headers, right-aligned numbers",
        "header_row": {
            "bg_color": DARK_GREEN,
            "fg_color": WHITE,
            "bold": True,
            "font_size": 10,
            "align": "CENTER",
            "row_num": 1,
        },
        "columns": {
            "A": {"width": 2},  # Spacer
            "B-H": {"width": 12, "align": "LEFT"},
            "I-Z": {"width": 14, "align": "RIGHT"},
        },
        "freeze": {"rows": 1, "columns": 1},
        "borders": {"style": "SOLID", "color": CREAM_DARK},
        "alternating_rows": {
            "bg_color_even": WHITE,
            "bg_color_odd": WARM_CREAM,
            "data_start_row": 2,
        },
    },
    "kpi_dashboard": {
        "description": "KPI metrics style: large bold metrics, section headers, accent colors",
        "header_row": {
            "bg_color": DARK_GREEN,
            "fg_color": WHITE,
            "bold": True,
            "font_size": 14,
            "align": "CENTER",
            "row_num": 1,
        },
        "section_headers": {
            "bg_color": FOREST_GREEN,
            "fg_color": WHITE,
            "bold": True,
            "font_size": 11,
        },
        "columns": {
            "A": {"width": 2},
            "B-C": {"width": 20, "align": "LEFT"},
            "D-F": {"width": 14, "align": "RIGHT", "format": "$#,##0"},
        },
        "freeze": {"rows": 1, "columns": 0},
    },
}


# ============================================================================
# MAIN SHEETFORMATTER CLASS
# ============================================================================


class SheetFormatter:
    """Builder-pattern API for Google Sheets formatting.

    Accumulates formatting specifications and applies them to a sheet via
    Google Sheets batchUpdate API. Uses Hickory brand colors and CLAUDE.md
    Spreadsheet Standards by default.

    Attributes:
        sheet_id: Google Sheets spreadsheet ID
        token_path: Path to OAuth token file
        service: Google Sheets API service object (lazy-loaded)

    Example:
        >>> fmt = SheetFormatter("1abc...", "token.json")
        >>> fmt.profile("summary_tab").freeze_rows(1).apply()

        >>> fmt = SheetFormatter("1abc...")
        >>> fmt.header_row(1, bold=True, bg_color=DARK_GREEN) \\
        ...     .column("C", align="RIGHT", format="$#,##0.00") \\
        ...     .freeze_rows(1) \\
        ...     .apply(tabs=["Summary"], force=False)
    """

    def __init__(
        self,
        sheet_id: str,
        token_path: Optional[str] = None,
        service: Optional[Any] = None,
    ):
        """Initialize SheetFormatter.

        Args:
            sheet_id: Google Sheets spreadsheet ID (required)
            token_path: Path to OAuth token JSON file. If None, checks env var
                       SHEETS_TOKEN_FILE, then falls back to default location.
            service: Pre-instantiated Google Sheets API service object.
                    If None, auto-creates via googleapiclient.discovery.build()

        Raises:
            FileNotFoundError: If token file not found
            ValueError: If sheet_id is empty
        """
        if not sheet_id:
            raise ValueError("sheet_id is required")

        self.sheet_id = sheet_id
        self.token_path = token_path or os.getenv(
            "SHEETS_TOKEN_FILE",
            str(Path.home() / ".sheets_token.json"),
        )
        self.service = service

        # Storage for accumulated formatting specs
        self._specs = {
            "header_rows": [],  # List of header_row dicts
            "columns": {},  # Dict of col_letter -> col_spec
            "freeze": None,  # {"rows": n, "columns": m}
            "borders": [],  # List of border requests
            "number_formats": {},  # Dict of col_range -> format
        }

        # Track if a profile was applied (for merge behavior)
        self._active_profile = None

    def profile(self, name: str) -> "SheetFormatter":
        """Apply a pre-built formatting profile.

        Pre-built profiles enforce consulting standards and Hickory branding.
        Custom settings can override profile defaults via subsequent method calls.

        Args:
            name: Profile name. Valid options:
                 - "summary_tab": Executive summary (bold headers, centered, alternating rows)
                 - "data_detail": Data table (left text, right numbers, frozen header)
                 - "kpi_dashboard": KPI metrics (large numbers, section headers)

        Returns:
            self (for method chaining)

        Raises:
            ValueError: If profile not found

        Example:
            >>> fmt.profile("summary_tab")  # Apply defaults
            >>> fmt.header_row(1, bold=False)  # Override: not bold
        """
        if name not in PROFILES:
            raise ValueError(
                f"Profile '{name}' not found. Valid profiles: {list(PROFILES.keys())}"
            )

        self._active_profile = name
        p = PROFILES[name]

        # Load header row from profile
        if "header_row" in p:
            hr = p["header_row"]
            self._specs["header_rows"].append({
                "row_num": hr.get("row_num", 1),
                "bold": hr.get("bold", True),
                "bg_color": hr.get("bg_color", DARK_GREEN),
                "fg_color": hr.get("fg_color", WHITE),
                "font_size": hr.get("font_size", 11),
                "align": hr.get("align", "CENTER"),
            })

        # Load columns from profile
        if "columns" in p:
            self._specs["columns"].update(p["columns"])

        # Load freeze from profile
        if "freeze" in p:
            self._specs["freeze"] = p["freeze"]

        return self

    def header_row(
        self,
        row_num: int,
        bold: Optional[bool] = None,
        bg_color: Optional[dict] = None,
        fg_color: Optional[dict] = None,
        font_size: Optional[int] = None,
        align: Optional[str] = None,
    ) -> "SheetFormatter":
        """Format a header row with specified styling.

        Args:
            row_num: 1-indexed row number
            bold: Bold text (True/False). If None, uses profile default or False.
            bg_color: Background color dict (e.g., DARK_GREEN). If None, uses WHITE.
            fg_color: Text color dict (e.g., WHITE). If None, uses BLACK.
            font_size: Font size in points (8-24). If None, uses 11.
            align: Text alignment: "LEFT", "CENTER", "RIGHT". If None, uses "CENTER".

        Returns:
            self (for method chaining)

        Raises:
            ValueError: If row_num < 1 or align not in valid options

        Example:
            >>> fmt.header_row(1, bold=True, bg_color=DARK_GREEN, fg_color=WHITE)
        """
        if row_num < 1:
            raise ValueError("row_num must be >= 1")
        if align and align not in ["LEFT", "CENTER", "RIGHT"]:
            raise ValueError(f"Invalid alignment: {align}")

        self._specs["header_rows"].append({
            "row_num": row_num,
            "bold": bold if bold is not None else True,
            "bg_color": bg_color if bg_color is not None else WHITE,
            "fg_color": fg_color if fg_color is not None else BLACK,
            "font_size": font_size if font_size is not None else 11,
            "align": align if align is not None else "CENTER",
        })

        return self

    def column(
        self,
        col_letter: str,
        width: Optional[int] = None,
        align: Optional[str] = None,
        format: Optional[str] = None,
        bg_color: Optional[dict] = None,
        fg_color: Optional[dict] = None,
    ) -> "SheetFormatter":
        """Format a column or column range.

        Args:
            col_letter: Column letter or range: "A", "B", "C:E", "D:Z"
            width: Column width in character units (approx 1 char = 7-8 pixels)
            align: Text alignment: "LEFT", "CENTER", "RIGHT"
            format: Number format (Sheets syntax): "$#,##0.00", "0.0%", "yyyy-mm-dd"
            bg_color: Background color dict
            fg_color: Text color dict

        Returns:
            self (for method chaining)

        Raises:
            ValueError: If col_letter format invalid or align not in valid options

        Example:
            >>> fmt.column("C", width=14, align="RIGHT", format="$#,##0.00")
            >>> fmt.column("D:F", width=12, align="CENTER")
        """
        if align and align not in ["LEFT", "CENTER", "RIGHT"]:
            raise ValueError(f"Invalid alignment: {align}")

        col_key = col_letter.upper()
        self._specs["columns"][col_key] = {
            "width": width,
            "align": align,
            "format": format,
            "bg_color": bg_color,
            "fg_color": fg_color,
        }

        return self

    def freeze_rows(self, n: int) -> "SheetFormatter":
        """Freeze the first n rows (header rows).

        Args:
            n: Number of rows to freeze (1-based)

        Returns:
            self (for method chaining)

        Raises:
            ValueError: If n < 0

        Example:
            >>> fmt.freeze_rows(1)  # Freeze header row
            >>> fmt.freeze_rows(3)  # Freeze first 3 rows
        """
        if n < 0:
            raise ValueError("n must be >= 0")

        if self._specs["freeze"] is None:
            self._specs["freeze"] = {"rows": 0, "columns": 0}
        self._specs["freeze"]["rows"] = n

        return self

    def freeze_columns(self, n: int) -> "SheetFormatter":
        """Freeze the first n columns (label columns).

        Args:
            n: Number of columns to freeze (0-based, e.g., 1 freezes column A)

        Returns:
            self (for method chaining)

        Raises:
            ValueError: If n < 0

        Example:
            >>> fmt.freeze_columns(1)  # Freeze column A
            >>> fmt.freeze_columns(2)  # Freeze columns A and B
        """
        if n < 0:
            raise ValueError("n must be >= 0")

        if self._specs["freeze"] is None:
            self._specs["freeze"] = {"rows": 0, "columns": 0}
        self._specs["freeze"]["columns"] = n

        return self

    def freeze(self, rows: int, columns: int = 0) -> "SheetFormatter":
        """Freeze rows and columns simultaneously.

        Args:
            rows: Number of rows to freeze (header rows)
            columns: Number of columns to freeze (label columns, default 0)

        Returns:
            self (for method chaining)

        Example:
            >>> fmt.freeze(1, 1)  # Freeze row 1 and column A
        """
        self.freeze_rows(rows)
        self.freeze_columns(columns)
        return self

    def border(
        self,
        col_range: str = "A:Z",
        style: str = "SOLID",
        color: Optional[dict] = None,
        position: str = "BOTTOM",
    ) -> "SheetFormatter":
        """Add borders to cells.

        Args:
            col_range: Column range: "A:A", "B:D", "A:Z" (default all)
            style: Border line style: "SOLID", "DOTTED", "DASHED" (default SOLID)
            color: Border color dict (default CREAM_DARK)
            position: Which edges: "TOP", "BOTTOM", "LEFT", "RIGHT", "ALL"
                     (default BOTTOM)

        Returns:
            self (for method chaining)

        Example:
            >>> fmt.border("A:Z", style="SOLID", color=CREAM_DARK, position="BOTTOM")
        """
        if style not in ["SOLID", "DOTTED", "DASHED"]:
            raise ValueError(f"Invalid border style: {style}. Must be SOLID, DOTTED, or DASHED.")
        if position not in ["TOP", "BOTTOM", "LEFT", "RIGHT", "ALL"]:
            raise ValueError(f"Invalid border position: {position}. Must be TOP, BOTTOM, LEFT, RIGHT, or ALL.")

        self._specs["borders"].append({
            "col_range": col_range,
            "style": style,
            "color": color or CREAM_DARK,
            "position": position,
        })

        return self

    def apply(
        self,
        tabs: Optional[list[str]] = None,
        force: bool = False,
    ) -> None:
        """Apply accumulated formatting to the sheet via Google Sheets API.

        Applies formatting to specified tabs (or all tabs if None).
        By default, prompts user for confirmation before applying.

        Args:
            tabs: List of tab names to format (e.g., ["Summary", "Detail"]).
                 If None, formats all tabs in the sheet.
            force: If True, skip confirmation prompt (for automation/CI).
                  If False (default), prompt user before applying.

        Returns:
            None

        Raises:
            RuntimeError: If user declines confirmation
            RuntimeError: If batch formatting fails (with detailed status)
            ValueError: If tabs not found in sheet
            EnvironmentError: If non-TTY environment and force=False
            FileNotFoundError: If token file not found
            Exception: On Google Sheets API errors (401, 403, 429, etc.)

        Side Effects:
            - Formats cells, columns, and rows in the specified tabs
            - May refresh OAuth token if expired
            - Prints status messages to stdout

        Example:
            >>> fmt.apply()  # Format all tabs with confirmation
            >>> fmt.apply(tabs=["Summary"], force=True)  # No confirmation
        """
        start_time = time.time()

        # 1. TTY check
        if not force and not sys.stdin.isatty():
            raise EnvironmentError(
                "apply(force=False) requires an interactive terminal (TTY). "
                "Use apply(force=True) or --force flag in CI/CD environments."
            )

        # 2. Get service and list tabs
        service = self._get_sheets_service()
        spreadsheet = service.spreadsheets().get(spreadsheetId=self.sheet_id).execute()
        all_tabs = [s["properties"]["title"] for s in spreadsheet["sheets"]]
        target_tabs = tabs if tabs is not None else all_tabs

        # Validate tabs exist
        missing = [t for t in target_tabs if t not in all_tabs]
        if missing:
            raise ValueError(f"Tabs not found in sheet: {missing}. Available: {all_tabs}")

        # 3. Confirm
        if not force:
            if not self._prompt_confirmation(target_tabs):
                raise RuntimeError("Formatting cancelled by user.")

        # 4. Apply per tab with error tracking
        succeeded = []
        failed = []
        for tab_name in target_tabs:
            try:
                tab_props = next(
                    s["properties"] for s in spreadsheet["sheets"]
                    if s["properties"]["title"] == tab_name
                )
                sheet_id = tab_props["sheetId"]
                requests = self._build_batch_requests(tab_name, sheet_id)
                if not requests:
                    succeeded.append(tab_name)
                    continue
                service.spreadsheets().batchUpdate(
                    spreadsheetId=self.sheet_id,
                    body={"requests": requests}
                ).execute()
                succeeded.append(tab_name)
            except Exception as e:
                failed.append((tab_name, str(e)))

        # 5. Report
        elapsed = time.time() - start_time
        print(f"[sheet_formatter] Formatted {len(succeeded)} tab(s): {succeeded} in {elapsed:.1f}s")
        if failed:
            raise RuntimeError(
                f"Formatting failed for {len(failed)} tab(s):\n"
                + "\n".join(f"  {tab}: {err}" for tab, err in failed)
            )

    def _build_batch_requests(self, tab_name: str, sheet_id: int) -> list[dict]:
        """Build Google Sheets batchUpdate request dicts from accumulated specs.

        Converts stored formatting specs into Sheets API request format.

        Args:
            tab_name: Tab name being formatted (for logging)
            sheet_id: Sheets API sheetId (numeric ID)

        Returns:
            List of batchUpdate request dicts (see Google Sheets API docs)

        Raises:
            ValueError: If specs are invalid or inconsistent

        Example:
            >>> requests = fmt._build_batch_requests("Summary", 12345)
            >>> # requests = [
            >>> #   {"repeatCell": {...}},
            >>> #   {"updateDimensionProperties": {...}},
            >>> #   {"updateSheetProperties": {...}},
            >>> # ]
        """
        requests = []
        MAX_COL = 26  # A-Z

        # 1. Header rows (repeatCell)
        for hr in self._specs["header_rows"]:
            row = hr["row_num"] - 1  # 0-indexed
            cell_fmt = {}
            tf = {}
            fields = []

            if hr.get("bold") is not None:
                tf["bold"] = hr["bold"]
            if hr.get("fg_color"):
                tf["foregroundColor"] = hr["fg_color"]
            if hr.get("font_size"):
                tf["fontSize"] = hr["font_size"]
            if tf:
                cell_fmt["textFormat"] = tf
                fields.append("userEnteredFormat.textFormat")
            if hr.get("bg_color"):
                cell_fmt["backgroundColor"] = hr["bg_color"]
                fields.append("userEnteredFormat.backgroundColor")
            if hr.get("align"):
                cell_fmt["horizontalAlignment"] = hr["align"]
                fields.append("userEnteredFormat.horizontalAlignment")

            if cell_fmt:
                requests.append({
                    "repeatCell": {
                        "range": {
                            "sheetId": sheet_id,
                            "startRowIndex": row, "endRowIndex": row + 1,
                            "startColumnIndex": 0, "endColumnIndex": MAX_COL,
                        },
                        "cell": {"userEnteredFormat": cell_fmt},
                        "fields": ",".join(fields),
                    }
                })

        # 2. Column widths
        for col_spec_key, spec in self._specs["columns"].items():
            if spec.get("width") is None:
                continue
            # Parse "A", "B", "C:E", "B-H"
            col_spec_key = col_spec_key.replace("-", ":")
            parts = col_spec_key.split(":")
            start = ord(parts[0].strip().upper()) - ord("A")
            end = ord(parts[-1].strip().upper()) - ord("A") + 1
            px = spec["width"] * 8  # char units → pixels
            requests.append({
                "updateDimensionProperties": {
                    "range": {"sheetId": sheet_id, "dimension": "COLUMNS",
                              "startIndex": start, "endIndex": end},
                    "properties": {"pixelSize": px},
                    "fields": "pixelSize",
                }
            })

        # 3. Freeze rows/columns
        if self._specs["freeze"]:
            freeze = self._specs["freeze"]
            grid_props = {}
            fields = []
            if freeze.get("rows") is not None and freeze["rows"] > 0:
                grid_props["frozenRowCount"] = freeze["rows"]
                fields.append("gridProperties.frozenRowCount")
            if freeze.get("columns") is not None and freeze["columns"] > 0:
                grid_props["frozenColumnCount"] = freeze["columns"]
                fields.append("gridProperties.frozenColumnCount")
            if grid_props:
                requests.append({
                    "updateSheetProperties": {
                        "properties": {"sheetId": sheet_id, "gridProperties": grid_props},
                        "fields": ",".join(fields),
                    }
                })

        # 4. Borders (updateBorders)
        for border_spec in self._specs.get("borders", []):
            col_range = border_spec["col_range"].replace("-", ":")
            parts = col_range.split(":")
            start_col = ord(parts[0].strip().upper()) - ord("A")
            end_col = ord(parts[-1].strip().upper()) - ord("A") + 1

            # Build border objects for each position
            border_obj = {}
            if border_spec["position"] in ["TOP", "ALL"]:
                border_obj["top"] = {
                    "style": border_spec["style"],
                    "color": border_spec["color"],
                }
            if border_spec["position"] in ["BOTTOM", "ALL"]:
                border_obj["bottom"] = {
                    "style": border_spec["style"],
                    "color": border_spec["color"],
                }
            if border_spec["position"] in ["LEFT", "ALL"]:
                border_obj["left"] = {
                    "style": border_spec["style"],
                    "color": border_spec["color"],
                }
            if border_spec["position"] in ["RIGHT", "ALL"]:
                border_obj["right"] = {
                    "style": border_spec["style"],
                    "color": border_spec["color"],
                }

            # Create updateBorders request
            update_borders_req = {
                "updateBorders": {
                    "range": {
                        "sheetId": sheet_id,
                        "startColumnIndex": start_col,
                        "endColumnIndex": end_col,
                    },
                }
            }

            # Add border positions to request
            if "top" in border_obj:
                update_borders_req["updateBorders"]["top"] = border_obj["top"]
            if "bottom" in border_obj:
                update_borders_req["updateBorders"]["bottom"] = border_obj["bottom"]
            if "left" in border_obj:
                update_borders_req["updateBorders"]["left"] = border_obj["left"]
            if "right" in border_obj:
                update_borders_req["updateBorders"]["right"] = border_obj["right"]

            requests.append(update_borders_req)

        return requests

    def _get_sheets_service(self):
        """Get or create Google Sheets API service object.

        Returns:
            Google Sheets API service (from googleapiclient.discovery)

        Raises:
            FileNotFoundError: If token file not found
            Exception: On authentication error
        """
        if self.service is not None:
            return self.service

        from googleapiclient.discovery import build
        from google.oauth2.credentials import Credentials

        if not Path(self.token_path).exists():
            raise FileNotFoundError(f"Token file not found: {self.token_path}")

        with open(self.token_path) as f:
            data = json.load(f)

        # Token files use either "access_token" or "token" as the key
        token_key = "access_token" if "access_token" in data else "token"
        creds = Credentials(
            token=data[token_key],
            refresh_token=data.get("refresh_token"),
            client_id=data.get("client_id"),
            client_secret=data.get("client_secret"),
            token_uri="https://oauth2.googleapis.com/token",
        )
        self.service = build("sheets", "v4", credentials=creds)
        return self.service

    def _prompt_confirmation(self, tabs: list[str]) -> bool:
        """Prompt user to confirm formatting before applying.

        Shows sheet URL and list of tabs to be formatted.

        Args:
            tabs: List of tab names to be formatted

        Returns:
            True if user confirms, False if user declines

        Raises:
            EnvironmentError: If stdin not available (non-TTY environment)
        """
        sheet_url = f"https://docs.google.com/spreadsheets/d/{self.sheet_id}"
        print(f"\n[sheet_formatter] About to apply formatting to:")
        print(f"  Sheet: {sheet_url}")
        print(f"  Tabs ({len(tabs)}): {', '.join(tabs)}")
        answer = input("  Proceed? (y/N): ").strip().lower()
        return answer in ("y", "yes")


# ============================================================================
# HELPER FUNCTIONS
# ============================================================================


def hex_to_sheets_color(hex_color: str) -> dict:
    """Convert hex color to Sheets API RGB format.

    Args:
        hex_color: Hex color (e.g., "#1D231C")

    Returns:
        Dict with keys "red", "green", "blue" (values 0.0-1.0)

    Example:
        >>> hex_to_sheets_color("#1D231C")
        {'red': 0.114, 'green': 0.137, 'blue': 0.110}
    """
    return hex_to_rgb_float(hex_color)


def load_profile_from_json(config_path: str) -> dict:
    """Load custom formatting profile from JSON file.

    Args:
        config_path: Path to JSON config file

    Returns:
        Dict with profile configuration

    Raises:
        FileNotFoundError: If config file not found
        json.JSONDecodeError: If JSON is invalid
        ValueError: If config schema is invalid

    Schema:
        {
            "profile": "summary_tab",  # Base profile (optional)
            "sheet_id": "1abc...",     # Google Sheets ID (optional, for CLI)
            "header_row": {
                "row_num": 1,
                "bold": true,
                "bg_color": "#1D231C",  # Hex color
                "fg_color": "#FFFFFF",
                "font_size": 12,
                "align": "CENTER"
            },
            "columns": {
                "A": {"width": 2},
                "B": {"width": 18, "align": "LEFT"}
            },
            "freeze": {"rows": 1, "columns": 0}
        }

    Example:
        >>> profile = load_profile_from_json("custom_format.json")
        >>> fmt = SheetFormatter(profile.get("sheet_id"))
        >>> fmt.profile(profile.get("profile")).apply(force=True)
    """
    config_file = Path(config_path)
    if not config_file.exists():
        raise FileNotFoundError(f"Config file not found: {config_path}")

    try:
        with open(config_file) as f:
            config = json.load(f)
    except json.JSONDecodeError as e:
        raise ValueError(f"Invalid JSON in {config_path}: {e}")

    # Validate required fields (must have profile or header_row or columns or freeze)
    if not any(key in config for key in ["profile", "header_row", "columns", "freeze"]):
        raise ValueError("Config must specify at least one of: 'profile', 'header_row', 'columns', 'freeze'")

    # Convert hex colors to Sheets API format if present
    if "header_row" in config:
        hr = config["header_row"]
        if "bg_color" in hr and isinstance(hr["bg_color"], str):
            hr["bg_color"] = hex_to_sheets_color(hr["bg_color"])
        if "fg_color" in hr and isinstance(hr["fg_color"], str):
            hr["fg_color"] = hex_to_sheets_color(hr["fg_color"])

    if "columns" in config:
        for col_spec in config["columns"].values():
            if "bg_color" in col_spec and isinstance(col_spec["bg_color"], str):
                col_spec["bg_color"] = hex_to_sheets_color(col_spec["bg_color"])
            if "fg_color" in col_spec and isinstance(col_spec["fg_color"], str):
                col_spec["fg_color"] = hex_to_sheets_color(col_spec["fg_color"])

    return config


if __name__ == "__main__":
    # Example usage (for testing during development)
    print("SheetFormatter module loaded successfully")
    print(f"Available profiles: {list(PROFILES.keys())}")
    print(f"Hickory colors: DARK_GREEN, FOREST_GREEN, WARM_CREAM, WHITE, BLACK, CREAM_DARK")
