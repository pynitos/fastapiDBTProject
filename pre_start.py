import asyncio
import logging

from src.diary_ms.infrastructure.gateways.sqla.db.init_db import init_db

if __name__ == "__main__":
    asyncio.run(init_db())
    logging.info("Data incerted!")
