from datetime import datetime, UTC


def get_status_payload(config):
    return {
        "app": config.APP_NAME,
        "environment": config.APP_ENV,
        "version": config.APP_VERSION,
        "message": config.MESSAGE,
        "timestamp_utc": datetime.now(UTC).isoformat(),
    }