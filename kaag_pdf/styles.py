"""
PDF Styles for KAAG PDF Exports
===============================

Centralized style definitions for consistent PDF formatting.
Aligned with the 2025 frontend PDF styling (matching pdf_generator.py).
"""

from dataclasses import dataclass
from typing import Tuple, Optional
from reportlab.lib.units import mm


@dataclass
class PDFStyles:
    """
    Central style configuration for PDF generation.
    
    All measurements are in mm (millimeters) unless otherwise noted.
    """
    
    # Page settings (match pdf_generator.py)
    page_margin_top: float = 15 * mm
    page_margin_bottom: float = 15 * mm
    page_margin_left: float = 15 * mm
    page_margin_right: float = 15 * mm
    
    # Header settings (matches PDFStyles in pdf_generator)
    header_height: float = 28 * mm
    header_logo_width: float = 50 * mm
    header_logo_height: float = 16 * mm
    
    # Typography - Font sizes (in points)
    font_size_title: int = 20
    font_size_h1: int = 18
    font_size_h2: int = 13
    font_size_h3: int = 12
    font_size_body: int = 10
    font_size_small: int = 9
    font_size_tiny: int = 7
    
    # Line heights (multipliers)
    line_height_title: float = 1.2
    line_height_heading: float = 1.3
    line_height_body: float = 1.4
    
    # Spacing
    section_spacing: float = 10 * mm
    paragraph_spacing: float = 4 * mm
    item_spacing: float = 2 * mm
    
    # Table settings
    table_header_height: float = 6 * mm
    table_row_height: float = 5 * mm
    table_cell_padding: float = 2 * mm
    
    # Chart settings
    radar_chart_size: float = 60 * mm
    bar_chart_height: float = 4 * mm
    bar_chart_width: float = 80 * mm
    
    # Footer settings
    footer_height: float = 15 * mm
    footer_font_size: int = 8
    
    # Border settings
    border_width_thin: float = 0.5
    border_width_normal: float = 1.0
    border_width_thick: float = 2.0
    
    # Rounded corners
    corner_radius: float = 2 * mm
    corner_radius_large: float = 4 * mm
    
    def get_content_width(self, page_width: float) -> float:
        """Calculate available content width."""
        return page_width - self.page_margin_left - self.page_margin_right
    
    def get_content_height(self, page_height: float) -> float:
        """Calculate available content height (excluding header/footer)."""
        return page_height - self.page_margin_top - self.page_margin_bottom - self.header_height - self.footer_height


# =============================================================================
# Default Styles Instance
# =============================================================================

DEFAULT_STYLES = PDFStyles()


# =============================================================================
# Compact Styles (for dense reports)
# =============================================================================

COMPACT_STYLES = PDFStyles(
    page_margin_top=12 * mm,
    page_margin_bottom=14 * mm,
    page_margin_left=12 * mm,
    page_margin_right=12 * mm,
    
    header_height=24 * mm,
    header_logo_width=40 * mm,
    header_logo_height=14 * mm,
    
    font_size_title=18,
    font_size_h1=14,
    font_size_h2=12,
    font_size_h3=10,
    font_size_body=9,
    font_size_small=8,
    font_size_tiny=6,
    
    section_spacing=8 * mm,
    paragraph_spacing=3 * mm,
    item_spacing=1.5 * mm,
    
    table_header_height=6 * mm,
    table_row_height=4.5 * mm,
    
    radar_chart_size=52 * mm,
    bar_chart_height=3.5 * mm,
    bar_chart_width=72 * mm,
    
    footer_height=12 * mm,
)


# =============================================================================
# Style Presets for Specific Report Types
# =============================================================================

@dataclass
class ReportStylePreset:
    """Preset configuration for specific report types."""
    name: str
    description: str
    styles: PDFStyles
    header_style: str  # "full", "minimal", "none"
    footer_style: str  # "full", "page_numbers", "none"
    show_watermark: bool = False
    show_confidential: bool = False


PRESET_SCOUTING_REPORT = ReportStylePreset(
    name="scouting_report",
    description="Player scouting report with detailed statistics",
    styles=DEFAULT_STYLES,
    header_style="full",
    footer_style="page_numbers",
)

PRESET_FINAL_REPORT = ReportStylePreset(
    name="final_report",
    description="Comprehensive final evaluation report",
    styles=DEFAULT_STYLES,
    header_style="full",
    footer_style="page_numbers",
    show_confidential=True,
)

PRESET_QUICK_OVERVIEW = ReportStylePreset(
    name="quick_overview",
    description="Single-page player overview",
    styles=COMPACT_STYLES,
    header_style="minimal",
    footer_style="none",
)

PRESET_DATA_EXPORT = ReportStylePreset(
    name="data_export",
    description="Data-focused export with tables",
    styles=PDFStyles(
        font_size_body=8,
        font_size_small=7,
        table_row_height=4.5 * mm,
        table_cell_padding=1.5 * mm,
    ),
    header_style="minimal",
    footer_style="page_numbers",
)


# =============================================================================
# Helper Functions
# =============================================================================

def get_font_size(style: str, styles: PDFStyles = DEFAULT_STYLES) -> int:
    """
    Get font size for a style name.
    
    Args:
        style: One of "title", "h1", "h2", "h3", "body", "small", "tiny"
        styles: PDFStyles instance to use
        
    Returns:
        Font size in points
    """
    style_map = {
        "title": styles.font_size_title,
        "h1": styles.font_size_h1,
        "h2": styles.font_size_h2,
        "h3": styles.font_size_h3,
        "body": styles.font_size_body,
        "small": styles.font_size_small,
        "tiny": styles.font_size_tiny,
    }
    return style_map.get(style, styles.font_size_body)


def calculate_text_height(font_size: int, line_count: int = 1, line_height: float = 1.4) -> float:
    """
    Calculate the height needed for text.
    
    Args:
        font_size: Font size in points
        line_count: Number of lines
        line_height: Line height multiplier
        
    Returns:
        Height in mm
    """
    # 1 point = 0.3528 mm
    point_to_mm = 0.3528
    return font_size * point_to_mm * line_height * line_count
