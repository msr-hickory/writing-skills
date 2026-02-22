"""Hickory brand color palette for spreadsheet formatting.

Reference: C:/Users/mspit/AI/Hickory/Hickory-Brand-Theme-Guide.md

All colors are defined as:
- HEX: Standard hex code (e.g., "#1D231C")
- RGB_FLOAT: Normalized RGB for Google Sheets API (0.0-1.0)
- RGB_INT: Integer RGB for general use (0-255)

Google Sheets batchUpdate API expects RGB as {"red": 0.0-1.0, "green": ..., "blue": ...}
"""

# Core Hickory Brand Palette
# ===========================

# Primary Dark - Used for main headers, titles, primary text
DARK_GREEN_HEX = "#1D231C"
DARK_GREEN_RGB_INT = (29, 35, 28)
DARK_GREEN_RGB_FLOAT = {"red": 0.114, "green": 0.137, "blue": 0.110}

# Accent - Used for subheaders, highlights, links, accent elements
FOREST_GREEN_HEX = "#51714E"
FOREST_GREEN_RGB_INT = (81, 113, 78)
FOREST_GREEN_RGB_FLOAT = {"red": 0.318, "green": 0.443, "blue": 0.306}

# Light Accent - Used for section backgrounds, alternating rows, table shading
WARM_CREAM_HEX = "#E1DFD9"
WARM_CREAM_RGB_INT = (225, 223, 217)
WARM_CREAM_RGB_FLOAT = {"red": 0.882, "green": 0.875, "blue": 0.851}

# Background - Page/slide backgrounds, card fills
WHITE_HEX = "#FFFFFF"
WHITE_RGB_INT = (255, 255, 255)
WHITE_RGB_FLOAT = {"red": 1.0, "green": 1.0, "blue": 1.0}

# Text - Body text, secondary labels
BLACK_HEX = "#000000"
BLACK_RGB_INT = (0, 0, 0)
BLACK_RGB_FLOAT = {"red": 0.0, "green": 0.0, "blue": 0.0}


# Extended Palette (Derived Tints for Charts, Tables, Data Visualization)
# =========================================================================

# Forest Green 75% - Chart series 2, lighter accent
FOREST_GREEN_75_HEX = "#7D9A7B"
FOREST_GREEN_75_RGB_INT = (125, 154, 123)
FOREST_GREEN_75_RGB_FLOAT = {"red": 0.490, "green": 0.604, "blue": 0.482}

# Forest Green 50% - Chart series 3, muted fills
FOREST_GREEN_50_HEX = "#A8B8A7"
FOREST_GREEN_50_RGB_INT = (168, 184, 167)
FOREST_GREEN_50_RGB_FLOAT = {"red": 0.659, "green": 0.722, "blue": 0.655}

# Forest Green 25% - Subtle highlights, hover states
FOREST_GREEN_25_HEX = "#D3DCD3"
FOREST_GREEN_25_RGB_INT = (211, 220, 211)
FOREST_GREEN_25_RGB_FLOAT = {"red": 0.827, "green": 0.863, "blue": 0.827}

# Dark Green 75% - Secondary dark, chart axis labels
DARK_GREEN_75_HEX = "#555B54"
DARK_GREEN_75_RGB_INT = (85, 91, 84)
DARK_GREEN_75_RGB_FLOAT = {"red": 0.333, "green": 0.357, "blue": 0.329}

# Dark Green 50% - Tertiary text, gridlines
DARK_GREEN_50_HEX = "#8E928E"
DARK_GREEN_50_RGB_INT = (142, 146, 142)
DARK_GREEN_50_RGB_FLOAT = {"red": 0.557, "green": 0.573, "blue": 0.557}

# Cream Dark - Table borders, divider lines
CREAM_DARK_HEX = "#C9C5BC"
CREAM_DARK_RGB_INT = (201, 197, 188)
CREAM_DARK_RGB_FLOAT = {"red": 0.788, "green": 0.773, "blue": 0.737}


# Convenience Dicts for Google Sheets API
# ========================================

# Use these for direct batchUpdate API calls
# Example: {"backgroundColor": DARK_GREEN_SHEETS}

DARK_GREEN_SHEETS = DARK_GREEN_RGB_FLOAT
FOREST_GREEN_SHEETS = FOREST_GREEN_RGB_FLOAT
WARM_CREAM_SHEETS = WARM_CREAM_RGB_FLOAT
WHITE_SHEETS = WHITE_RGB_FLOAT
BLACK_SHEETS = BLACK_RGB_FLOAT
FOREST_GREEN_75_SHEETS = FOREST_GREEN_75_RGB_FLOAT
FOREST_GREEN_50_SHEETS = FOREST_GREEN_50_RGB_FLOAT
FOREST_GREEN_25_SHEETS = FOREST_GREEN_25_RGB_FLOAT
DARK_GREEN_75_SHEETS = DARK_GREEN_75_RGB_FLOAT
DARK_GREEN_50_SHEETS = DARK_GREEN_50_RGB_FLOAT
CREAM_DARK_SHEETS = CREAM_DARK_RGB_FLOAT


# Color Mapping Utilities
# =======================

def hex_to_rgb_float(hex_color: str) -> dict:
    """Convert hex color (e.g., '#1D231C') to Sheets API RGB format.

    Args:
        hex_color: Hex color string (e.g., '#1D231C')

    Returns:
        Dict with keys 'red', 'green', 'blue' (values 0.0-1.0)

    Example:
        >>> hex_to_rgb_float('#1D231C')
        {'red': 0.114, 'green': 0.137, 'blue': 0.110}
    """
    hex_color = hex_color.lstrip("#")
    if len(hex_color) != 6:
        raise ValueError(f"Invalid hex color: {hex_color}")

    r = int(hex_color[0:2], 16) / 255.0
    g = int(hex_color[2:4], 16) / 255.0
    b = int(hex_color[4:6], 16) / 255.0

    return {"red": round(r, 3), "green": round(g, 3), "blue": round(b, 3)}


def rgb_int_to_float(rgb_int: tuple[int, int, int]) -> dict:
    """Convert integer RGB (0-255) to Sheets API RGB format (0.0-1.0).

    Args:
        rgb_int: Tuple of (red, green, blue) with values 0-255

    Returns:
        Dict with keys 'red', 'green', 'blue' (values 0.0-1.0)

    Example:
        >>> rgb_int_to_float((29, 35, 28))
        {'red': 0.114, 'green': 0.137, 'blue': 0.110}
    """
    r, g, b = rgb_int
    return {
        "red": round(r / 255.0, 3),
        "green": round(g / 255.0, 3),
        "blue": round(b / 255.0, 3),
    }


# Quick Reference
# ===============
# Use the HEX values when documenting or sharing with designers:
#
#   Dark Green:       #1D231C (primary headers, titles)
#   Forest Green:     #51714E (accent, subheaders)
#   Warm Cream:       #E1DFD9 (light backgrounds, alternating rows)
#   White:            #FFFFFF (main background)
#   Black:            #000000 (body text)
#   Forest Green 75%: #7D9A7B (lighter accent, chart series 2)
#   Forest Green 50%: #A8B8A7 (muted fills, chart series 3)
#   Forest Green 25%: #D3DCD3 (subtle highlights)
#   Dark Green 75%:   #555B54 (secondary dark)
#   Dark Green 50%:   #8E928E (tertiary text, gridlines)
#   Cream Dark:       #C9C5BC (borders, divider lines)
