from dataclasses import dataclass


@dataclass
class TelemetryConfig:
    endpoint: str
    app_name: str = "api-diary"
    log_correlation: bool = True
