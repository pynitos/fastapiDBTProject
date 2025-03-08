from logging.config import dictConfig

from src.diary_ms.infrastructure.log.config import LogConfig


def configure_logging(cfg: LogConfig) -> None:
    logging_config = {
        "version": 1,
        "disable_existing_loggers": False,
        "formatters": {
            "default": {
                "format": cfg.format,
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
            "": {  # Корневой логгер
                "handlers": ["console"],
                "level": cfg.level,  # Уровень логирования
                "propagate": True,
            },
            "uvicorn": {  # Логгер Uvicorn
                "handlers": ["console"],
                "level": cfg.level,  # Уровень логирования
                "propagate": False,
            },
            "uvicorn.error": {  # Логгер ошибок Uvicorn
                "handlers": ["console"],
                "level": cfg.level,  # Уровень логирования
                "propagate": False,
            },
            "uvicorn.access": {  # Логгер доступа Uvicorn
                "handlers": ["console"],
                "level": cfg.level,  # Уровень логирования
                "propagate": False,
            },
        },
    }

    dictConfig(logging_config)
