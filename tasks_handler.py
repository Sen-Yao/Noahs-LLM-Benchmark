import yaml
import os
import re

# tasks/base_task.py
from abc import ABC, abstractmethod
from evaluate import OpenAIJudger

class BenchmarkTask(ABC):
    """
    所有基准测试任务的抽象基类。
    每个子类代表一个具体的测试单元。
    """
    @abstractmethod
    def get_name(self) -> str:
        """返回任务的唯一名称。"""
        pass

    @abstractmethod
    def get_description(self) -> str:
        """返回任务的详细描述。"""
        pass

    @abstractmethod
    def generate_prompt(self) -> str:
        """生成用于本次测试的Prompt。"""
        pass

    @abstractmethod
    def evaluate(self, response: str, judger: OpenAIJudger) -> tuple[float, str]:
        """
        评估模型的返回结果。
        :param response: 模型的输出字符串。
        :return: 一个元组 (分数, 评估理由)。分数范围建议为 0.0 到 1.0。
        """
        pass

class ConfigurableTask(BenchmarkTask):
    def __init__(self, config_path: str):
        with open(config_path, 'r', encoding='utf-8') as f:
            self.config = yaml.safe_load(f)
        
    def get_name(self) -> str:
        return self.config.get('name', '未命名任务')

    def get_description(self) -> str:
        return self.config.get('description', '无描述')
    
    def generate_prompt(self) -> str:
        # 自动填充模板中的变量（如 {article}）
        return self.config['prompt_template']

    def evaluate(self, response: str, judger=None) -> tuple[float, str]:
        method = self.config['evaluation']['method']
        
        # 路由到不同的评估策略
        if method == "exact_match":
            return self._evaluate_exact(response)
        elif method == "llm_eval":
            return self._evaluate_llm(response, judger)
    
    def _evaluate_exact(self, response: str) -> tuple[float, str]:
        """
        精确匹配评估：用于选择题或分类题。
        """
        # 获取配置
        eval_cfg = self.config.get('evaluation', {})
        mapping = eval_cfg.get('mapping', {})
        default_score = eval_cfg.get('default_score', 0.0)
        default_reason = eval_cfg.get('default_reason', "回答未匹配到任何预设选项")

        # 归一化处理
        # 去掉首尾空格、转小写、去掉可能包含的引号（有的模型喜欢加引号）
        processed_res = response.strip().lower().replace('"', '').replace("'", "")
        
        # 针对选择题，有的模型会输出 "A." 或 "选项 A"，这里尝试提取第一个字母
        # 逻辑：如果匹配项里全是单字母，我们只看回答的第一个字母
        is_choice_question = all(len(k) == 1 for k in mapping.keys())
        if is_choice_question and len(processed_res) > 0:
            # 简单正则：提取第一个出现的字母
            match = re.search(r'[a-zA-Z]', processed_res)
            if match:
                processed_res = match.group()

        # 查表匹配
        if processed_res in mapping:
            result = mapping[processed_res]
            # 支持 YAML 中简写为 score: 100 或 结构化 {score: 100, reason: "..."}
            if isinstance(result, dict):
                return float(result.get('score', 0)), result.get('reason', '匹配成功')
            else:
                return float(result), "回答正确"

        return float(default_score), default_reason

    def _evaluate_llm(self, response: str, judger=None) -> tuple[float, str]:
        """
        LLM 裁判评估：用于开放式推理、文学分析等。
        """
        if judger is None:
            return 0.0, "错误：未提供 Judger，无法进行 LLM 评分"

        eval_cfg = self.config.get('evaluation', {})
        standard = eval_cfg.get('standard', "无具体评分标准")

        # 调用你的 Judger 适配器接口
        # 这里的 judger.evaluate 应该返回 (score, reason)
        try:
            score, reason = judger.evaluate(standard, response)
            return float(score), reason
        except Exception as e:
            return 0.0, f"Judger 评分过程出错: {str(e)}"

def load_all_tasks(config_dir: str):
    tasks = []
    # 扫描目录下所有的 .yaml 文件
    for filename in os.listdir(config_dir):
        if filename.endswith('.yaml') or filename.endswith('.yml'):
            file_path = os.path.join(config_dir, filename)
            with open(file_path, 'r', encoding='utf-8') as f:
                # 实例化统一的任务类
                task_instance = ConfigurableTask(file_path)
                tasks.append(task_instance)
    return tasks