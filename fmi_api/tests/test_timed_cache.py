"""
 This code was published by myrheimb without license at:
 https://gist.github.com/Morreski/c1d08a3afa4040815eafd3891e16b945
"""

import unittest


class Testing(unittest.TestCase):
    def test_timed_cache(self):
        """Test the timed_cache decorator."""

        from .._timed_cache import timed_cache

        import logging
        import time

        cache_logger = logging.getLogger("foo_log")

        @timed_cache(seconds=1)
        def cache_testing_function(num1, num2):
            cache_logger.info("Not cached yet.")
            return num1 + num2

        with self.assertLogs(level="INFO") as cache_log:

            result1 = cache_testing_function(2, 3)
            self.assertEqual(cache_log.output[0], "INFO:foo_log:Not cached yet.")
            assert result1 == 5

            result2 = cache_testing_function(2, 3)
            assert len(cache_log.output) == 1
            assert result2 == 5

            time.sleep(1)

            result3 = cache_testing_function(2, 3)
            self.assertEqual(cache_log.output[1], "INFO:foo_log:Not cached yet.")
            assert result3 == 5
