# custom_test_runner.py

from django.test.runner import DiscoverRunner


class CustomTestRunner(DiscoverRunner):
    def setup_databases(self, **kwargs):
        # Skip creating the test database
        return []
