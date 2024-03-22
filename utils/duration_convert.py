from typing import Optional, Dict


def convert_duration_to_time(
        duration: Optional[str]
) -> Optional[Dict[Optional[int], Optional[int]]]:
    """
    Convert duration string to hours and minutes.

    Args:
        duration (Optional[str]): Duration string in format 'XhYm'.

    Returns:
        Optional[Dict[Optional[int], Optional[int]]]: Dictionary containing hours and minutes.
    """
    if not duration:
        return None

    hours, minutes = None, None

    if "h" in duration and "m" in duration:
        h_index = duration.index("h")
        m_index = duration.index("m")

        hours = int(duration[:h_index])
        minutes = int(duration[h_index + 1:m_index])

    if "h" in duration and "m" not in duration:
        h_index = duration.index("h")
        hours = int(duration[:h_index])

    if "h" not in duration and "m" in duration:
        m_index = duration.index("m")
        minutes = int(duration[:m_index])

    return {"hours": hours, "minutes": minutes}
