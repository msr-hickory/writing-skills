# SheetFormatter Guide

Consulting-grade Google Sheets formatting utility for Python. Apply professional formatting to Google Sheets using pre-built profiles, custom configurations, or programmatic API.

## Quick Start

### Library Usage

```python
from sheet_formatter import SheetFormatter

# Create formatter with a pre-built profile
fmt = SheetFormatter(sheet_id="1glOaEsjg97KcF2yD20a40nJtXcLAKlnYqz8DPQLI8EQ")
fmt.profile("data_detail") \
   .apply(tabs=["All Leads"], force=True)
```

### CLI Usage

```bash
# Format all tabs with a profile
python format_sheet.py \
  --sheet-id 1glOaEsjg97KcF2yD20a40nJtXcLAKlnYqz8DPQLI8EQ \
  --profile summary_tab \
  --force

# Format specific tabs
python format_sheet.py \
  --sheet-id 1glOaEsjg97KcF2yD20a40nJtXcLAKlnYqz8DPQLI8EQ \
  --profile data_detail \
  --tabs "All Leads" "Summary" \
  --force

# Format with JSON config
python format_sheet.py \
  --config custom_format.json \
  --force
```

---

## Table of Contents

1. [Pre-Built Profiles](#pre-built-profiles)
2. [Builder Pattern API](#builder-pattern-api)
3. [CLI Tool](#cli-tool)
4. [Custom Formatting](#custom-formatting)
5. [JSON Configuration](#json-configuration)
6. [Error Handling](#error-handling)
7. [Integration Examples](#integration-examples)
8. [Hickory Color Palette](#hickory-color-palette)

---

## Pre-Built Profiles

SheetFormatter includes 3 consulting-grade profiles ready to use.

### Profile 1: `summary_tab`

**Use Case:** Executive summaries, KPI dashboards, financial summaries

**Features:**
- Bold Dark Green headers (#1D231C), centered, 12pt
- Bold Forest Green section headers (#51714E), 11pt
- Alternating White/Warm Cream data rows (#FFFFFF / #E1DFD9)
- Column widths: 2 (spacer), 18 (labels), 14 (data)
- Freeze row 1

**Example:**
```python
fmt = SheetFormatter(sheet_id)
fmt.profile("summary_tab").apply(tabs=["Summary"], force=True)
```

### Profile 2: `data_detail`

**Use Case:** Data tables, audit results, detailed reports

**Features:**
- Bold Dark Green headers, centered, 10pt
- Alternating White/Warm Cream data rows
- Column widths: 2 (spacer), 12 (text), 14 (numbers)
- Freeze row 1 + column A (label preservation)
- Solid bottom borders on data rows

**Example:**
```python
fmt = SheetFormatter(sheet_id)
fmt.profile("data_detail").apply(tabs=["Detail"], force=True)
```

### Profile 3: `kpi_dashboard`

**Use Case:** KPI metrics, team scorecards, live dashboards

**Features:**
- Bold Dark Green headers, 14pt (large)
- Bold Forest Green section headers
- Right-aligned large metric values
- Currency formatting ($#,##0)

**Example:**
```python
fmt = SheetFormatter(sheet_id)
fmt.profile("kpi_dashboard").apply(tabs=["Metrics"], force=True)
```

---

## Builder Pattern API

SheetFormatter uses a fluent builder pattern for method chaining. All methods return `self`, allowing you to chain operations.

### Constructor

```python
from sheet_formatter import SheetFormatter

# With default token path (uses SHEETS_TOKEN_FILE env var)
fmt = SheetFormatter(sheet_id="1abc...")

# With custom token path
fmt = SheetFormatter(sheet_id="1abc...", token_path="/path/to/token.json")

# With mock service (for testing)
fmt = SheetFormatter(sheet_id="1abc...", service=mock_service)
```

### Methods (Chainable)

#### `profile(name: str)`
Load a pre-built profile. Must be one of: `"summary_tab"`, `"data_detail"`, `"kpi_dashboard"`.

```python
fmt.profile("data_detail")
```

#### `header_row(row_num, bold=True, bg_color=None, fg_color=None, font_size=11, align="CENTER")`
Format a header row (usually row 1).

```python
fmt.header_row(1, bold=True, bg_color=DARK_GREEN, fg_color=WHITE)
```

**Args:**
- `row_num`: Row number (1-based)
- `bold`: Bold text (default True)
- `bg_color`: Background color dict (default WHITE)
- `fg_color`: Foreground color dict (default BLACK)
- `font_size`: Font size in points (default 11)
- `align`: Text alignment: "LEFT", "CENTER", "RIGHT" (default "CENTER")

#### `column(col_letter, width=None, align=None, format=None, bg_color=None, fg_color=None)`
Format a column or column range.

```python
fmt.column("A", width=2)  # Single column
fmt.column("B:D", width=14, align="RIGHT")  # Range (B, C, D)
fmt.column("E-G", width=12, format="$#,##0.00")  # Alternative range syntax
```

**Args:**
- `col_letter`: Column letter(s): "A", "C:E", "B-H"
- `width`: Column width in character units (approximately)
- `align`: "LEFT", "CENTER", "RIGHT"
- `format`: Number format (e.g., "$#,##0.00" for currency, "0.00%" for percentages)
- `bg_color`: Background color dict
- `fg_color`: Foreground color dict

#### `freeze_rows(n)`
Freeze the first n rows.

```python
fmt.freeze_rows(1)  # Freeze header row
fmt.freeze_rows(3)  # Freeze first 3 rows
```

#### `freeze_columns(n)`
Freeze the first n columns.

```python
fmt.freeze_columns(1)  # Freeze column A
fmt.freeze_columns(2)  # Freeze columns A and B
```

#### `freeze(rows, columns=0)`
Freeze rows and columns simultaneously.

```python
fmt.freeze(1, 1)  # Freeze row 1 and column A
```

#### `border(col_range="A:Z", style="SOLID", color=None, position="BOTTOM")`
Add borders to cells.

```python
fmt.border("A:Z", style="SOLID", position="BOTTOM")  # Bottom borders
fmt.border("B:D", style="DOTTED", position="ALL")    # All edges
```

**Args:**
- `col_range`: Column range (e.g., "A:Z", "B-H")
- `style`: "SOLID", "DOTTED", or "DASHED" (default "SOLID")
- `color`: Border color dict (default CREAM_DARK)
- `position`: "TOP", "BOTTOM", "LEFT", "RIGHT", or "ALL" (default "BOTTOM")

#### `apply(tabs=None, force=False)`
Apply all accumulated formatting to the spreadsheet.

```python
fmt.apply()  # Format all tabs with confirmation
fmt.apply(tabs=["Summary", "Detail"], force=False)  # Confirm
fmt.apply(tabs=["All Leads"], force=True)  # No confirmation (CI/CD)
```

**Args:**
- `tabs`: List of tab names to format. If None, formats all tabs.
- `force`: Skip confirmation prompt (True for CI/CD, False for interactive)

**Raises:**
- `EnvironmentError`: If non-TTY and force=False
- `ValueError`: If tab not found
- `RuntimeError`: If formatting failed or user declined

### Complete Example

```python
from sheet_formatter import SheetFormatter, DARK_GREEN, WHITE

fmt = SheetFormatter("1glOaEsjg97KcF2yD20a40nJtXcLAKlnYqz8DPQLI8EQ")

fmt.profile("data_detail") \
   .header_row(1, bold=True, bg_color=DARK_GREEN, fg_color=WHITE) \
   .column("A", width=2) \
   .column("B:D", width=12) \
   .column("E:G", width=14, align="RIGHT") \
   .freeze_rows(1) \
   .freeze_columns(1) \
   .border("A:Z", position="BOTTOM") \
   .apply(tabs=["All Leads"], force=True)

print("[OK] Dashboard formatted successfully")
```

---

## CLI Tool

The `format_sheet.py` CLI tool provides a command-line interface for formatting without writing Python code.

### Installation

No installation needed. Run directly from repo root:

```bash
python format_sheet.py --help
```

### Arguments

| Argument | Type | Required | Default | Description |
|----------|------|----------|---------|-------------|
| `--sheet-id` | str | Yes* | — | Google Sheets ID |
| `--profile` | str | No | — | Profile name: summary_tab, data_detail, kpi_dashboard |
| `--tabs` | list | No | all tabs | Tab names to format (space-separated) |
| `--token-path` | str | No | SHEETS_TOKEN_FILE env var | Path to OAuth token JSON |
| `--force` | flag | No | False | Skip confirmation prompt |
| `--config` | str | No | — | JSON config file path (alternative to --profile) |
| `--header-row` | int | No | — | Header row number (1-based) |
| `--header-bold` | flag | No | False | Bold header |
| `--freeze-rows` | int | No | — | Number of rows to freeze |
| `--freeze-columns` | int | No | — | Number of columns to freeze |

*Either `--config` or `--sheet-id` (with `--profile`) is required.

### Usage Examples

**Format all tabs with profile:**
```bash
python format_sheet.py \
  --sheet-id 1glOaEsjg97KcF2yD20a40nJtXcLAKlnYqz8DPQLI8EQ \
  --profile data_detail \
  --force
```

**Format specific tabs:**
```bash
python format_sheet.py \
  --sheet-id 1glOaEsjg97KcF2yD20a40nJtXcLAKlnYqz8DPQLI8EQ \
  --profile summary_tab \
  --tabs Summary Executive-Report \
  --force
```

**Override profile defaults:**
```bash
python format_sheet.py \
  --sheet-id 1glOaEsjg97KcF2yD20a40nJtXcLAKlnYqz8DPQLI8EQ \
  --profile data_detail \
  --freeze-rows 2 \
  --freeze-columns 2 \
  --force
```

**Use JSON config file:**
```bash
python format_sheet.py \
  --config my_format.json \
  --force
```

---

## Custom Formatting

### Override Profile Defaults

Load a profile, then override specific settings:

```python
fmt = SheetFormatter(sheet_id)

# Start with data_detail profile
fmt.profile("data_detail")

# Override: use 2 frozen rows instead of 1
fmt.freeze_rows(2)

# Add custom column widths
fmt.column("H", width=20, format="$#,##0.00")

# Apply
fmt.apply(tabs=["Detailed Report"], force=True)
```

### Build Custom Formatting (No Profile)

If you don't need a pre-built profile, build custom formatting from scratch:

```python
from sheet_formatter import SheetFormatter, DARK_GREEN, WHITE, WARM_CREAM

fmt = SheetFormatter(sheet_id)

# Define header
fmt.header_row(1, bold=True, bg_color=DARK_GREEN, fg_color=WHITE, font_size=12)

# Define columns
fmt.column("A", width=2)  # Spacer
fmt.column("B:C", width=18, align="LEFT")  # Labels
fmt.column("D:H", width=12, align="RIGHT")  # Numbers

# Add borders
fmt.border("D:H", position="BOTTOM")

# Freeze
fmt.freeze(1, 2)

# Apply
fmt.apply(tabs=["Custom Report"], force=True)
```

### Column Width Guidelines

- **Spacer columns:** 2 character units (A)
- **Text/labels:** 18-20 character units (B:C)
- **Numbers/currency:** 12-14 character units (D:H)

Character units are approximate; they translate to pixels at 8px per character unit.

---

## JSON Configuration

### Config File Format

Create a JSON file with formatting specifications:

```json
{
  "sheet_id": "1glOaEsjg97KcF2yD20a40nJtXcLAKlnYqz8DPQLI8EQ",
  "profile": "data_detail",
  "header_row": {
    "row_num": 1,
    "bold": true,
    "bg_color": "#1D231C",
    "fg_color": "#FFFFFF",
    "font_size": 12,
    "align": "CENTER"
  },
  "columns": {
    "A": {
      "width": 2
    },
    "B:C": {
      "width": 18,
      "align": "LEFT"
    },
    "D:H": {
      "width": 12,
      "align": "RIGHT",
      "format": "$#,##0.00"
    }
  },
  "freeze": {
    "rows": 1,
    "columns": 2
  }
}
```

### Config Fields

**Top-level:**
- `sheet_id` (string): Google Sheets ID (required for CLI)
- `profile` (string): Pre-built profile (optional: summary_tab, data_detail, kpi_dashboard)

**header_row** (object, optional):
- `row_num` (int): Row number (1-based)
- `bold` (bool): Bold text
- `bg_color` (string): Hex color (#RRGGBB)
- `fg_color` (string): Hex color (#RRGGBB)
- `font_size` (int): Font size in points
- `align` (string): LEFT, CENTER, RIGHT

**columns** (object, optional):
- Keys are column letters/ranges (e.g., "A", "B:C", "D-H")
- Values are column specs:
  - `width` (int): Character units
  - `align` (string): LEFT, CENTER, RIGHT
  - `format` (string): Number format (e.g., "$#,##0.00")
  - `bg_color` (string): Hex color
  - `fg_color` (string): Hex color

**freeze** (object, optional):
- `rows` (int): Number of rows to freeze
- `columns` (int): Number of columns to freeze

### Load and Apply Config

```python
from sheet_formatter import load_profile_from_json, SheetFormatter

# Load config from JSON file
config = load_profile_from_json("custom_format.json")

# Create formatter and apply
fmt = SheetFormatter(config["sheet_id"])
if "profile" in config:
    fmt.profile(config["profile"])
fmt.apply(force=True)
```

---

## Error Handling

### Common Errors and Solutions

#### Error: "TTY required..."

**Cause:** Running in non-interactive environment (CI/CD) without `--force` flag.

**Solution:** Add `--force` flag:
```bash
python format_sheet.py --sheet-id <ID> --profile summary_tab --force
```

Or in Python:
```python
fmt.apply(force=True)
```

#### Error: "Tabs not found in sheet..."

**Cause:** Specified tab names don't exist in the spreadsheet.

**Solution:** Check available tabs:
```bash
python format_sheet.py --sheet-id <ID> --help
# (CLI will list available tabs on error)
```

Or remove `--tabs` to format all tabs:
```bash
python format_sheet.py --sheet-id <ID> --profile summary_tab --force
```

#### Error: "Token file not found..."

**Cause:** OAuth token missing or path incorrect.

**Solution:** Set `SHEETS_TOKEN_FILE` environment variable:
```bash
export SHEETS_TOKEN_FILE=/path/to/.sheets_token.json
python format_sheet.py --sheet-id <ID> --profile summary_tab --force
```

Or pass `--token-path`:
```bash
python format_sheet.py \
  --sheet-id <ID> \
  --profile summary_tab \
  --token-path /path/to/.sheets_token.json \
  --force
```

#### Error: "Invalid alignment..."

**Cause:** Invalid alignment value. Must be LEFT, CENTER, or RIGHT.

**Solution:** Fix the alignment:
```python
fmt.column("B", align="LEFT")  # Correct
# Not: align="JUSTIFY"  # Wrong
```

---

## Integration Examples

### Example 1: Dashboard Daily Refresh

Format the dashboard before writing data:

```python
from sheet_formatter import SheetFormatter
from angi_dashboard.config import DEFAULT_SPREADSHEET_ID

def run_daily_refresh():
    # ... extract and transform rows ...

    # Format sheet before writing data
    fmt = SheetFormatter(DEFAULT_SPREADSHEET_ID)
    fmt.profile("data_detail").apply(tabs=["All Leads"], force=True)

    # ... write data to formatted sheet ...
```

### Example 2: Audit Report Generation

Format summary and detail tabs separately:

```python
from sheet_formatter import SheetFormatter

def generate_audit_report(sheet_id):
    # ... write audit data to sheet ...

    # Format executive summary with summary_tab profile
    fmt = SheetFormatter(sheet_id)
    fmt.profile("summary_tab").apply(tabs=["Exec Summary"], force=True)

    # Format detailed audit with data_detail profile
    fmt.profile("data_detail").apply(tabs=["Detailed Audit"], force=True)
```

### Example 3: Custom Dashboard

Build custom formatting for a one-off dashboard:

```python
from sheet_formatter import SheetFormatter, DARK_GREEN, WHITE, FOREST_GREEN

def format_custom_dashboard(sheet_id):
    fmt = SheetFormatter(sheet_id)

    # Header row
    fmt.header_row(1, bold=True, bg_color=DARK_GREEN, fg_color=WHITE, font_size=14)

    # Section headers (row 3)
    fmt.header_row(3, bold=True, bg_color=FOREST_GREEN, fg_color=WHITE, font_size=11)

    # Columns
    fmt.column("A", width=2)
    fmt.column("B:C", width=16, align="LEFT")
    fmt.column("D:F", width=14, align="RIGHT", format="$#,##0")

    # Freeze
    fmt.freeze_rows(3)

    # Apply to all tabs
    fmt.apply(force=True)
```

---

## Hickory Color Palette

SheetFormatter includes the official Hickory brand colors in RGB float format (0.0-1.0) for Sheets API compatibility.

### Primary Colors

| Color | Hex | Usage |
|-------|-----|-------|
| Dark Green | #1D231C | Headers, primary text, main accents |
| Forest Green | #51714E | Section headers, sub-accents, links |
| Warm Cream | #E1DFD9 | Light backgrounds, alt rows |
| White | #FFFFFF | Data backgrounds |
| Black | #000000 | Body text |

### Import and Use

```python
from sheet_formatter import (
    DARK_GREEN,
    FOREST_GREEN,
    WARM_CREAM,
    WHITE,
    BLACK,
    CREAM_DARK,  # Extended palette
)

# Use in formatting
fmt.header_row(1, bg_color=DARK_GREEN, fg_color=WHITE)
fmt.column("B:C", bg_color=WARM_CREAM)
```

---

## Troubleshooting

### Verify Installation

```bash
cd C:/Users/mspit/AI/lib
python -c "from sheet_formatter import SheetFormatter; print('OK: SheetFormatter imported')"
```

### Check Available Profiles

```bash
python -c "from sheet_formatter import PROFILES; print(list(PROFILES.keys()))"
```

### Test with Dry Run

Test formatting without applying (requires mock service):

```python
from unittest.mock import MagicMock
from sheet_formatter import SheetFormatter

mock_service = MagicMock()
mock_service.spreadsheets().get().execute.return_value = {
    "sheets": [{"properties": {"title": "Test", "sheetId": 0}}]
}

fmt = SheetFormatter("fake_id", service=mock_service)
fmt.profile("data_detail").apply(tabs=["Test"], force=True)
print("[OK] Dry run successful")
```

---

## API Reference

### SheetFormatter Class

**Constructor:**
```python
SheetFormatter(sheet_id: str, token_path: str = None, service = None) -> SheetFormatter
```

**Methods:**
| Method | Returns | Chainable |
|--------|---------|-----------|
| `profile(name)` | SheetFormatter | Yes |
| `header_row(...)` | SheetFormatter | Yes |
| `column(...)` | SheetFormatter | Yes |
| `freeze_rows(n)` | SheetFormatter | Yes |
| `freeze_columns(n)` | SheetFormatter | Yes |
| `freeze(rows, cols)` | SheetFormatter | Yes |
| `border(...)` | SheetFormatter | Yes |
| `apply(tabs, force)` | None | No |

**Helper Functions:**
```python
hex_to_sheets_color(hex_color: str) -> dict
load_profile_from_json(config_path: str) -> dict
```

---

## Support & Questions

For issues, questions, or feature requests:
1. Check the [Troubleshooting](#troubleshooting) section above
2. Review error messages and [Error Handling](#error-handling) section
3. Inspect the code: `sheet_formatter.py`
4. Check integration examples: [Integration Examples](#integration-examples)

---

**Last Updated:** 2026-02-20
**Version:** Phase 3 (CLI + docs complete)
**Location:** C:/Users/mspit/AI/lib/
