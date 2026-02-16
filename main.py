# main.py
import argparse
import os
from pprint import pprint
import datetime

from benchmark_runner import BenchmarkRunner
from model_adapter import OpenAIAdapter,OllamaAdapter
from evaluate import OpenAIJudger, OllamaJudger
from logger import setup_markdown_logger
from tasks_handler import load_all_tasks

def main():
    parser = argparse.ArgumentParser(description="Personal LLM Benchmark Framework")
    parser.add_argument("--adapter_type", type=str, default="openai", choices=["openai", "ollama"], help="The type of adapter to use.")
    parser.add_argument("--api_base", type=str, default="https://api.openai.com/v1", help="Optional: The base URL for the API (for local models).")
    parser.add_argument("--api_key", type=str, default="sk-your-key-here", help="API Key for the LLM service.")
    parser.add_argument("--model_id", type=str, default="gpt-4", help="The ID of the model to be benchmarked.")

    parser.add_argument("--judger_adapter_type", type=str, default="openai", choices=["openai", "ollama"], help="The type of judger adapter to use.")
    parser.add_argument("--judger_api_base", type=str, default="https://api.openai.com/v1", help="The base URL for the LLM Judger API (for local models).")
    parser.add_argument("--judger_api_key", type=str, default="sk-your-key-here", help="API Key for the LLM Judger service.")
    parser.add_argument("--judger_model_id", type=str, default="gpt-4o", help="Model for the LLM Judger service.")

    parser.add_argument("--task", type=int, default=0, help="Test on specific task, default is 0 (all tasks).")
    
    args = parser.parse_args()
    benchmark_logger = setup_markdown_logger()
    benchmark_logger.info("# Noah's LLM Benchmark 结果\n")
    benchmark_logger.info(f"- 测评模型: {args.model_id}\n")
    benchmark_logger.info(f"- 评价模型: {args.judger_model_id}\n")
    benchmark_logger.info(f"- 运行时间: {datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
    benchmark_logger.info(f"- 题库版本: 20260216\n")

    if args.adapter_type == "openai" and args.api_key == "sk-your-key-here":
        # 如果被测模型为外部模型，且没有提供 API Key，则提示错误
        parser.error("--api_key is required for the selected adapter type")
    
    if args.judger_adapter_type == "openai" and args.judger_api_key == "sk-your-key-here":
        # 如果裁判模型为外部模型，且没有提供 API Key，则提示错误
        parser.error("--judger_api_key is required for the selected judger adapter type")


    if args.adapter_type == "openai":
        model_adapter = OpenAIAdapter(
            api_key=args.api_key,
            model_id=args.model_id,
            api_base=args.api_base
        )
    elif args.adapter_type == "ollama":
        model_adapter = OllamaAdapter(
            api_key=args.api_key, # 即使被忽略，也传入以保持一致性
            model_id=args.model_id,
            api_base=args.api_base
        )
    else:
        raise ValueError(f"Unknown adapter type: {args.adapter_type}")
    
    if args.judger_adapter_type == "openai":
        judger_model_adapter = OpenAIJudger(
            api_key=args.judger_api_key,
            model_id=args.judger_model_id,
            api_base=args.judger_api_base
        )
    elif args.judger_adapter_type == "ollama":
        judger_model_adapter = OllamaJudger(
            api_key=args.judger_api_key, # 即使被忽略，也传入以保持一致性
            model_id=args.judger_model_id,
            api_base=args.judger_api_base
        )
    else:
        raise ValueError(f"Unknown judger adapter type: {args.judger_adapter_type}")

    all_tasks = load_all_tasks("tasks")

    # 初始化 Benchmark Runner

    runner = BenchmarkRunner(model_adapter, all_tasks, judger_model_adapter, args.task, benchmark_logger)

    # 运行并获取结果
    final_report = runner.run()

    # 打印最终报告
    print("\n\n========== 📊 FINAL BENCHMARK REPORT ==========")
    pprint(final_report)
    print("==============================================")

if __name__ == "__main__":
    main()