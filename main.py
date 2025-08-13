# main.py
import argparse
import os
from pprint import pprint

from benchmark_runner import BenchmarkRunner
from model_adapter import OpenAIAdapter,OllamaAdapter
from tasks import ALL_TASKS # 从 tasks 包中导入所有任务
from evaluate import LLMJudger

def main():
    parser = argparse.ArgumentParser(description="Personal LLM Benchmark Framework")
    parser.add_argument("--adapter_type", type=str, default="openai", choices=["openai", "ollama"], help="The type of adapter to use.")
    parser.add_argument("--api_base", type=str, default="https://api.openai.com/v1", help="Optional: The base URL for the API (for local models).")
    parser.add_argument("--api_key", type=str, default="sk-your-key-here", help="API Key for the LLM service.")
    parser.add_argument("--model_id", type=str, default="gpt-4", help="The ID of the model to be benchmarked.")
    parser.add_argument("--eval_api_base", type=str, default="https://api.openai.com/v1", help="The base URL for the LLM Judger API (for local models).")
    parser.add_argument("--eval_api_key", type=str, default="sk-your-key-here", help="API Key for the LLM Judger service.")
    parser.add_argument("--eval_model_id", type=str, default="gpt-4o", help="Model for the LLM Judger service.")

    parser.add_argument("--task", type=int, default=0, help="Test on specific task, default is 0 (all tasks).")
    
    args = parser.parse_args()
    if args.adapter_type == "openai" and (args.api_key == "sk-your-key-here" or args.eval_api_key == "sk-your-key-here"):
        # 如果没有提供 API Key，则提示错误
        parser.error("--api_key and eval_api_key is required for the selected adapter type")


    if args.adapter_type == "openai":
        if args.api_key == "none":
            # 对于OpenAI, api_key 是必须的
            parser.error("--api-key is required for adapter type 'openai'")
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

    judger = LLMJudger(
        api_base=args.eval_api_base,
        api_key=args.eval_api_key,
        model_id=args.eval_model_id
    )
    # 初始化 Benchmark Runner
    # 它会自动加载我们定义在 tasks/__init__.py 中的所有任务
    runner = BenchmarkRunner(model_adapter, ALL_TASKS, judger, args.task)

    # 运行并获取结果
    final_report = runner.run()

    # 4. 打印最终报告
    print("\n\n========== 📊 FINAL BENCHMARK REPORT ==========")
    pprint(final_report)
    print("==============================================")

if __name__ == "__main__":
    main()