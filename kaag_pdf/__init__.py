"""
KAAG PDF Exports Package
========================

A centralized Python package for generating styled PDF exports
across all KAAG projects with consistent branding.

Features:
- Unified color schemes (KAA Gent branding)
- Custom font support (Poppins, Obviously, IvyPresto)
- Reusable PDF components (headers, tables, charts)
- Multiple export formats

Usage:
    from kaag_pdf import PDFGenerator, ColorScheme, KAAG_COLORS
    
    generator = PDFGenerator(color_scheme=KAAG_COLORS)
    pdf = generator.create_report("Player Report", player_data)
    pdf.save("report.pdf")
"""

from .colors import (
    ColorScheme,
    KAAG_COLORS,
    KAAG_COLORS_LIGHT,
    CHART_PALETTE,
    PERFORMANCE_GRADIENT,
)
from .fonts import FontManager, FONTS
from .styles import PDFStyles
from .components import (
    PDFHeader,
    PDFFooter,
    InfoBlock,
    SectionHeader,
    StatsTable,
    RadarChart,
    PerformanceBar,
)
from .generator import PDFGenerator

__version__ = "0.2.0"
__all__ = [
    "ColorScheme",
    "KAAG_COLORS",
    "KAAG_COLORS_LIGHT",
    "CHART_PALETTE",
    "PERFORMANCE_GRADIENT",
    "FontManager",
    "FONTS",
    "PDFStyles",
    "PDFHeader",
    "PDFFooter",
    "InfoBlock",
    "SectionHeader",
    "StatsTable",
    "RadarChart",
    "PerformanceBar",
    "PDFGenerator",
]
