# tasks/chinese_idiom.py
import os
from .task_0_base_task import BenchmarkTask
from evaluate import OpenAIJudger

_CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))
_ASSETS_DIR = os.path.join(_CURRENT_DIR, '..', 'prompt_assets') # 指向项目根目录下的 prompt_assets

class StickPassThroughTheGate(BenchmarkTask):
    def get_name(self) -> str:
        return "Stick Pass Through The Gate"

    def get_description(self) -> str:
        return "测试模型能否具有生活常识和逻辑推理能力"

    def generate_prompt(self) -> str:        
        # 使用 f-string 构建 prompt 模板，非常清晰
        prompt = f"""有一根长度为 5.5 米的细木棍，能否通过高 4 米，宽 3 米的门洞？
        已知门洞两侧足够宽敞，木棍可以自由旋转和倾斜。

        回答时请直接给出「可以」或「不可以」，同时用简单的语言描述为什么可以或不可以，不要涉及复杂的数学公式或计算。"""
        return prompt

    def evaluate(self, response: str, judger: OpenAIJudger) -> tuple[float, str]:
        response = response.lower()

        evaluation_standard = f"""你是一个回答评分器，需要根据给定的标准对 AI 的回答进行评分。我给 AI 的问题是：有一根长度为 5.5 米的细木棍，能否通过高 4 米，宽 3 米的门洞？
        标准答案为，可以将木棍放平穿过门洞。

        若模型的回答为「可以」，且模型能够指出，"可以将木棍放平穿过门洞"，或"可以把木棍几乎竖直地穿过门口", "木棍在门口的横向投影会变得很小"之类的描述，则评分为 100 分。

        若模型的回答为「不可以」，且模型能够指出，利用勾股定理计算发现，对角线长度为 5 米，不足以容纳 5.5 米，所以无法通过，则评分为 70 分。

        若模型的回答为「可以」，但是理由与标准答案不符，或误认为门洞的对角线距离大于木棍的长度，则评分为 50 分。

        若模型的回答为「不可以」，但是理由与上述的「勾股定理」相关的回答不同，则评分为 20 分。
        若模型回答与上述内容无关，则评分为 0 分。"""
        
        score, reason = judger.evaluate(evaluation_standard, response)
        return round(score, 2), reason