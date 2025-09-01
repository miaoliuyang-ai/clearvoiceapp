#!/usr/bin/env python3
"""
测试 ClearVoice API 日志系统
Test script for ClearVoice API logging system.
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from utilities.logging_manager import setup_api_logging

def test_logger():
    """测试日志功能"""
    print("🎵 测试 ClearVoice API 日志系统")
    print("=" * 50)

    # 初始化日志系统
    logger = setup_api_logging()

    # 测试不同级别的日志
    logger.info("✅ 信息日志测试")
    logger.warning("⚠️  警告日志测试")
    logger.error("❌ 错误日志测试")
    logger.debug("🔍 调试日志测试（可能不显示，取决于配置）")

    print("📝 日志测试完成！请查看控制台输出和日志文件")

if __name__ == "__main__":
    test_logger()
