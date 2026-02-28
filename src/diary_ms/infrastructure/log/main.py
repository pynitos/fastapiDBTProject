from logging.config import dictConfig

from diary_ms.infrastructure.log.config import LogConfig


def configure_logging(cfg: LogConfig) -> None:
    UVICORN_ACCESS_LOG_FORMAT = "%(asctime)s %(levelname)s [%(name)s] [%(filename)s:%(lineno)d] [trace_id=%(otelTraceID)s span_id=%(otelSpanID)s resource.service.name=%(otelServiceName)s] - %(message)s"  # noqa: E501
    logging_config = {
        "version": 1,
        "disable_existing_loggers": False,
        "formatters": {
            "default": {
                "format": cfg.format,
            },
            "access": {
                "()": "uvicorn.logging.AccessFormatter",
                "fmt": UVICORN_ACCESS_LOG_FORMAT,
                "use_colors": True,
            },
        },
        "handlers": {
            "console": {
                "class": "logging.StreamHandler",
                "formatter": "default",
                "stream": "ext://sys.stdout",
            },
        },
        "loggers": {
            "": {  # Root logger
                "handlers": ["console"],
                "level": cfg.level,
                "propagate": True,
            },
            "aiokafka": {
                "handlers": ["console"],
                "level": "WARNING",
                "propagate": False,
            },
        },
    }

    dictConfig(logging_config)
