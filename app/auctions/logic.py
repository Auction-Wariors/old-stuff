def count_down_func(time):
    time_left = time.total_seconds()
    days = time_left // (24 * 3600)
    time_left = time_left % (24 * 3600)
    hours = time_left // 3600
    time_left %= 3600
    minutes = time_left // 60
    count_down = {
        'days': int(days),
        'hours': int(hours),
        'minutes': int(minutes),
    }
    return count_down
