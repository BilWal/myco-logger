"""
Utility functions for calculations and data formatting.
Provides helper functions for date calculations, success rates, and formatting.
"""

from datetime import datetime, date
from typing import Optional, Tuple


def calculate_days_elapsed(start_date, end_date: Optional[date] = None) -> Optional[int]:
    """
    Calculate the number of days elapsed between two dates.

    Args:
        start_date: Starting date (can be string, date, or datetime)
        end_date: Ending date (defaults to today if None)

    Returns:
        int: Number of days elapsed, or None if start_date is invalid
    """
    try:
        # Convert start_date to date object if needed
        if isinstance(start_date, str):
            start_date = datetime.strptime(start_date, "%Y-%m-%d").date()
        elif isinstance(start_date, datetime):
            start_date = start_date.date()
        elif not isinstance(start_date, date):
            return None

        # Use today if end_date not provided
        if end_date is None:
            end_date = date.today()
        elif isinstance(end_date, str):
            end_date = datetime.strptime(end_date, "%Y-%m-%d").date()
        elif isinstance(end_date, datetime):
            end_date = end_date.date()

        # Calculate difference
        delta = end_date - start_date
        return delta.days

    except (ValueError, TypeError, AttributeError):
        return None


def calculate_success_rate(total: int, contaminated: int) -> float:
    """
    Calculate success rate as a percentage.

    Args:
        total: Total number of experiments
        contaminated: Number of contaminated experiments

    Returns:
        float: Success rate as percentage (0-100)
    """
    if total <= 0:
        return 0.0

    successful = total - contaminated
    success_rate = (successful / total) * 100

    return round(success_rate, 1)


def format_date(date_string: Optional[str], format_str: str = "%Y-%m-%d") -> str:
    """
    Format a date string for display.

    Args:
        date_string: Date string in YYYY-MM-DD format
        format_str: Desired output format (default: "%Y-%m-%d")

    Returns:
        str: Formatted date string, or "N/A" if date is None or invalid
    """
    if not date_string or date_string == "None":
        return "N/A"

    try:
        date_obj = datetime.strptime(date_string, "%Y-%m-%d")
        return date_obj.strftime(format_str)
    except (ValueError, TypeError, AttributeError):
        return "N/A"


def get_status_color(status: str) -> str:
    """
    Get color code for a given status.

    Args:
        status: Status string (inoculating, colonizing, etc.)

    Returns:
        str: Hex color code for the status
    """
    color_map = {
        'inoculating': '#2196F3',   # Blue
        'colonizing': '#FFC107',    # Yellow/Orange
        'pinning': '#9C27B0',       # Purple
        'fruiting': '#4CAF50',      # Green
        'done': '#9E9E9E',          # Gray
        'contaminated': '#F44336'   # Red
    }

    return color_map.get(status.lower(), '#000000')  # Default to black


def get_status_background_color(status: str) -> str:
    """
    Get background color for a given status (lighter versions for styling).

    Args:
        status: Status string

    Returns:
        str: CSS background color string
    """
    background_colors = {
        'inoculating': '#E3F2FD',   # Light blue
        'colonizing': '#FFF3E0',    # Light orange
        'pinning': '#F3E5F5',       # Light purple
        'fruiting': '#E8F5E9',      # Light green
        'done': '#F5F5F5',          # Light gray
        'contaminated': '#FFEBEE'   # Light red
    }

    return background_colors.get(status.lower(), '#FFFFFF')  # Default to white


def validate_date(date_input, allow_future: bool = False) -> Tuple[bool, str]:
    """
    Validate a date input.

    Args:
        date_input: Date to validate (can be string, date, or datetime)
        allow_future: Whether to allow future dates (default: False)

    Returns:
        tuple: (is_valid: bool, error_message: str)
               If valid, error_message is empty string
    """
    try:
        # Convert to date object if needed
        if isinstance(date_input, str):
            if not date_input or date_input.strip() == "":
                return False, "Date is required"
            date_obj = datetime.strptime(date_input, "%Y-%m-%d").date()
        elif isinstance(date_input, datetime):
            date_obj = date_input.date()
        elif isinstance(date_input, date):
            date_obj = date_input
        else:
            return False, "Invalid date format"

        # Check if date is in the future
        if not allow_future and date_obj > date.today():
            return False, "Date cannot be in the future"

        return True, ""

    except (ValueError, TypeError, AttributeError):
        return False, "Invalid date format (expected YYYY-MM-DD)"


def calculate_biological_efficiency(harvest_weight_grams: float, substrate_weight_kg: float) -> Optional[float]:
    """
    Calculate Biological Efficiency (BE) percentage.

    BE = (Total fresh weight harvested / Dry substrate weight) × 100

    Args:
        harvest_weight_grams: Total fresh weight harvested in grams
        substrate_weight_kg: Dry substrate weight in kilograms

    Returns:
        float: Biological efficiency percentage, or None if calculation not possible
    """
    if substrate_weight_kg <= 0 or harvest_weight_grams < 0:
        return None

    # Convert substrate weight to grams
    substrate_weight_grams = substrate_weight_kg * 1000

    # Calculate BE
    be_percentage = (harvest_weight_grams / substrate_weight_grams) * 100

    return round(be_percentage, 1)


def format_weight(weight_grams: Optional[float], unit: str = "g") -> str:
    """
    Format weight for display with appropriate unit.

    Args:
        weight_grams: Weight in grams
        unit: Desired unit ('g' for grams, 'kg' for kilograms)

    Returns:
        str: Formatted weight string
    """
    if weight_grams is None or weight_grams < 0:
        return "N/A"

    if unit.lower() == 'kg':
        weight_kg = weight_grams / 1000
        return f"{weight_kg:.2f} kg"
    else:
        return f"{weight_grams:.1f} g"
