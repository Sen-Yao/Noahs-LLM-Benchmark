# tasks/chinese_idiom.py
import os
from .task_0_base_task import BenchmarkTask
from evaluate import LLMJudger

# 获取当前文件所在目录的绝对路径
# 这能确保无论从哪里运行脚本，都能找到 'prompt_assets' 目录
_CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))
_ASSETS_DIR = os.path.join(_CURRENT_DIR, '..', 'prompt_assets') # 指向项目根目录下的 prompt_assets

class SpiritInTheBottle(BenchmarkTask):
    def __init__(self, article_filename: str):
        self.article_filename = article_filename
        self.article_path = os.path.join(_ASSETS_DIR, self.article_filename)
    def get_name(self) -> str:
        return "Spirit in the Bottle"

    def get_description(self) -> str:
        return "Tests the model's long context understanding and reasoning capabilities by asking it to guess a character in a noval."

    def _read_article(self) -> str:
        try:
            with open(self.article_path, 'r', encoding='utf-8') as f:
                return f.read()
        except FileNotFoundError:
            print(f"Error: Prompt asset file not found at {self.article_path}")
            return "[Error: Article file not found]"
        except Exception as e:
            print(f"Error reading prompt asset file: {e}")
            return f"[Error: {e}]"

    def generate_prompt(self) -> str:
        article_content = self._read_article()
        
        # 使用 f-string 构建 prompt 模板，非常清晰
        prompt = f"""请阅读下方的一段短篇小说：

            --- ARTICLE BEGINS ---
            {article_content}
            --- ARTICLE ENDS ---

            结合小说内容判断，诺亚可能是谁？
            注意：不要给出任何解释或理由或推理过程，只需直接用简单的一句话回答。
            """
        return prompt

    def evaluate(self, response: str, judger: LLMJudger) -> tuple[float, str]:
        response = response.lower()

        evaluation_standard = f"""
        若模型的回答接近于「安德烈的灵魂的另一面」，则评分为 100 分。
        若模型的回答接近于「安德烈」，则评分为 50 分。
        若模型的回答接近于「安德烈的兄弟」，则评分为 20 分。
        若模型回答与上述内容无关，则评分为 0 分。
        """
        
        score, reason = judger.evaluate(evaluation_standard, response)
        return round(score, 2), reason