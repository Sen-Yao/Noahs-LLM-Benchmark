import re
from model_adapter import OpenAIAdapter 

class LLMJudger(OpenAIAdapter):
    def __init__(self, model_id: str = "gpt-4o", api_key: str = "sk-your-judge-api-key", api_base: str = "https://api.openai.com/v1"):
        self.JUDGE_MODEL_ID = model_id
        # 确保裁判模型有自己的API Key
        self.JUDGE_API_KEY = api_key
        self.JUDGE_API_BASE = api_base

    def get_name(self) -> str:
        return "Use LLM to Judge LLM's output"

    def get_description(self) -> str:
        return "This task uses a separate LLM to evaluate the output of another LLM based on a given prompt"

    def _get_judge_prompt(self, evaluation_standard: str, response_to_judge: str) -> str:
        return f"""
        你是一个回答评分器，需要根据给定的标准对 AI 的回答进行评分。

        [评判要求：]
        {evaluation_standard}

        [AI 的回答]
        {response_to_judge}

        请按照下面的格式给出你的评分，除此之外不要包含其他内容。

        Score: [Total score out of 10]
        Reason: [Your brief justification for the score]
        """

    def evaluate(self, evaluation_standard: str, response: str) -> tuple[float, str]:
        # 初始化裁判适配器
        judge_adapter = OpenAIAdapter(api_key=self.JUDGE_API_KEY, model_id=self.JUDGE_MODEL_ID, api_base=self.JUDGE_API_BASE)
        
        judging_prompt = self._get_judge_prompt(evaluation_standard, response)
        # print("Judger Evaluating...")
        # 让裁判模型打分
        judge_response = judge_adapter.query(judging_prompt)
        
        # 从裁判的回复中提取分数和理由
        try:
            score_match = re.search(r"Score:\s*(\d+\.?\d*)", judge_response)
            reason_match = re.search(r"Reason:\s*(.*)", judge_response, re.DOTALL)
            
            if score_match and reason_match:
                score = float(score_match.group(1)) / 1.0
                reason = reason_match.group(1).strip()
                return score, f"Judge's Verdict: {reason}"
            else:
                return 0.0, f"Could not parse judge's response: {judge_response}"
        except Exception as e:
            return 0.0, f"Error during judging: {e}"