from dataclasses import dataclass


@dataclass
class TelemetryConfig:
    endpoint: str | None = None
    app_name: str = "api-diary"
    log_correlation: bool = True
