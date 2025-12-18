"""
PDF Generator Base Class for KAAG PDF Exports
==============================================

Provides a base class for building PDF generators with consistent
styling and functionality.
"""

from typing import Optional, List, Dict, Any, Callable
from pathlib import Path
from io import BytesIO
from datetime import datetime

from reportlab.lib.pagesizes import A4
from reportlab.pdfgen.canvas import Canvas
from reportlab.lib.units import mm

from .colors import ColorScheme, KAAG_COLORS
from .fonts import FontManager, FONTS, get_font
from .styles import PDFStyles, DEFAULT_STYLES
from .components import (
    PDFHeader,
    PDFFooter,
    HeaderData,
    FooterData,
    SectionHeader,
    InfoBlock,
    StatsTable,
    RadarChart,
    PerformanceBar,
    RadarChartData,
    PerformanceBarData,
)


class PDFGenerator:
    """
    Base class for generating PDF documents with KAAG styling.
    
    This class provides common functionality for PDF generation
    and can be subclassed for specific report types.
    
    Usage:
        generator = PDFGenerator()
        pdf_bytes = generator.create_report(
            title="Player Report",
            subtitle="Season 2024-2025",
            content_callback=my_content_function,
        )
        
        # Save to file
        with open("report.pdf", "wb") as f:
            f.write(pdf_bytes)
    """
    
    def __init__(
        self,
        colors: Optional[ColorScheme] = None,
        styles: Optional[PDFStyles] = None,
        font_dir: Optional[str] = None,
        logo_path: Optional[str] = None,
    ):
        """
        Initialize the PDF generator.
        
        Args:
            colors: Color scheme to use (default: KAAG_COLORS)
            styles: PDF styles to use (default: DEFAULT_STYLES)
            font_dir: Path to custom fonts directory
            logo_path: Path to logo image for header
        """
        self.colors = colors or KAAG_COLORS
        self.styles = styles or DEFAULT_STYLES
        self.logo_path = logo_path
        
        # Initialize font manager
        self.font_manager = FontManager(font_dir)
        self.font_manager.register_fonts()
        
        # Initialize components
        self.header_component = PDFHeader(self.colors, self.styles)
        self.footer_component = PDFFooter(self.colors, self.styles)
        self.section_header = SectionHeader(self.colors, self.styles)
        self.info_block = InfoBlock(self.colors, self.styles)
        self.stats_table = StatsTable(self.colors, self.styles)
        self.radar_chart = RadarChart(self.colors, self.styles)
        self.performance_bar = PerformanceBar(self.colors, self.styles)
        
        # Page tracking
        self._current_page = 0
        self._total_pages = 0
        self._page_size = A4
    
    def create_report(
        self,
        title: str,
        subtitle: Optional[str] = None,
        content_callback: Optional[Callable[['PDFGenerator', Canvas, float], float]] = None,
        data: Optional[Dict[str, Any]] = None,
    ) -> bytes:
        """
        Create a PDF report using a two-pass approach for correct page numbers.
        
        Args:
            title: Report title
            subtitle: Report subtitle (optional)
            content_callback: Function to render content. Receives (generator, canvas, start_y)
                            and should return the final y position.
            data: Optional data dict passed to content_callback
                            
        Returns:
            PDF file as bytes
        """
        # First pass - count pages
        buffer = BytesIO()
        canvas = Canvas(buffer, pagesize=self._page_size)
        self._current_page = 1
        self._total_pages = 0
        
        start_y = self._draw_header(canvas, title, subtitle)
        
        if content_callback:
            content_callback(self, canvas, start_y, data, counting_only=True)
        
        canvas.showPage()
        self._total_pages = self._current_page
        
        # Second pass - render with correct page numbers
        buffer = BytesIO()
        canvas = Canvas(buffer, pagesize=self._page_size)
        self._current_page = 1
        
        start_y = self._draw_header(canvas, title, subtitle)
        self._draw_footer(canvas)
        
        if content_callback:
            content_callback(self, canvas, start_y, data, counting_only=False)
        
        canvas.save()
        
        buffer.seek(0)
        return buffer.getvalue()
    
    def _draw_header(self, canvas: Canvas, title: str, subtitle: Optional[str] = None) -> float:
        """Draw the page header and return the y position after it."""
        header_data = HeaderData(
            title=title,
            subtitle=subtitle,
            date=datetime.now().strftime("%d %B %Y"),
            logo_path=self.logo_path,
        )
        return self.header_component.draw(canvas, header_data, self._page_size[0])
    
    def _draw_footer(self, canvas: Canvas) -> None:
        """Draw the page footer."""
        footer_data = FooterData(
            show_page_numbers=True,
            total_pages=self._total_pages,
        )
        self.footer_component.draw(canvas, footer_data, self._current_page, self._page_size[0])
    
    def new_page(self, canvas: Canvas, title: str, subtitle: Optional[str] = None) -> float:
        """
        Start a new page and return the y position for content.
        
        Args:
            canvas: ReportLab canvas
            title: Page title
            subtitle: Page subtitle (optional)
            
        Returns:
            Y position for content
        """
        canvas.showPage()
        self._current_page += 1
        
        start_y = self._draw_header(canvas, title, subtitle)
        self._draw_footer(canvas)
        
        return start_y
    
    def check_page_break(
        self,
        canvas: Canvas,
        current_y: float,
        needed_height: float,
        title: str,
        subtitle: Optional[str] = None,
    ) -> float:
        """
        Check if a page break is needed and start a new page if necessary.
        
        Args:
            canvas: ReportLab canvas
            current_y: Current y position
            needed_height: Height needed for next content
            title: Title for new page (if needed)
            subtitle: Subtitle for new page (optional)
            
        Returns:
            Y position (either current_y or new page start)
        """
        min_y = self.styles.page_margin_bottom + self.styles.footer_height + 10 * mm
        
        if current_y - needed_height < min_y:
            return self.new_page(canvas, title, subtitle)
        
        return current_y
    
    # =========================================================================
    # Convenience Methods for Drawing Components
    # =========================================================================
    
    def draw_section(
        self,
        canvas: Canvas,
        y: float,
        title: str,
        show_line: bool = True,
    ) -> float:
        """Draw a section header."""
        return self.section_header.draw(
            canvas,
            self.styles.page_margin_left,
            y,
            title,
            show_line=show_line,
        )
    
    def draw_info_block(
        self,
        canvas: Canvas,
        y: float,
        items: List[tuple],
        title: Optional[str] = None,
        width: Optional[float] = None,
        x: Optional[float] = None,
    ) -> float:
        """Draw an info block with key-value pairs."""
        if width is None:
            width = (self._page_size[0] - 2 * self.styles.page_margin_left) / 2 - 5 * mm
        if x is None:
            x = self.styles.page_margin_left
        return self.info_block.draw(canvas, x, y, width, items, title)
    
    def draw_stats_table(
        self,
        canvas: Canvas,
        y: float,
        headers: List[str],
        rows: List[List[str]],
        col_widths: Optional[List[float]] = None,
    ) -> float:
        """Draw a statistics table."""
        return self.stats_table.draw(
            canvas,
            self.styles.page_margin_left,
            y,
            headers,
            rows,
            col_widths,
        )
    
    def draw_radar_chart(
        self,
        canvas: Canvas,
        center_x: float,
        center_y: float,
        data: RadarChartData,
        size: Optional[float] = None,
    ) -> None:
        """Draw a radar chart."""
        self.radar_chart.draw(canvas, center_x, center_y, data, size)
    
    def draw_performance_bar(
        self,
        canvas: Canvas,
        y: float,
        data: PerformanceBarData,
        label_width: float = 40 * mm,
        bar_width: Optional[float] = None,
        x: Optional[float] = None,
    ) -> float:
        """Draw a performance bar."""
        if x is None:
            x = self.styles.page_margin_left
        return self.performance_bar.draw(
            canvas, x, y, data, label_width, bar_width
        )
    
    def draw_performance_bars(
        self,
        canvas: Canvas,
        y: float,
        bars: List[PerformanceBarData],
        label_width: float = 40 * mm,
        bar_width: Optional[float] = None,
    ) -> float:
        """Draw multiple performance bars."""
        current_y = y
        for bar_data in bars:
            current_y = self.draw_performance_bar(
                canvas, current_y, bar_data, label_width, bar_width
            )
        return current_y
    
    # =========================================================================
    # Properties
    # =========================================================================
    
    @property
    def page_width(self) -> float:
        """Get page width."""
        return self._page_size[0]
    
    @property
    def page_height(self) -> float:
        """Get page height."""
        return self._page_size[1]
    
    @property
    def content_width(self) -> float:
        """Get available content width."""
        return self.styles.get_content_width(self._page_size[0])
    
    @property
    def current_page(self) -> int:
        """Get current page number."""
        return self._current_page
    
    @property
    def total_pages(self) -> int:
        """Get total page count (after first pass)."""
        return self._total_pages


# =============================================================================
# Exports
# =============================================================================

__all__ = ["PDFGenerator"]
