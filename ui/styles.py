"""
Design Tokens and Theme Constants for StockMind AI:
Clean, modern, light professional financial interface with soft 3D depth,
subtle shadows, and high contrast readability.
"""

THEME_CONFIG = {
    "name": "Light Professional Financial",
    "colors": {
        "bg_primary": "#F8FAFC",       # Off-white clean slate
        "bg_surface": "#FFFFFF",       # Pure white cards
        "bg_elevated": "#F1F5F9",      # Elevated secondary surfaces
        "border_subtle": "#E2E8F0",    # Crisp hairline borders
        "border_focus": "#3B82F6",     # Professional royal blue
        
        "text_primary": "#0F172A",     # Deep obsidian slate
        "text_secondary": "#475569",   # Balanced neutral
        "text_muted": "#94A3B8",       # Subtle captions
        
        "accent_positive": "#10B981",  # Institutional emerald green
        "accent_negative": "#EF4444",  # Institutional rose red
        "accent_neutral": "#64748B",   # Slate neutral
        "accent_brand": "#2563EB",     # StockMind brand blue
        "accent_warning": "#F59E0B",   # Amber warning
        
        "badge_green_bg": "#ECFDF5",
        "badge_green_text": "#065F46",
        "badge_red_bg": "#FEF2F2",
        "badge_red_text": "#991B1B",
        "badge_blue_bg": "#EFF6FF",
        "badge_blue_text": "#1E40AF",
        "badge_amber_bg": "#FFFBEB",
        "badge_amber_text": "#92400E"
    },
    "typography": {
        "font_family": "'Inter', -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif",
        "font_mono": "'JetBrains Mono', 'Fira Code', monospace"
    },
    "shadows": {
        "card": "0 1px 3px 0 rgba(0, 0, 0, 0.05), 0 1px 2px -1px rgba(0, 0, 0, 0.05)",
        "hover": "0 10px 25px -5px rgba(0, 0, 0, 0.08), 0 8px 10px -6px rgba(0, 0, 0, 0.04)",
        "input": "0 4px 14px 0 rgba(0, 0, 0, 0.04)"
    },
    "radii": {
        "sm": "8px",
        "md": "12px",
        "lg": "16px",
        "full": "9999px"
    }
}
