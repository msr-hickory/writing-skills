---
name: spreadsheet-standards
description: Use when building, writing to, or designing any Google Sheets deliverable. Enforces IB/consulting-grade layout, formula discipline, formatting conventions, and MCP API constraints. Auto-apply when writing to Google Sheets via MCP or Python.
---

# Spreadsheet Standards Skill

**Last Updated**: 2026-02-19
**Owner**: Michael
**Status**: Active

---

## Trigger Conditions

Use this skill when:
- Building a new Google Sheets deliverable (scorecard, report, model, dashboard)
- Writing data to an existing spreadsheet via MCP or Python
- Designing tab structure, formulas, or layouts for a spreadsheet
- Reviewing or auditing an existing spreadsheet for quality
- Any task where the output is a Google Sheets document

---

## Core Philosophy

Spreadsheets are deliverables, not scratchpads. Every sheet you produce should be hand-off ready — an analyst at an investment bank, Big 4 firm, or MBB consultancy would look at it and find it clean, auditable, and professional. The FAST Standard applies: **Flexible, Appropriate, Structured, Transparent.**

The quality bar: MBB / Big 4 / Wall Street IB.

---

## Part 1: Layout & Structure

### Rule 1: Column A is a Spacer

Column A is always a narrow blank spacer. Labels start in B, data in C+. This creates a clean left margin and prevents data from butting up against the sheet edge.

### Rule 2: Tab Organization

Tabs follow a logical hierarchy:

```
1. Summary / exec tab (first)
2. Consolidated views
3. Detail / data tabs
4. Supporting schedules (last)
```

Number-prefix tabs if sort order matters: "1-Summary", "2-Detail", "3-Raw Data".

### Rule 3: Short Tab Names

Under 15 characters. Descriptive, not generic.

| Good | Bad |
|------|-----|
| Exec Summary | Sheet1 |
| Monthly Detail | Monthly Revenue Detail by Brand and Region |
| Raw Data | Data |

### Rule 4: Header Block on Every Tab

Summary and exec tabs get the full block:
- Date, Version, Owner, Status, Period

Data tabs get at minimum:
- Title + subtitle (what the data represents and the date range)

### Rule 5: Units Row

State units clearly: "$ in thousands", "$ in millions", "Count", "Rate (%)". Consistent across all tabs in the same workbook.

### Rule 6: Section Structure

- Bold total rows
- Indent sub-items (use leading spaces in cell values)
- Blank rows between sections
- Single top-border for subtotals, double bottom-border for grand totals (note for manual polish — MCP can't control borders)

### Rule 7: No Merged Cells

Merged cells break formulas, sorting, and filtering. Use alignment and indentation instead.

### Rule 8: Freeze Panes

Freeze label columns and header rows so they stay visible when scrolling. Note for manual polish — MCP cannot set freeze panes.

---

## Part 2: Formulas & Modeling

### Rule 9: Formulas Over Hardcoding

Never embed a hard-coded number in a formula. All assumptions go in labeled cells. Raw data on detail tabs; summaries use `SUMIFS`, `AVERAGEIFS`, `VLOOKUP` referencing those tabs.

**Write pattern**: Write raw data tabs from Python/MCP. Let formulas handle all rollups and aggregations in the exec/summary tabs. This keeps the sheet auditable and self-updating.

### Rule 10: One Formula Per Row

The formula in the first data column should be copyable across the entire row. If the logic changes mid-row, split into two rows.

### Rule 11: Calculate Once, Reference Many

A value should be computed in exactly one place. Everywhere else links to that cell. Never re-derive the same calculation in multiple locations.

### Rule 12: IFERROR Thoughtfully

Wrap divisions in `IFERROR`, but return `"Check"` or `"—"` — never silently return 0 when the error indicates a real problem.

```
=IFERROR(B5/B4, "—")
```

### Rule 13: Check Figures

Add cross-foot checks where calculations can be validated:
- "Total should equal X" rows
- Error-check rows that flag discrepancies
- Difference columns that should sum to zero

### Rule 14: LET() is Broken via API

The `LET()` function does not work when written via the Google Sheets API. Always use expanded formulas instead:

```
# Bad (breaks via API)
=LET(x, SUMIFS(...), y, SUMIFS(...), IFERROR(x/y, 0))

# Good (works via API)
=IFERROR(SUMIFS(...)/SUMIFS(...), 0)
```

---

## Part 3: Formatting

### Rule 15: Number Formatting

| Type | Format | Example |
|------|--------|---------|
| Dollars | `$#,##0` | $1,234,567 |
| Percentages | `0.0%` or `0%` | 88.5% |
| Negatives | `($#,##0)` | ($1,234) |
| Missing / N/A | `—` (em-dash) | — |
| Blank cells in output areas | Never blank | Use "—" or "N/A" |

### Rule 16: Color Convention (Manual Polish)

MCP cannot control font colors, but note these for manual polish:
- **Blue font** = hardcoded inputs / assumptions
- **Black font** = formulas
- **Green font** = links to other tabs

### Rule 17: Column Widths and Alignment (Manual Polish)

- Data columns: uniform width (10-14 chars)
- Label columns: wider
- Numbers: right-aligned
- Text: left-aligned
- **Header alignment matches data**: Column headers inherit the alignment of the data beneath them. Metric/number columns get right-aligned headers; text/label columns get left-aligned headers.

### Rule 18: Source Citations

Every assumption and data point should cite its source in a nearby cell, a footnote row, or a "Sources" section at the bottom of the tab. Examples: "Source: BQ vi_dataset.jobs_table", "Source: Management estimate, 2/15/2026".

---

## Part 4: Google Sheets MCP Constraints

These are hard API limitations. Plan around them.

### What MCP Can Do
- Read and write cell values
- Create new tabs (via `addSpreadsheetSheet`)
- Clear ranges (via `clearSpreadsheetRange`)
- Write formulas (with `USER_ENTERED` value input option)

### What MCP Cannot Do
- Bold, italic, or font styling
- Font colors or background colors
- Borders
- Column widths or row heights
- Merge cells (and you shouldn't anyway — Rule 7)
- Charts or sparklines
- Freeze panes
- Rename tabs

**Always note manual polish items** when producing a sheet. Include a comment at the top or a checklist of formatting that needs to be applied manually.

### Write Chunking

- **MCP**: 25 rows max per `writeSpreadsheet` call
- **Python**: 100-row chunks with 0.5s throttle between calls
- Always re-read the sheet before writing a second batch (concurrent edit hazard)

### Value Input Options

| Data Type | Value Input Option | Why |
|-----------|-------------------|-----|
| Numbers, currency, percentages, formulas | `USER_ENTERED` | Sheets parses and formats the values |
| Text, definitions, labels | `RAW` | Prevents Sheets from interpreting text as formulas |

### clearSpreadsheetRange Before Rewriting

Always clear the target range before rewriting data. This prevents stale data from persisting if the new dataset is shorter than the old one. `clearSpreadsheetRange` preserves cell formatting.

### Grid Sizing

When creating a new tab with `fresh=True` for multi-step appends, pass explicit `grid_rows=250+` or later write steps will hit the grid ceiling.

---

## Part 5: Python → Sheets Type Coercion

When writing BigQuery results to Google Sheets via Python, watch for these type mismatches:

### Decimal

BQ returns `decimal.Decimal` for `NUMERIC`/`BIGNUMERIC` columns — even after `SAFE_CAST(x AS FLOAT64)`. This will crash `json.dumps()` and the Sheets API.

**Fix**: Use a `safe_num()` helper to convert before appending rows:

```python
def safe_num(val):
    """Convert BQ Decimal to float for Sheets serialization."""
    if val is None:
        return ""
    if isinstance(val, decimal.Decimal):
        return float(val)
    return val
```

### Boolean

Python `True`/`False` serialize as JSON strings `"True"`/`"False"` in Sheets. If you use `COUNTIF` or other formulas against boolean columns, they won't match.

**Fix**: Write `"Yes"`/`"No"` explicitly and match `COUNTIF` formulas to those strings.

### Last-Row Detection

When detecting the last occupied row, always scan a wide range like `A:H` — not just `A:A`. Rows with a blank column A are invisible to single-column reads.

---

## Part 6: Tab Design Patterns

### The Exec + Data Pattern

The standard pattern for any analytical deliverable:

```
Tab 1: "Exec Summary"
  - Header block (date, version, owner, status)
  - Key metrics at top (3-5 numbers)
  - Summary table with formulas referencing data tabs
  - Questions/Assumptions section at TOP
  - Source citations

Tab 2: "Detail" (or "Monthly Detail", "Brand Detail", etc.)
  - Column headers with units row
  - Raw aggregated data (from Python/BQ)
  - No hardcoded numbers — all from data tabs or formulas

Tab 3: "Raw Data"
  - Direct BQ output written by Python
  - Minimal formatting
  - Column headers match BQ field names
```

### Questions/Assumptions at the Top

Executives see risks first. Every deliverable with a summary tab should have a "Questions / Assumptions / Clarifications" section near the top — before the data.

---

## Pre-Build Checklist

Before writing any data to a spreadsheet:

- [ ] **Tab structure planned**: Which tabs, what order, what goes where?
- [ ] **Column A blank**: Labels start in B, data in C+
- [ ] **Header block**: Title, subtitle, date range on every tab
- [ ] **Units stated**: Clear unit labels on all numeric columns
- [ ] **Formulas designed**: Summary tab uses formulas referencing data tabs, not hardcoded values
- [ ] **Write chunking planned**: 25 rows/call for MCP, 100 rows/call for Python
- [ ] **Value input option correct**: `USER_ENTERED` for numbers/formulas, `RAW` for text
- [ ] **Type coercion handled**: `safe_num()` for Decimals, `"Yes"/"No"` for booleans
- [ ] **Clear before write**: Using `clearSpreadsheetRange` before rewriting
- [ ] **Manual polish notes**: List of formatting items MCP can't handle (bold, colors, borders, freeze panes, column widths)

## Post-Build Checklist

After the sheet is written:

- [ ] **Cross-foot checks**: Do totals match? Do check figures balance?
- [ ] **No merged cells**: Verify none were introduced
- [ ] **No blank cells in output areas**: All filled with data or "—"
- [ ] **Negatives in parentheses**: `($1,234)` not `-$1,234`
- [ ] **Source citations present**: Every data point traceable to a source
- [ ] **Tab names under 15 chars**: Short and descriptive
- [ ] **Questions/Assumptions section**: Present on summary tabs

---

## Sources & Influences

- **FAST Standard** (Flexible, Appropriate, Structured, Transparent) — IB/consulting spreadsheet methodology
- **McKinsey / Goldman Sachs / Morgan Stanley** spreadsheet conventions — layout, color coding, formula discipline
- **Hickory operational experience** — MCP constraints, BQ→Sheets type coercion, write chunking patterns
