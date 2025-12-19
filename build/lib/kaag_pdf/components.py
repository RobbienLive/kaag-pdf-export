"""
Reusable PDF Components for KAAG PDF Exports
============================================

Building blocks for PDF generation: headers, footers, tables, charts, etc.
"""

from typing import Optional, List, Dict, Any, Tuple
from dataclasses import dataclass
import math
from reportlab.lib.units import mm
from reportlab.pdfgen.canvas import Canvas
from reportlab.lib.pagesizes import A4

from .colors import ColorScheme, KAAG_COLORS, get_performance_color
from .fonts import FONTS, get_font
from .styles import PDFStyles, DEFAULT_STYLES


# =============================================================================
# Data Classes for Components
# =============================================================================

@dataclass
class HeaderData:
    """Data for PDF header."""
    title: str
    subtitle: Optional[str] = None
    logo_path: Optional[str] = None


@dataclass
class FooterData:
    """Data for PDF footer."""
    left_text: Optional[str] = None
    center_text: Optional[str] = None
    right_text: Optional[str] = None
    show_page_numbers: bool = True
    total_pages: int = 1


@dataclass
class RadarChartData:
    """Data for radar charts."""
    labels: List[str]
    values: List[float]  # 0-100 scale
    background_values: Optional[List[float]] = None  # For comparison (e.g., group average)
    title: Optional[str] = None
    max_value: float = 100.0


@dataclass
class PerformanceBarData:
    """Data for performance bars."""
    label: str
    value: float  # The actual score
    percentile: float  # Top X% (0-100, lower is better)
    max_value: float = 100.0


# =============================================================================
# Component Classes
# =============================================================================

class PDFHeader:
    """Renders PDF headers with logo and title."""
    
    def __init__(
        self,
        colors: ColorScheme = KAAG_COLORS,
        styles: PDFStyles = DEFAULT_STYLES,
    ):
        self.colors = colors
        self.styles = styles
    
    def draw(
        self,
        canvas: Canvas,
        data: HeaderData,
        page_width: float = A4[0],
        y_position: Optional[float] = None,
    ) -> float:
        """
        Draw header on the canvas.
        
        Returns the y position after the header.
        """
        if y_position is None:
            y_position = A4[1] - self.styles.page_margin_top
        
        c = canvas
        header_y = y_position - self.styles.header_height
        
        # Background bar
        r, g, b = self.colors.primary_normalized()
        c.setFillColorRGB(r, g, b)
        c.rect(0, header_y, page_width, self.styles.header_height, fill=True, stroke=False)
        
        # Logo (if provided) - positioned left
        logo_x = 10 * mm
        logo_y = header_y + (self.styles.header_height - self.styles.header_logo_height) / 2
        
        if data.logo_path:
            try:
                c.drawImage(
                    data.logo_path,
                    logo_x,
                    logo_y,
                    width=self.styles.header_logo_width,
                    height=self.styles.header_logo_height,
                    preserveAspectRatio=True,
                    mask='auto'
                )
                print(f"Logo drawn at {data.logo_path}")
            except Exception as e:
                pass  # Skip if logo can't be loaded
        
        # Title and Subtitle in the center-right
        r, g, b = self.colors.get_normalized("text_light")
        c.setFillColorRGB(r, g, b)
        
        title_x = self.styles.page_margin_left + self.styles.header_logo_width + 10 * mm
        title_y = header_y + self.styles.header_height - 8 * mm
        
        # Title
        c.setFont(get_font("HEADING"), self.styles.font_size_h1)
        c.drawString(title_x, title_y, data.title)
        
        # Subtitle (if present)
        if data.subtitle:
            subtitle_y = title_y - 8 * mm
            c.setFont(get_font("BODY"), self.styles.font_size_h3)
            c.drawString(title_x, subtitle_y, data.subtitle)
        
        return header_y


class PDFFooter:
    """Renders PDF footers with page numbers."""
    
    def __init__(
        self,
        colors: ColorScheme = KAAG_COLORS,
        styles: PDFStyles = DEFAULT_STYLES,
    ):
        self.colors = colors
        self.styles = styles
    
    def draw(
        self,
        canvas: Canvas,
        data: FooterData,
        current_page: int,
        page_width: float = A4[0],
    ) -> None:
        """Draw footer on the canvas."""
        c = canvas
        y = self.styles.page_margin_bottom - 3 * mm
        
        r, g, b = self.colors.text_secondary_normalized()
        c.setFillColorRGB(r, g, b)
        c.setFont(get_font("BODY"), 8)
        
        # Left text
        if data.left_text:
            c.drawString(self.styles.page_margin_left, y, data.left_text)
        
        # Center text or page numbers
        if data.show_page_numbers:
            page_text = f"Pagina {current_page} van {data.total_pages}"
            text_width = c.stringWidth(page_text, get_font("BODY"), 8)
            c.drawString((page_width - text_width) / 2, y, page_text)
        elif data.center_text:
            text_width = c.stringWidth(data.center_text, get_font("BODY"), 8)
            c.drawString((page_width - text_width) / 2, y, data.center_text)
        
        # Right text
        if data.right_text:
            text_width = c.stringWidth(data.right_text, get_font("BODY"), 8)
            c.drawString(page_width - self.styles.page_margin_right - text_width, y, data.right_text)


class InfoBlock:
    """Renders info blocks (key-value pairs in a box)."""
    
    def __init__(
        self,
        colors: ColorScheme = KAAG_COLORS,
        styles: PDFStyles = DEFAULT_STYLES,
    ):
        self.colors = colors
        self.styles = styles
    
    def draw(
        self,
        canvas: Canvas,
        x: float,
        y: float,
        width: float,
        items: List[Tuple[str, str]],  # [(label, value), ...]
        title: Optional[str] = None,
    ) -> float:
        """
        Draw an info block with key-value pairs.
        
        Returns the y position after the block.
        """
        c = canvas
        
        # Calculate height
        row_height = 5 * mm
        height = len(items) * row_height + 3 * mm
        if title:
            height += 5 * mm
        
        # Background
        r, g, b = self.colors.get_normalized("background_alt")
        c.setFillColorRGB(r, g, b)
        c.rect(x, y - height, width, height, fill=True, stroke=False)
        
        # Border
        r, g, b = self.colors.get_normalized("border")
        c.setStrokeColorRGB(r, g, b)
        c.setLineWidth(self.styles.border_width_thin)
        c.rect(x, y - height, width, height, fill=False, stroke=True)
        
        current_y = y - 2 * mm
        
        # Title
        if title:
            r, g, b = self.colors.primary_normalized()
            c.setFillColorRGB(r, g, b)
            c.setFont(get_font("SUBHEADING"), 11)
            c.drawString(x + 2 * mm, current_y - 3 * mm, title)
            current_y -= 5 * mm
        
        # Items
        for label, value in items:
            # Label
            r, g, b = self.colors.text_secondary_normalized()
            c.setFillColorRGB(r, g, b)
            c.setFont(get_font("BODY"), 9)
            c.drawString(x + 2 * mm, current_y, f"{label}:")
            
            # Value
            r, g, b = self.colors.text_primary_normalized()
            c.setFillColorRGB(r, g, b)
            c.setFont(get_font("BODY_BOLD"), 10)
            c.drawString(x + width * 0.35, current_y, str(value))
            
            current_y -= row_height
        
        return y - height - 2 * mm


class SectionHeader:
    """Renders section headers with optional accent line."""
    
    def __init__(
        self,
        colors: ColorScheme = KAAG_COLORS,
        styles: PDFStyles = DEFAULT_STYLES,
    ):
        self.colors = colors
        self.styles = styles
    
    def draw(
        self,
        canvas: Canvas,
        x: float,
        y: float,
        title: str,
        width: Optional[float] = None,
        show_line: bool = True,
    ) -> float:
        """
        Draw a section header.
        
        Returns the y position after the header.
        """
        c = canvas
        
        if width is None:
            width = A4[0] - 2 * self.styles.page_margin_left
        
        # Accent line (left)
        if show_line:
            r, g, b = self.colors.secondary_normalized()
            c.setStrokeColorRGB(r, g, b)
            c.setLineWidth(self.styles.border_width_thick)
            c.line(x, y - 2 * mm, x + 15 * mm, y - 2 * mm)
        
        # Title text
        r, g, b = self.colors.primary_normalized()
        c.setFillColorRGB(r, g, b)
        c.setFont(get_font("HEADING"), 13)
        c.drawString(x, y - 7 * mm, title)
        
        return y - 12 * mm


class StatsTable:
    """Renders statistics tables."""
    
    def __init__(
        self,
        colors: ColorScheme = KAAG_COLORS,
        styles: PDFStyles = DEFAULT_STYLES,
    ):
        self.colors = colors
        self.styles = styles
    
    def draw(
        self,
        canvas: Canvas,
        x: float,
        y: float,
        headers: List[str],
        rows: List[List[str]],
        col_widths: Optional[List[float]] = None,
    ) -> float:
        """
        Draw a statistics table.
        
        Returns the y position after the table.
        """
        c = canvas
        
        if col_widths is None:
            total_width = A4[0] - 2 * self.styles.page_margin_left
            col_widths = [total_width / len(headers)] * len(headers)
        
        total_width = sum(col_widths)
        header_height = 6 * mm
        row_height = 5 * mm
        
        # Header row
        r, g, b = self.colors.primary_normalized()
        c.setFillColorRGB(r, g, b)
        c.rect(x, y - header_height, total_width, header_height, fill=True, stroke=False)
        
        # Header text (white on blue)
        r, g, b = self.colors.get_normalized("text_light")
        c.setFillColorRGB(r, g, b)
        c.setFont(get_font("LABEL"), 9)
        
        col_x = x
        for header, width in zip(headers, col_widths):
            c.drawString(col_x + 2 * mm, y - 4.5 * mm, header)
            col_x += width
        
        current_y = y - header_height
        
        # Data rows
        for row_idx, row in enumerate(rows):
            # Alternating row background
            if row_idx % 2 == 1:
                r, g, b = self.colors.get_normalized("background_alt")
                c.setFillColorRGB(r, g, b)
                c.rect(x, current_y - row_height, total_width, row_height, fill=True, stroke=False)
            
            # Row data
            r, g, b = self.colors.text_primary_normalized()
            c.setFillColorRGB(r, g, b)
            c.setFont(get_font("BODY"), 9)
            
            col_x = x
            for cell, width in zip(row, col_widths):
                c.drawString(col_x + 2 * mm, current_y - 4 * mm, str(cell))
                col_x += width
            
            current_y -= row_height
        
        return current_y - 2 * mm


class RadarChart:
    """Renders radar/spider charts for multi-dimensional data."""
    
    def __init__(
        self,
        colors: ColorScheme = KAAG_COLORS,
        styles: PDFStyles = DEFAULT_STYLES,
    ):
        self.colors = colors
        self.styles = styles
    
    def draw(
        self,
        canvas: Canvas,
        center_x: float,
        center_y: float,
        data: RadarChartData,
        size: Optional[float] = None,
    ) -> None:
        """Draw a radar chart."""
        c = canvas
        
        if size is None:
            size = self.styles.radar_chart_size
        
        radius = size / 2
        n = len(data.labels)
        
        if n < 3:
            return  # Need at least 3 points
        
        # Calculate point positions
        def get_point(angle: float, r: float) -> Tuple[float, float]:
            return (
                center_x + r * math.cos(angle - math.pi / 2),
                center_y + r * math.sin(angle - math.pi / 2)
            )
        
        angles = [2 * math.pi * i / n for i in range(n)]
        
        # Draw grid circles
        r, g, b = self.colors.get_normalized("border")
        c.setStrokeColorRGB(r, g, b)
        c.setLineWidth(0.3)
        
        for level in [0.25, 0.5, 0.75, 1.0]:
            path = c.beginPath()
            for i, angle in enumerate(angles):
                x, y = get_point(angle, radius * level)
                if i == 0:
                    path.moveTo(x, y)
                else:
                    path.lineTo(x, y)
            path.close()
            c.drawPath(path, stroke=True, fill=False)
        
        # Draw axis lines
        for angle in angles:
            x, y = get_point(angle, radius)
            c.line(center_x, center_y, x, y)
        
        # Draw background values (e.g., group average)
        if data.background_values and len(data.background_values) == n:
            r, g, b = self.colors.get_normalized("chart_background")
            c.setFillColorRGB(r, g, b, 0.5)
            c.setStrokeColorRGB(r, g, b)
            
            path = c.beginPath()
            for i, (angle, val) in enumerate(zip(angles, data.background_values)):
                r_val = radius * (val / data.max_value)
                x, y = get_point(angle, r_val)
                if i == 0:
                    path.moveTo(x, y)
                else:
                    path.lineTo(x, y)
            path.close()
            c.drawPath(path, stroke=True, fill=True)
        
        # Draw main values
        r, g, b = self.colors.primary_normalized()
        c.setFillColorRGB(r, g, b, 0.3)
        c.setStrokeColorRGB(r, g, b)
        c.setLineWidth(1.5)
        
        path = c.beginPath()
        for i, (angle, val) in enumerate(zip(angles, data.values)):
            r_val = radius * (val / data.max_value)
            x, y = get_point(angle, r_val)
            if i == 0:
                path.moveTo(x, y)
            else:
                path.lineTo(x, y)
        path.close()
        c.drawPath(path, stroke=True, fill=True)
        
        # Draw data points
        c.setFillColorRGB(r, g, b)
        for angle, val in zip(angles, data.values):
            r_val = radius * (val / data.max_value)
            x, y = get_point(angle, r_val)
            c.circle(x, y, 2, fill=True)
        
        # Draw labels
        r, g, b = self.colors.text_primary_normalized()
        c.setFillColorRGB(r, g, b)
        c.setFont(get_font("BODY"), 7)
        
        for angle, label in zip(angles, data.labels):
            x, y = get_point(angle, radius + 8 * mm)
            
            # Adjust text position based on angle
            text_width = c.stringWidth(label, get_font("BODY"), 7)
            
            # Horizontal centering based on position
            if abs(math.cos(angle - math.pi / 2)) < 0.1:  # Top or bottom
                x -= text_width / 2
            elif math.cos(angle - math.pi / 2) < 0:  # Left side
                x -= text_width
            
            c.drawString(x, y - 2, label)
        
        # Title
        if data.title:
            r, g, b = self.colors.primary_normalized()
            c.setFillColorRGB(r, g, b)
            c.setFont(get_font("SUBHEADING", "Helvetica-Bold"), 9)
            title_width = c.stringWidth(data.title, get_font("SUBHEADING", "Helvetica-Bold"), 9)
            c.drawString(center_x - title_width / 2, center_y + radius + 15 * mm, data.title)


class PerformanceBar:
    """Renders performance indicator bars with percentile labels."""
    
    def __init__(
        self,
        colors: ColorScheme = KAAG_COLORS,
        styles: PDFStyles = DEFAULT_STYLES,
    ):
        self.colors = colors
        self.styles = styles
    
    def draw(
        self,
        canvas: Canvas,
        x: float,
        y: float,
        data: PerformanceBarData,
        label_width: float = 40 * mm,
        bar_width: Optional[float] = None,
        show_value: bool = True,
        show_percentile: bool = True,
    ) -> float:
        """
        Draw a performance bar with label.
        
        Returns the y position after the bar.
        """
        c = canvas
        
        if bar_width is None:
            bar_width = self.styles.bar_chart_width
        
        bar_height = self.styles.bar_chart_height
        
        # Label
        r, g, b = self.colors.text_primary_normalized()
        c.setFillColorRGB(r, g, b)
        c.setFont(get_font("BODY"), 9)
        c.drawString(x, y - bar_height / 2 - 1, data.label)
        
        bar_x = x + label_width
        
        # Background bar
        r, g, b = self.colors.get_normalized("background_alt")
        c.setFillColorRGB(r, g, b)
        c.roundRect(bar_x, y - bar_height, bar_width, bar_height, 1.5, fill=True, stroke=False)
        
        # Filled bar (based on percentile - lower is better, so fill more)
        fill_percent = 1 - (data.percentile / 100)
        fill_width = bar_width * fill_percent
        
        # Color based on performance
        bar_color = get_performance_color(data.percentile)
        r, g, b = bar_color[0] / 255, bar_color[1] / 255, bar_color[2] / 255
        c.setFillColorRGB(r, g, b)
        c.roundRect(bar_x, y - bar_height, fill_width, bar_height, 1.5, fill=True, stroke=False)
        
        # Value and percentile text
        text_x = bar_x + bar_width + 3 * mm
        
        if show_value:
            r, g, b = self.colors.text_secondary_normalized()
            c.setFillColorRGB(r, g, b)
            c.setFont(get_font("BODY"), 8)
            value_str = f"{data.value:.1f}"
            c.drawString(text_x, y - bar_height / 2 - 1, value_str)
            text_x += c.stringWidth(value_str, get_font("BODY"), 8) + 3 * mm
        
        if show_percentile:
            bar_color = get_performance_color(data.percentile)
            r, g, b = bar_color[0] / 255, bar_color[1] / 255, bar_color[2] / 255
            c.setFillColorRGB(r, g, b)
            c.setFont(get_font("BODY_BOLD"), 9)
            c.drawString(text_x, y - bar_height / 2 - 1, f"Top {data.percentile:.0f}%")
        
        return y - bar_height - self.styles.item_spacing


# =============================================================================
# Convenience function exports
# =============================================================================

__all__ = [
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
