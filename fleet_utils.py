# fleet_utils.py
# Helpers for fleet reporting. Modernised 2025.
# Dead code (is_due, parse_service_date, chunk_list) removed — none of it
# was imported or called anywhere in the project.

KM_PER_MILE = 1.60934          # exact: 1 mile = 1.60934 km
MILES_PER_KM = 1 / KM_PER_MILE  # ≈ 0.6214 — previously the constant was inverted


def km_to_miles(km: float) -> float:
    """Convert kilometres to miles.

    Used by the nightly run for the UK partner report.
    """
    return km * MILES_PER_KM


def format_number(value: float) -> str:
    """Format a float to one decimal place."""
    return f"{value:.1f}"


def format_percent(value: float) -> str:
    """Format a number as a whole-number percentage string."""
    return f"{int(value)}%"


def mean(values: list[float]) -> float:
    """Return the arithmetic mean of a list, or 0 if the list is empty.

    Note: ``statistics.mean`` has been available since Python 3.4 and is
    preferred for new code; this function is kept for compatibility.
    """
    if not values:
        return 0
    return sum(values) / len(values)
