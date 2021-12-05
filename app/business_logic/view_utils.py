

def count_down(time):
    """Calculate time left"""
    time_left = time.total_seconds()
    days = time_left // (24 * 3600)
    time_left = time_left % (24 * 3600)
    hours = time_left // 3600
    time_left %= 3600
    minutes = time_left // 60

    return {
        'days': int(days),
        'hours': int(hours),
        'minutes': int(minutes),
    }
