from faststream.kafka.broker import KafkaBroker

from src.diary_ms.main.config import settings

message_broker: KafkaBroker = KafkaBroker(settings.BROKER_URI)
