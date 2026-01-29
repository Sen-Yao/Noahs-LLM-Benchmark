# model_adapter.py
from abc import ABC, abstractmethod
import os
from openai import OpenAI
import requests
import json


class BaseModelAdapter(ABC):
    """
    模型适配器的基类。
    """
    def __init__(self, api_key: str, model_id: str, api_base: str = None):
        self.api_key = api_key
        self.model_id = model_id
        self.api_base = api_base

    @abstractmethod
    def query(self, prompt: str) -> str:
        """
        向模型发送请求并获取返回结果。
        :param prompt: 发送给模型的提示词。
        :return: 模型的文本输出。
        """
        pass

class OpenAIAdapter(BaseModelAdapter):
    """
    适用于 OpenAI API 的适配器。
    也兼容所有遵循 OpenAI API 格式的本地模型服务，例如 LM Studio, LocalAI 等。
    """
    def __init__(self, api_key: str, model_id: str, api_base: str = None):
        super().__init__(api_key, model_id, api_base)
        self.client = OpenAI(
            api_key=self.api_key,
            base_url=self.api_base,
        )

    def query(self, prompt: str) -> str:
        try:
            chat_completion = self.client.chat.completions.create(
                messages=[
                    {
                        "role": "user",
                        "content": prompt,
                    }
                ],
                model=self.model_id,
                seed=42,  # 设置随机种子以确保结果可复现
            )
            return chat_completion.choices[0].message.content
        except Exception as e:
            print(f"Error calling OpenAI API: {e}")
            return f"Error: {e}"


class OllamaAdapter(BaseModelAdapter):
    """
    适用于本地运行的 Ollama 服务的适配器。
    """
    def __init__(self, api_key: str, model_id: str, api_base: str = None):
        # api_key 在此适配器中被忽略，但为了接口统一性而保留
        super().__init__(api_key, model_id, api_base)
        # 如果用户未提供 api_base，则使用 Ollama 的默认地址
        self.api_base = api_base or "http://localhost:11434"
        self.api_endpoint = f"{self.api_base}/api/chat"

    def query(self, prompt: str) -> str:
        """
        使用 /api/chat 端点向 Ollama 模型发送请求。
        """
        payload = {
            "model": self.model_id,
            "messages": [
                {
                    "role": "user",
                    "content": prompt,
                }
            ],
            "stream": False,
            "seed": 42,  # 设置随机种子以确保结果可复现
        }

        try:
            response = requests.post(
                self.api_endpoint,
                headers={"Content-Type": "application/json"},
                data=json.dumps(payload),
                timeout=60 # 设置60秒超时，防止长时间无响应
            )
            # 如果API返回错误状态码（如 404, 500），则会抛出异常
            response.raise_for_status()
            
            response_data = response.json()

            response_with_think = response_data.get('message', {}).get('content', '').strip()
            
            # 从返回的JSON中提取核心回复内容
            return self.extract_ollama_thinking_and_category(response_with_think).get('answer', response_with_think)

        except requests.exceptions.RequestException as e:
            error_message = f"Error calling Ollama API: {e}"
            print(error_message)
            return f"Error: {error_message}"
        except KeyError:
            error_message = f"Error: Unexpected response format from Ollama. Response: {response.text}"
            print(error_message)
            return error_message
    def extract_ollama_thinking_and_category(self, response_str):
        # 移除 'response': '<think>' 和末尾的单引号
        processed_str = response_str.replace("'response': '<think>", "").strip()
        if processed_str.endswith("'"):
            processed_str = processed_str[:-1].strip()

        # 找到 </think> 的位置
        end_think_index = processed_str.find('</think>')

        if end_think_index != -1:
            # 思考内容是 </think> 之前的部分
            thinking_content = processed_str[:end_think_index].strip()
            
            # 分类结果是 </think> 之后，直到字符串末尾的部分
            # 首先移除 </think> 标签，然后取最后一行
            remaining_str = processed_str[end_think_index + len('</think>'):].strip()
            
            # 分类结果通常是最后一行，所以我们按行分割并取最后一行
            lines = remaining_str.splitlines()
            answer = lines[-1].strip() if lines else ""

            return {
                "thinking": thinking_content,
                "answer": answer
            }
        else:
            # 如果没有 <think> 标签，可能是纯文本结果或者格式不同
            # 尝试直接将整个内容作为分类结果（或者根据实际情况调整）
            lines = processed_str.splitlines()
            answer = lines[-1].strip() if lines else ""
            return {
                "thinking": "", # 或者可以返回原始字符串作为思考，取决于预期
                "answer": answer
            }
