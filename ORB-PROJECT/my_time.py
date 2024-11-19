import ntptime
import time


class MyTime:
    def __init__(self):
        # offset hours behind UTC
        ntptime.settime()
        self._utc_offset = -7 * 60 * 60

    def get_date_time(self):
        return time.localtime(time.time() + self._utc_offset)

    def get_time(self):
        raw_time = time.localtime(time.time() + self._utc_offset)

        return raw_time[3:6]

    def __str__(self):
        curr_time = self.get_time()
        return f"{curr_time[0]}:{curr_time[1]}:{curr_time[2]}"
