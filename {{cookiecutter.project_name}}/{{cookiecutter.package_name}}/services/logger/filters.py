from logging import Filter


class HealthCheckFilter(Filter):
    """
    Filter class that stops health-check
    requests from being logged
    """

    def filter(self, record) -> bool:
        is_health_check = "health/check" in record.url
        return not is_health_check
