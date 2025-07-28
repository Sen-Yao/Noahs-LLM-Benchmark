# benchmark_runner.py
import time
from model_adapter import BaseModelAdapter
from tasks.task_0_base_task import BenchmarkTask
from evaluate import LLMJudger
from typing import List
from evaluate import LLMJudger

class BenchmarkRunner:
    def __init__(self, model_adapter: BaseModelAdapter, tasks: List[BenchmarkTask], judger: LLMJudger):
        self.model_adapter = model_adapter
        self.tasks = tasks
        self.results = []
        self.judger = judger

    def run(self):
        print(f"🚀 Starting benchmark for model: {self.model_adapter.model_id}")
        print(f"Total tasks to run: {len(self.tasks)}\n")
        
        total_start_time = time.time()



        for i, task in enumerate(self.tasks):
            print(f"===== Running Task {i+1}/{len(self.tasks)}: {task.get_name()} =====")
            print(f"Description: {task.get_description()}")
            
            prompt = task.generate_prompt()
            print(f"Prompt: \n---\n{prompt}\n---\n")
            
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
            
        total_end_time = time.time()
        total_execution_time = round(total_end_time - total_start_time, 2)
        print(f"✅ Benchmark finished in {total_execution_time}s.")
        return self.get_summary()

    def get_summary(self):
        total_score = sum(res["score"] for res in self.results)
        average_score = round(total_score / len(self.tasks), 3) if self.tasks else 0

        summary = {
            "model_id": self.model_adapter.model_id,
            "total_tasks": len(self.tasks),
            "average_score": average_score,
            "detailed_results": self.results
        }
        return summary