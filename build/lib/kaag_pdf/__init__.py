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

from .generator import (
    PDFGenerator,
    create_radar_chart,
)
from .colors import (
    ColorScheme,
    KAAG_COLORS,
    KAAG_COLORS_LIGHT,
    CHART_PALETTE,
    PERFORMANCE_GRADIENT,
    get_performance_color,
    interpolate_color,
)
from .fonts import FontManager, FONTS, get_font
from .styles import PDFStyles, DEFAULT_STYLES
from .components import (
    HeaderData,
    FooterData,
    RadarChartData,
    PerformanceBarData,
    PDFHeader,
    PDFFooter,
    InfoBlock,
    SectionHeader,
    StatsTable,
    RadarChart,
    PerformanceBar,
)

__version__ = "0.2.0"
__all__ = [
    "PDFGenerator",
    "create_radar_chart",
    "ColorScheme",
    "KAAG_COLORS",
    "KAAG_COLORS_LIGHT",
    "CHART_PALETTE",
    "PERFORMANCE_GRADIENT",
    "get_performance_color",
    "interpolate_color",
    "FontManager",
    "FONTS",
    "get_font",
    "PDFStyles",
    "DEFAULT_STYLES",
    "HeaderData",
    "FooterData",
    "RadarChartData",
    "PerformanceBarData",
    "PDFHeader",
    "PDFFooter",
    "InfoBlock",
    "SectionHeader",
    "StatsTable",
    "RadarChart",
    "PerformanceBar",
]
