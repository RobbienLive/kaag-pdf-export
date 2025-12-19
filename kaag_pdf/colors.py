"""
Color Schemes for KAAG PDF Exports
==================================

Centralized color definitions for KAA Gent branding and themes.
Updated to match the 2025 frontend palette (index.css) so PDF exports
stay visually aligned with the React components.
"""

from dataclasses import dataclass
from typing import Tuple


# Type alias for RGB colors (0-255 range)
RGBColor = Tuple[int, int, int]


@dataclass
class ColorScheme:
    """
    Color scheme for PDF generation.
    
    All colors are RGB tuples with values 0-255.
    
    Attributes:
        primary: Main brand color (headers, accents)
        secondary: Secondary accent color
        text_primary: Main text color
        text_secondary: Muted/secondary text
        text_light: Light text (for dark backgrounds)
        background: Page background
        background_alt: Alternating row background
        border: Border/divider color
        success: Positive values (green)
        warning: Warning values (orange/yellow)
        danger: Negative values (red)
        chart_primary: Primary chart color
        chart_secondary: Secondary chart color
        chart_background: Chart background/grid color
    """
    primary: RGBColor
    primary_dark: RGBColor
    secondary: RGBColor
    text_primary: RGBColor
    text_secondary: RGBColor
    text_light: RGBColor
    background: RGBColor
    background_alt: RGBColor
    border: RGBColor
    success: RGBColor
    warning: RGBColor
    danger: RGBColor
    chart_primary: RGBColor
    chart_secondary: RGBColor
    chart_background: RGBColor
    
    def primary_normalized(self) -> Tuple[float, float, float]:
        """Get primary color normalized to 0-1 range for ReportLab."""
        return self._normalize(self.primary)
    
    def primary_dark_normalized(self) -> Tuple[float, float, float]:
        """Get primary_dark color normalized to 0-1 range for ReportLab."""
        return self._normalize(self.primary_dark)
    
    def secondary_normalized(self) -> Tuple[float, float, float]:
        """Get secondary color normalized to 0-1 range for ReportLab."""
        return self._normalize(self.secondary)
    
    def text_primary_normalized(self) -> Tuple[float, float, float]:
        """Get text_primary color normalized to 0-1 range for ReportLab."""
        return self._normalize(self.text_primary)
    
    def text_secondary_normalized(self) -> Tuple[float, float, float]:
        """Get text_secondary color normalized to 0-1 range for ReportLab."""
        return self._normalize(self.text_secondary)
    
    def get_normalized(self, color_name: str) -> Tuple[float, float, float]:
        """Get any color by name, normalized to 0-1 range."""
        color = getattr(self, color_name, None)
        if color is None:
            raise ValueError(f"Unknown color: {color_name}")
        return self._normalize(color)
    
    @staticmethod
    def _normalize(rgb: RGBColor) -> Tuple[float, float, float]:
        """Convert RGB (0-255) to normalized (0-1) for ReportLab."""
        return (rgb[0] / 255, rgb[1] / 255, rgb[2] / 255)
    
    def to_hex(self, color_name: str) -> str:
        """Convert a color to hex format."""
        color = getattr(self, color_name, None)
        if color is None:
            raise ValueError(f"Unknown color: {color_name}")
        return f"#{color[0]:02x}{color[1]:02x}{color[2]:02x}"


# =============================================================================
# KAA Gent Official Colors (2025 palette aligned with frontend index.css)
# =============================================================================

KAAG_COLORS = ColorScheme(
    # Brand colors (from index.css)
    primary=(0, 80, 160),          # #0050a0
    primary_dark=(29, 67, 109),     # #1d436d
    secondary=(151, 188, 200),     # #97bcc8
    text_primary=(33, 53, 71),     # #213547
    text_secondary=(107, 114, 128),# #6b7280
    text_light=(255, 255, 255),    # #ffffff

    # Backgrounds & borders
    background=(255, 255, 255),    # #ffffff
    background_alt=(242, 242, 242),# #f2f2f2
    border=(216, 216, 216),        # #d8d8d8

    # Status colors (matching React components)
    success=(16, 185, 129),        # #10b981
    warning=(245, 158, 11),        # #f59e0b
    danger=(239, 68, 68),          # #ef4444

    # Charts
    chart_primary=(0, 80, 160),    # #0050a0
    chart_secondary=(0, 189, 153), # #00bd99 (accent/tertiary)
    chart_background=(229, 231, 235), # #e5e7eb
)


KAAG_COLORS_LIGHT = ColorScheme(
    # Slightly lighter variant for dense tables
    primary=(0, 95, 180),          # lighten primary
    primary_dark=(49, 87, 130),    # lighten primary_dark
    secondary=(173, 205, 214),     # lighten secondary
    text_primary=(51, 65, 85),     # darker slate
    text_secondary=(125, 135, 148),
    text_light=(255, 255, 255),

    background=(248, 250, 252),    # near-white
    background_alt=(238, 242, 245),
    border=(220, 225, 230),

    success=(16, 185, 129),
    warning=(245, 158, 11),
    danger=(239, 68, 68),

    chart_primary=(0, 95, 180),
    chart_secondary=(0, 189, 153),
    chart_background=(232, 234, 237),
)


# =============================================================================
# Additional Color Palettes for Charts
# =============================================================================

# Palette for multiple data series in charts
CHART_PALETTE = [
    (0, 80, 160),     # Primary blue
    (0, 189, 153),    # Tertiary green-teal
    (151, 188, 200),  # Secondary blue-grey
    (245, 158, 11),   # Warning amber
    (239, 68, 68),    # Danger red
    (16, 185, 129),   # Success green
    (90, 103, 216),   # Indigo accent
    (168, 85, 247),   # Purple accent
]

# Gradient colors for performance bars
PERFORMANCE_GRADIENT = {
    "excellent": (16, 185, 129),     # Green (>=85)
    "good": (0, 80, 160),            # Primary blue (70-85)
    "average": (151, 188, 200),      # Secondary (50-70)
    "below_average": (245, 158, 11), # Amber (30-50)
    "poor": (239, 68, 68),           # Red (<30)
}


def get_performance_color(percentile: float) -> RGBColor:
    """
    Get color based on percentile (higher is better: 100 = top performer).

    Args:
        percentile: Value 0-100 where higher = better performance

    Returns:
        RGB tuple for the performance level
    """
    if percentile >= 85:
        return PERFORMANCE_GRADIENT["excellent"]
    elif percentile >= 70:
        return PERFORMANCE_GRADIENT["good"]
    elif percentile >= 50:
        return PERFORMANCE_GRADIENT["average"]
    elif percentile >= 30:
        return PERFORMANCE_GRADIENT["below_average"]
    else:
        return PERFORMANCE_GRADIENT["poor"]


def interpolate_color(color1: RGBColor, color2: RGBColor, factor: float) -> RGBColor:
    """
    Interpolate between two colors.
    
    Args:
        color1: Start color (RGB tuple)
        color2: End color (RGB tuple)
        factor: 0.0 = color1, 1.0 = color2
        
    Returns:
        Interpolated RGB color
    """
    factor = max(0.0, min(1.0, factor))
    return (
        int(color1[0] + (color2[0] - color1[0]) * factor),
        int(color1[1] + (color2[1] - color1[1]) * factor),
        int(color1[2] + (color2[2] - color1[2]) * factor),
    )
