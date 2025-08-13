import logging
import os
from datetime import datetime

def setup_markdown_logger():
    """
    设置一个 Markdown 日志记录器，自动在 ./results/ 目录下创建带时间戳的文件。
    如果 ./results/ 目录不存在，则会自动创建。
    """
    # 创建 ./results 目录（如果不存在）
    results_dir = "results"
    os.makedirs(results_dir, exist_ok=True)

    # 生成带时间戳的文件名
    timestamp = datetime.now().strftime("%Y-%m-%d-%H%M%S")
    file_path = os.path.join(results_dir, f"{timestamp}.md")

    # 创建一个 Logger 实例
    logger = logging.getLogger("benchmark_logger")
    logger.setLevel(logging.INFO) # 只记录 INFO 及以上级别的日志

    # 避免重复添加 Handler
    if not logger.handlers:
        # 创建一个 FileHandler，将日志写入 Markdown 文件
        file_handler = logging.FileHandler(file_path, mode='w', encoding='utf-8')

        # 自定义一个 Formatter，用于将日志信息转换为 Markdown 格式
        formatter = logging.Formatter('%(message)s')
        file_handler.setFormatter(formatter)

        # 将 Handler 添加到 Logger
        logger.addHandler(file_handler)

    return logger