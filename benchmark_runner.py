# benchmark_runner.py
import time
from tqdm import tqdm
import logging

from model_adapter import BaseModelAdapter
from tasks.task_0_base_task import BenchmarkTask
from evaluate import LLMJudger
from typing import List
from evaluate import LLMJudger

# logging.basicConfig(level=logging.DEBUG)

class BenchmarkRunner:
    def __init__(self, model_adapter: BaseModelAdapter, tasks: List[BenchmarkTask], judger: LLMJudger, task_index: int = 0, benchmark_logger: logging.Logger = None):
        self.model_adapter = model_adapter
        self.tasks = tasks
        self.results = []
        self.judger = judger
        self.task_index = task_index
        self.benchmark_logger = benchmark_logger

    def run(self):
        print(f"\n\n🚀 Starting benchmark for model: {self.model_adapter.model_id}")
        
        
        total_start_time = time.time()

        if self.task_index != 0:
            # 如果指定了特定任务，则只运行该任务
            task = self.tasks[self.task_index - 1]
            print(f"===== Running Task: {task.get_name()} =====")
            print(f"Description: {task.get_description()}")
            prompt = task.generate_prompt()
            start_time = time.time()
            response = self.model_adapter.query(prompt)
            end_time = time.time()
            
            execution_time = round(end_time - start_time, 2)
            
            print(f"Model Response (took {execution_time}s): \n---\n{response}\n---\n")

            score, reason = task.evaluate(response, self.judger)
            print(f"📊 Score: {score}/1.0")
            print(f"Reason: {reason}\n")
            
            self.results.append({
                "task_name": task.get_name(),
                "execution_time": execution_time,
                # "prompt": prompt,
                # "response": response,
                "score": score,
                "reason": reason,
            })
        else:
            for i, task in tqdm(enumerate(self.tasks), total=len(self.tasks), desc="Running tasks"):
                # print(f"===== Running Task {i+1}/{len(self.tasks)}: {task.get_name()} =====")
                # print(f"Description: {task.get_description()}")
                self.benchmark_logger.info(f"## Task {i+1}: {task.get_name()} ")
                self.benchmark_logger.info("### 提示词\n")
                prompt = task.generate_prompt()
                self.benchmark_logger.info("```markdown\n" + prompt + "\n```")
                
                start_time = time.time()
                response = self.model_adapter.query(prompt)
                end_time = time.time()
                self.benchmark_logger.info("### 模型响应\n")
                
                execution_time = round(end_time - start_time, 2)
                self.benchmark_logger.info(f"模型输出耗时：{execution_time}s\n\n")
                self.benchmark_logger.info(f"模型输出：\n")
                self.benchmark_logger.info("```markdown\n" + response + "\n```\n")
                
                # print(f"Model Response (took {execution_time}s): \n---\n{response}\n---\n")
                score, reason = task.evaluate(response, self.judger)
                self.benchmark_logger.info("### 评价结果\n")
                self.benchmark_logger.info(f"📊回答评分: **{score}**\n")
                self.benchmark_logger.info(f"评分理由: {reason}\n")
                
                self.results.append({
                    "task_name": task.get_name(),
                    "execution_time": execution_time,
                    # "prompt": prompt,
                    # "response": response,
                    "score": score,
                    "reason": reason,
                })
            
        total_end_time = time.time()
        self.total_execution_time = round(total_end_time - total_start_time, 2)
        print(f"✅ Benchmark finished in {self.total_execution_time}s.")
        return self.get_summary()

    def get_summary(self):
        total_score = sum(res["score"] for res in self.results)
        average_score = round(total_score / len(self.tasks), 2) if self.tasks else 0
        self.benchmark_logger.info("## 最终结果\n")
        self.benchmark_logger.info(f"测评模型: {self.model_adapter.model_id}\n")
        self.benchmark_logger.info(f"测评耗时: {self.total_execution_time}s\n")
        self.benchmark_logger.info(f"📊 平均分: {average_score}")

        summary = {
            "model_id": self.model_adapter.model_id,
            "total_tasks": len(self.tasks),
            "average_score": average_score,
            # "detailed_results": self.results
        }
        return summary