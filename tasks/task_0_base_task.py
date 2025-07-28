# tasks/base_task.py
from abc import ABC, abstractmethod
from evaluate import LLMJudger

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
    def evaluate(self, response: str, judger: LLMJudger) -> tuple[float, str]:
        """
        评估模型的返回结果。
        :param response: 模型的输出字符串。
        :return: 一个元组 (分数, 评估理由)。分数范围建议为 0.0 到 1.0。
        """
        pass