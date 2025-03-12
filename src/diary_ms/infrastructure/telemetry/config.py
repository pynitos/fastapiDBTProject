from dataclasses import dataclass


@dataclass
class TelemetryConfig:
    app_name: str = 'diary_app'
    oltp_grpc_endpoint: str = 'http://tempo:4317'
    log_correlation: bool = True

