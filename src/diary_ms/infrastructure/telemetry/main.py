
import logging
from opentelemetry import trace
from opentelemetry.exporter.otlp.proto.grpc.trace_exporter import OTLPSpanExporter
from opentelemetry.instrumentation.fastapi import FastAPIInstrumentor
from opentelemetry.instrumentation.logging import LoggingInstrumentor
from opentelemetry.sdk.resources import Resource
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.trace.export import BatchSpanProcessor
from fastapi import FastAPI

from src.diary_ms.infrastructure.telemetry.config import TelemetryConfig
from src.diary_ms.infrastructure.telemetry.utils import PrometheusMiddleware, metrics


def configure_telemetry_fastapi(app: FastAPI, cfg: TelemetryConfig) -> None:
    # Setting OpenTelemetry
    # set the service name to show in traces
    app_name = cfg.app_name
    endpoint = cfg.oltp_grpc_endpoint
    log_correlation = cfg.log_correlation

    app.add_middleware(PrometheusMiddleware, app_name=app_name)
    app.add_route("/metrics", metrics)

    resource = Resource.create(attributes={
        "service.name": app_name,
        "compose_service": app_name
    })

    # set the tracer provider
    tracer = TracerProvider(resource=resource)
    trace.set_tracer_provider(tracer)

    tracer.add_span_processor(BatchSpanProcessor(
        OTLPSpanExporter(endpoint=endpoint)))

    if log_correlation:
        LoggingInstrumentor().instrument(set_logging_format=True)

    FastAPIInstrumentor.instrument_app(app, tracer_provider=tracer)

    class EndpointFilter(logging.Filter):
        # Uvicorn endpoint access log filter
        def filter(self, record: logging.LogRecord) -> bool:
            return record.getMessage().find("GET /metrics") == -1
        
    # Filter out /endpoint
    logging.getLogger("uvicorn.access").addFilter(EndpointFilter())
