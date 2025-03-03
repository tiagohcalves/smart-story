import time
import threading

class RateLimiter:
    def __init__(self, max_calls: int, period: float):
        """
        Initialize the rate limiter.

        :param max_calls: Maximum number of calls allowed in the period.
        :param period: Time window in seconds.
        """
        self.max_calls = max_calls
        self.period = period
        self.lock = threading.Lock()
        self.calls = []

    def acquire(self):
        """Block until a request is allowed."""
        with self.lock:
            now = time.time()
            # Remove timestamps outside the time window
            self.calls = [t for t in self.calls if t > now - self.period]

            if len(self.calls) >= self.max_calls:
                sleep_time = self.calls[0] + self.period - now
                if sleep_time > 0:
                    time.sleep(sleep_time)

            # Register the new call
            self.calls.append(time.time())
