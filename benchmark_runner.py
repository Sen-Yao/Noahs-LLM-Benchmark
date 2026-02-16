# benchmark_runner.py
import time
from tqdm import tqdm
import logging

from collections import defaultdict
from typing import List

from model_adapter import BaseModelAdapter
from evaluate import OpenAIJudger
from typing import List
from evaluate import OpenAIJudger

# logging.basicConfig(level=logging.DEBUG)

class BenchmarkRunner:
    def __init__(self, model_adapter: BaseModelAdapter, tasks: List, judger: OpenAIJudger, task_index: int = 0, benchmark_logger: logging.Logger = None):
        self.model_adapter = model_adapter
        self.tasks = tasks
        self.results = []
        self.judger = judger
        self.task_index = task_index
        self.benchmark_logger = benchmark_logger

    def run(self):
        print(f"\n\n🚀 Starting benchmark for model: {self.model_adapter.model_id}")
        
        total_start_time = time.time()
        self.total_execution_time = 0.0

        if self.task_index != 0:
            # 如果指定了特定任务，则只运行该任务
            task = self.tasks[self.task_index - 1]
            print(f"===== Running Task: {task.get_name()} =====")
            print(f"Category: {task.get_category()}")
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
                "category": task.get_category(),  # ✅ 新增分类
                "execution_time": execution_time,
                "score": score,
                "reason": reason,
            })
        else:
            for i, task in tqdm(enumerate(self.tasks), total=len(self.tasks), desc="Running tasks"):
                self.benchmark_logger.info(f"## Task {i+1}: {task.get_name()} ")
                self.benchmark_logger.info(f"**分类**: {task.get_category()}\n")  # ✅ 记录分类
                self.benchmark_logger.info("### 提示词\n")
                prompt = task.generate_prompt()
                self.benchmark_logger.info("```markdown\n" + prompt + "\n```")
                
                start_time = time.time()
                response = self.model_adapter.query(prompt)
                end_time = time.time()
                self.benchmark_logger.info("### 模型响应\n")
                
                execution_time = 0.0  # 初始化，防止超时时未定义
                
                if "Error calling" in response and "timeout" in response:
                    self.benchmark_logger.info(f"模型超时！\n{response}\n\n")
                    score = 0
                    reason = "无法在规定时间内生成完整响应"
                else:
                    execution_time = round(end_time - start_time, 2)
                    self.benchmark_logger.info(f"模型输出耗时：{execution_time}s\n\n")
                    self.benchmark_logger.info(f"模型输出：\n")
                    self.benchmark_logger.info("```markdown\n" + response + "\n```\n")
                    
                    score, reason = task.evaluate(response, self.judger)
                
                self.benchmark_logger.info("### 评价结果\n")
                self.benchmark_logger.info(f"📊回答评分: **{score}**\n")
                self.benchmark_logger.info(f"评分理由: {reason}\n")
                
                self.results.append({
                    "task_name": task.get_name(),
                    "category": task.get_category(),
                    "execution_time": execution_time,
                    "score": score,
                    "reason": reason,
                })
                self.total_execution_time += execution_time
            
        total_end_time = time.time()
        self.total_benchmark_time = round(total_end_time - total_start_time, 2)
        print(f"✅ Benchmark finished in {self.total_benchmark_time}s.")
        return self.get_summary()

    def get_summary(self):
        """
        按类别汇总统计，输出每个类别的平均分。
        """
        # ============ 1. 按类别分组统计 ============
        category_scores = defaultdict(list)
        for res in self.results:
            category_scores[res["category"]].append(res["score"])
        
        # 计算每个类别的平均分
        category_avg = {}
        for category, scores in category_scores.items():
            avg = round(sum(scores) / len(scores), 2) if scores else 0
            category_avg[category] = {
                "average": avg,
                "count": len(scores),
                "total": round(sum(scores), 2)
            }
        
        # 按类别名排序，保证输出顺序一致
        sorted_categories = sorted(category_avg.keys())
        
        # ============ 2. 计算总平均分 ============
        total_score = sum(res["score"] for res in self.results)
        total_count = len(self.results)
        overall_average = round(total_score / total_count, 2) if total_count > 0 else 0
        
        # ============ 3. 生成 Markdown 表格（按类别） ============
        # 表头：| 模型名 | 类别1 | 类别2 | ... | 总平均分 | 耗时(s) |
        header_row = "| 模型名 | " + " | ".join(sorted_categories) + " | 总平均分 | 耗时(s) |"
        
        # 分割线
        separator_row = "|---" * (len(sorted_categories) + 3) + "|"
        
        # 数据行：各类别平均分
        category_scores_str = [str(category_avg[cat]["average"]) for cat in sorted_categories]
        data_row = f"| {self.model_adapter.model_id} | " + " | ".join(category_scores_str) + f" | {overall_average} | {self.total_execution_time} |"
        
        # ============ 4. 打印详细日志 ============
        self.benchmark_logger.info("## 最终评价摘要\n")
        self.benchmark_logger.info(f"测评模型: {self.model_adapter.model_id}\n")
        self.benchmark_logger.info(f"测评耗时: {self.total_benchmark_time}s\n")
        self.benchmark_logger.info(f"📊 总平均分: {overall_average}\n\n")
        
        # 打印各类别详情
        self.benchmark_logger.info("### 各类别得分详情\n")
        self.benchmark_logger.info("| 类别 | 任务数 | 类别总分 | 类别平均分 |")
        self.benchmark_logger.info("|---|---|---|---|")
        for cat in sorted_categories:
            info = category_avg[cat]
            self.benchmark_logger.info(f"| {cat} | {info['count']} | {info['total']} | {info['average']} |")
        self.benchmark_logger.info("\n")
        
        # 打印汇总表格
        self.benchmark_logger.info("### 汇总表格\n")
        self.benchmark_logger.info(f"{header_row}\n{separator_row}\n{data_row}\n")

        # ============ 5. 返回结构化 Summary ============
        summary = {
            "model_id": self.model_adapter.model_id,
            "total_tasks": total_count,
            "overall_average": overall_average,
            "total_execution_time": self.total_execution_time,
            "total_benchmark_time": self.total_benchmark_time,
            "category_summary": category_avg,  # ✅ 各类别统计
        }
        return summary