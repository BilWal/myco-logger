"""
Asset management module for Myco Logger.
Centralizes paths to icons, images, and branding assets.
"""

import os
from pathlib import Path

# Base paths
ASSETS_DIR = Path(__file__).parent / "assets"
ICONS_DIR = ASSETS_DIR / "icons"
STATUS_DIR = ICONS_DIR / "status"
SUBSTRATE_DIR = ICONS_DIR / "substrates"
BRANDING_DIR = ASSETS_DIR / "branding"

# Status icons mapping
STATUS_ICONS = {
    'inoculating': str(STATUS_DIR / 'inoculating.png'),
    'colonizing': str(STATUS_DIR / 'colonizing.png'),
    'pinning': str(STATUS_DIR / 'pinning.png'),
    'fruiting': str(STATUS_DIR / 'fruiting.png'),
    'done': str(STATUS_DIR / 'done.png'),
    'contaminated': str(STATUS_DIR / 'contaminated.png'),
}

# Substrate icons mapping
SUBSTRATE_ICONS = {
    'cardboard': str(SUBSTRATE_DIR / 'cardboard.png'),
    'coffee grounds': str(SUBSTRATE_DIR / 'coffee.png'),
    'coffee': str(SUBSTRATE_DIR / 'coffee.png'),  # alias
    'straw': str(SUBSTRATE_DIR / 'straw.png'),
    'sawdust pellets': str(SUBSTRATE_DIR / 'sawdust.png'),
    'sawdust': str(SUBSTRATE_DIR / 'sawdust.png'),  # alias
    'mix': str(SUBSTRATE_DIR / 'mixed.png'),
    'mixed': str(SUBSTRATE_DIR / 'mixed.png'),
    'other': str(SUBSTRATE_DIR / 'mixed.png'),  # fallback
}

# Branding
LOGO_HEADER = str(BRANDING_DIR / 'logo_header.png')


def get_status_icon(status: str) -> str:
    """
    Get path to status icon, with fallback.

    Args:
        status: Status string (inoculating, colonizing, etc.)

    Returns:
        str: Path to icon file
    """
    status_lower = status.lower()
    # Handle "colonizing" variations
    if 'coloniz' in status_lower and status_lower not in STATUS_ICONS:
        return STATUS_ICONS.get('colonizing', '')
    return STATUS_ICONS.get(status_lower, STATUS_ICONS.get('inoculating', ''))


def get_substrate_icon(substrate: str) -> str:
    """
    Get path to substrate icon, with fallback.

    Args:
        substrate: Substrate type string

    Returns:
        str: Path to icon file
    """
    substrate_lower = substrate.lower()
    return SUBSTRATE_ICONS.get(substrate_lower, SUBSTRATE_ICONS.get('mixed', ''))


def verify_assets() -> dict:
    """
    Verify all assets exist and return status.

    Returns:
        dict: Status dictionary with 'all_present' bool and 'missing' list
    """
    missing = []

    # Check status icons
    for status, path in STATUS_ICONS.items():
        if not os.path.exists(path):
            missing.append(f"Status icon: {status} ({path})")

    # Check substrate icons
    unique_substrate_paths = set(SUBSTRATE_ICONS.values())
    for path in unique_substrate_paths:
        if not os.path.exists(path):
            missing.append(f"Substrate icon: {path}")

    # Check branding
    if not os.path.exists(LOGO_HEADER):
        missing.append(f"Logo: {LOGO_HEADER}")

    return {
        'all_present': len(missing) == 0,
        'missing': missing
    }


def safe_image_display(st, image_path: str, width=None, fallback_emoji="🍄"):
    """
    Display image with emoji fallback if image missing.

    Args:
        st: Streamlit module reference
        image_path: Path to image file
        width: Optional width for image
        fallback_emoji: Emoji to show if image not found
    """
    try:
        if os.path.exists(image_path):
            st.image(image_path, width=width)
        else:
            st.write(fallback_emoji)
    except Exception as e:
        st.write(fallback_emoji)
