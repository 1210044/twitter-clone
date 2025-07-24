import logging
import sys
from typing import Optional

from src.core.config.project_config import settings

def setup_logging(log_level: Optional[str] = None) -> None:
    """Настройка логгирования для всего приложения"""
    
    if log_level is None:
        log_level = settings.LOG_LEVEL
    
    # Базовая конфигурация
    logging.basicConfig(
        level=getattr(logging, log_level.upper()),
        format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
        handlers=[
            logging.StreamHandler(sys.stdout),
            # Можно добавить FileHandler для логов в файл
        ]
    )

def get_logger(name: str) -> logging.Logger:
    """Получение настроенного логгера"""
    return logging.getLogger(name)

# Глобальный логгер для core компонентов
logger = get_logger(__name__)