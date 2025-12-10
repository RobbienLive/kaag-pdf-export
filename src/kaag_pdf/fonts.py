"""
Font Management for KAAG PDF Exports
====================================

Handles registration and management of custom fonts
for ReportLab PDF generation.
"""

import os
from pathlib import Path
from typing import Dict, Optional, List
from dataclasses import dataclass, field

from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont


# =============================================================================
# Font Configuration
# =============================================================================

@dataclass
class FontFamily:
    """
    Definition of a font family with all its variants.
    
    Attributes:
        name: Base name of the font family (e.g., "Poppins")
        regular: Filename for regular weight
        bold: Filename for bold weight (optional)
        italic: Filename for italic style (optional)
        bold_italic: Filename for bold italic (optional)
        semibold: Filename for semibold weight (optional)
        light: Filename for light weight (optional)
        medium: Filename for medium weight (optional)
    """
    name: str
    regular: str
    bold: Optional[str] = None
    italic: Optional[str] = None
    bold_italic: Optional[str] = None
    semibold: Optional[str] = None
    light: Optional[str] = None
    medium: Optional[str] = None
    
    def get_variants(self) -> Dict[str, str]:
        """Get all available font variants as a dict."""
        variants = {"Regular": self.regular}
        if self.bold:
            variants["Bold"] = self.bold
        if self.italic:
            variants["Italic"] = self.italic
        if self.bold_italic:
            variants["BoldItalic"] = self.bold_italic
        if self.semibold:
            variants["SemiBold"] = self.semibold
        if self.light:
            variants["Light"] = self.light
        if self.medium:
            variants["Medium"] = self.medium
        return variants


# =============================================================================
# KAAG Font Definitions
# =============================================================================

FONT_FAMILIES = {
    "Poppins": FontFamily(
        name="Poppins",
        regular="poppins-regular.ttf",
        # Add more variants when available:
        # bold="poppins-bold.ttf",
        # italic="poppins-italic.ttf",
        # semibold="poppins-semibold.ttf",
        # light="poppins-light.ttf",
        # medium="poppins-medium.ttf",
    ),
    "Obviously": FontFamily(
        name="Obviously",
        # Note: only bold currently available, use as "regular"
        regular="obviously-bold.ttf",
        bold="obviously-bold.ttf",
        # semibold="obviously-semibold.ttf",
    ),
    "IvyPresto": FontFamily(
        name="IvyPresto",
        regular="ivy-presto-display.ttf",
        # italic="ivy-presto-display-italic.ttf",
    ),
}


# Quick access to font names
FONTS = {
    # Poppins family
    "POPPINS_REGULAR": "Poppins-Regular",
    "POPPINS_BOLD": "Poppins-Bold",
    "POPPINS_SEMIBOLD": "Poppins-SemiBold",
    "POPPINS_LIGHT": "Poppins-Light",
    "POPPINS_MEDIUM": "Poppins-Medium",
    "POPPINS_ITALIC": "Poppins-Italic",
    
    # Obviously family
    "OBVIOUSLY_REGULAR": "Obviously-Regular",
    "OBVIOUSLY_BOLD": "Obviously-Bold",
    "OBVIOUSLY_SEMIBOLD": "Obviously-SemiBold",
    
    # IvyPresto family
    "IVYPRESTO_REGULAR": "IvyPrestoDisplay-Regular",
    "IVYPRESTO_ITALIC": "IvyPrestoDisplay-Italic",
    
    # Aliases for common uses
    "HEADING": "Obviously-Bold",
    "SUBHEADING": "Poppins-SemiBold",
    "BODY": "Poppins-Regular",
    "BODY_BOLD": "Poppins-Bold",
    "ACCENT": "IvyPrestoDisplay-Italic",
    "LABEL": "Poppins-Medium",
    "SMALL": "Poppins-Light",
}


# =============================================================================
# Font Manager
# =============================================================================

class FontManager:
    """
    Manages font registration and availability for PDF generation.
    
    Usage:
        font_manager = FontManager()
        font_manager.register_fonts()
        
        # Or with custom font directory:
        font_manager = FontManager(font_dir="/path/to/fonts")
        font_manager.register_fonts()
        
        # Check if fonts are available:
        if font_manager.is_font_available("Poppins-Bold"):
            # Use the font
            pass
    """
    
    def __init__(self, font_dir: Optional[str] = None):
        """
        Initialize the FontManager.
        
        Args:
            font_dir: Path to the fonts directory. If None, uses the
                     package's built-in fonts directory.
        """
        if font_dir:
            self.font_dir = Path(font_dir)
        else:
            # Default to package's assets/fonts directory
            self.font_dir = Path(__file__).parent / "assets" / "fonts"
        
        self._registered_fonts: List[str] = []
        self._fallback_used = False
    
    def register_fonts(self, families: Optional[List[str]] = None) -> Dict[str, bool]:
        """
        Register fonts with ReportLab.
        
        Args:
            families: List of font family names to register.
                     If None, registers all available families.
                     
        Returns:
            Dict mapping font names to registration success status.
        """
        results = {}
        
        if families is None:
            families = list(FONT_FAMILIES.keys())
        
        for family_name in families:
            if family_name not in FONT_FAMILIES:
                print(f"Warning: Unknown font family '{family_name}'")
                continue
                
            family = FONT_FAMILIES[family_name]
            
            for variant_name, filename in family.get_variants().items():
                font_name = f"{family.name}-{variant_name}"
                font_path = self.font_dir / filename
                
                if font_path.exists():
                    try:
                        pdfmetrics.registerFont(TTFont(font_name, str(font_path)))
                        self._registered_fonts.append(font_name)
                        results[font_name] = True
                    except Exception as e:
                        print(f"Warning: Failed to register font '{font_name}': {e}")
                        results[font_name] = False
                else:
                    print(f"Warning: Font file not found: {font_path}")
                    results[font_name] = False
        
        # Check if we need fallbacks
        if not any(results.values()):
            self._fallback_used = True
            print("Warning: No custom fonts loaded, using system defaults")
        
        return results
    
    def is_font_available(self, font_name: str) -> bool:
        """Check if a font has been registered."""
        return font_name in self._registered_fonts
    
    def get_font(self, font_key: str, fallback: str = "Helvetica") -> str:
        """
        Get a font name, with fallback if not available.
        
        Args:
            font_key: Key from FONTS dict or direct font name
            fallback: Fallback font name if requested font not available
            
        Returns:
            The font name to use
        """
        # First, resolve key to font name
        font_name = FONTS.get(font_key, font_key)
        
        # Check if available
        if self.is_font_available(font_name):
            return font_name
        
        return fallback
    
    def get_bold_font(self, base_font: str) -> str:
        """
        Get the bold variant of a font.
        
        Args:
            base_font: Base font name (e.g., "Poppins-Regular")
            
        Returns:
            Bold variant name, or base font if bold not available
        """
        # Try to derive family name
        if "-" in base_font:
            family = base_font.split("-")[0]
        else:
            family = base_font
        
        bold_name = f"{family}-Bold"
        if self.is_font_available(bold_name):
            return bold_name
        
        # Try generic bold
        if self.is_font_available("Helvetica-Bold"):
            return "Helvetica-Bold"
        
        return base_font
    
    @property
    def registered_fonts(self) -> List[str]:
        """List of all registered font names."""
        return self._registered_fonts.copy()
    
    @property
    def using_fallback(self) -> bool:
        """Whether fallback fonts are being used."""
        return self._fallback_used


# =============================================================================
# Convenience Functions
# =============================================================================

_default_manager: Optional[FontManager] = None


def get_font_manager() -> FontManager:
    """Get the default FontManager instance."""
    global _default_manager
    if _default_manager is None:
        _default_manager = FontManager()
        _default_manager.register_fonts()
    return _default_manager


def get_font(font_key: str, fallback: str = "Helvetica") -> str:
    """
    Convenience function to get a font name.
    
    Args:
        font_key: Key from FONTS dict or direct font name
        fallback: Fallback font name if requested font not available
        
    Returns:
        The font name to use
    """
    return get_font_manager().get_font(font_key, fallback)
