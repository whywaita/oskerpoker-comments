import datastore


def sanitize_player_name(text: str) -> str:
    """Sanitize player name

    Args:
        text: player name
    Returns:
        text: sanitized player name
    """
    # remove prefix numbers
    text = text.strip()
    if text[0].isdigit():
        text = text[1:]

    # remove white space
    text = text.strip()
    return text


def get_display_elapsed_time(elapsed_time_ms: float) -> str:
    elapsed_time_s = int(elapsed_time_ms / 1000)  # Convert ms to s
    hours, remainder = divmod(elapsed_time_s, 3600)  # Get hours and remainder
    minutes, seconds = divmod(remainder, 60)  # Get minutes and seconds from the remainder
    elapsed_time = f"{hours:02d}:{minutes:02d}:{seconds:02d}"
    # print(f"Elapsed time when add_player was called: {elapsed_time}")
    return elapsed_time


def is_check_early_close(elapsed_time_ms: float) -> bool:
    """Check if Flop is closed early

    VIDEOPOKERNET application light in the Flop area when the Flop is opened.
    But this illumination occurred in the early close. So we need to check.
    """
    open_flop_time = datastore.get_open_flop_time()
    return (elapsed_time_ms - open_flop_time) < 5000