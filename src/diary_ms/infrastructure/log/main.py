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
            'file': {
                'level': cfg.level,
                'class': 'logging.FileHandler',  # Запись в файл
                'filename': './logs/app.log',  # Имя файла
                'formatter': 'default',
                },
        },
        "loggers": {
            "": {  # Root logger
                "handlers": ["console", "file"],
                "level": cfg.level,
                "propagate": True,
            },
            "aiokafka": {
                "handlers": ["console", "file"],
                "level": "WARNING",
                "propagate": False,
            },
        },
    }

    dictConfig(logging_config)
