# km_wachter.py
# KM-Waechter decides when a Vossberg Mobility car needs a service.
# Written in 2013. Modernised 2025.

SERVICE_INTERVAL_KM = 15000
WARN_AT_PERCENT = 80


def wear_percent(km_since_service: float, interval: int) -> float:
    """Return how many percent of the service interval have been used up.

    Uses true division so a car at 14,900 of 15,000 km reports ~99.3 %,
    not 0 % (which the old integer floor-division produced).
    """
    return (km_since_service / interval) * 100


def needs_service(car: dict) -> bool:
    """Return True only when a car's wear reaches the warning threshold.

    A car with no ``last_service_km`` reading is treated as unknown, not
    as zero — returning False avoids a false alarm.
    """
    if "last_service_km" not in car:
        return False
    last = car["last_service_km"]
    km_since = car["odometer"] - last
    return wear_percent(km_since, SERVICE_INTERVAL_KM) >= WARN_AT_PERCENT


def check_fleet(fleet: list[dict]) -> list[str]:
    """Flag every car that needs a service and return their IDs."""
    flagged = []
    for car in fleet:
        if needs_service(car):
            flagged.append(car["id"])
            print(f"SERVICE DUE: {car['id']}")
    return flagged
