"""Packet delay models, Chapter 1."""


def transmission_delay(packet_bits: int, rate_bps: float) -> float:
    """Return transmission delay in seconds (L/R)."""
    if packet_bits < 0 or rate_bps <= 0:
        raise ValueError("packet_bits must be >= 0 and rate_bps must be > 0")
    return packet_bits / rate_bps


def propagation_delay(distance_m: float, speed_mps: float = 2e8) -> float:
    """Return propagation delay in seconds (d/s)."""
    if distance_m < 0 or speed_mps <= 0:
        raise ValueError("distance_m must be >= 0 and speed_mps must be > 0")
    return distance_m / speed_mps


def nodal_delay(
    processing_s: float,
    queueing_s: float,
    transmission_s: float,
    propagation_s: float
) -> float:
    """Return the total nodal delay in seconds."""

    delays = (
        processing_s,
        queueing_s,
        transmission_s,
        propagation_s
    )

    if any(delay < 0 for delay in delays):
        raise ValueError("Delay components must not be negative")

    return sum(delays)

