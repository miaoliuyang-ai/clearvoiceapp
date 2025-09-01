"""
ClearVoice API 日志管理器
Logging manager for ClearVoice API service.

基于 HuaweiCloudAICall 的日志管理系统，实现统一的日志管理功能。
"""

import logging
import os
from datetime import datetime
from typing import Optional


# 日志配置常量
LOG_LEVEL = "INFO"
LOG_FORMAT = "%(asctime)s [%(levelname)s] %(name)s: %(message)s"
LOG_DIR = "logs"


class ClearVoiceLoggingManager:
    """
    ClearVoice API 集中化日志管理器
    Centralized logging manager for ClearVoice API service.
    """

    _loggers = {}
    _initialized = False
    _current_log_file = None

    @classmethod
    def setup_logging_system(cls, log_dir: Optional[str] = None) -> None:
        """
        初始化整个日志系统

        Args:
            log_dir: 保存日志文件的目录，默认使用配置中的LOG_DIR
        """
        if cls._initialized:
            return

        log_directory = log_dir or LOG_DIR
        os.makedirs(log_directory, exist_ok=True)

        # 创建带时间戳的日志文件
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        log_file_path = os.path.join(log_directory, f'clearvoice_api_{timestamp}.log')
        cls._current_log_file = log_file_path

        # 文件处理器：保存到文件
        file_handler = logging.FileHandler(log_file_path, encoding='utf-8')
        file_handler.setLevel(getattr(logging, LOG_LEVEL))
        file_handler.setFormatter(logging.Formatter(LOG_FORMAT))

        # 控制台处理器：输出到控制台
        console_handler = logging.StreamHandler()
        console_handler.setLevel(getattr(logging, LOG_LEVEL))
        console_handler.setFormatter(logging.Formatter(LOG_FORMAT))

        # 配置根日志记录器
        logging.basicConfig(
            level=getattr(logging, LOG_LEVEL),
            handlers=[file_handler, console_handler],
            force=True  # 强制重新配置
        )

        cls._initialized = True
        print(f"📝 ClearVoice API 日志系统已初始化，日志文件: {log_file_path}")

    @classmethod
    def get_logger(cls, module_name: str) -> logging.Logger:
        """
        获取指定模块的日志记录器实例

        Args:
            module_name: 模块名称（通常是 __name__）

        Returns:
            配置好的日志记录器实例
        """
        if not cls._initialized:
            cls.setup_logging_system()

        if module_name not in cls._loggers:
            cls._loggers[module_name] = logging.getLogger(module_name)

        return cls._loggers[module_name]

    @classmethod
    def get_current_log_file(cls) -> Optional[str]:
        """
        获取当前日志文件路径

        Returns:
            当前日志文件的完整路径，如果未初始化则返回None
        """
        return cls._current_log_file

    @classmethod
    def shutdown_logging(cls) -> None:
        """
        关闭日志系统，清理资源
        """
        logging.shutdown()
        cls._initialized = False
        cls._loggers.clear()
        cls._current_log_file = None


def get_logger(module_name: str) -> logging.Logger:
    """
    获取日志记录器的便捷函数

    Args:
        module_name: 模块名称

    Returns:
        配置好的日志记录器实例
    """
    return ClearVoiceLoggingManager.get_logger(module_name)


def setup_api_logging() -> logging.Logger:
    """
    设置 ClearVoice API 专用日志

    Returns:
        API日志记录器实例
    """
    ClearVoiceLoggingManager.setup_logging_system()
    return ClearVoiceLoggingManager.get_logger('ClearVoiceAPI')


# 统一别名
LoggerManager = ClearVoiceLoggingManager
