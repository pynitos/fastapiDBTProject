from dataclasses import dataclass


@dataclass
class TelemetryConfig:
    telemetry_url: str
    app_name: str = 'diary_app'
    log_correlation: bool = True

