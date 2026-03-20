from datetime import datetime, UTC
from prometheus_client import Counter

REQUEST_COUNT = Counter(
    "my_devops_app_requests_total",
    "Total number of HTTP requests to my-devops-app",
    ["endpoint"]
)


def get_status_payload(config):
    return {
        "app": config.APP_NAME,
        "environment": config.APP_ENV,
        "version": config.APP_VERSION,
        "message": config.MESSAGE,
        "timestamp_utc": datetime.now(UTC).isoformat(),
    }